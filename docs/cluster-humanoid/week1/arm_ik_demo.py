"""미니 Cyclo: AI Worker2(FFW-SG2) 오른팔 MoveL을 MuJoCo 단독(ROS 없음)으로 재현

구조 (Cyclo movel과 같은 흐름)
  목표 자세 + 시간 T → 시간 스케일링 s(t)로 직선 보간 → 목표 작업공간 속도 ẋ_d = ẋ_ff + K·e
  → 미분 IK로 관절 속도 q̇ (DLS 또는 QP) → q_cmd ← q_cmd + q̇·Δt → 위치 액추에이터 목표로 전송

사용법
  python3 arm_ik_demo.py --scene <ai_worker>/ffw_description/mujoco/ffw_sg2/scene.xml        # DLS + 5차
  python3 arm_ik_demo.py --scene ... --view                                                  # 3D 뷰어
  python3 arm_ik_demo.py --scene ... --profile cubic                                         # Cyclo와 같은 3차
  python3 arm_ik_demo.py --scene ... --solver qp                                             # Cyclo식 QP (osqp 필요)

Modern Robotics 대응
  자코비안  mj_jacBody: world 원점 기준이 아니라 "말단 위치 + world 축" 기준 → Pinocchio LOCAL_WORLD_ALIGNED와 같음 (MR 5.1)
  DLS       q̇ = Jᵀ(JJᵀ + λ²I)⁻¹ẋ_d   (MR 6.3 역속도 기구학 + 특이점 근처 감쇠)
  적분      q_cmd = q_측정 + q̇Δt (Cyclo ai_worker_movel_controller_node.cpp 499행과 같음)
  QP        min ‖Jq̇ − ẋ_d‖²_W + w_d‖q̇‖²  s.t. 속도 한계, 관절 한계 CBF  (Cyclo VRController::setCost/setIneqConstraint)
  궤적      5차 s = 10τ³ − 15τ⁴ + 6τ⁵ / 3차 s = 3τ² − 2τ³   (MR 9.2 시간 스케일링)
  피드백    ẋ_d = ẋ_ff + K·e   (MR 11.3 속도 입력 작업공간 제어)
"""
import argparse, csv
import numpy as np
import mujoco

ap = argparse.ArgumentParser()
ap.add_argument('--scene', required=True)
ap.add_argument('--target', type=float, nargs=3, default=[0.35, -0.20, 0.85],
                help='base_link 기준 목표 위치 [m] (Cyclo MoveL 예시와 같은 값)')
ap.add_argument('--T', type=float, default=3.0, help='이동 시간 [s]')
ap.add_argument('--profile', choices=['quintic', 'cubic'], default='quintic')
ap.add_argument('--solver', choices=['dls', 'qp'], default='dls')
ap.add_argument('--lam', type=float, default=0.05, help='DLS 감쇠 λ')
ap.add_argument('--K', type=float, default=50.0, help='오차 피드백 게인 (Cyclo kp_position = 50)')
ap.add_argument('--rate', type=float, default=100.0, help='IK 주기 [Hz] (Cyclo = 100)')
ap.add_argument('--qdmax', type=float, default=1.5, help='관절 속도 한계 [rad/s] (QP용, 가정값)')
ap.add_argument('--alpha', type=float, default=50.0, help='CBF 계수 (Cyclo cbf_alpha = 50)')
ap.add_argument('--integrate', choices=['feedback', 'command'], default='command',
                help='feedback: q_cmd = q_측정 + q̇Δt (Cyclo 방식) / command: q_cmd = q_cmd + q̇Δt')
ap.add_argument('--out', default='arm_ik', help='결과 파일 이름 앞부분')
ap.add_argument('--view', action='store_true')
args = ap.parse_args()

m = mujoco.MjModel.from_xml_path(args.scene)
d = mujoco.MjData(m)
dt = m.opt.timestep
n_ctrl = max(1, round(1.0 / (args.rate * dt)))         # 시뮬 몇 스텝마다 IK를 돌릴지
dt_ctrl = n_ctrl * dt

ARM = [f'arm_r_joint{i}' for i in range(1, 8)]
jid = [m.joint(n).id for n in ARM]
dof = np.array([m.jnt_dofadr[j] for j in jid])          # 자코비안에서 쓸 열
qadr = np.array([m.jnt_qposadr[j] for j in jid])
qmin, qmax = m.jnt_range[jid, 0], m.jnt_range[jid, 1]
aid = np.array([m.actuator(n).id for n in ARM])          # 액추에이터 이름 = 관절 이름
ee = m.body('end_effector_r_link').id
base = m.body('base_link').id

# 위치 액추에이터 목표 = 현재 관절값 → 1초 정착 (바퀴로 바닥에 서는 시간)
for i in range(m.nu):
    if m.actuator_biastype[i] != 0:
        d.ctrl[i] = d.qpos[m.jnt_qposadr[m.actuator_trnid[i][0]]]
for _ in range(int(1.0 / dt)):
    mujoco.mj_step(m, d)

p0 = d.xpos[ee].copy()
quat0 = np.zeros(4); mujoco.mju_mat2Quat(quat0, d.xmat[ee])     # 자세는 시작 자세 유지
Rb, pb = d.xmat[base].reshape(3, 3).copy(), d.xpos[base].copy()
p1 = pb + Rb @ np.array(args.target)                    # base_link 기준 → world
print(f'[{args.solver}/{args.profile}/{args.integrate}] 시작 {np.round(p0,3)} → 목표 {np.round(p1,3)}, 거리 {np.linalg.norm(p1-p0):.3f} m')


def scaling(t, T):
    tau = np.clip(t / T, 0.0, 1.0)
    if args.profile == 'quintic':
        return 10*tau**3 - 15*tau**4 + 6*tau**5, (30*tau**2 - 60*tau**3 + 30*tau**4) / T
    return 3*tau**2 - 2*tau**3, (6*tau - 6*tau**2) / T


W = np.diag([10, 10, 10, 1, 1, 1.0])                     # Cyclo weight_position 10, weight_orientation 1
w_damp = 0.1                                             # Cyclo weight_damping 0.1


def solve_dls(J, xd):
    return J.T @ np.linalg.solve(J @ J.T + args.lam**2 * np.eye(6), xd)


def solve_qp(J, xd, q):
    import osqp
    from scipy import sparse
    P = 2 * (J.T @ W @ J + w_damp * np.eye(7))
    c = -2 * J.T @ W @ xd
    lo = np.maximum(-args.qdmax, -args.alpha * (q - qmin))   # CBF: q가 q_min에 다가가는 속도 제한
    hi = np.minimum(args.qdmax, args.alpha * (qmax - q))
    prob = osqp.OSQP()
    prob.setup(sparse.csc_matrix(np.triu(P)), c, sparse.identity(7, format='csc'), lo, hi, verbose=False)
    return prob.solve().x


q_cmd = d.qpos[qadr].copy()
jacp, jacr = np.zeros((3, m.nv)), np.zeros((3, m.nv))
dq = np.zeros(7)
log = []
if args.view:
    import mujoco.viewer
    viewer = mujoco.viewer.launch_passive(m, d)
else:
    viewer = None

step, t = 0, 0.0
while t < args.T + 1.0:
    s, ds = scaling(t, args.T)
    p_des = p0 + s * (p1 - p0)                           # 직선 경로 (MR 9.2.1)
    v_ff = ds * (p1 - p0)
    if step % n_ctrl == 0:                               # 100 Hz 제어 루프
        mujoco.mj_jacBody(m, d, jacp, jacr, ee)
        J = np.vstack([jacp[:, dof], jacr[:, dof]])       # 6×7
        e_p = p_des - d.xpos[ee]
        quat = np.zeros(4); mujoco.mju_mat2Quat(quat, d.xmat[ee])
        e_r = np.zeros(3); mujoco.mju_subQuat(e_r, quat0, quat)
        xd = np.hstack([v_ff + args.K * e_p, args.K * e_r])
        q_base = d.qpos[qadr].copy() if args.integrate == 'feedback' else q_cmd
        dq = solve_dls(J, xd) if args.solver == 'dls' else solve_qp(J, xd, q_base)
        q_cmd = np.clip(q_base + dq * dt_ctrl, qmin, qmax)
        d.ctrl[aid] = q_cmd
    mujoco.mj_step(m, d)
    step += 1
    t += dt
    if viewer is not None:
        viewer.sync()
    e_now = np.linalg.norm(p_des - d.xpos[ee])
    log.append([t, *p_des, *d.xpos[ee], e_now, np.abs(dq).max(), *(d.qpos[qadr] - q_cmd)])

log = np.array(log)
with open(args.out + '_log.csv', 'w', newline='') as f:
    w = csv.writer(f)
    w.writerow(['t', 'xd', 'yd', 'zd', 'x', 'y', 'z', 'pos_err', 'max_qdot'] + [f'sag_j{i}' for i in range(1, 8)])
    w.writerows(log)
sag = np.degrees(np.abs(log[-1, 9:16]).max())
print(f'최대 위치 오차 {log[:,7].max()*1000:.1f} mm · 최종 {log[-1,7]*1000:.1f} mm · '
      f'최대 관절 속도 {log[:,8].max():.2f} rad/s · 명령 대비 관절 처짐 최대 {sag:.2f} deg')

try:
    import matplotlib; matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    fig, ax = plt.subplots(2, 1, figsize=(7, 5), sharex=True)
    for k, c in enumerate('xyz'):
        ax[0].plot(log[:, 0], log[:, 1+k], '--', label=f'{c} desired')
        ax[0].plot(log[:, 0], log[:, 4+k], label=f'{c} actual')
    ax[0].set_ylabel('EE position [m]'); ax[0].legend(ncol=3, fontsize=7)
    ax[0].set_title(f'{args.solver.upper()} / {args.profile} / T={args.T}s')
    ax[1].plot(log[:, 0], log[:, 7] * 1000); ax[1].set_ylabel('pos error [mm]'); ax[1].set_xlabel('t [s]')
    fig.tight_layout(); fig.savefig(args.out + '_plot.png', dpi=120)
    print(f'저장: {args.out}_log.csv, {args.out}_plot.png')
except ImportError:
    print('matplotlib 없음 → CSV만 저장')
if viewer is not None:
    viewer.close()
