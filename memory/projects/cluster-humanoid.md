# 군집 휴머노이드 (DREAM Lab 학부연구) — Cyclo Control 학습 단계

세션: 2026-10-01 (로컬) · **대화 기반**. 1차 미팅 메모 = `Desktop\광운대학교\학부연구생\군집 휴머노이드\1(1차 미팅).docx` (사용자 작성, 10/1)

## 1차 미팅(10/1) 교수님 조언 요지 (사용자 메모 기준)
- 모델 기반 전신제어기 (Modern Robotics 기준, space/body). 힘 대응은 sim에서 힘 피드백, 리더-팔로워 구조
- 이기종: 모바일 매니퓰레이터 + 휴머노이드 — task space의 EE·relative pose가 출력, **충돌회피 중요**. G1 사용 가능 → G1 + 모바일 매니퓰레이터 응용
- I 게인은 응답이 느려 잘 안 씀 → 물체 움직이기 전 **무게 탐지**, 접촉력 + 하중 분산, 처짐 하중을 모델에 넣어 feedforward
- 전류 제어: 토크 상수 identification(감으로라도), Lift 이슈. 임피던스는 위치 제어 대신 토크(전류 제어 모드). sim 토크(자코비안 토크-힘)로 정밀 확인 후 실증 확장
- **Cyclo**(ROBOTIS cyclo_control): IK/dynamics, command pose 구조 → **IK 구조 이해가 우선 목표** (궤적 생성, spline)
- 할 일: **40시간 중 투자 가능한 비율 교수님께 보고**

## Cyclo Control 확인 사항 (2026-10-01 웹 확인)
- repo `ROBOTIS-GIT/cyclo_control` (ROS 2 **Jazzy**, numpy<2). 패키지: `cyclo_motion_controller_core`(solver·controller·retargeting) /
  `_ros`(노드·launch·YAML) / `_ros_py` / `_models`(URDF·RViz) / `osqp_eigen_vendor`. 의존: **Pinocchio + OSQP-Eigen**
- QP 기반 수치 IK: 명령 추종 + 관절 위치 범위·속도 한계·**자기충돌 회피** 제약. 출력은 joint trajectory(위치 수준) — 힘 계층 없음
- 모드: `movel`(기본, 직선 보간) / `movej` / `bimanual_movel`(rigid grasp 유지 양팔) / `bimanual_movej`
- 실행: `ros2 launch cyclo_motion_controller_ros ai_worker_controller.launch.py controller_type:=movel`, 모델 보기 `view_ffw_sg2_follower.launch.py`
- 토픽: 입력 `/r_goal_move` `/l_goal_move`, 양팔 `/capture_grasp` `/virtual_object_goal_move`, 출력 `/leader/joint_trajectory_command_broadcaster_right/joint_trajectory`, 상태 `/joint_states`
- 시뮬: Gazebo `ros2 launch ffw_bringup ffw_bg2_follower_ai_gazebo.launch.py`(SG2 명령 불명확), MuJoCo `ros2 launch ai_worker_mujoco_bringup robot.launch.py robot_model:=ffw_sg2`(검색 결과 기준, 미검증).
  **Cyclo를 시뮬에 붙이는 공식 절차는 문서에 없음** → 토픽 리매핑 필요 추정
- 참빛과의 관계: 같은 FFW-SG2. `bimanual_movel`은 참빛 협동 운반(박스 = 가상 물체)과 직결 → 참빛 IK를 자체 구현할지 Cyclo를 베이스라인으로 쓸지 판단 필요

## 10/2~10/9 일정 (확정본, 2026-10-01)
- 파일: `Desktop\광운대학교\학부연구생\미팅월 1주차 일정(cyclo).docx` (가로 A4 3쪽, 바탕체 10pt). 생성 `docs/cluster-humanoid/build_cyclo.py`
  (서식 도우미는 `docs/chambit-plan/weekly/build_plan.py` 앞부분을 exec — 같은 폴더에 두고 실행)
- **총 15시간**으로 축소(처음 제안 27h → 사용자 시간 제약 반영): 10/2 21-23 환경 · 10/3(개천절) 9-12 아키텍처 · 주말 전공 ·
  10/6 21-23 QP 정식화 · 10/7 21-23 시뮬 연결 · 10/8 20-23 movel·bimanual_movel · 10/9(한글날) 9-12 자체 궤적·보고

## 주간 활동시간 책정 (2026-10-01)
- 사용자 제약: **내년 1학기 조기졸업 → 전공 공부 최우선**, 연구는 하루 2~3시간, 주말은 전공 몰아서. 활동비는 주 40시간 중 기여 시간 비례
- 평일 가능 시간(사용자 제공): 월 9-12·18-23 / 화 9-12·21-23 / 수 9-12·13-14·20-23 / 목 9-12·19-23 / 금 9-15·19-23 = **37h**
- 배정: 연구 **12h**(월 21-23, 화 21-23, 수 20-23, 목 21-23, 금 9-12) / 전공 23h / 여유 2h(금 21-23)
- **보고값 주 12시간(30%)**. 12h 중 약 6h가 참빛 계획(66h/12주)분. 시험 주 2h, 참빛 실증(11/2~11/22) 최대 15h
- 확인 필요: 참빛 시간과 과제 시간을 **겹쳐 보고해도 되는지** (활동비 관련) 교수님께 질문

## AI Worker2 매뉴얼 초안 (2026-10-02)
- 파일: `Desktop\광운대학교\학부연구생\AI Worker2 매뉴얼(초안).docx` (세로 A4 7쪽, 바탕체 10pt, 코드는 영문만 Consolas). 생성 `docs/cluster-humanoid/build_manual.py`
- 사용자가 **직접 읽고 이해한 대로 고칠 초안**. 각 절 끝 "□ 내 메모" 칸
- 입력: 사용자 랩 실사용 메모(SSH `robotis@ffw-SNPR48A1043.local`, `./docker/container.sh enter`, bringup `ffw_sg2_follower_ai.launch.py`,
  Cyclo movel + `/r_goal_move` 예시, 리더 `ffw_lg2_leader_ai.launch.py`, 관절 궤적 직접 publish 예시) + docs.robotis.com AI Worker 문서 11개 페이지
- 확인한 사실: SG2 25 DOF(팔 7×2·그리퍼 2·머리 2·리프트 1·베이스 6), 페이로드 정격 3/6 kg·최대 5/10 kg, ros2_control 100 Hz·컨트롤러 전부 위치 궤적(JTC)+스워브,
  RMW = Zenoh(2.0.0~, bringup 전 `ros2 run rmw_zenoh_cpp rmw_zenohd` 필요), 처음 켜면 토크 오프 → 원격 E-STOP A 버튼, Orin에서 apt upgrade 금지,
  Cyclo 파라미터(kp/weight/weight_damping/cbf_alpha/slack_penalty/lift_vel_bound…)
- 짚은 것: ① 메모에 Zenoh 데몬 단계 없음 ② bringup 명령의 `\ ` 줄바꿈 오류 ③ 관절 궤적 직접 publish 토픽 = Cyclo 출력 토픽 → QP 안전 필터 우회, 안전 경로는 movej + raw_joint_trajectory
  ④ 리더·Cyclo·직접 발행 동시 사용 금지(추정) ⑤ 전류(토크) 제어 경로가 기본 구성에 없음 → 참빛 임피던스 확인 필요

## 1주차 정기미팅(10/8 목) Cyclo 공부 매뉴얼 (2026-10-04)
- 파일: `학부연구생\군집 휴머노이드\1주차 정기미팅_cyclo 공부 매뉴얼.docx` (세로 A4 11쪽, 레고 매뉴얼식 STEP 1~13 + 체크박스) + 같은 폴더 `arm_ik_demo.py`, `model_info.py`.
  생성·스크립트 사본 `docs/cluster-humanoid/week1/` (build_study.py는 `../plan/build_manual.py` 헬퍼를 exec — 경로 맞춰 실행)
- 방법: Cyclo MoveL을 **MuJoCo 단독(ROS 없음) "미니 Cyclo"**로 재현 → 소스와 대응. 일정 월 21-23 A / 화 21-23 B / 수 20-23 C+D (7h)
- 확인 사실 (Windows, MuJoCo 3.14.0에서 직접 실행):
  · AI Worker MJCF = `ROBOTIS-GIT/ai_worker` `ffw_description/mujoco/ffw_sg2/{ffw_sg2,scene}.xml` (sparse checkout 147MB). **MuJoCo 3.3.0은 "body mass is too small" 에러** → 최신 필요
  · nq 38 / nv 37 / nu 25, dt 0.002, 관절별 position 액추에이터(이름 = 관절명, 팔1~3 kp 3000), base는 freejoint, EE body `end_effector_r_link`
  · viewer CLI 플래그는 `--mjcf=`
- Cyclo 소스(cyclo_control) 확인: MoveL 노드는 **3차 보간**(cubicVector/rotationCubic), v_d = v_ff + kp·e(kp 50, 358행),
  **q_desired = q_feedback + q̇·dt (499행)**, MoveL 클래스는 VRController 상속 → QP는 `vr_controller.cpp` setCost/Bound/Ineq:
  비용 Σ‖J q̇ − v_d‖²_W + q̇ᵀW_d q̇ + ρΣs (W 10/1, W_d 0.1, ρ 1000), 속도 bound, 관절 한계 CBF(α 50), 자기충돌 CBF(buffer 0.05, safe 0.02), 특이점 slack 1개.
  Jacobian = Pinocchio LOCAL_WORLD_ALIGNED
- 실험 결과(K=50, T=3 기본): E1 DLS 5차 최대 6.8 mm / E2 3차 7.2 / E3 K5 13.2 / E4 λ0.3 38.5 / E5 QP 4.7 /
  **E6 T=1 DLS 관절속도 12.9 rad/s 폭주** / **E7 T=1 QP 1.5 rad/s 한계 유지** / **E8 Cyclo식 측정값 적분 → 중력 처짐 정상상태 11.8 mm**
  → 보고 핵심: QP를 쓰는 이유(E6/E7), 중력·하중 feedforward 필요(E8, 교수님 조언과 연결)
- 다음 주(PART E, 미검증): 실로봇 movel 같은 목표 비교 / `shkwon98/mujoco_ros2_control_menagerie`의 `ai_worker_mujoco_bringup` + Cyclo 토픽 리매핑

### 개정 (2026-10-04 오후) — 실제 Cyclo까지 미팅 전 필수
- 사용자 지시: **실제 Cyclo를 MuJoCo에서 확인하는 것까지가 미팅(10/8 목) 전 할 일.** 일정: 일 MR 이론 3h / 월 하루 종일(실습 + 이론 마무리) / 화 오전 현대와 공유(작업 없음) / 수 3~4h 보완 + 예상 질문
- "석사 선배 파일" = 10/2 붙여넣은 실사용 메모가 맞음 (사용자 확인)
- 매뉴얼 개정본(같은 파일명 덮어씀, 16쪽): PART 0 MR1(일) → A 환경·ROS 설치 선행 → B 미니 Cyclo → **C 실제 Cyclo 빌드 + `cyclo_mujoco_bridge.py`** → D 소스·MR2 → E 화요일 1장 → F 수요일 슬라이드 8장 + 예상 질문 13개
- **연결 방식 = 자체 브리지 노드**(ros2_control MuJoCo 패키지 대신): /joint_states 100 Hz 발행 + `/leader/joint_trajectory_command_broadcaster_{right,left}/joint_trajectory`·`/leader/joystick_controller_right/joint_trajectory` 구독 → 위치 액추에이터 목표. Cyclo 수정 없음.
  MJCF 관절 31개 이름이 Cyclo URDF(`cyclo_motion_controller_models/models/ai_worker/ffw_sg2_follower.urdf`)와 전부 일치(확인). Sim 클래스는 Windows에서 실행 검증, **rclpy 부분은 미검증**
- `--gravcomp`(qfrc_applied = qfrc_bias, 팔 14축): 미니 Cyclo E9에서 Cyclo식 적분 정상상태 오차 11.8 → 3.4 mm
- Cyclo 빌드: README대로 `vcs import < cyclo_control_ci.repos`(robotis_interfaces) → rosdep → colcon Release. 브리지 venv는 `--system-site-packages` + `numpy<2`
- 실제 Cyclo 실험 C1~C7(예측 포함): 기본 / gravcomp / T=0 / 자기충돌(두 손 모은 뒤 오른손을 왼손 자리로) / 도달 불가 / config_file로 kp·α 변경 / FK 일치(/r_gripper_pose vs MuJoCo)
