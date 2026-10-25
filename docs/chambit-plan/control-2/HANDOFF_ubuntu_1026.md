# HANDOFF — Windows → Ubuntu (2026-10-26 월)

Windows Claude 세션에서 참빛설계(AI Worker2 2대 협동 박스 운반) **하위 제어 담당 계획**까지 정했다.
**오늘(10/26)부터 Ubuntu에서 Gazebo → 실물 순으로 구현한다.** 이 파일 하나로 이어받을 수 있게 썼다.

## Ubuntu Claude가 먼저 할 것

1. 이 파일을 끝까지 읽는다. 이어서 `memory/STATE.md`의 참빛 절과 `memory/LEDGER.md`에서 `2026-10-0`~`2026-10-09` 줄을 읽는다.
2. 사용자: 호칭 **민기님**, 한국어, 결론 먼저, 장황한 AI식 설명 금지. Notion 정리는 **본인 문장·형식을 유지하고 틀린 것만 첨삭**한다
   (`docs/cluster-humanoid/week1/ubuntu_1005/notion-note-editing-style.md`).
3. 학습 방식(사용자 결정): MR을 처음부터 읽지 않는다. **시뮬·실물에서 먼저 돌리고 → 방금 쓴 식에 해당하는 MR 절만 15~30분 → Notion에 "식 한 줄 + 코드 줄 번호 + 그래프"**.
4. 보안: 로봇 접속 비밀번호 등 랩 내부 정보는 이 레포(공개)에 적지 않는다.
5. **역할의 정본은 Notion 역할분담 페이지**다. 이 문서의 계획 중 노션과 다른 부분은 "노션과 이 계획이 다른 점" 표에 따로 적었다 — 확정된 것처럼 말하지 말 것.

## 역할과 범위

**정본 = Notion "프로젝트 task/역할분담"** https://app.notion.com/p/3f459c1c337e8027b29ed70f6814e665
(김현대 진행상황 하위, 현대가 작성 — **수정하지 말 것**. 2026-10-26 확인 시 마지막 편집 10/9, 아래 내용과 같음)

- **민기 = 2번 Dynamics / Operational Space Impedance Control [하위 제어]**
  목표: Cyclo가 계산한 reference를 joint torque로 추종하고, 수직·수평 강성을 다르게 줘서 물체를 지지하면서 베이스 위치 오차를 완충
  - Current Control: DYNAMIXEL Current Control Mode 적용, ROS 2 current command interface, joint torque → motor current 변환, current·torque limit
  - Dynamics: URDF 기반 모델, M(q), RNEA 중력 보상, **Lift joint 제외 Arm Jacobian**, Λ(q)
  - Impedance: Cartesian 위치·자세 오차, Operational Space PD 임피던스, Jᵀ 토크, Stiffness·Damping, **Leader–Follower 강성·감쇠 차등**
  - 실물 검증: joint static friction 영향 분석, 중력 보상·저속 움직임 검증, 수직 지지·수평 compliance 평가
  - 추가 실험: 말단 Link 5·6·7 질량·관성 변화에 따른 응답 비교, 전류 기반 외력·internal force 추정
  - 핵심 식(노션): F = K_p(p_d − p) + D_p(ṗ_d − ṗ), τ = J_vᵀF + g(q) — **병진부터, 검증 후 필요하면 방위·OS 동역학 추가**
  - Lift 분리(노션 2번 핵심 4): Lift는 별도 위치제어기, 임피던스 토크 계산에서 Lift 열 제외, FK·중력 보상엔 실제 Lift 높이 반영
  - 진행 단계(노션): 1 Current Control·중력 보상 → 2 단일 팔 OS 임피던스 → 3 양팔 임피던스·게인 튜닝 → 4 리더-팔로워 강성 차등 → 5 수평 compliance로 베이스 오차 완충 → 6 안정성·성능
- **김현대 = 1번 Cyclo / Multi-Robot Cooperative Control [상위 + 모바일 베이스]**: Cyclo MoveL·Bimanual·QP 분석, Cyclo 위치제어 중 외력 인가 실험,
  Rigid Grasp, **Lift를 QP에서 제외하고 별도 위치제어 구성**, Cyclo joint reference를 하위로 전달, 물체 좌표계·파지점·Object Trajectory,
  4팔 협조, 베이스(거리·속도 명령, odometry), 두 로봇 ROS 2 통신, Task Manager
- **공동**: 제어기 인터페이스(Cyclo reference·임피던스 입력·제어 주기·좌표계 통일), **Gazebo** 검증, 단일 팔 → 4팔 실물 적용, Safety, 실험 평가, 성능 비교

### 노션과 이 계획이 다른 점 (Windows Claude 권고 — 노션 미반영, 현대와 합의 필요)

| 항목 | 노션 | 이 계획(권고) | 처리 |
|---|---|---|---|
| Lift 위치 제어 | 1번 표에 "별도 위치제어 구성", 2번 핵심 4에도 "별도 위치제어기" → **담당이 겹침** | 2번 = 하드웨어 위치 모드 유지·안전 확인(리프트 gpio `Goal Position` 그대로), 1번 = 리프트 높이 명령 생성 | **현대와 정해서 노션에 반영할지 결정** |
| 방위(자세) 제어 | 병진부터, 필요하면 추가 | 2주차에 6D(자세 포함)로 — 박스 들면 손목이 돌아가 미끄러짐 | 노션 "필요하면 추가" 범위 안 |
| null-space | 없음 | 7자유도라 토크 제어 시 팔꿈치 흘러내림 → 2주차에 자세 유지·감쇠 추가 | 노션 범위 밖 추가 항목 |
| Λ 활용 | Λ 계산 | Λ로 축별 임계감쇠 D = 2ζ√(ΛK) 설정 | 노션 범위 안 |
| 추가 실험 2개 | 5·6·7 관성 비교, 전류 기반 외력·internal force 추정 | 5·6·7 관성은 Λ 단계(2주차)에서 시뮬로 짧게 / **외력·internal force 추정은 4주 범위 밖**(마찰에 묻힘 — 1차 면담 피드백과 같은 이유) | 4주 뒤로 미룸 |
| 진행 단계 4·5 (4팔·베이스 완충) | 2번 단계에 포함 | 4주 안엔 **Gazebo에서만**(4주차 화), 실물은 1대 양팔까지 | 교수님께 범위 조정 말씀 필요 |

- 현대 **11/2~11/15 대회로 부재**
- 10/8 미팅(교수님): 작업공간 수직 딱딱·수평 부드럽게, 리더 딱딱·팔로워 부드럽게(베이스 거리 오차 흡수), 토크 모드 필수,
  리프트는 토크 제어에서 제외, τ = JᵀF, **PD만(I 없음)**, 관절 마찰 심함(정지마찰·끊김), 손목 5·6·7 관성 키워 Λ 구성.
  회의록: https://app.notion.com/p/3f359c1c337e80e79390f8e90e9c6602
- **4주 목표(11/20 금): 실물 1대 양팔 리더-팔로워로 박스 들기→유지→내리기.** 2대 협동은 Gazebo에서만.
  → 실물 2대가 4주 안에 어렵다는 범위 조정은 **목요일 미팅에서 교수님께 먼저 말씀드리기로** 권함 (말씀드렸는지 확인할 것)
- 4주 범위 밖: 전류 기반 외력·internal force 추정(노션 2번 추가 실험 — 4주 뒤), 그래스프 행렬 하중 분배, 실물 베이스 주행, MPC(겨울방학 → 논문)

## 기술 근거 (2026-10-09 직접 확인)

`ROBOTIS-GIT/ai_worker` `9bc7f7b`(2026-09-28), `ROBOTIS-GIT/dynamixel_hardware_interface` `6bb5f93`

| 사실 | 위치 |
|---|---|
| SG2 ros2_control 설정 하나에서 `use_sim`으로 하드웨어만 교체: `gz_ros2_control/GazeboSimSystem` ↔ `dynamixel_hardware_interface/DynamixelHardware` | `ffw_description/ros2_control/ffw_sg2_rev1_follower/ffw_sg2_follower.ros2_control.xacro` |
| 시뮬 `ros2 launch ffw_bringup ffw_sg2_follower_ai_gazebo.launch.py` / 실물 `ros2 launch ffw_bringup ffw_sg2_follower_ai.launch.py` | `ffw_bringup/launch/` |
| 현재 팔 14축: `command_interface position`, 모터 `Goal Position`, **Operating Mode 3**(위치), 4 Mbps, 22축 | 위 xacro 166행~ (gpio dxl1~) |
| 컨트롤러: arm_l/arm_r/head/lift = JointTrajectoryController(position), **update_rate 100 Hz** | `ffw_bringup/config/ffw_sg2_rev1_follower/ffw_sg2_follower_ai_hardware_controller.yaml` |
| ROS `effort` 명령 ↔ 모터 `Goal Current` 변환 지원 | dynamixel_hardware_interface `include/.../dynamixel_hardware_interface.hpp` 380~399 (`ros2_to_dxl_cmd_map`) |
| **전류 모드 실사용 예**: 리더 트리거 모터 Operating Mode 0 + `Goal Current` + `ffw_spring_actuator_controller` | `ffw_description/ros2_control/ffw_lg2_leader/*.xacro` 81·85행, `ffw_spring_actuator_controller/src/spring_actuator_controller.cpp` 80~120 |
| 공식 MuJoCo는 MJCF만(ROS 연동 없음) | `ffw_description/mujoco/ffw_sg2` |
| Gazebo 의존성: ros_gz_sim, ros_gz_bridge, gz_ros2_control, ros2_controllers | `ffw_bringup/package.xml`, 추가 저장소 `ai_worker_ci.repos`(dynamixel_hardware_interface, robotis_hand, robotis_interfaces) |

spring_actuator_controller가 하는 일 (2번의 템플릿):
```
τ = −k(q − q₀) − d·q̇
|q̇| < 임계값이면 τ ± static_friction_scalar·|τ|  (매 주기 부호 교대 dither)
명령 = τ × torque_scaling_factor   (Nm → 전류 단위. Kt 확인 필요)
```

전류 모드로 바꿀 때 고칠 것: 팔 관절 `command_interface position→effort`, gpio `Goal Position→Goal Current`, `Operating Mode 3→0`.
**리프트 gpio는 그대로(Goal Position)** → 한 하드웨어에서 팔 토크 + 리프트 위치. 같은 xacro라 Gazebo·실물에 같이 적용됨.

## 제어기 설계

- 형태: **Python 노드(Pinocchio) + `effort_controllers/JointGroupEffortController`**. 시뮬·실물 같은 코드. C++ 플러그인은 지터 문제 시에만
- 입력 `/joint_states`(리프트 실제 높이 포함) → 출력 팔 effort 명령, 100 Hz
- 식
  ```
  F = [K_p e_p + D_p ė_p ; K_o e_o + D_o ω_e],   e_o = log(R_d Rᵀ)  (Cyclo와 같은 자세 오차)
  τ = Jᵀ F + g(q) + N(−K_n(q − q_rest) − D_n q̇)
  N = I − Jᵀ J̄ᵀ,  J̄ = M⁻¹ Jᵀ Λ,  Λ = (J M⁻¹ Jᵀ)⁻¹   (손목 5·6·7 armature 키운 모델)
  D = 2ζ √(Λ K)  축별 임계감쇠
  K_leader = 전 축 높게 / K_follower = 수평(x,y) 낮게, 수직 z 높게
  쥐는 힘 ≈ K_수평 × δ  (손 목표를 박스 안쪽으로 δ) → 박스 무게·마찰계수로 δ 결정
  ```
- 병진만(J_v)으로는 손목이 돌아가 박스가 미끄러짐 → **6D 필수**. 7자유도라 **null-space 처리 필수**(토크 제어에선 팔꿈치가 흘러내림)
- 팔로워 수평 강성 하한: 손끝 기준 마찰력 J⁻ᵀτ_s 보다 K·(허용 변위)가 커야 순응이 일어남
- 1번과 인터페이스: Cyclo q_d → 2번 노드에서 FK로 x_d (Cyclo 수정 불필요). 11/15까지는 자체 5차 궤적으로 검증(1번 비의존)

## 4주 계획 (주 16h: 월 2 · 화 2 · 수 3 · 목 2 · 금 낮 6(실물) · 금 밤 1)

목요일 9:30 정기미팅, **1시간 전까지 Slack Group DM**에 공부·셋업·막힌 점 몇 줄.

### 1주차 10/26~11/1 — 관절 1개를 토크로
| 요일 | 할 일 | 끝 기준 |
|---|---|---|
| 월 | Gazebo SG2 실행, 기존 위치 컨트롤러로 팔 이동 확인. **실물 Operating Mode 변경 허락을 선배·교수님께 요청**. 현대에게 "노션과 다른 점" 표 공유(특히 Lift 담당) — 현대가 이번 주까지만 있음 | Gazebo에 SG2, 팔 움직임 |
| 화 | xacro: 오른팔 관절 1개 effort + effort 컨트롤러, Python 노드로 τ = −k(q−q₀) − d·q̇ | 관절 1개 스프링 동작 |
| 수 | 오른팔 7축 effort, τ = g(q) + K(q₀−q) − D q̇ (Pinocchio). 리프트 위치 유지 | 중력 보상만으로 팔이 떠 있음 |
| 목 | 미팅. 실물 준비: 팔 모터 기종·전류 단위·Kt·전류 한계·안전 절차 | 실물 체크리스트 |
| 금(실물) | 팔 받친 상태로 관절 1개 전류 모드 스프링 → **관절별 정지마찰 측정**(전류 램프, 양방향) → 가능하면 한 팔 중력 보상 | 1관절 전류 제어, 마찰 표 |
| 금 밤 | MR 8.1(M·c·g), 11.4(식 11.38~11.39) | Notion 1단락 |
게이트: 실물 전류 제어 불가 → 플랜 B(모터 위치 P 게인 낮추기 / 전류 기반 위치 모드로 관절 공간 순응)

### 2주차 11/2~11/8 (현대 부재) — 한 팔 작업공간 임피던스
| 요일 | 할 일 | 끝 기준 |
|---|---|---|
| 월 | 리프트 열 뺀 J, FK, 6D 오차, τ = Jᵀ(Ke + Dė) + g | Gazebo에서 손이 목표로 |
| 화 | null-space 자세·감쇠, K = diag(수평 낮게, 수직 높게) | 팔꿈치 유지, 축별로 다르게 밀림 |
| 수 | Λ(손목 armature) → D = 2ζ√(ΛK), 자체 5차 궤적, URDF `<dynamics friction>`에 측정값 | 궤적 추종 그래프 |
| 목 | 미팅. 마찰 보상(원하는 속도 부호 feedforward) | 보상 전후 비교 |
| 금(실물) | 중력 보상 → 관절 임피던스 → **작업공간 임피던스**(낮은 게인부터), 손으로 밀며 변위·전류 기록 | 수평 밀림·수직 버팀이 데이터로 |
| 금 밤 | MR 5.2(τ=JᵀF), 8.6(Λ), 11.7(임피던스) | Notion 1단락 |

### 3주차 11/9~11/15 (현대 부재) — 1대 양팔 리더-팔로워 박스
| 요일 | 할 일 | 끝 기준 |
|---|---|---|
| 월 | 양팔 확장, 리더/팔로워 게인 파라미터 파일 | Gazebo 양팔 |
| 화 | Gazebo 박스, 쥐는 오프셋 δ 계산 | 박스 안 미끄러짐 |
| 수 | 들기→유지→내리기 상태머신(임시), 토크 포화·명령 끊김 감시 | 시뮬 시퀀스 완주 |
| 목 | 미팅. 로그·그래프 스크립트(손 위치, 박스 기울기, 전류) | 자동 그래프 |
| 금(실물) | 양팔 임피던스 → **가벼운 박스 들기→유지→내리기** | **최소 성공 기준** |
| 금 밤 | 양팔 = 폐연쇄, 내력 개념(MR 12장 앞부분) | Notion 1단락 |

### 4주차 11/16~11/22 (현대 복귀) — 통합·정리
| 요일 | 할 일 | 끝 기준 |
|---|---|---|
| 월 | Cyclo q_d → FK → x_d 연결 (Gazebo) | Cyclo 목표로 임피던스 팔 이동 |
| 화 | Gazebo 2대: 강성 차등, 한쪽 베이스 5 cm 밀어 흡수 확인 | 흡수 그래프 |
| 수 | 실물 반복 실험 계획, 지표(성공률·박스 기울기·팔로워 손 변위) | 실험표 |
| 목 | 미팅 | — |
| 금(실물) | 1대 양팔 박스 반복 5회+, 여유 시 Cyclo reference 연결 | 결과 표·영상 |
| 금 밤 | 결과 정리(12월 발표 재료) | 그래프 3장 + 한계 목록 |

## 위험

- 실물은 금요일 낮뿐 → 랩에 금요일 고정 + 예비 1회 확보
- **전류 모드에서 제어기가 죽으면 팔이 떨어짐**: 팔 받침, 낮은 자세 시작, 낮은 전류 한계, E-Stop 손에
- 공용 로봇: 원래 xacro·yaml 백업 후 수정, 끝나면 원상 복구
- Gazebo 설치에서 반나절 이상 막히면: ai_worker Docker 이미지, 또는 MuJoCo 브리지(`~/cyclo_study/cyclo_mujoco_bridge.py`, qfrc_applied 사용 중)에 토크 토픽 구독 추가로 대체

## 오늘(10/26 월) 시작 명령 — 실행 전 상태 확인부터

`~/ros2_ws/src`에 이미 cyclo_control·robotis_interfaces가 있고, `~/cyclo_study/ai_worker`에 ai_worker 클론이 있을 수 있다(10/5 기준). 중복 클론·충돌 확인 후 진행.
```bash
source /opt/ros/jazzy/setup.bash
ls ~/ros2_ws/src
sudo apt install -y python3-vcstool ros-jazzy-ros-gz ros-jazzy-gz-ros2-control ros-jazzy-ros2-controllers
cd ~/ros2_ws/src && git clone https://github.com/ROBOTIS-GIT/ai_worker.git      # 없을 때만
vcs import < ai_worker/ai_worker_ci.repos                                       # 이미 있는 저장소는 건너뛰기
cd ~/ros2_ws && rosdep install --from-paths src --ignore-src -r -y
colcon build --symlink-install --packages-up-to ffw_bringup
source install/setup.bash
ros2 launch ffw_bringup ffw_sg2_follower_ai_gazebo.launch.py
```
기존 Cyclo 실습 자산: `~/cyclo_study/`(env.sh, t1_bridge.sh, t2_cyclo.sh, send.sh, fk.sh, cyclo_mujoco_bridge.py), Notion 실습 https://app.notion.com/p/3f059c1c337e80ceada0c94688c8241a (C4·C5는 사용자가 고치는 중 — 덮어쓰지 말 것)

## 세션 끝날 때

이 레포 `memory/STATE.md` 참빛 절과 `memory/LEDGER.md`를 갱신하고 커밋·푸시한다 (mingi-loop 규칙).
