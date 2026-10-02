import sys
from docx import Document
from docx.shared import Pt, Cm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_CELL_VERTICAL_ALIGNMENT
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

OUT = sys.argv[1]
FONT = '바탕체'
doc = Document()

def _fonts(rpr):
    f = rpr.find(qn('w:rFonts'))
    if f is None:
        f = OxmlElement('w:rFonts'); rpr.insert(0, f)
    for k in ('w:ascii', 'w:hAnsi', 'w:eastAsia', 'w:cs'):
        f.set(qn(k), FONT)

for sname in ('Normal', 'Heading 1', 'Heading 2'):
    st = doc.styles[sname]
    st.font.name = FONT
    st.font.color.rgb = RGBColor(0, 0, 0)
    _fonts(st.element.get_or_add_rPr())
doc.styles['Normal'].font.size = Pt(10)
doc.styles['Normal'].paragraph_format.space_after = Pt(2)
doc.styles['Normal'].paragraph_format.line_spacing = 1.15
for n, sz, b, a in (('Heading 1', 13, 14, 4), ('Heading 2', 11, 8, 3)):
    doc.styles[n].font.size = Pt(sz)
    doc.styles[n].paragraph_format.space_before = Pt(b)
    doc.styles[n].paragraph_format.space_after = Pt(a)

sec = doc.sections[0]
sec.page_width, sec.page_height = Cm(21.0), Cm(29.7)
sec.left_margin = sec.right_margin = Cm(2.0)
sec.top_margin = sec.bottom_margin = Cm(2.0)
USABLE = 21.0 - 4.0


def run(p, text, bold=False, size=10):
    r = p.add_run(text)
    r.bold = bold
    r.font.size = Pt(size)
    r.font.name = FONT
    _fonts(r._element.get_or_add_rPr())
    return r


def rich(p, text, bold=False, size=10):
    for i, t in enumerate(text.split('**')):
        if t:
            run(p, t, bold=bold or i % 2 == 1, size=size)


def para(text='', bold=False, size=10, align=None, after=None):
    p = doc.add_paragraph()
    if align is not None:
        p.alignment = align
    if after is not None:
        p.paragraph_format.space_after = Pt(after)
    rich(p, text, bold, size)
    return p


def bullet(text, level=0):
    p = doc.add_paragraph()
    pf = p.paragraph_format
    pf.left_indent = Cm(0.5 + 0.6 * level)
    pf.first_line_indent = Cm(-0.4)
    pf.space_after = Pt(1)
    rich(p, ('- ' if level == 0 else '· ') + text)


def heading(text, level=1):
    h = doc.add_heading(level=level)
    run(h, text, bold=True, size=13 if level == 1 else 11)


def shade_el(el_pr, fill):
    shd = OxmlElement('w:shd')
    shd.set(qn('w:val'), 'clear'); shd.set(qn('w:color'), 'auto'); shd.set(qn('w:fill'), fill)
    el_pr.append(shd)


def code(text):
    """회색 배경 코드 블록 — 줄마다 한 문단"""
    lines = text.strip('\n').split('\n')
    for k, line in enumerate(lines):
        p = doc.add_paragraph()
        pf = p.paragraph_format
        pf.left_indent = Cm(0.4)
        pf.space_after = Pt(0)
        pf.space_before = Pt(3) if k == 0 else Pt(0)
        pf.line_spacing = 1.0
        if k == len(lines) - 1:
            pf.space_after = Pt(4)
        shade_el(p._p.get_or_add_pPr(), 'F2F2F2')
        r = run(p, line if line else ' ', size=9)
        f = r._element.get_or_add_rPr().find(qn('w:rFonts'))
        f.set(qn('w:ascii'), 'Consolas'); f.set(qn('w:hAnsi'), 'Consolas')   # 바탕체는 \ 를 ₩로 표시하므로 코드의 영문만 Consolas
        if line.startswith(' '):
            t = r._element.find(qn('w:t'))
            t.set('{http://www.w3.org/XML/1998/namespace}space', 'preserve')


def memo():
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(2)
    rich(p, '□ 내 메모: ')
    run(p, '_' * 60)


def cell_text(cell, content, bold=False, center=False):
    cell.vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.CENTER if center else WD_CELL_VERTICAL_ALIGNMENT.TOP
    items = content if isinstance(content, list) else [content]
    for k, item in enumerate(items):
        p = cell.paragraphs[0] if k == 0 else cell.add_paragraph()
        p.paragraph_format.space_after = Pt(1)
        p.paragraph_format.line_spacing = 1.1
        if center:
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        if item.startswith('- '):
            p.paragraph_format.left_indent = Cm(0.3)
            p.paragraph_format.first_line_indent = Cm(-0.3)
        rich(p, item, bold=bold)


def table(widths, header, rows, first_bold=True, center_cols=()):
    t = doc.add_table(rows=1, cols=len(widths))
    t.style = 'Table Grid'
    t.alignment = WD_TABLE_ALIGNMENT.CENTER
    t.autofit = False
    for i, w in enumerate(widths):
        c = t.rows[0].cells[i]
        c.width = Cm(w)
        cell_text(c, header[i], bold=True, center=True)
        shade_el(c._tc.get_or_add_tcPr(), 'D9D9D9')
    trPr = t.rows[0]._tr.get_or_add_trPr()
    th = OxmlElement('w:tblHeader'); th.set(qn('w:val'), 'true'); trPr.append(th)
    for r in rows:
        row = t.add_row()
        cs = OxmlElement('w:cantSplit'); cs.set(qn('w:val'), 'true')
        row._tr.get_or_add_trPr().append(cs)
        for i, w in enumerate(widths):
            c = row.cells[i]
            c.width = Cm(w)
            cell_text(c, r[i], bold=(i == 0 and first_bold), center=(i in center_cols))
            if i == 0 and first_bold:
                shade_el(c._tc.get_or_add_tcPr(), 'F2F2F2')
    doc.add_paragraph().paragraph_format.space_after = Pt(2)


BASE = 'https://docs.robotis.com/docs/systems/aiworker/'

# =====================================================================
t = doc.add_paragraph(); t.alignment = WD_ALIGN_PARAGRAPH.CENTER
run(t, 'AI Worker2 (FFW-SG2) 사용 매뉴얼 — 초안', bold=True, size=16)
para('ROBOTIS 공식 문서 + 랩 실사용 메모 정리 · 작성 2026-10-02 · 이 초안을 읽고 이해한 대로 고쳐 쓸 것',
     align=WD_ALIGN_PARAGRAPH.CENTER, after=8)

heading('0. 이 문서를 쓰는 법')
bullet('**1장의 순서대로** 공식 문서를 읽는다. 각 항목에 "무엇을 중점적으로 볼지"를 적어 두었다')
bullet('3장은 랩에서 받은 실사용 메모를 실행 순서대로 정리하고 명령마다 설명을 붙인 것이다. 로봇 앞에서는 3장만 보면 된다')
bullet('각 절 끝의 "□ 내 메모" 칸에 직접 확인한 내용을 적는다. 공식 문서와 메모가 다른 곳은 8장에 모아 두었다')
bullet('내용은 2026-10-02 기준 공식 문서를 읽고 정리한 것이며, **실제 로봇에서 확인하지 않은 부분은 "확인 필요"로 표시**했다')

# ---------------------------------------------------------------------
heading('1. 읽기 가이드라인 (순서대로)')
para('지금 목표(Cyclo Control 구조 이해, 참빛 협동 운반)에 필요한 것부터 읽는다. 모방학습·내비게이션·Autonomy Studio는 지금은 건너뛴다.')
table([0.9, 4.3, 8.8, 3.0], ['순서', '문서 (docs.robotis.com)', '중점적으로 볼 것', '왜'], [
    ['1', ['Specifications', '› Hardware'], ['- FFW-SG2 자유도 구성(팔 7×2, 그리퍼, 머리 2, 리프트 1, 베이스 6)', '- 관절별 DYNAMIXEL 모델', '- **페이로드: 정격 한 팔 3.0 kg / 양팔 6.0 kg, 최대 5.0 / 10.0 kg**', '- 팔 도달 거리 641 mm'], '참빛 박스 중량·규격 근거'],
    ['2', ['Specifications', '› Software'], ['- ros2_control 100 Hz, 컨트롤러 6개 이름과 역할', '- JointTrajectoryController = 위치 궤적 명령'], '내 명령이 어디로 들어가는지'],
    ['3', ['Quick Start Guide', '› Setup Overview › Hardware'], ['- 전원 켜는 순서 (키 2시 방향 → 전원 버튼 3초)', '- **처음 켜면 토크 오프 → 원격 E-STOP의 A 버튼을 눌러야 모터 통신 시작**', '- E-STOP 누르기/해제(시계 방향 회전 후 A)'], '안전, 로봇이 안 움직일 때 1순위 원인'],
    ['4', ['Setup Overview', '› Software'], ['- SSH 주소 형식(ffw-시리얼번호.local), 기본 계정', '- container.sh start / enter / stop', '- **로봇 Orin에서 apt upgrade 금지**'], '접속·도커 진입'],
    ['5', ['Setup Overview', '› Zenoh Communication'], ['- AI Worker 2.0.0부터 RMW가 Zenoh', '- 내 PC에서 로봇 토픽을 보려면 RMW_IMPLEMENTATION, ZENOH_CONFIG_OVERRIDE 설정 (포트 7447)'], '외부 PC에서 RViz·코드 실행'],
    ['6', ['Operation Guide', '› Cyclo Manager › Bringup'], ['- Zenoh 데몬 → Robot Bringup 순서', '- bringup 로그 위치 /var/log/ai_worker_bringup/current'], 'GUI로도 켤 수 있음'],
    ['7', ['Operation Guide', '› Teleoperation'], ['- 리더 실행 명령, **양손 트리거 2초 이상 눌러야 follower가 움직임**', '- 스워브 모드에서도 팔은 계속 움직임'], '데이터 수집·수동 조작'],
    ['8', ['Advanced Features', '› **Cyclo Control**'], ['- 모드 6개(movel, movej, bimanual_movel, bimanual_movej, vr, leader)', '- 입력·출력 토픽, MoveL 메시지 구조', '- 파라미터(가중치, CBF, slack) — **QP 구조를 읽는 실마리**', '- 문제 해결 절'], '**가장 중요.** 군집 휴머노이드 1주차 목표, 참빛 협동 운반과 직결'],
    ['9', ['Simulation', '› Gazebo'], ['- SG2 Gazebo 실행 명령, MoveIt use_sim'], '로봇 없이 연습'],
    ['10', ['Support', '› Clearing Multi-turn Error'], ['- 증상(에러 코드 0xc)과 처리 절차의 큰 흐름만', '- **직접 하지 말고 선배·교수님께 먼저 보고**'], '사고 시 대응'],
], center_cols=(0,))
para('문서 주소는 모두 ' + BASE + ' 아래에 있다 (예: ' + BASE + 'advanced_features/cyclo_control).')
memo()

# ---------------------------------------------------------------------
heading('2. 로봇 개요 (FFW-SG2)')
table([4.0, USABLE - 4.0], ['항목', '내용'], [
    ['자유도', '총 25: 팔 7×2, 그리퍼 1×2, 머리 2, 리프트 1, 모바일 베이스 6 (스워브 3륜: 조향 3 + 구동 3)'],
    ['액추에이터', '팔 1~3: YM080-230-R099-RH · 팔 4~6: YM070-210-R099-RH · 팔 7: PH42-020-S300-R · 리프트: YM080-230-B001-RH · 머리: XH540 / XH430 · 조향: YM070-210-R051-RH · 그리퍼: RH-P12-RN'],
    ['페이로드', '정격 한 팔 3.0 kg, 양팔 6.0 kg / 최대 한 팔 5.0 kg, 양팔 10.0 kg'],
    ['크기·무게', '604 × 602 × 1,623 mm · 90 kg · 팔 도달 641 mm(손목까지)'],
    ['베이스', '스워브 드라이브, 운용 속도 1.5 m/s'],
    ['전원·연산', '25 V 80 Ah 배터리(2,040 Wh) · NVIDIA Jetson AGX Orin 32GB (JetPack 6.2)'],
    ['센서', '머리 ZED Mini · 손목 RealSense D405 ×2 · LiDAR LakiBeam 1 ×2 · IMU'],
    ['내부 통신', 'U2D2, RS-485 4 Mbps, DYNAMIXEL Protocol 2.0'],
    ['소프트웨어', 'Docker 안의 ROS 2 Jazzy, ros2_control 100 Hz, RMW = Zenoh'],
])
heading('ros2_control 컨트롤러', 2)
table([5.2, 4.8, USABLE - 10.0], ['컨트롤러', '종류', '담당'], [
    ['arm_l_controller', 'JointTrajectoryController', '왼팔 + 그리퍼 (8)'],
    ['arm_r_controller', 'JointTrajectoryController', '오른팔 + 그리퍼 (8)'],
    ['head_controller', 'JointTrajectoryController', '머리 (2)'],
    ['lift_controller', 'JointTrajectoryController', '리프트 (1)'],
    ['swerve_drive_controller', 'SwerveDriveController', '베이스 (6, 속도 모드)'],
    ['joint_state_broadcaster', 'JointStateBroadcaster', '/joint_states 발행'],
], first_bold=False)
para('팔·리프트·머리는 모두 **위치 궤적(JointTrajectory)** 으로 명령한다. 토크(전류) 명령 경로는 기본 구성에 없다 → 참빛의 임피던스(전류 제어 모드)는 별도 확인이 필요하다.')
memo()

# ---------------------------------------------------------------------
heading('3. 실행 절차 (랩 메모 정리)')
heading('3-1. 켜기 전 확인', 2)
bullet('로봇이 **공유기(TP-Link)에 연결**돼 있는지, 내 PC도 같은 네트워크인지 확인')
bullet('로봇 전원: 키를 꽂아 **2시 방향** → **전원 버튼 3초**')
bullet('**원격 E-STOP의 A 버튼**을 눌렀는지 확인. 처음 켜면 토크가 꺼진 상태라 A를 눌러야 DYNAMIXEL과 통신한다')
bullet('E-STOP은 언제든 누를 수 있게 손 가까이 둔다. 해제는 버튼을 시계 방향으로 돌린 뒤 A')

heading('3-2. 접속과 도커 진입 (터미널마다 반복)', 2)
code('''ssh robotis@ffw-SNPR48A1043.local     # 우리 로봇 시리얼: SNPR48A1043
cd ai_worker
./docker/container.sh enter''')
bullet('비밀번호: root (공식 문서의 기본값). 랩 내부 정보이므로 외부에 공유하지 않는다')
bullet('컨테이너가 꺼져 있으면 enter 전에 ./docker/container.sh start')
bullet('**새 터미널을 열 때마다 ssh → docker 진입을 다시 해야 한다**')

heading('3-3. Zenoh 데몬 (확인 필요)', 2)
para('공식 문서는 AI Worker 2.0.0부터 **bringup 전에 Zenoh 데몬을 먼저 켜야 한다**고 한다. 랩 메모에는 이 단계가 없다. 로봇에서 자동으로 켜지는지 선배에게 확인하고, 아니면 별도 터미널에서 실행한다.')
code('ros2 run rmw_zenoh_cpp rmw_zenohd      # 또는 별칭 zenohd')

heading('3-4. Bringup (follower 로봇 스택 실행)', 2)
code('ros2 launch ffw_bringup ffw_sg2_follower_ai.launch.py')
bullet('랩 메모에는 "ffw_bringup \\ ffw_sg2..."처럼 줄바꿈 기호가 중간에 있다. **한 줄로 입력**해야 한다')
bullet('이 터미널은 계속 켜 둔다. 확인: 다른 터미널에서 ros2 topic echo /joint_states 가 나오면 정상')

heading('3-5. Cyclo Control로 팔 움직이기 (자기충돌 고려됨)', 2)
para('새 터미널(ssh + docker 진입)에서 컨트롤러 실행:')
code('ros2 launch cyclo_motion_controller_ros ai_worker_controller.launch.py controller_type:=movel')
para('또 새 터미널에서 오른팔 목표 자세 발행:')
code('''ros2 topic pub --once /r_goal_move robotis_interfaces/msg/MoveL "{
  pose: {
    header: {frame_id: 'base_link'},
    pose: {
      position: {x: 0.35, y: -0.20, z: 0.85},
      orientation: {x: 0.0, y: 0.0, z: 0.0, w: 1.0}
    }
  },
  time_from_start: {sec: 2, nanosec: 0}
}"''')
table([4.2, USABLE - 4.2], ['필드', '의미'], [
    ['/r_goal_move', '오른팔 MoveL 입력 토픽 (왼팔은 /l_goal_move)'],
    ['frame_id: base_link', '목표 자세를 로봇 베이스 좌표계로 준다'],
    ['position', '손끝 목표 위치 [m]. x 앞, y 왼쪽(+)/오른쪽(−), z 위 — 오른팔이라 y가 음수 (축 방향은 RViz에서 확인 필요)'],
    ['orientation', '목표 자세(쿼터니언). w=1은 base_link와 같은 방향'],
    ['time_from_start', '현재 자세 → 목표까지 걸리는 시간. 짧을수록 빠르다 → **처음엔 2초 이상**'],
])
bullet('MoveL은 손끝이 **직선 경로**로 가도록 보간하고, QP가 관절 범위·속도·자기충돌을 지키며 관절 궤적을 만든다')
bullet('출력은 /leader/joint_trajectory_command_broadcaster_right(left)/joint_trajectory 로 나간다')
bullet('RViz에서 마커로 움직이려면 launch 뒤에 start_interactive_marker:=true 추가')

heading('3-6. 리더(원격조종)', 2)
para('새 터미널(ssh + docker 진입):')
code('ros2 launch ffw_bringup ffw_lg2_leader_ai.launch.py')
bullet('**양손 트리거를 2초 이상** 눌러야 follower가 움직이기 시작한다. 처음엔 리더 위치로 천천히 가다가, 오차가 줄면 빠르게 따라온다')
bullet('그립 버튼 = 그리퍼, 오른쪽 조이스틱 = 리프트 상하, 왼쪽 조이스틱 = 머리')
bullet('스워브 모드(두 스위치 동시): 왼쪽 조이스틱 = 전후·좌우, 오른쪽 = 회전. **이때도 팔은 계속 움직인다**')
bullet('일시정지 = 양손 트리거 2초 / 종료 = 실행 터미널에서 Ctrl+C')

heading('3-7. 관절 궤적을 직접 보내기 (주의)', 2)
code('''ros2 topic pub --once \\
/leader/joint_trajectory_command_broadcaster_left/joint_trajectory \\
trajectory_msgs/msg/JointTrajectory \\
"{
  joint_names: ['arm_l_joint1','arm_l_joint2','arm_l_joint3','arm_l_joint4',
                'arm_l_joint5','arm_l_joint6','arm_l_joint7','gripper_l_joint1'],
  points: [{
    positions: [0.0, 0.2, 0.0, -0.4, 0.0, -0.2, 0.0, 0.02],
    time_from_start: {sec: 5, nanosec: 0}
  }]
}"''')
bullet('관절 7개[rad] + 그리퍼 1개, 5초 동안 이동')
bullet('**이 토픽은 Cyclo의 출력 토픽과 같다.** 여기로 직접 보내면 Cyclo의 QP(자기충돌·속도 제한)를 거치지 않는다 → 작은 값, 긴 시간으로만 시험')
bullet('안전하게 관절 명령을 주려면 Cyclo **movej** 모드를 켜고 …/raw_joint_trajectory 토픽으로 보낸다 (Cyclo가 걸러서 출력)')
bullet('(추정) 리더 텔레옵, Cyclo, 직접 발행이 모두 같은 토픽에 쓰므로 **동시에 켜지 않는다**')

heading('3-8. 끄기', 2)
bullet('명령 발행 중지 → Cyclo·리더 터미널 Ctrl+C → bringup Ctrl+C → 팔을 안전 자세로 둔 상태에서 E-STOP → 전원 (공식 문서에 끄는 순서가 따로 없어 켜는 순서의 역순으로 정리. 확인 필요)')
memo()

heading('3-9. 터미널 구성 한눈에', 2)
table([1.6, 5.0, USABLE - 6.6], ['터미널', '역할', '명령'], [
    ['T1', '(필요 시) Zenoh 데몬', 'ros2 run rmw_zenoh_cpp rmw_zenohd'],
    ['T2', 'Bringup', 'ros2 launch ffw_bringup ffw_sg2_follower_ai.launch.py'],
    ['T3', 'Cyclo 또는 리더 (둘 중 하나)', 'ros2 launch cyclo_motion_controller_ros ai_worker_controller.launch.py controller_type:=movel / ros2 launch ffw_bringup ffw_lg2_leader_ai.launch.py'],
    ['T4', '명령 발행·확인', 'ros2 topic pub … / ros2 topic echo /joint_states'],
], center_cols=(0,))

# ---------------------------------------------------------------------
heading('4. Cyclo Control 자세히')
heading('4-1. 모드', 2)
table([3.6, USABLE - 3.6], ['모드', '설명'], [
    ['movel (기본)', '손끝 목표 자세 + 시간 → 현재 자세에서 직선으로 보간한 경로를 따라감'],
    ['movej', '관절 공간 궤적을 받아 안전 제약을 걸러서 실행. 손끝 경로는 곡선이 될 수 있음'],
    ['bimanual_movel', '현재 양손 사이 변환을 "잡았다"고 고정(6D rigid grasp)한 뒤, 가상 물체를 직선 보간으로 이동 → **참빛 협동 운반과 같은 문제**'],
    ['bimanual_movej', '양손 상대 자세를 유지하며 관절 궤적을 걸러 실행'],
    ['vr / leader', 'VR 원격조종 / 리더 장치 동기화'],
])
heading('4-2. 토픽', 2)
table([7.6, 4.6, USABLE - 12.2], ['토픽', '메시지', '용도'], [
    ['/r_goal_move, /l_goal_move', 'robotis_interfaces/MoveL', 'movel 입력'],
    ['…broadcaster_right(left)/raw_joint_trajectory', 'JointTrajectory', 'movej 입력'],
    ['/capture_grasp', 'std_msgs/Bool', 'bimanual: true면 양손 상대 자세 고정'],
    ['/virtual_object_goal_move', 'robotis_interfaces/MoveL', 'bimanual: 가상 물체 목표'],
    ['…broadcaster_right(left)/joint_trajectory', 'JointTrajectory', '출력 (follower로 감)'],
    ['/r_gripper_pose, /l_gripper_pose', 'PoseStamped', '현재 손끝 자세 (로깅용)'],
    ['/joint_states', 'JointState', '측정 상태 (없으면 Cyclo가 멈춤)'],
], first_bold=False)
code('''# 양팔 예시 (controller_type:=bimanual_movel start_interactive_marker:=true 로 실행 후)
ros2 topic pub --once /capture_grasp std_msgs/msg/Bool "{data: true}"
ros2 topic pub --once /virtual_object_goal_move robotis_interfaces/msg/MoveL "{pose: {header: {frame_id: 'base_link'}, pose: {position: {x: 0.35, y: 0.0, z: 0.95}, orientation: {x: 0.0, y: 0.0, z: 0.0, w: 1.0}}}, time_from_start: {sec: 3, nanosec: 0}}"''')

heading('4-3. 파라미터 — QP 구조를 읽는 실마리 (ai_worker_config.yaml)', 2)
table([5.0, USABLE - 5.0], ['파라미터', '의미와 QP에서의 역할 (추정 포함, 소스로 확인할 것)'], [
    ['kp_position, kp_orientation', '손끝 위치·자세 오차에 곱하는 게인 → 목표 속도(작업공간)를 만든다'],
    ['weight_position, weight_orientation', 'QP 비용에서 위치·자세 추종의 가중치'],
    ['weight_damping', '관절 속도 크기를 줄이는 정규화 항 (DLS의 댐핑과 같은 역할)'],
    ['collision_buffer, collision_safe_distance', '자기충돌 거리 여유'],
    ['cbf_alpha', '제어 장벽 함수(CBF)의 반응 속도 → 충돌 거리가 줄어드는 속도를 제한하는 제약'],
    ['slack_penalty', '제약을 조금 어겨도 되게 하는 slack 변수의 비용 → QP가 풀리지 않는 상황 방지'],
    ['lift_vel_bound', '리프트 관절 속도 범위 (0이면 리프트 사용 안 함) → 리프트를 IK에 넣을지 결정'],
    ['control_frequency, time_step, trajectory_time', '루프 주기와 출력 궤적의 시간 필드'],
    ['joint_state_timeout', '/joint_states가 이보다 오래되면 명령을 멈추고 유지'],
    ['kp_joint, weight_tracking (movej)', '관절 공간 추종 게인과 가중치'],
])
para('읽을 때 질문: 결정 변수는 관절 속도인가? 비용은 ‖J·q̇ − v_목표‖²(가중) + 댐핑 항인가? 제약은 관절 범위·속도 + CBF 충돌 + (양팔) rigid grasp인가? → 10/6 QP 정식화 정리의 뼈대')
memo()

# ---------------------------------------------------------------------
heading('5. 시뮬레이션')
code('''ros2 launch ffw_bringup ffw_sg2_follower_ai_gazebo.launch.py     # SG2 Gazebo
ros2 launch ffw_moveit_config moveit.launch.py use_sim:=true       # MoveIt (선택)''')
bullet('Gazebo도 bringup 전에 Zenoh 데몬이 필요하다고 공식 문서에 적혀 있다')
bullet('Cyclo Control을 Gazebo에 붙이는 방법은 공식 문서에 없다 → 출력 토픽이 시뮬 컨트롤러로 가는지 직접 확인 (10/7 일정)')
memo()

# ---------------------------------------------------------------------
heading('6. 내 PC에서 로봇 토픽 보기 (Zenoh)')
code('''export RMW_IMPLEMENTATION=rmw_zenoh_cpp
export ZENOH_CONFIG_OVERRIDE='transport/shared_memory/enabled=true;mode="client";connect/endpoints=["tcp/로봇IP:7447"]'
ros2 topic list
ros2 topic echo /joint_states''')
bullet('내 PC에도 AI Worker 도커 컨테이너를 띄우고, 그 안에서 위 변수를 설정한다. 로봇 7447 포트에 접근 가능해야 한다')
memo()

# ---------------------------------------------------------------------
heading('7. 문제가 생겼을 때')
table([5.0, USABLE - 5.0], ['증상', '확인할 것'], [
    ['팔이 전혀 안 움직임', 'E-STOP이 눌려 있지 않은지, A 버튼으로 토크를 켰는지, bringup이 살아 있는지'],
    ['MoveL에 반응 없음', '/joint_states가 나오는지, /r_goal_move에 메시지가 도착하는지 (ros2 topic echo)'],
    ['Cyclo가 갑자기 멈추고 유지', '/joint_states가 joint_state_timeout보다 오래됐는지'],
    ['RViz에 마커 없음', 'InteractiveMarkers 디스플레이 추가, Fixed Frame = base_link'],
    ['bringup 중 "0xc (Multi-turn Error)"', 'DYNAMIXEL의 다회전 IC 문제. 해당 관절을 기준 위치에 맞추고 Dynamixel Wizard로 펌웨어·클리어하는 절차가 있으나 **혼자 하지 말고 선배·교수님께 보고**'],
    ['ros2 명령이 안 먹음', '도커 컨테이너 안인지 확인 (새 터미널마다 다시 진입)'],
    ['로봇 Orin 패키지 문제', '**apt upgrade 금지** (공식 경고)'],
])
memo()

# ---------------------------------------------------------------------
heading('8. 확인 필요 (메모와 공식 문서의 차이 포함)')
bullet('**Zenoh 데몬**: 공식 문서는 bringup 전에 필수라 하는데 랩 메모에 없음 → 자동 실행인지 선배에게 확인')
bullet('**bringup 명령의 "\\ "**: 메모의 줄바꿈 기호 때문에 그대로 붙여넣으면 실패할 수 있음 → 한 줄로')
bullet('**직접 관절 명령(3-7)**은 Cyclo 안전 필터를 거치지 않음 → 랩에서 허용하는 사용 범위 확인')
bullet('**전류(토크) 제어 모드**: 기본 컨트롤러는 모두 위치 궤적. 참빛 임피던스를 하려면 Y 시리즈 팔 모터를 전류 제어 모드로 쓰는 경로가 필요 → 교수님·ROBOTIS 확인')
bullet('base_link 축 방향, 오른팔 작업 가능 범위 (예시 좌표 x 0.35, y −0.20, z 0.85 기준)')
bullet('끄는 순서 (공식 문서에 없음)')

heading('참고 문서', 2)
for name, path in [('Introduction', 'introduction'), ('Hardware Specifications', 'specifications/hardware'),
                   ('Software Specifications', 'specifications/software'),
                   ('Setup Overview – Hardware', 'quick_start_guide/setup_overview/hardware'),
                   ('Setup Overview – Software', 'quick_start_guide/setup_overview/software'),
                   ('Zenoh Communication', 'quick_start_guide/setup_overview/zenoh_communication'),
                   ('Cyclo Manager – Bringup', 'quick_start_guide/operation_guide/cyclo_manager/bringup'),
                   ('Teleoperation', 'quick_start_guide/operation_guide/teleoperation'),
                   ('Cyclo Control', 'advanced_features/cyclo_control'),
                   ('Gazebo', 'simulation/gazebo'),
                   ('Clearing Multi-turn Error', 'support/multi_turn_troubleshooting_guide')]:
    bullet(name + ': ' + BASE + path)
bullet('GitHub: https://github.com/ROBOTIS-GIT/cyclo_control')

doc.save(OUT)
print('saved', OUT)
