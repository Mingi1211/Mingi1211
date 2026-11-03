# HANDOFF — 현대 Docker 환경 위에서 2번(하위 제어) 시뮬 구현 (2026-11-03)

Windows Claude가 작성. Ubuntu Claude는 이 파일 하나로 시작할 수 있게 썼다.

## 0. 먼저 읽을 것 · 지킬 것

1. 이 파일 끝까지 → `memory/STATE.md` 참빛 절 → `memory/LEDGER.md`에서 `2026-10-0`~`2026-11-0` 줄.
2. 이전 인수인계 `docs/chambit-plan/control-2/HANDOFF_ubuntu_1026.md`의 **제어기 설계·기술 근거** 절은 유효하다(4주 요일 일정은 구버전).
3. 이미 써 둔 노드: `docs/chambit-plan/control-2/sim/impedance_node.py` + `params.yaml`
   - 모드 3개(spring / gravity / task), 6D 임피던스, null-space, D = 2ζ√(Λ_ii K_ii) 매 주기 재계산, 토크 포화, joint_states 끊김 감시
   - 출력 토픽 `/arm_<s>_effort_controller/commands` — **현대 환경 토픽 이름(`/robotN/...`)에 맞게 바꿔야 함**
   - params.yaml의 K 값(리더 600 / 팔로워 xy 150, z 600 N/m)은 **임시값**. Λ·마찰 측정 후 재계산
4. 사용자: 호칭 **민기님**, 한국어, 결론 먼저, 짧게. 노션은 본인 문장·형식 유지, 틀린 것만 첨삭.
5. **현대의 노션 페이지·GitHub main 브랜치는 수정하지 않는다.** 바꿀 게 있으면 별도 브랜치/포크에서 하고 현대와 합의.
6. 보안: 로봇 접속 비밀번호 등 랩 내부 정보는 공개 레포(Mingi1211)에 쓰지 않는다.

## 1. 목표

- **1차**: Gazebo에서 AI Worker(FFW-SG2) **1대 양팔**로 박스를 잡고 → 들고 → 10초 유지.
  박스를 내부력으로 찌그러뜨리지(과도한 쥐는 힘) 않고, 떨어뜨리지(미끄러짐) 않는다.
- **2차**: 들고 옮기기 → 2대(4팔) 리더-팔로워 강성 차등.
- 구성 요소: 토크(effort) 경로, 동역학 모델(Pinocchio), 중력 보상, 작업공간 임피던스(6D + null-space),
  강성 조절(축별·리더/팔로워), 필요하면 마찰 모델.
- 교수님 지시(10/8 미팅): 토크 모드 필수, 수직 딱딱·수평 부드럽게, 리더 딱딱·팔로워 부드럽게, 리프트는 토크 제어에서 제외(J 열 제거),
  PD만(I 없음), 손목 5·6·7 관성 키워 Λ 구성. **F/T 센서 대신 토크 모드 임피던스**. F/T는 시뮬에서만 허용(어드미턴스 쓰려면).

## 2. 현대 환경 요약 (GitHub `jacob020328/KW_Internship` main, 2026-11-02 19:53Z 커밋 기준 직접 확인)

- 호스트 `~/internship_ws`(빌드: `bash scripts/build_host.bash`, 이미지: `docker compose -f docker/compose.yaml build`)
- 실행: `source scripts/environment.bash; xhost +si:localuser:root; COOP_GUI=true docker compose -f docker/compose.yaml up -d --no-build`
- 상태: `ros2 run coop_carry_bringup robot_command --status` → `ready` 확인 후 명령
- 컨테이너 4개(network_mode host): router(zenoh) / gazebo / robot1 / robot2. `RMW_IMPLEMENTATION=rmw_zenoh_cpp`, `ROS_DOMAIN_ID=71`, `GZ_PARTITION=internship_dual`
- 로봇 배치(`config/robots.yaml`): robot1 (0, −0.9, 0.2), robot2 (0, +0.9, 0.2), 둘 다 yaw 0. 베이스는 월드에 고정 관절. 초기 팔 각도 0(현대 노트: Cyclo 허용 자세와 맞춰야 함, 기존 테스트 일부 불일치)
- 명령 흐름(로봇마다):
  `robot_command` → `/robotN/r_goal_move` → `robot_adapter`(준비·형식 검사) → `/robotN/qp/r_goal_move` → Cyclo bimanual MoveL QP
  → `/robotN/arm_r_controller/joint_trajectory` → **SerializedJointTrajectoryController(위치)** → `RemoteGazeboSystem`(C++ 하드웨어 플러그인)
  → `/sim/robotN/joint_commands`(JointState) → `sim_command_adapter.py` → `/sim/robotN/actuators`(actuator_msgs/Actuators) → ros_gz_bridge
  → `GazeboJointActuator`(gz 플러그인)
- 상태 흐름: gz `JointStatePublisher` 100 Hz → `/sim/robotN/joint_states` → 브리지 → RemoteGazeboSystem → joint_state_broadcaster(`/robotN/joint_states`)
- QP: 100 Hz, `lift_vel_bound: 0`(리프트 컨트롤러 없음 → 리프트 고정), EE 프레임 `end_effector_{r,l}_link`, 그리퍼 `gripper_{r,l}_joint1`
- 월드: `ffw_bringup/worlds/default.sdf` 복사(Sensors 시스템 제거). **박스 없음**
- 모델 파일은 실행 시 생성(`/run/coop/robotN/physics.urdf`, `control.urdf`, `controllers.yaml`, `joint_map.yaml`, `bridge.yaml`) → 직접 편집 말고 `simulation.py`/`model_factory.py`를 고칠 것

## 3. 결론: 현재 환경 그대로는 토크·임피던스 불가 → 토크 경로를 추가해야 함

근거(코드):
- `gazebo_joint_actuator.cpp`는 매 스텝 `JointVelocityCmd = clamp(10·(q_target − q), ±v_max)` — **속도 명령 서보**. 중력·관성이 사실상 무시되고 힘이 안 걸림
- `RemoteGazeboSystem`은 command interface **position만** export (주석: "Existing JTC interfaces remain position/velocity")
- `sim_command_adapter.py`·브리지도 `position` 필드만 전달. `actuator_msgs/Actuators`에는 effort 필드가 없음(position / velocity / normalized)

필요한 변경 (현대 코드의 기본 동작은 그대로 두고 **`control_mode: position | effort` 플래그**로 분기 — 현대와 합의 후):

| # | 파일 | 변경 |
|---|---|---|
| A | `coop_carry_hardware/src/gazebo_joint_actuator.cpp` | effort 모드 관절은 `JointForceCmd`(effort limit로 clamp)만 쓰고 `JointVelocityCmd`는 지움. **명령이 끊기면(timeout) 지금처럼 현재 위치 hold로 복귀**(안전). 리프트·머리·(초기엔) 그리퍼는 기존 속도 서보 유지 |
| B | 브리지/어댑터 | effort 전달 경로. 후보 ① `Actuators.normalized`에 토크를 싣는 규약 ② 별도 토픽 `std_msgs/Float64MultiArray ↔ gz.msgs.Double_V`(ros_gz_bridge 매핑 지원 여부 확인 필요) |
| C | `remote_gazebo_system.cpp` | 팔 관절에 `effort` command interface export → 실물과 같은 `effort_controllers/JointGroupEffortController` 구조. (빠른 검증용으로는 B만 만들어 노드가 직접 발행해도 됨 — 아래 S1) |
| D | `model_factory.py` | effort 모드일 때 팔 컨트롤러를 JTC 대신 JointGroupEffortController로. Cyclo QP 출력(`/robotN/arm_*_controller/joint_trajectory`)은 **임피던스 노드가 구독해 q_d → FK → x_d**로 사용(`impedance_node.py`의 `source: cyclo`) |
| E | `simulation.py` (월드) | 박스 모델 추가(질량·관성·마찰 μ 명시), robot1 앞. **시뮬 전용 측정**: 손목 `ForceTorque` 센서 또는 박스 `Contact` 센서(+ 해당 gz 시스템 플러그인) → 내부력·쥐는 힘 정답값 |
| F | `config/robots.yaml` | 박스 잡기 좋은 초기 팔 자세(0 자세는 토크 모드 시작에 부적합). 현대 테스트와 충돌하므로 합의 |

**지연 확인(필수)**: 토크 루프가 컨테이너 → zenoh → 브리지 → gz를 지난다. 상태 수신 → 명령 반영까지 왕복 지연을 먼저 재고,
20 ms를 넘으면 게인을 낮추거나 임피던스 계산을 gazebo 컨테이너 안(또는 gz 플러그인)으로 옮기는 안을 민기님과 상의.

## 4. 단계별 진행 (끝 기준 포함)

| 단계 | 내용 | 끝 기준 |
|---|---|---|
| S0 | 현대 환경 그대로 빌드·실행, 4팔 `verify_motion` 통과 확인, 위 지연 측정 | 두 로봇 ready, 지연 수치 |
| S1 | A + B(최소): robot1 오른팔 관절 1개만 effort, `τ = −k(q−q0) − d q̇`, 나머지는 속도 hold | 관절 하나 스프링 동작 |
| S2 | 오른팔 7축 effort, **중력 보상** `τ = g(q) + Kq(q0−q) − Dq q̇` (Kq 작게). Pinocchio 모델은 생성된 `control.urdf`(= physics와 같은 관성) | 여러 자세에서 팔이 떠 있음 + 관절 드리프트 그래프 |
| S3 | g 검증: Pinocchio `computeGeneralizedGravity` vs gz 실측(정지 시 필요한 토크). 손목 armature 반영 | 관절별 오차 표 |
| S4 | 오른팔 작업공간 임피던스 6D + null-space (`impedance_node.py` task 모드), 축별 K, D = 2ζ√(ΛK), ζ=1 | 손을 밀면 수평은 밀리고 수직은 버팀(데이터) |
| S5 | 양팔 + 박스: 접근 → 잡기 → 쥐는 오프셋 δ → **박스 무게 피드포워드 τ += J_vᵀ[0,0,m g/2]를 잡은 뒤 ~1 s에 걸쳐 램프** → 들기 → 10 s 유지 → 내리기(램프 다운) | 아래 성공 기준 |
| S6 | 옮기기(자체 5차 궤적 → Cyclo q_d 연결), 이후 robot2 추가해 리더-팔로워 강성 차등 | 2차 목표 |

S5 성공 기준(제안 — 민기님 확인):
- 박스 z 하강 < 1 cm, 박스-손 미끄러짐 < 5 mm
- 쥐는 힘 F_sq: `2 μ F_sq ≥ m g`(안 미끄러짐) 이상, 설정 상한(예: 30 N, "찌그러짐" 대용) 이하 — 시뮬 F/T·접촉 센서로 측정
- 토크 포화 없음, 떨림 없음

## 5. 게인 설정 규칙 (민기님 문서 `학부연구생/미팅/작업공간 임피던스 제어 PD gain 설정.docx`와 동일)

- K = F / e_ss (정상상태). 축마다 하한·상한:
  - K_z 하한 = (무게 추정 오차 × g) / Δz_max (무게 피드포워드 있을 때). 피드포워드 없으면 m g / Δz_max
  - K_xy 상한 = F_allow / Δ(베이스·팔 위치 오차), 하한 = 손끝 마찰력 / δ. 옆에서 눌러 잡으면 쥐는 힘 = K_xy·δ
  - 공통 상한: 토크 포화(m g + K e_max ≤ F_max), ωn = √(K/Λ) ≤ ~62.8 rad/s(100 Hz 경험칙), 두 팔 z 불일치 내력
- D는 직접 넣지 않고 **ζ만 지정**(기본 1), 코드가 매 주기 Λ(q)로 D 계산
- K_z > K_xy 순서 유지(교수님 의도)
- Λ 값은 박스 잡는 자세 몇 개에서 `np.diag(Lambda)` 출력해 최소·최대 기록

## 6. 민기님께 먼저 확인할 것

1. 박스 잡는 방식: **그리퍼로 손잡이 집기** vs **양손으로 옆면 눌러 잡기**(δ 오프셋). 후자가 "내부력 조절" 실험에 직접 맞음
2. 현대 레포 수정 방식: 포크/브랜치 + `control_mode` 플래그로 합의됐는지. 현대 일정(대회 부재 기간) 확인
3. 박스 질량·크기·마찰계수 μ, 쥐는 힘 상한

## 7. 위험

- effort 모드에서 노드가 죽으면 팔이 떨어짐 → 플러그인 timeout 시 위치 hold 복귀(A)를 반드시 먼저 구현
- Gazebo에는 실물의 정지마찰·엔코더 분해능·통신 지연이 없음 → 시뮬에서 되는 게인이 실물에선 떨릴 수 있음(실물은 낮은 게인부터)
- 0 초기 자세 + 토크 모드 시작 → 큰 초기 오차로 포화. 시작 시 현재 자세를 목표로 잡고(q0 = 현재), 게인 램프

## 8. 세션 끝날 때

`memory/STATE.md` 참빛 절과 `memory/LEDGER.md` 갱신 후 이 레포에 커밋·푸시(mingi-loop 규칙).
현대 레포에 낸 변경은 브랜치 이름·커밋을 STATE에 적는다.
