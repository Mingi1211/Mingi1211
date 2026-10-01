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

## 10/2~10/9 일정 (Claude 제안)
환경·문서(10/2) → 아키텍처 그림(10/3) → QP 정식화 ↔ Modern Robotics 대조(10/4) → 시뮬 연결(10/5) → movel 실습(10/6) →
bimanual_movel 실습(10/7) → 자체 5차/spline 궤적 스트리밍·파라미터 변경(10/8) → 보고 자료·투자 비율(10/9)
