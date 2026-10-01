import sys, os
# build_plan.py의 서식 도우미(바탕체 10pt, 가로 A4, 표 함수)를 그대로 가져온다
_src = open(os.path.join(os.path.dirname(__file__), 'build_plan.py'), encoding='utf-8').read()
exec(_src.split('# =====')[0])

t = doc.add_paragraph()
t.alignment = WD_ALIGN_PARAGRAPH.CENTER
run(t, '10월 1주차 일정 — Cyclo Control 구조 이해·시뮬레이션 실습', bold=True, size=16)
para('군집 휴머노이드 과제 · 김민기 · 기간 10/2(목) ~ 10/9(목) · 작성 2026-10-01', align=WD_ALIGN_PARAGRAPH.CENTER, after=8)

heading('0. 목표와 산출물')
table([4.2, USABLE - 4.2], ['항목', '내용'], [
    ['출발점', '1차 미팅(10/1) 교수님 조언: Cyclo는 command pose를 받아 IK(및 dynamics)로 푸는 구조이므로 **IK 구조를 이해하는 것을 먼저 목표**로 한다 (궤적 생성, spline)'],
    ['이번 주 목표', 'Cyclo Control의 ① 아키텍처(노드·토픽·데이터 흐름) ② QP IK 정식화(비용·제약) ③ 시뮬레이션 실행과 실습(MoveL, 양팔, 자체 궤적 입력)'],
    ['산출물 (10/9 보고)', '아키텍처 그림 1장 · QP 정식화 정리 1장 · 실습 그래프 3개 · 막힌 것 · 다음 단계 · 주간 투자 시간(4장)'],
    ['시간 예산', '**총 15시간.** 평일은 하루 2~3시간, 주말(10/4~10/5)은 전공 공부. 공휴일 10/3·10/9에 3시간씩'],
], first_col_fill='F2F2F2')

heading('1. Cyclo Control 기본 정보 (공식 문서·GitHub 기준, 직접 실행 전)')
table([4.2, USABLE - 4.2], ['항목', '내용'], [
    ['저장소', 'ROBOTIS-GIT/cyclo_control · ROS 2 **Jazzy** · numpy<2 필요'],
    ['패키지', 'cyclo_motion_controller_core (solver·controller·retargeting) / cyclo_motion_controller_ros (노드·launch·YAML) / cyclo_motion_controller_ros_py / cyclo_motion_controller_models (URDF·RViz) / osqp_eigen_vendor'],
    ['핵심 구조', '**Pinocchio + OSQP 기반 QP 수치 IK.** 명령 추종과 함께 관절 위치 범위·관절 속도 한계·자기충돌 회피를 제약으로 둔다. 출력은 관절 궤적(위치 수준)이며 힘 계층은 없다'],
    ['제어 모드', 'movel (기본, 직선 보간) / movej / bimanual_movel (가상 물체를 잡은 채 양팔 상대 자세 유지) / bimanual_movej'],
    ['실행', 'ros2 launch cyclo_motion_controller_ros ai_worker_controller.launch.py controller_type:=movel  ·  모델 보기: view_ffw_sg2_follower.launch.py'],
    ['토픽', '입력 /r_goal_move, /l_goal_move · 양팔 /capture_grasp, /virtual_object_goal_move · 출력 /leader/joint_trajectory_command_broadcaster_right/joint_trajectory · 상태 /joint_states'],
    ['시뮬레이션', 'Gazebo: ffw_bringup (SG2 전용 명령은 문서에 없음) · MuJoCo: ai_worker_mujoco_bringup robot.launch.py robot_model:=ffw_sg2 (검색 결과 기준). **Cyclo를 시뮬에 붙이는 공식 절차는 없어 토픽 리매핑이 필요할 것으로 예상**'],
], first_col_fill='F2F2F2')

heading('2. 일별 일정')
W = [3.0, 2.3, 3.0, 11.0, USABLE - 19.3]
table(W, ['날짜', '시간', '주제', '할 일', '끝났다는 기준'], [
    [['**10/2 (목)**'], '21~23\n(2h)'.split('\n'), '환경·문서',
     ['- Ubuntu 24.04 원격 환경에서 ROS 2 Jazzy 확인 → cyclo_control 클론·빌드 (osqp_eigen_vendor, numpy<2 주의)', '- view_ffw_sg2_follower.launch.py로 RViz 모델 띄우기', '- 공식 문서(Cyclo Control 페이지) 정독'],
     ['- RViz에 FFW-SG2 모델 표시']],
    [['**10/3 (금)**', '개천절'], '9~12\n(3h)'.split('\n'), '아키텍처',
     ['- ai_worker_controller.launch.py와 YAML 읽기 → 노드별 입력·출력 토픽 정리, rqt_graph', '- core의 include/·src/ 파일 목록으로 클래스 구조 그리기 (solver / controller / retargeting)'],
     ['- **아키텍처 그림 1장** (명령 → 보간 → QP IK → 관절 궤적)']],
    [['**10/4~10/5**', '주말'], ['—'], '전공 공부', ['연구 없음. 빌드가 막혀 있으면 원인 메모만'], ['—']],
    [['**10/6 (월)**'], '21~23\n(2h)'.split('\n'), 'QP 정식화',
     ['- 소스에서 비용(말단 오차 추종)과 제약(관절 위치·속도·자기충돌)을 찾아 OSQP 표준형(½xᵀPx + qᵀx, l ≤ Ax ≤ u)에 대응', '- Modern Robotics 5·6장(space/body 자코비안, 수치 IK)과 비교', '- movel 보간(spline) 방식 확인'],
     ['- **QP 정식화 정리 1장** (변수·비용·제약이 코드 어디에 있는지)']],
    [['**10/7 (화)**'], '21~23\n(2h)'.split('\n'), '시뮬 연결',
     ['- Gazebo 또는 MuJoCo 기동 → Cyclo 출력 토픽을 시뮬 컨트롤러 입력으로 리매핑', '- 안 되면: RViz + 출력 궤적을 /joint_states로 되돌려주는 간이 노드로 대체'],
     ['- 명령을 넣으면 시뮬(또는 RViz) 팔이 움직임']],
    [['**10/8 (수)**'], '20~23\n(3h)'.split('\n'), '실습 1·2',
     ['- **movel**: interactive marker와 /r_goal_move 직접 publish, 목표 vs 실제 말단 로깅, 관절 한계·특이점 근처 명령으로 제약이 걸리는 모습 확인', '- **bimanual_movel**: /capture_grasp → /virtual_object_goal_move, 양팔 상대 자세 오차 측정'],
     ['- 추종 오차 그래프', '- 양팔 상대 자세 유지 그래프']],
    [['**10/9 (목)**', '한글날'], '9~12\n(3h)'.split('\n'), '실습 3·보고',
     ['- 5차 다항식 궤적을 goal 토픽으로 스트리밍 → Cyclo 내부 보간과 비교 (시간 부족 시 이것만 다음 주로)', '- 보고 자료: 아키텍처 그림, QP 정식화, 그래프 3개, 막힌 것, 다음 단계(힘 계층을 어디에 붙일지), 주간 투자 시간'],
     ['- **교수님 보고 자료 완성**']],
], first_col_fill='F2F2F2', center_cols=(1,))

heading('3. 참빛설계학기와 겹치는 부분')
bullet('로봇이 같은 **FFW-SG2**다. 참빛 1주차(10/5~)의 URDF 정비·Pinocchio 환경 구축은 이번 주 작업과 같으므로 한 번에 처리한다')
bullet('**bimanual_movel**은 가상 물체를 잡은 채 양팔 상대 자세를 유지하는 모드라 참빛 협동 박스 운반과 같은 문제다. 이번 주 결과를 보고 **참빛 IK를 직접 구현할지, Cyclo를 기준선으로 두고 비교할지** 정한다')
bullet('Cyclo 출력은 위치 수준 관절 궤적이다. 교수님 메모의 "한 번 더 제어(힘)"는 그 아래 토크·전류 계층이며, 참빛의 임피던스 제어(전류 제어 모드)가 들어갈 자리다')

heading('4. 교수님 보고용 — 주간 투자 시간 (주 40시간 기준)')
para('우선순위는 **내년 1학기 조기졸업을 위한 전공 공부**다. 평일 가능 시간 37시간 중 연구에 하루 2~3시간을 쓰고, 주말은 전공 공부에 쓴다.')
table([2.6, 3.0, 7.5, 6.0, USABLE - 19.1], ['요일', '가능 시간', '전공 공부', '연구 (군집 휴머노이드 + 참빛)', '여유'], [
    ['월', '8h', '9~12, 18~21 (6h)', '21~23 (2h)', ''],
    ['화', '5h', '9~12 (3h)', '21~23 (2h)', ''],
    ['수', '7h', '9~12, 13~14 (4h)', '20~23 (3h)', ''],
    ['목', '7h', '9~12, 19~21 (5h)', '21~23 (2h)', ''],
    ['금', '10h', '12~15, 19~21 (5h)', '9~12 (3h) — 낮 시간, 실로봇·공동 실험', '21~23 (2h)'],
    ['**합계**', '**37h**', '**23h** (+ 주말)', '**12h**', '**2h**'],
], center_cols=(1, 4), first_col_fill='F2F2F2')
bullet('**보고할 값: 주 12시간 (40시간 중 30%)**')
bullet('12시간 중 약 6시간은 참빛 계획서(12주 66시간)의 활동에 해당한다. 참빛 작업이 곧 이기종 통합제어기의 일부이므로 같은 코드를 진행한다')
bullet('변동: 시험 주간(10/19~10/25, 12월 기말) 2시간(미팅·보고만) / 참빛 실로봇 실증 주간(11/2~11/22) 최대 15시간 (금 21~23 여유 2시간 + 주말 1시간)')
bullet('**확인 필요**: 활동비가 걸린 시간이므로, 참빛 활동시간과 과제 참여시간을 같은 시간으로 겹쳐 보고해도 되는지 교수님께 여쭤본다')

heading('5. 막혔을 때')
table([5.5, USABLE - 5.5], ['상황', '대응'], [
    ['빌드 실패 (의존성·버전)', 'RViz 모델 보기까지만 확보하고, 소스 읽기(2·3일차 내용)를 먼저 진행. 에러 로그는 보고 자료에 포함'],
    ['시뮬 연결 실패', 'RViz + /joint_states 되먹임 간이 노드로 대체 (IK 구조 이해라는 목표에는 충분)'],
    ['시간 부족', '실습 3(자체 궤적 스트리밍)을 다음 주로 미루고, 아키텍처·QP 정식화·실습 1·2는 반드시 끝낸다'],
], first_col_fill='F2F2F2')

doc.save(OUT)
print('saved', OUT)
