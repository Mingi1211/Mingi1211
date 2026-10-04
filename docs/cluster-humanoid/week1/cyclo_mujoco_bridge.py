#!/usr/bin/env python3
"""실제 Cyclo Control ↔ MuJoCo 브리지 (AI Worker2 FFW-SG2 한 대)

실로봇에서 follower 로봇이 하던 일을 MuJoCo가 대신한다.
  - /joint_states 발행 (100 Hz)            ← Cyclo가 측정값으로 읽음 (joint_state_broadcaster 역할)
  - Cyclo가 내보내는 관절 궤적 구독       → 위치 액추에이터 목표로 넣음 (arm_r/l_controller 역할)
      /leader/joint_trajectory_command_broadcaster_right/joint_trajectory  (오른팔 7 + gripper_r_joint1)
      /leader/joint_trajectory_command_broadcaster_left/joint_trajectory   (왼팔 7 + gripper_l_joint1)
      /leader/joystick_controller_right/joint_trajectory                   (리프트, lift_vel_bound ≠ 0일 때만)
  - 오른손 끝 위치(base_link 기준)를 CSV로 기록 → MuJoCo가 본 "실제" 위치

사용법 (ROS 2 Jazzy를 source한 터미널, mujoco가 설치된 venv에서)
  python3 cyclo_mujoco_bridge.py --scene <ai_worker>/ffw_description/mujoco/ffw_sg2/scene.xml
  python3 cyclo_mujoco_bridge.py --scene ... --gravcomp          # 팔에 이상적인 중력 보상 feedforward 추가
  python3 cyclo_mujoco_bridge.py --scene ... --no-view           # 화면 없는 환경
"""
import argparse, csv, threading, time
import numpy as np
import mujoco


class Sim:
    """ROS와 무관한 MuJoCo 부분 — 따로 시험할 수 있게 분리"""

    def __init__(self, scene, gravcomp=False):
        self.m = mujoco.MjModel.from_xml_path(scene)
        self.d = mujoco.MjData(self.m)
        self.gravcomp = gravcomp
        self.lock = threading.Lock()
        m = self.m
        # 이름 있는 1자유도 관절(hinge, slide)만 /joint_states에 싣는다 (floating base 제외)
        self.names, self.qadr, self.vadr = [], [], []
        for j in range(m.njnt):
            if m.jnt_type[j] in (mujoco.mjtJoint.mjJNT_HINGE, mujoco.mjtJoint.mjJNT_SLIDE):
                self.names.append(m.joint(j).name)
                self.qadr.append(m.jnt_qposadr[j])
                self.vadr.append(m.jnt_dofadr[j])
        self.act = {m.actuator(i).name: i for i in range(m.nu)}     # 액추에이터 이름 = 관절 이름
        self.arm_dof = [m.jnt_dofadr[m.joint(f'arm_{s}_joint{i}').id] for s in 'rl' for i in range(1, 8)]
        self.ee = m.body('end_effector_r_link').id
        self.base = m.body('base_link').id
        # 모든 위치 액추에이터 목표 = 현재 관절값 (자세 유지)
        for i in range(m.nu):
            if m.actuator_biastype[i] != 0:
                self.d.ctrl[i] = self.d.qpos[m.jnt_qposadr[m.actuator_trnid[i][0]]]

    def apply_trajectory(self, joint_names, positions):
        """JointTrajectory 마지막 점의 위치를 액추에이터 목표로 (Cyclo는 점 1개, time_from_start = 0)"""
        n = 0
        with self.lock:
            for name, q in zip(joint_names, positions):
                if name in self.act:
                    self.d.ctrl[self.act[name]] = q
                    n += 1
        return n

    def joint_state(self):
        with self.lock:
            return (list(self.names),
                    [float(self.d.qpos[a]) for a in self.qadr],
                    [float(self.d.qvel[a]) for a in self.vadr])

    def step(self):
        with self.lock:
            if self.gravcomp:                                   # τ_ff = g(q) + C(q,q̇)q̇ (RNEA)
                self.d.qfrc_applied[self.arm_dof] = self.d.qfrc_bias[self.arm_dof]
            mujoco.mj_step(self.m, self.d)

    def ee_in_base(self):
        with self.lock:
            Rb = self.d.xmat[self.base].reshape(3, 3)
            return Rb.T @ (self.d.xpos[self.ee] - self.d.xpos[self.base])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--scene', required=True)
    ap.add_argument('--gravcomp', action='store_true')
    ap.add_argument('--no-view', action='store_true')
    ap.add_argument('--log', default='bridge_log.csv')
    args = ap.parse_args()

    import rclpy
    from rclpy.node import Node
    from rclpy.executors import SingleThreadedExecutor
    from sensor_msgs.msg import JointState
    from trajectory_msgs.msg import JointTrajectory

    sim = Sim(args.scene, args.gravcomp)

    class Bridge(Node):
        def __init__(self):
            super().__init__('mujoco_bridge')
            self.pub = self.create_publisher(JointState, '/joint_states', 10)
            topics = ['/leader/joint_trajectory_command_broadcaster_right/joint_trajectory',
                      '/leader/joint_trajectory_command_broadcaster_left/joint_trajectory',
                      '/leader/joystick_controller_right/joint_trajectory']
            for tp in topics:
                self.create_subscription(JointTrajectory, tp, self.on_traj, 10)
            self.create_timer(0.01, self.on_timer)              # 100 Hz
            self.n_cmd = 0

        def on_traj(self, msg):
            if msg.points:
                sim.apply_trajectory(msg.joint_names, msg.points[-1].positions)
                self.n_cmd += 1

        def on_timer(self):
            names, pos, vel = sim.joint_state()
            js = JointState()
            js.header.stamp = self.get_clock().now().to_msg()
            js.name, js.position, js.velocity = names, pos, vel
            self.pub.publish(js)

    rclpy.init()
    node = Bridge()
    ex = SingleThreadedExecutor()
    ex.add_node(node)
    threading.Thread(target=ex.spin, daemon=True).start()
    node.get_logger().info(f'MuJoCo 브리지 시작: 관절 {len(sim.names)}개 발행, gravcomp={args.gravcomp}')

    viewer = None
    if not args.no_view:
        import mujoco.viewer
        viewer = mujoco.viewer.launch_passive(sim.m, sim.d)

    dt = sim.m.opt.timestep
    f = open(args.log, 'w', newline='')
    w = csv.writer(f)
    w.writerow(['t', 'x_base', 'y_base', 'z_base', 'n_cmd'])
    t0 = time.perf_counter()
    k = 0
    try:
        while viewer is None or viewer.is_running():
            sim.step()
            k += 1
            if k % 10 == 0:                                      # 50 Hz로 기록
                w.writerow([k * dt, *np.round(sim.ee_in_base(), 5), node.n_cmd])
            if viewer is not None and k % 8 == 0:                # 화면은 약 60 Hz
                with sim.lock:
                    viewer.sync()
            lag = k * dt - (time.perf_counter() - t0)            # 실시간에 맞춰 대기
            if lag > 0:
                time.sleep(lag)
    except KeyboardInterrupt:
        pass
    finally:
        f.close()
        if viewer is not None:
            viewer.close()
        ex.shutdown()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
