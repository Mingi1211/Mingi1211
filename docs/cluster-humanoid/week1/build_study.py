import sys, os
HERE = os.path.dirname(os.path.abspath(__file__))
_src = open(os.path.join(HERE, '..', 'plan', 'build_manual.py'), encoding='utf-8').read()
exec(_src.split('# =====')[0])          # 바탕체 10pt, 세로 A4, code()/table()/bullet() 등
from docx.shared import Cm as _Cm

SCENE = 'ai_worker/ffw_description/mujoco/ffw_sg2/scene.xml'


def step(no, title, when=''):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(8)
    p.paragraph_format.space_after = Pt(3)
    p.paragraph_format.keep_with_next = True
    shade_el(p._p.get_or_add_pPr(), 'D9E2F3')
    run(p, f'☐ STEP {no}. ', bold=True, size=11)
    run(p, title, bold=True, size=11)
    if when:
        run(p, f'   ({when})', size=9)


def ok(text):
    p = doc.add_paragraph()
    p.paragraph_format.left_indent = Cm(0.4)
    p.paragraph_format.space_after = Pt(1)
    run(p, '✔ 확인: ', bold=True)
    rich(p, text)


def ng(text):
    p = doc.add_paragraph()
    p.paragraph_format.left_indent = Cm(0.4)
    p.paragraph_format.space_after = Pt(1)
    run(p, '✗ 안 되면: ', bold=True)
    rich(p, text)


def part(title, sub):
    h = doc.add_heading(level=1)
    run(h, title, bold=True, size=13)
    para(sub, after=4)


def picture(path, width_cm, caption):
    doc.add_picture(os.path.join(HERE, path), width=_Cm(width_cm))
    doc.paragraphs[-1].alignment = WD_ALIGN_PARAGRAPH.CENTER
    p = para(caption, size=9, align=WD_ALIGN_PARAGRAPH.CENTER, after=6)


def mr(text):
    p = doc.add_paragraph()
    p.paragraph_format.left_indent = Cm(0.4)
    p.paragraph_format.space_after = Pt(1)
    shade_el(p._p.get_or_add_pPr(), 'FFF2CC')
    run(p, '▶ MR 읽기  ', bold=True)
    rich(p, text)


# =====================================================================
t = doc.add_paragraph(); t.alignment = WD_ALIGN_PARAGRAPH.CENTER
run(t, '1주차 정기미팅 — Cyclo 공부 매뉴얼', bold=True, size=16)
para('AI Worker2(FFW-SG2) 한 대 · MuJoCo에서 팔 움직이기 · Modern Robotics로 개념 잡기',
     align=WD_ALIGN_PARAGRAPH.CENTER)
para('군집 휴머노이드 과제 · 김민기 · 보고: 10/8(목) 정기 미팅 · 작성 2026-10-04',
     align=WD_ALIGN_PARAGRAPH.CENTER, after=8)

heading('0. 이번 주에 할 일 한눈에')
table([3.4, USABLE - 3.4], ['항목', '내용'], [
    ['목표', '교수님 1차 미팅 조언 그대로 — **Cyclo의 IK 구조를 먼저 이해**한다(궤적 생성, spline). 구현만 해보는 게 아니라 **아키텍처 · 기구학/IK · 궤적 생성 개념**을 Modern Robotics(MR)와 연결해 보고한다'],
    ['방법', 'Cyclo가 하는 일(목표 자세 → 보간 → 목표 속도 → QP IK → 관절 명령)을 **MuJoCo에서 ROS 없이 직접 재현**(= "미니 Cyclo")하고, 실제 Cyclo 소스와 한 줄씩 대응시킨다'],
    ['결과물 (목요일)', '① Cyclo 아키텍처 그림 ② QP 정식화 + MR 대응표 ③ MuJoCo 실험 결과(표 1개 + 그래프 2개) ④ 관찰과 다음 단계'],
    ['준비물', 'Ubuntu 24.04 PC · 인터넷 · MR 책(또는 PDF) · 이 매뉴얼 · **arm_ik_demo.py** (이 문서와 같은 폴더에 있음 → USB·메일·git으로 Ubuntu로 옮길 것)'],
    ['시간 (7시간)', '**월 21~23** PART A 환경·모델 / **화 21~23** PART B 미니 Cyclo·실험 / **수 20~23** PART C 소스 읽기 + PART D 보고 자료 / **목** 미팅'],
    ['참고', 'PART E(실제 Cyclo 패키지를 ROS 2로 MuJoCo·실로봇에 연결)는 **다음 주** 일. 실로봇 실행법은 「AI Worker2 매뉴얼(초안)」 3장'],
], first_bold=True)
para('표시 규칙: ☐ = 끝나면 체크 · ✔ = 이렇게 나오면 성공 · ✗ = 안 될 때 · ▶ MR 읽기 = 그날 읽을 MR 절. '
     '코드 박스의 "~/cyclo_study"는 작업 폴더이며, 명령은 그 폴더에서 venv를 켠 상태로 입력한다.', size=9)

heading('1. 큰 그림 — 왜 이 순서인가')
bullet('Cyclo Control은 ROS 2 노드 + C++ QP 라이브러리라서, 바로 실행하면 "돌아가긴 하는데 안에서 무슨 일이 일어나는지"가 안 보인다')
bullet('그래서 **이번 주는 Cyclo가 매 주기(100 Hz) 하는 계산을 파이썬 150줄로 똑같이 만들고**, MuJoCo로 결과를 눈과 숫자로 확인한다')
bullet('Cyclo의 MoveL 한 주기: ① 목표 자세와 시간 T를 받는다 → ② 3차 다항식으로 지금 있어야 할 자세 x_ref(t)를 만든다 → '
       '③ 목표 속도 v_d = v_ff + kp·(x_ref − x) → ④ QP로 관절 속도 q̇를 푼다 → ⑤ q_d = q + q̇·Δt를 관절 명령으로 보낸다')
bullet('이번 주에 만드는 미니 Cyclo도 ①~⑤가 같다. 다른 점은 2장 표와 STEP 12에 정리했다')

# ---------------------------------------------------------------------
part('PART A — 환경 만들고 모델 띄우기 (월 21~23)', '목표: MuJoCo에서 AI Worker2가 서 있고, 관절을 손으로 움직여 볼 수 있다.')

step(1, '작업 폴더와 파이썬 가상환경 만들기', '10분')
code('''mkdir -p ~/cyclo_study && cd ~/cyclo_study
sudo apt install -y python3-venv git
python3 -m venv venv
source venv/bin/activate          # 새 터미널마다 다시 실행
pip install --upgrade pip
pip install mujoco numpy matplotlib osqp scipy''')
ok('python3 -c "import mujoco; print(mujoco.__version__)" → **3.4 이상**이면 된다 (작성자는 3.14.0에서 확인)')
ng('나중에 "body mass is too small" 에러가 나면 MuJoCo가 옛 버전이다 → pip install -U mujoco. '
   'Ubuntu 24.04는 시스템 파이썬에 바로 pip 설치가 막혀 있으니 반드시 venv 안에서 설치')

step(2, 'AI Worker 모델(MJCF) 받기', '10분 · 약 150MB')
code('''cd ~/cyclo_study
git clone --depth 1 --filter=blob:none --sparse https://github.com/ROBOTIS-GIT/ai_worker.git
cd ai_worker && git sparse-checkout set ffw_description && cd ..
ls ai_worker/ffw_description/mujoco/ffw_sg2''')
ok('ffw_sg2.xml  scene.xml 두 파일이 보인다. 메시는 ffw_description/meshes에 있다 (xml의 meshdir="../../")')
bullet('sparse checkout = 저장소 전체가 아니라 ffw_description 폴더만 받는 방법. MuJoCo 모델은 ROBOTIS가 2.2.8 버전부터 ai_worker 저장소 안에서 관리한다')

step(3, '뷰어로 열어서 관절 움직여 보기', '20분')
code('python3 -m mujoco.viewer --mjcf=' + SCENE)
ok('로봇이 바닥에 서 있다. 오른쪽 패널 **Control**의 arm_r_joint1~7 슬라이더를 하나씩 움직이며 각 관절이 어느 축으로 도는지 메모')
ok('Ctrl + 오른쪽 드래그로 물체에 힘을 줄 수 있다 → 팔이 밀렸다가 돌아오면 위치 액추에이터(PD)가 동작하는 것')
ng('SSH 원격이라 화면이 없으면 뷰어는 건너뛴다. STEP 7부터는 --view 없이 실행해도 그래프와 CSV가 저장된다')
table([3.2, 2.6, 3.6, USABLE - 9.4], ['관절', '회전축', '범위 [rad]', '내 메모 (어느 방향으로 움직이나)'], [
    ['arm_r_joint1', 'y', '−3.14 ~ 3.14', ''], ['arm_r_joint2', 'x', '−3.14 ~ 0', ''],
    ['arm_r_joint3', 'z', '−3.14 ~ 3.14', ''], ['arm_r_joint4', 'y', '−2.94 ~ 1.08', ''],
    ['arm_r_joint5', 'z', '−3.14 ~ 3.14', ''], ['arm_r_joint6', 'y', '−1.57 ~ 1.57', ''],
    ['arm_r_joint7', 'x', '−1.82 ~ 1.58', ''],
], first_bold=False, center_cols=(1, 2))

step(4, 'Cyclo 소스 받기 (읽기용, 빌드 안 함)', '5분')
code('''cd ~/cyclo_study
git clone --depth 1 https://github.com/ROBOTIS-GIT/cyclo_control.git''')
ok('아래 다섯 파일이 있는지 확인 (PART C에서 읽는다)')
table([9.2, USABLE - 9.2], ['파일', '하는 일'], [
    ['cyclo_motion_controller_ros/src/nodes/ai_worker/ai_worker_movel_controller_node.cpp', 'MoveL 노드: 3차 보간, v_d 계산, QP 호출, 관절 명령 발행'],
    ['cyclo_motion_controller_core/src/controllers/ai_worker/vr_controller.cpp', 'QP의 비용·제약을 만드는 곳 (MoveL도 이 클래스를 상속)'],
    ['cyclo_motion_controller_core/include/.../optimization/qp_base.hpp', 'OSQP 래퍼: 변수·제약 크기, 풀기'],
    ['cyclo_motion_controller_core/src/kinematics/kinematics_solver.cpp', 'Pinocchio: FK, 자코비안, 자기충돌 거리'],
    ['cyclo_motion_controller_ros/config/ai_worker_config.yaml', '게인·가중치·CBF 등 파라미터'],
], first_bold=False)

step(5, '모델 정보 출력해 보기', '15분')
para('~/cyclo_study 에 model_info.py로 저장하고 실행:')
code('''import mujoco, numpy as np
m = mujoco.MjModel.from_xml_path('ai_worker/ffw_description/mujoco/ffw_sg2/scene.xml')
d = mujoco.MjData(m)
mujoco.mj_forward(m, d)                    # 순기구학 계산 (MR 4장)
print('nq =', m.nq, ' nv =', m.nv, ' nu =', m.nu, ' timestep =', m.opt.timestep)
for i in range(1, 8):
    j = m.joint(f'arm_r_joint{i}')
    print(f'arm_r_joint{i}: 축 {j.axis}, 범위 {np.round(j.range, 3)} rad')
a = m.actuator('arm_r_joint1')
print('arm_r_joint1 액추에이터 kp =', a.gainprm[0], ' 힘 범위 =', a.forcerange)
print('오른손 끝(end_effector_r_link) 위치 =', np.round(d.body('end_effector_r_link').xpos, 3))''')
ok('nq = 38, nv = 37, nu = 25, timestep = 0.002 · kp = 3000, 힘 범위 ±61.4 · 손끝 위치 [−0.02, −0.227, 0.725]')
bullet('nq(38) ≠ nv(37)인 이유: 베이스가 free joint라 위치는 쿼터니언 4개, 속도는 각속도 3개로 표현되기 때문 (MR 3장 회전 표현)')
bullet('관절마다 **위치 액추에이터(kp·오차 − kv·속도)**가 달려 있다 = 실제 DYNAMIXEL 위치 제어 모드를 흉내 낸 것')
mr('**4.1 (PoE 순기구학)** 훑기 → **5.1 (자코비안: space / body)** 정독. '
   '질문: ① space 자코비안과 body 자코비안은 어떤 좌표계에서 본 twist인가? ② 7자유도 팔의 자코비안은 몇 × 몇인가? (6×7)')

# ---------------------------------------------------------------------
part('PART B — 미니 Cyclo 돌리고 실험하기 (화 21~23)', '목표: 오른팔을 Cyclo MoveL 예시와 같은 목표(base_link 기준 0.35, −0.20, 0.85)로 보내고, 파라미터를 바꿔 차이를 숫자로 본다.')

step(6, 'arm_ik_demo.py 옮기기', '5분')
para('이 문서와 같은 폴더의 arm_ik_demo.py를 ~/cyclo_study 로 복사한다. 전체 코드는 부록 B에 있다.')

step(7, '기본 실행', '10분')
code('python3 arm_ik_demo.py --scene ' + SCENE + ' --view')
ok('터미널에 아래와 비슷한 값이 나온다 (작성자가 Windows + MuJoCo 3.14로 돌린 값. 환경에 따라 조금 다를 수 있음)')
code('''[dls/quintic/command] 시작 [-0.02 -0.227 0.571] → 목표 [0.35 -0.2 0.85], 거리 0.464 m
최대 위치 오차 6.8 mm · 최종 0.1 mm · 최대 관절 속도 1.06 rad/s · 명령 대비 관절 처짐 최대 0.42 deg''')
ok('arm_ik_plot.png 가 생기고 아래 그림처럼 실제 궤적(실선)이 목표(점선)를 따라간다')
picture('E1_plot.png', 12.5, '참고 그림 — 기본 실행 결과 (DLS, 5차, T = 3 s)')
bullet('시작 위치 z가 0.725가 아니라 0.571인 이유: 처음 1초 동안 로봇이 바퀴로 바닥에 내려앉기 때문')

step(8, '코드 읽기 — 한 블록씩 Cyclo·MR과 연결', '30분')
table([4.2, 5.6, USABLE - 9.8], ['코드 블록 (arm_ik_demo.py)', '대응하는 Cyclo 코드', 'MR 개념'], [
    ['scaling(): 5차 / 3차 시간 스케일링', 'movel 노드의 cubicVector, rotationCubic (Cyclo는 **3차**)', '9.2 시간 스케일링'],
    ['p_des = p0 + s·(p1 − p0)', '직선 보간 (MoveL = linear)', '9.2.1 직선 경로'],
    ['xd = v_ff + K·e', 'desired_vel = feedforward + kp_position·error (358행)', '11.3 속도 입력 작업공간 제어'],
    ['mj_jacBody → J (6×7)', 'getJacobian (Pinocchio LOCAL_WORLD_ALIGNED)', '5.1 자코비안'],
    ['solve_dls()', '(Cyclo에는 없음, QP 대신 쓰는 단순판)', '6.3 역속도 기구학, 특이점 감쇠'],
    ['solve_qp()', 'VRController::setCost / setBoundConstraint / setIneqConstraint', 'MR 밖 — QP, CBF (STEP 11)'],
    ['q_cmd = q_base + dq·Δt', 'q_desired_ = q_feedback + optimal_velocities·time_step (499행)', '수치 적분'],
    ['d.ctrl[aid] = q_cmd', 'JointTrajectory 발행 → follower 위치 제어', '—'],
], first_bold=False)
bullet('**자코비안 좌표계 주의**: MuJoCo mj_jacBody와 Pinocchio LOCAL_WORLD_ALIGNED는 둘 다 "말단 위치에서의 속도를 world 축으로 표현"한 것이다. '
       'MR의 space 자코비안(world 원점 기준)이나 body 자코비안(말단 축 기준)과 **둘 다 조금 다르다** → 보고 때 짚으면 좋은 포인트')

step(9, '실험 8개 — 하나씩 바꿔 보기', '50분')
para('기본 명령 뒤에 아래 옵션을 붙여 실행한다. 결과는 --out 이름으로 따로 저장된다 (예: E3_plot.png).')
code('python3 arm_ik_demo.py --scene ' + SCENE + ' --K 5 --out E3      # 예시')
table([1.0, 4.4, 2.0, 2.0, 2.2, USABLE - 11.6], ['#', '옵션', '최대 오차', '최종 오차', '최대 q̇', '볼 것 · 내 결과'], [
    ['E1', '(기본) DLS, 5차, T=3 s, K=50', '6.8 mm', '0.1 mm', '1.06', '기준'],
    ['E2', '--profile cubic', '7.2', '0.0', '0.98', 'Cyclo와 같은 3차. 시작·끝 가속도 차이'],
    ['E3', '--K 5', '13.2', '3.5', '1.07', '피드백 게인이 작으면 뒤처짐'],
    ['E4', '--lam 0.3', '38.5', '0.0', '1.41', '감쇠가 크면 특이점엔 강하지만 추종이 느림'],
    ['E5', '--solver qp', '4.7', '0.0', '1.11', 'Cyclo식 QP. 결과가 DLS와 비슷한지'],
    ['E6', '--T 1.0', '180.4', '112.3', '**12.92**', 'DLS는 속도 한계가 없어 명령이 폭주'],
    ['E7', '--T 1.0 --solver qp', '104.2', '3.6', '**1.50**', 'QP는 속도 한계(1.5)를 지키는 대신 뒤처짐'],
    ['E8', '--integrate feedback', '32.1', '**11.8**', '3.58', 'Cyclo 적분 방식 → 중력 처짐으로 오차가 남음'],
], first_bold=True, center_cols=(0, 2, 3, 4))
picture('compare.png', 15.0, '왼쪽: 명령 적분(E1) vs 측정값 기준 적분(E8) / 오른쪽: 빠른 이동에서 DLS(E6) vs QP(E7)의 관절 속도')
bullet('**E6 vs E7 (보고 핵심 ①)**: 제약이 없는 DLS는 관절 속도가 12.9 rad/s까지 튀고 로봇이 명령을 못 따라간다. '
       'QP는 속도 한계를 제약으로 넣었기 때문에 1.5 rad/s를 넘지 않는다 → **Cyclo가 QP를 쓰는 이유를 숫자로 보여주는 실험**')
bullet('**E8 (보고 핵심 ②)**: Cyclo처럼 "측정 관절각 + q̇Δt"를 명령으로 주면, 위치 액추에이터 목표가 측정값과 거의 같아 **중력을 버틸 토크가 안 나온다** → 11.8 mm 정상상태 오차. '
       '실제 DYNAMIXEL은 내부 게인이 더 강해 덜할 수 있지만(확인 필요), 교수님이 말씀하신 **"하중에 의한 처짐을 모델에 넣어 feedforward"**가 필요한 이유와 연결된다')
mr('**6.2 (Newton–Raphson 수치 IK)**, **6.3 (역속도 기구학, 의사역행렬)**, **9.1~9.2 (경로·시간 스케일링, 3차·5차 다항식)**, **11.3 (속도 입력 작업공간 제어)**. '
   '질문: ③ 3차와 5차 시간 스케일링은 경계 조건이 몇 개씩이고 무엇이 0인가? ④ Newton–Raphson IK(한 번에 수렴할 때까지 반복)와 Cyclo의 미분 IK(주기마다 한 번)는 무엇이 다른가?')

# ---------------------------------------------------------------------
part('PART C — Cyclo 소스로 아키텍처와 QP 정리 (수 20~21:30)', '목표: 아래 그림의 상자마다 실제 파일·함수를 확인하고, QP를 수식으로 적는다.')

step(10, 'MoveL 아키텍처 따라가기', '40분')
picture('cyclo_arch.png', 16.0, 'Cyclo MoveL 한 주기 (100 Hz) — 작성자가 소스에서 확인한 구조')
para('그림의 번호 순서대로 파일을 열고 체크한다:')
for txt in [
    '① ai_worker_config.yaml에서 right_movel_topic = /r_goal_move 확인',
    '② movel 노드에서 cubicVector / rotationCubic 호출부(약 405~455행)와 desired_vel = feedforward + kp_position·error(358행) 찾기',
    '③ kinematics_solver.cpp에서 pinocchio::computeFrameJacobian(..., LOCAL_WORLD_ALIGNED) 와 computeDistances(자기충돌) 찾기',
    '④ vr_controller.cpp의 setCost(), setBoundConstraint(), setIneqConstraint() 세 함수 읽기',
    '⑤ movel 노드 499행 q_desired_ = q_feedback + optimal_velocities * time_step_',
    '⑥ publishTrajectory()에서 JointTrajectory의 time_from_start = trajectory_time (기본 0.0)',
    '⑦ joint_state_timeout: /joint_states가 끊기면 명령을 멈추는 안전장치',
]:
    bullet('☐ ' + txt)

step(11, 'QP 정식화를 수식으로 적기', '50분')
para('vr_controller.cpp를 보며 아래 빈칸을 채운다 (작성자가 읽은 내용을 미리 적어 둠 — 직접 확인할 것):')
table([3.0, 6.6, USABLE - 9.6], ['구성', '수식', '코드 · 의미'], [
    ['결정 변수', 'x = [q̇, s_qmin, s_qmax, s_sing, s_col]', 'q̇ = 관절 속도, s = slack(제약을 조금 어겨도 되게 하는 변수)'],
    ['비용', 'Σ (J_i q̇ − v_d,i)ᵀ W_i (J_i q̇ − v_d,i) + q̇ᵀ W_d q̇ + ρ Σ s', 'setCost(). W = weight_position 10 / orientation 1, W_d = weight_damping 0.1, ρ = slack_penalty 1000'],
    ['속도 한계', 'q̇_min ≤ q̇ ≤ q̇_max,  s ≥ 0', 'setBoundConstraint(). 관절 속도 한계는 URDF에서'],
    ['관절 한계 CBF', 'q̇ + s ≥ −α (q − q_min),  −q̇ + s ≥ −α (q_max − q)', 'setIneqConstraint(). α = cbf_alpha 50'],
    ['자기충돌 CBF', 'ḋ(q̇) + s ≥ −α (d − d_safe)   (d ≤ collision_buffer일 때만)', 'd = 링크 사이 최소 거리, d_safe = 0.02, buffer = 0.05'],
    ['특이점', '제약 1개 + slack 1개 (s_sing)', '코드에서 직접 확인할 것 — 조작성(manipulability) 관련으로 추정'],
], first_bold=True)
bullet('**CBF(Control Barrier Function) 한 줄 설명**: 안전 거리 h(q) ≥ 0을 지키고 싶을 때 "ḣ ≥ −α·h"를 걸면, h가 0에 가까워질수록 줄어드는 속도도 0에 가까워진다 → 경계를 넘지 않고 부드럽게 멈춘다. MR에는 없는 개념이니 슬라이드에 1장으로 설명')
bullet('**slack을 쓰는 이유**: 제약끼리 충돌해 QP가 풀리지 않으면 로봇이 멈춘다. slack에 큰 벌점(1000)을 주면 평소엔 0이고, 불가능할 때만 조금 어긴다')
bullet('**DLS와의 관계**: 제약을 전부 빼면 비용의 최소점은 (JᵀWJ + W_d)q̇ = JᵀW v_d → W = I, W_d = λ²I이면 DLS 식과 같다. **즉 DLS는 제약 없는 QP의 특수한 경우**')

step(12, '내 미니 Cyclo와 실제 Cyclo의 차이 정리', '10분')
table([4.0, 5.6, USABLE - 9.6], ['항목', '실제 Cyclo', '미니 Cyclo (arm_ik_demo.py)'], [
    ['언어 · 통신', 'C++ / ROS 2 토픽', '파이썬 / ROS 없음'],
    ['보간', '3차 (cubicVector, rotationCubic)', '5차 기본, --profile cubic으로 3차. 자세는 고정'],
    ['IK', 'QP (OSQP), slack 포함', 'DLS 기본, --solver qp는 slack 없는 단순 QP'],
    ['제약', '관절 한계 CBF + 속도 한계 + 자기충돌 CBF + 특이점', '관절 한계 CBF + 속도 한계 (충돌 없음)'],
    ['관절 속도 한계', 'URDF 값', '1.5 rad/s 가정값 (--qdmax)'],
    ['적분', '측정값 기준 (q_측정 + q̇Δt)', '명령값 기준 기본, --integrate feedback으로 Cyclo 방식'],
    ['자코비안', 'Pinocchio (URDF)', 'MuJoCo (MJCF) — 같은 로봇, 다른 모델 파일'],
], first_bold=True)

# ---------------------------------------------------------------------
part('PART D — 목요일 보고 자료 만들기 (수 21:30~23)', '슬라이드 7장. 그림과 표는 이 문서와 내가 만든 결과를 그대로 쓴다.')
step(13, '슬라이드 구성', '80분')
table([1.0, 4.0, USABLE - 5.0], ['#', '제목', '넣을 것'], [
    ['1', '이번 주 목표', '교수님 조언(IK 구조 이해 우선) → 방법: Cyclo를 MuJoCo에서 직접 재현해 이해'],
    ['2', 'Cyclo 아키텍처', 'STEP 10 그림 + 각 상자의 파일 이름'],
    ['3', 'IK = QP', 'STEP 11 수식 표 + CBF 한 줄 설명 + "DLS는 제약 없는 QP의 특수한 경우"'],
    ['4', 'MR 개념 대응', 'STEP 8 표 (시간 스케일링 9.2, 자코비안 5.1, 역속도 6.3, 속도 제어 11.3) + 자코비안 좌표계 차이'],
    ['5', '실험 결과', 'STEP 9 표(내 결과로 교체) + 비교 그래프'],
    ['6', '관찰', '① 빠른 이동에서 DLS는 속도 한계 위반, QP는 지킴 → QP를 쓰는 이유 ② 측정값 기준 적분은 중력 처짐으로 오차 → 중력·하중 feedforward 필요 ③ Cyclo는 3차, 5차와 차이는 작았음'],
    ['7', '다음 주 계획 · 질문', 'PART E(실제 Cyclo + MuJoCo/실로봇 연결), 힘 계층을 어디에 붙일지, 교수님께 여쭐 것 1~2개'],
], first_bold=True, center_cols=(0,))
heading('예상 질문과 답할 거리', 2)
table([5.6, USABLE - 5.6], ['질문', '답할 거리'], [
    ['왜 ROS로 Cyclo를 바로 안 돌렸나?', 'IK 구조를 이해하는 게 먼저라는 조언에 따라, 계산을 직접 재현해 숫자로 확인했다. 실제 패키지 연결은 다음 주(PART E)'],
    ['Cyclo는 왜 QP를 쓰나?', 'E6/E7 결과: 제약 없는 IK는 관절 속도 한계를 넘는다. QP는 속도·관절 한계·충돌을 제약으로 직접 넣을 수 있다'],
    ['CBF가 뭔가?', '"ḣ ≥ −α·h" — 경계에 가까울수록 다가가는 속도를 줄여 경계를 넘지 않게 하는 선형 부등식. QP에 그대로 들어간다'],
    ['3차와 5차 차이는?', '3차는 시작·끝 속도만 0, 5차는 가속도까지 0 → 5차가 더 부드럽다. 이번 실험에선 오차 차이가 작았다'],
    ['힘 제어는 어디에 붙나?', 'Cyclo 출력은 위치 수준 관절 명령이다. 힘은 그 아래 토크·전류 계층(중력 보상, 임피던스)에 붙여야 하고, E8의 처짐이 그 필요성을 보여준다'],
], first_bold=True)

# ---------------------------------------------------------------------
part('PART E — 다음 주: 실제 Cyclo 패키지 연결 (참고, 미검증)', '이번 주 필수 아님. 방향만 잡아 둔다.')
bullet('**길 1 (실로봇)**: 「AI Worker2 매뉴얼(초안)」 3장 순서대로 bringup → Cyclo movel 실행 → /r_goal_move에 이번 주와 **같은 목표**(0.35, −0.20, 0.85)를 보내고, /r_gripper_pose를 기록해 MuJoCo 결과와 비교')
bullet('**길 2 (시뮬)**: ROS 2 Jazzy에서 MuJoCo + ros2_control로 AI Worker를 띄우는 공개 패키지(shkwon98/mujoco_ros2_control_menagerie)가 있다')
code('''ros2 launch ai_worker_mujoco_bringup robot.launch.py robot_model:=ffw_sg2
ros2 launch cyclo_motion_controller_ros ai_worker_controller.launch.py controller_type:=movel''')
bullet('예상 문제: Cyclo 출력 토픽(/leader/joint_trajectory_command_broadcaster_right/joint_trajectory)과 시뮬 팔 컨트롤러 입력 토픽 이름이 다르다 → '
       'ros2 control list_controllers, ros2 topic info -v로 확인 후 리매핑 또는 relay 노드 필요. 팔 한쪽 관절만 담은 명령을 받아주는지(부분 관절 명령)도 확인')
bullet('Zenoh RMW(rmw_zenoh_cpp)가 필요한지, ROS 2 Jazzy 설치 여부도 확인')

# ---------------------------------------------------------------------
heading('부록 A. 문제가 생겼을 때')
table([5.4, USABLE - 5.4], ['증상', '해결'], [
    ['ValueError: body mass is too small', 'MuJoCo가 옛 버전 → pip install -U mujoco'],
    ['error: externally-managed-environment', 'venv를 안 켰다 → source ~/cyclo_study/venv/bin/activate'],
    ['XML Error: mesh file not found', 'STEP 2의 sparse checkout이 안 됨 → ai_worker/ffw_description/meshes 폴더 확인'],
    ['뷰어 창이 안 뜸 (SSH)', '--view 빼고 실행. 그래프는 PNG로 저장된다'],
    ['ModuleNotFoundError: osqp', '--solver qp 할 때만 필요 → pip install osqp scipy'],
    ['결과가 표와 크게 다름', 'MuJoCo 버전·모델 버전 차이일 수 있다. 경향(E6 폭주, E7 한계 유지, E8 처짐)이 같으면 OK'],
], first_bold=False)

heading('부록 B. arm_ik_demo.py 전체 코드')
para('파일로 같은 폴더에 있다. 아래는 읽기용.', size=9)
code(open(os.path.join(HERE, 'arm_ik_demo.py'), encoding='utf-8').read())

heading('참고', 2)
for s in ['Modern Robotics (Lynch & Park): 4.1, 5.1, 6.2~6.3, 9.1~9.2, 11.3',
          'Cyclo: https://github.com/ROBOTIS-GIT/cyclo  ·  Cyclo Control: https://github.com/ROBOTIS-GIT/cyclo_control',
          'Cyclo Control 문서: https://docs.robotis.com/docs/systems/aiworker/advanced_features/cyclo_control',
          'AI Worker MuJoCo 모델: https://github.com/ROBOTIS-GIT/ai_worker (ffw_description/mujoco)',
          'MuJoCo + ros2_control: https://github.com/shkwon98/mujoco_ros2_control_menagerie']:
    bullet(s)

doc.save(OUT)
print('saved', OUT)
