#!/usr/bin/env python3
"""2번 하위 제어 노드 — Pinocchio 기반 토크 제어 (Gazebo·실물 공용)

mode (params.yaml):
  spring  : 관절 1개만 τ = -k(q - q0) - d·q̇, 나머지 관절은 g + 관절 PD로 유지      (1주차 수)
  gravity : τ = g(q) + Kq(q0 - q) - Dq·q̇  (7축, Kq 작게 하면 "떠 있는" 팔)          (1주차 금)
  task    : τ = Jᵀ[K e + D ė] + g(q) + N(-Kn(q - q_rest) - Dn q̇)                     (2주차~)
            e = [p_d - p ; log(R_d Rᵀ)],  J = 리프트 열을 뺀 팔 7축 자코비안 (LOCAL_WORLD_ALIGNED)
            D = 2ζ√(Λ_ii K_ii),  Λ = (J M⁻¹ Jᵀ)⁻¹ (손목 5·6·7 armature 추가한 M)

입력: /joint_states, /robot_description, /impedance/<s>/goal (PoseStamped, base_link) 또는 Cyclo 관절 궤적
출력: /arm_<s>_effort_controller/commands (Float64MultiArray, 7개)
"""
import csv
import os
import time

import numpy as np
import pinocchio as pin
import rclpy
from geometry_msgs.msg import PoseStamped
from rclpy.node import Node
from rclpy.qos import DurabilityPolicy, QoSProfile, ReliabilityPolicy
from sensor_msgs.msg import JointState
from std_msgs.msg import Bool, Float64MultiArray, String
from trajectory_msgs.msg import JointTrajectory

CYCLO_TOPIC = {'r': '/leader/joint_trajectory_command_broadcaster_right/joint_trajectory',
               'l': '/leader/joint_trajectory_command_broadcaster_left/joint_trajectory'}


def quintic(tau):
    """5차 시간 스케일링 s(τ), ṡ(τ) (τ = t/T, MR 9.2)."""
    tau = min(max(tau, 0.0), 1.0)
    s = 10 * tau**3 - 15 * tau**4 + 6 * tau**5
    ds = 30 * tau**2 - 60 * tau**3 + 30 * tau**4
    return s, ds


class Arm:
    def __init__(self, node, side, model):
        self.node, self.s = node, side
        P = lambda name: node.get_parameter(name).value  # noqa: E731
        self.names = [f'arm_{side}_joint{i}' for i in range(1, 8)]
        self.jid = [model.getJointId(n) for n in self.names]
        self.v_idx = [model.joints[j].idx_v for j in self.jid]
        ee = P(f'ee_frame_{side}')
        if not model.existFrame(ee):
            raise RuntimeError(f'프레임 {ee} 없음 — list_frames.py로 확인')
        self.fid = model.getFrameId(ee)
        preset = P(f'preset_{side}')                      # leader | follower
        self.K = np.diag(list(P(f'{preset}_K_pos')) + list(P('K_rot')))
        self.pub = node.create_publisher(Float64MultiArray, f'/arm_{side}_effort_controller/commands', 10)
        node.create_subscription(PoseStamped, f'/impedance/{side}/goal', self.on_goal, 10)
        if P('source') == 'cyclo':
            node.create_subscription(JointTrajectory, CYCLO_TOPIC[side], self.on_cyclo, 10)
        self.q0 = None          # gravity/spring 모드 기준 자세 · task 모드 null-space 기준 자세
        self.traj = None        # (t0, T, p0, R0, pf, Rf)
        self.xd = None          # (p_d, R_d, v_d(6))
        self.cyclo_q = None
        self.tau = np.zeros(7)

    # ---------- 목표 ----------
    def on_goal(self, msg):
        if self.xd is None:
            return
        q = msg.pose.orientation
        pf = np.array([msg.pose.position.x, msg.pose.position.y, msg.pose.position.z])
        Rf = pin.Quaternion(q.w, q.x, q.y, q.z).normalized().toRotationMatrix()
        T = float(self.node.get_parameter('duration').value)
        self.traj = (time.monotonic(), T, self.xd[0].copy(), self.xd[1].copy(), pf, Rf)
        self.node.get_logger().info(f'[{self.s}] 목표 {np.round(pf, 3)} T={T}s')

    def on_cyclo(self, msg):
        if msg.points:
            self.cyclo_q = dict(zip(msg.joint_names, msg.points[-1].positions))

    def desired(self, p, R, model, data_tmp, q_full, qmap):
        """현재 목표 (p_d, R_d, v_d)."""
        if self.cyclo_q is not None:                       # Cyclo q_d → FK → x_d
            qd = q_full.copy()
            for n, v in self.cyclo_q.items():
                if n in qmap:
                    qd[qmap[n]] = v
            pin.framesForwardKinematics(model, data_tmp, qd)
            M = data_tmp.oMf[self.fid]
            pd, Rd = M.translation.copy(), M.rotation.copy()
            vd = np.zeros(6)
            if self.xd is not None:
                vd[:3] = (pd - self.xd[0]) * self.node.rate
            return pd, Rd, vd
        if self.traj is None:
            return (self.xd[0], self.xd[1], np.zeros(6)) if self.xd else (p, R, np.zeros(6))
        t0, T, p0, R0, pf, Rf = self.traj
        s, ds = quintic((time.monotonic() - t0) / T)
        w = pin.log3(R0.T @ Rf)
        pd = p0 + s * (pf - p0)
        Rd = R0 @ pin.exp3(w * s)
        vd = np.concatenate([(pf - p0) * ds / T, R0 @ w * ds / T])
        return pd, Rd, vd


class ImpedanceNode(Node):
    def __init__(self):
        super().__init__('impedance_controller')
        d = self.declare_parameter
        d('mode', 'gravity'); d('sides', ['r']); d('rate', 100.0); d('source', 'goal')
        d('ee_frame_r', 'end_effector_r_link'); d('ee_frame_l', 'end_effector_l_link')
        d('spring_joint', 4); d('k_spring', 20.0); d('d_spring', 1.0)
        d('Kq', [30.0] * 7); d('Dq', [2.0] * 7)
        d('preset_r', 'leader'); d('preset_l', 'follower')
        d('leader_K_pos', [600.0, 600.0, 600.0]); d('follower_K_pos', [150.0, 150.0, 600.0])
        d('K_rot', [30.0, 30.0, 30.0]); d('zeta', 1.0)
        d('K_null', 5.0); d('D_null', 1.0)
        d('armature_wrist', [0.0, 0.0, 0.0, 0.0, 0.05, 0.05, 0.05])
        d('fric_coulomb', [0.0] * 7)
        d('tau_max', [40.0, 40.0, 30.0, 30.0, 10.0, 10.0, 10.0])
        d('duration', 3.0); d('state_timeout', 0.1); d('log_dir', os.path.expanduser('~/impedance_logs'))
        self.rate = float(self.get_parameter('rate').value)
        self.model = None
        self.js = None
        self.js_time = 0.0
        self.enabled = True
        qos = QoSProfile(depth=1, durability=DurabilityPolicy.TRANSIENT_LOCAL,
                         reliability=ReliabilityPolicy.RELIABLE)
        self.create_subscription(String, '/robot_description', self.on_urdf, qos)
        self.create_subscription(JointState, '/joint_states', self.on_js, 50)
        self.create_subscription(Bool, '/impedance/enable', lambda m: setattr(self, 'enabled', m.data), 10)
        self.create_timer(1.0 / self.rate, self.step)
        os.makedirs(self.get_parameter('log_dir').value, exist_ok=True)
        fn = os.path.join(self.get_parameter('log_dir').value,
                          time.strftime('%m%d_%H%M%S') + f"_{self.get_parameter('mode').value}.csv")
        self.log = csv.writer(open(fn, 'w', newline=''))
        self.log.writerow(['t', 'side'] + [f'p{i}' for i in 'xyz'] + [f'pd{i}' for i in 'xyz']
                          + [f'eo{i}' for i in 'xyz'] + [f'tau{i}' for i in range(1, 8)]
                          + [f'q{i}' for i in range(1, 8)])
        self.t_start = time.monotonic()
        self.get_logger().info(f'로그: {fn}')

    def on_urdf(self, msg):
        if self.model is not None:
            return
        self.model = pin.buildModelFromXML(msg.data)
        self.data = self.model.createData()
        self.data_tmp = self.model.createData()
        self.qmap = {}                                   # 1자유도 관절 이름 → q 인덱스
        for j in range(1, self.model.njoints):
            if self.model.joints[j].nq == 1:
                self.qmap[self.model.names[j]] = self.model.joints[j].idx_q
        self.arms = [Arm(self, s, self.model) for s in self.get_parameter('sides').value]
        self.get_logger().info(f'모델 로드: nq={self.model.nq}, nv={self.model.nv}, 팔 {[a.s for a in self.arms]}')

    def on_js(self, msg):
        self.js = msg
        self.js_time = time.monotonic()

    def full_state(self):
        q = pin.neutral(self.model)
        v = np.zeros(self.model.nv)
        for n, i in enumerate(self.js.name):
            if i in self.qmap:
                q[self.qmap[i]] = self.js.position[n]
                if self.js.velocity:
                    v[self.model.joints[self.model.getJointId(i)].idx_v] = self.js.velocity[n]
        return q, v

    def step(self):
        if self.model is None or self.js is None:
            return
        if time.monotonic() - self.js_time > self.get_parameter('state_timeout').value:
            self.get_logger().warn('joint_states 끊김 — 명령 갱신 중지(마지막 토크 유지)', throttle_duration_sec=1.0)
            return
        P = lambda n: np.array(self.get_parameter(n).value, dtype=float)  # noqa: E731
        mode = self.get_parameter('mode').value
        q, v = self.full_state()
        m, d = self.model, self.data
        g_full = pin.computeGeneralizedGravity(m, d, q).copy()
        pin.computeJointJacobians(m, d, q)
        pin.updateFramePlacements(m, d)
        M_full = pin.crba(m, d, q)
        M_full = np.triu(M_full) + np.triu(M_full, 1).T
        t = time.monotonic() - self.t_start
        for a in self.arms:
            vi = a.v_idx
            qa = np.array([q[self.qmap[n]] for n in a.names])
            dqa = v[vi]
            g = g_full[vi]
            if a.q0 is None:
                a.q0 = qa.copy()
            oMf = d.oMf[a.fid]
            p, R = oMf.translation.copy(), oMf.rotation.copy()
            if a.xd is None:
                a.xd = (p.copy(), R.copy(), np.zeros(6))
            pd, Rd, eo = p, R, np.zeros(3)
            if not self.enabled:
                tau = g
            elif mode == 'spring':
                tau = g + P('Kq') * (a.q0 - qa) - P('Dq') * dqa
                k = int(self.get_parameter('spring_joint').value) - 1
                tau[k] = g[k] - self.get_parameter('k_spring').value * (qa[k] - a.q0[k]) \
                    - self.get_parameter('d_spring').value * dqa[k]
            elif mode == 'gravity':
                tau = g + P('Kq') * (a.q0 - qa) - P('Dq') * dqa
            else:  # task
                J = pin.getFrameJacobian(m, d, a.fid, pin.ReferenceFrame.LOCAL_WORLD_ALIGNED)[:, vi]
                Ma = M_full[np.ix_(vi, vi)] + np.diag(P('armature_wrist'))
                Minv = np.linalg.inv(Ma)
                Lam = np.linalg.inv(J @ Minv @ J.T + 1e-6 * np.eye(6))
                pd, Rd, vd = a.desired(p, R, m, self.data_tmp, q, self.qmap)
                a.xd = (pd, Rd, vd)
                eo = pin.log3(Rd @ R.T)
                e = np.concatenate([pd - p, eo])
                edot = vd - J @ dqa
                K = a.K
                D = np.diag(2 * self.get_parameter('zeta').value * np.sqrt(np.clip(np.diag(Lam) * np.diag(K), 0, None)))
                F = K @ e + D @ edot
                Jbar = Minv @ J.T @ Lam
                N = np.eye(7) - J.T @ Jbar.T
                tau_null = N @ (self.get_parameter('K_null').value * (a.q0 - qa)
                                - self.get_parameter('D_null').value * dqa)
                qd_dot = np.linalg.pinv(J) @ vd
                tau_f = P('fric_coulomb') * np.tanh(qd_dot / 0.01)
                tau = J.T @ F + g + tau_null + tau_f
            tau = np.clip(tau, -P('tau_max'), P('tau_max'))
            a.tau = tau
            a.pub.publish(Float64MultiArray(data=tau.tolist()))
            self.log.writerow([f'{t:.3f}', a.s, *np.round(p, 5), *np.round(pd, 5), *np.round(eo, 5),
                               *np.round(tau, 4), *np.round(qa, 5)])


def main():
    rclpy.init()
    node = ImpedanceNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
