# HANDOFF — 현대 Docker 환경 위에서 2번(하위 제어) 시뮬 구현 (2026-11-03, v2)

Windows Claude가 작성. Ubuntu Claude는 이 파일 하나로 시작할 수 있게 썼다.
v2 변경: ① **F/T·접촉 센서 없이** 진행(실물에 없으므로 시뮬에서도 안 씀) ② 민기님 공부 문서를 이론 배경으로 삼아 **식 ↔ 코드 대응**으로 구현(9·10절).

## 0. 먼저 읽을 것 · 지킬 것

1. 이 파일 끝까지 → `memory/STATE.md` 참빛 절 → `memory/LEDGER.md`에서 `2026-10-0`~`2026-11-0` 줄.
2. 이전 인수인계 `docs/chambit-plan/control-2/HANDOFF_ubuntu_1026.md`의 **제어기 설계·기술 근거** 절은 유효하다(4주 요일 일정은 구버전).
3. 이미 써 둔 노드: `docs/chambit-plan/control-2/sim/impedance_node.py` + `params.yaml`
   - 모드 3개(spring / gravity / task), 6D 임피던스, null-space, D = 2ζ√(Λ_ii K_ii) 매 주기 재계산, 토크 포화, joint_states 끊김 감시
   - 출력 토픽 `/arm_<s>_effort_controller/commands` — **현대 환경 토픽 이름(`/robotN/...`)에 맞게 바꿔야 함**
   - params.yaml의 K 값(리더 600 / 팔로워 xy 150, z 600 N/m)은 **임시값**. Λ·마찰 측정 후 9절 절차로 재계산
4. 민기님 공부 문서 **「작업공간 임피던스 제어 PD gain 설정.docx」**(Windows `학부연구생/미팅/`). 핵심 식·메모를 9절에 모두 옮겨 두었으니 9절을 기준으로 쓴다. 원본이 꼭 필요하면 민기님께 요청.
5. 사용자: 호칭 **민기님**, 한국어, 결론 먼저, 짧게. 노션은 본인 문장·형식 유지, 틀린 것만 첨삭.
6. **현대의 노션 페이지·GitHub main 브랜치는 수정하지 않는다.** 바꿀 게 있으면 별도 브랜치/포크에서 하고 현대와 합의.
7. 보안: 로봇 접속 비밀번호 등 랩 내부 정보는 공개 레포(Mingi1211)에 쓰지 않는다.

## 1. 목표와 원칙

- **1차**: Gazebo에서 AI Worker(FFW-SG2) **1대 양팔**로 박스를 잡고 → 들고 → 10초 유지.
  박스를 내부력으로 찌그러뜨리지(과도한 쥐는 힘) 않고, 떨어뜨리지(미끄러짐) 않는다.
- **2차**: 들고 옮기기 → 2대(4팔) 리더-팔로워 강성 차등.
- 구성 요소: 토크(effort) 경로, 동역학 모델(Pinocchio), 중력 보상, 작업공간 임피던스(6D + null-space),
  강성 조절(축별·리더/팔로워), 필요하면 마찰 모델.
- **원칙: 시뮬은 실물로 가는 징검다리.** 실물(DYNAMIXEL 전류 모드, F/T 없음)에서 쓸 수 없는 것은 시뮬에서도 제어·판정에 쓰지 않는다.
  - 제어 입력: 관절 위치·속도(`/robotN/joint_states`), 박스 질량(사전 측정값)뿐
  - **F/T 센서·접촉 센서 미사용.** 힘은 제어기 내부 값(F_cmd = K e + D ė)과 문서의 추정식 F̂_ext = Λë + Dė + Ke로만 본다
  - Gazebo가 주는 박스 자세는 **평가 기록용**으로만 쓴다(실물에서는 영상·마커·자로 대체). 제어 루프에 넣지 않는다
  - 시험용 외력은 Gazebo에서 링크에 알려진 힘을 가해 넣을 수 있다(실물의 "무게추 걸기"에 해당하는 **입력**이지 센서가 아님)
- 교수님 지시(10/8 미팅): 토크 모드 필수, 수직 딱딱·수평 부드럽게, 리더 딱딱·팔로워 부드럽게, 리프트는 토크 제어에서 제외(J 열 제거),
  PD만(I 없음), 손목 5·6·7 관성 키워 Λ 구성. F/T 센서가 없으니 **토크 모드 임피던스**로 한다.

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
| E | `simulation.py` (월드) | 박스 모델 추가(질량·관성·마찰 μ 명시), robot1 앞. **센서는 붙이지 않는다.** 시험용 외력 입력 도구(링크에 알려진 힘 인가)만 준비 |
| F | `config/robots.yaml` | 박스 잡기 좋은 초기 팔 자세(0 자세는 토크 모드 시작에 부적합). 현대 테스트와 충돌하므로 합의 |

**지연 확인(필수)**: 토크 루프가 컨테이너 → zenoh → 브리지 → gz를 지난다. 상태 수신 → 명령 반영까지 왕복 지연을 먼저 재고,
20 ms를 넘으면 게인을 낮추거나 임피던스 계산을 gazebo 컨테이너 안(또는 gz 플러그인)으로 옮기는 안을 민기님과 상의.

## 4. 단계별 진행 (끝 기준 포함, 각 단계가 검증하는 문서 식은 9절 번호)

| 단계 | 내용 | 끝 기준 |
|---|---|---|
| S0 | 현대 환경 그대로 빌드·실행, 4팔 `verify_motion` 통과 확인, 위 지연 측정 | 두 로봇 ready, 지연 수치 |
| S1 | A + B(최소): robot1 오른팔 관절 1개만 effort, `τ = −k(q−q0) − d q̇`, 나머지는 속도 hold | 관절 하나 스프링 동작 |
| S2 | 오른팔 7축 effort, **중력 보상** `τ = g(q) + Kq(q0−q) − Dq q̇` (Kq 작게). Pinocchio 모델은 생성된 `control.urdf` | 여러 자세에서 팔이 떠 있음 + 관절 드리프트 그래프 (T12) |
| S3 | g 검증: Pinocchio `computeGeneralizedGravity` vs gz에서 정지 유지에 필요한 토크. 손목 armature 반영 | 관절별 오차 표 |
| S4 | 오른팔 작업공간 임피던스 6D + null-space (`impedance_node.py` task 모드), 축별 K, ζ=1 | **알려진 외력 인가** → e_ss ≈ F/K, 계단 응답 오버슈트 ≈ 0, T_s ≈ 5.8/ωn (T4·T5) |
| S5 | 양팔 + 박스: 접근 → 잡기 → 쥐는 오프셋 δ → **박스 무게 피드포워드 τ += J_vᵀ[0,0,m g/2]ᵀ를 잡은 뒤 ~1 s 램프** → 들기 → 10 s 유지 → 내리기(램프 다운) | 아래 성공 기준 |
| S6 | 옮기기(자체 5차 궤적 → Cyclo q_d 연결), 이후 robot2 추가해 리더-팔로워 강성 차등 | 2차 목표 |

S5 성공 기준(제안 — 민기님 확인). 센서 없이 판정:
- 박스 z 하강 < 1 cm, 박스-손 미끄러짐 < 5 mm — Gazebo 박스 자세는 **기록용**(실물은 영상·마커)
- 쥐는 힘은 제어기 값으로 본다: 지령 F_sq ≈ K_xy·δ, 추정 F̂_ext(9절 #11). `2 μ F_sq ≥ m g`(안 미끄러짐) 이상, 설정 상한(예: 30 N) 이하
- 토크 포화 없음, 떨림 없음

## 5. 민기님께 먼저 확인할 것

1. 박스 잡는 방식: **그리퍼로 손잡이 집기** vs **양손으로 옆면 눌러 잡기**(δ 오프셋). 후자가 "내부력 조절" 실험에 직접 맞음
2. 현대 레포 수정 방식: 포크/브랜치 + `control_mode` 플래그로 합의됐는지. 현대 일정(대회 부재 기간) 확인
3. 박스 질량·크기·마찰계수 μ, 쥐는 힘 상한

## 6. 위험

- effort 모드에서 노드가 죽으면 팔이 떨어짐 → 플러그인 timeout 시 위치 hold 복귀(A)를 반드시 먼저 구현
- Gazebo에는 실물의 정지마찰·엔코더 분해능·통신 지연이 없음 → 시뮬에서 되는 게인이 실물에선 떨릴 수 있음(실물은 낮은 게인부터)
- 시뮬에는 관절 마찰이 없어 F̂_ext가 실제보다 잘 맞는다. 실물에서는 마찰만큼 틀린다는 점을 결과에 함께 적는다
- 0 초기 자세 + 토크 모드 시작 → 큰 초기 오차로 포화. 시작 시 현재 자세를 목표로 잡고(q0 = 현재), 게인 램프

## 7. 작업 방식 — 민기님이 모르는 부분을 최소화

민기님은 AI로 구현하되, 중간 과정을 자기 공부 내용으로 이해할 수 있어야 한다. 그래서:

1. **식 ↔ 코드 1:1.** 9절의 각 식을 구현하는 함수·블록 위에 `# [문서 #번호] 식` 주석을 단다. 변수 이름은 문서·코드 이미지와 같게
   (`M_inv`, `Lambda`, `J_bar_T`, `N_T`, `tau_task`, `tau_null`, `F_cmd`, `zeta`, `K`, `D`).
2. **문서 밖 내용은 표시하고 짧게 설명.** ROS 2 배관, Gazebo 플러그인 C++, 브리지, Docker 등 문서에 없는 것은 코드 주석과 보고에 `[문서 밖]`을 붙이고,
   보고할 때 3줄 이내로 "무엇을 왜" 설명한다. 이론에 해당하면 MR 절을 같이 적는다. 세션 끝에 **새로 나온 개념 목록**을 남긴다(STATE에).
3. **문서에 없는 제어 방법을 새로 들이지 않는다**(computed torque, 어드미턴스, 외력 관측기, MPC 등). 필요해 보이면 먼저 민기님께 묻는다.
4. **실행 전 "이 단계가 검증하는 식", 실행 후 "예측값 vs 결과" 그래프.** 예측값은 문서 공식으로 계산(예: e_ss = F/K, T_s ≈ 5.8/ωn).
5. 보고 형식(기존 학습 방식 유지): **식 한 줄 + 코드 줄 번호 + 그래프**. 그 단계에 해당하는 MR 절을 15~30분 분량으로 함께 알려 준다.

## 8. 테스트 목록 (식이 코드에서 맞는지 — 9절 번호와 대응)

| ID | 내용 | 통과 기준 |
|---|---|---|
| T3 | 임의 q·τ0에서 ‖Λ J M⁻¹ N τ0‖ (영공간이 작업공간에 간섭 안 함) | < 1e-9 |
| T6 | 문서 예제 재현: Λ=4, F=20 N, e_ss=0.02 m, ζ=1 → K=1000, ωn≈15.81, D≈126.5, T_s≈0.37 s | 계산값 일치 + 1자유도 시뮬 그래프 |
| T4 | Gazebo 오른팔: 알려진 외력 F 인가 → 정상상태 변위 | e_ss ≈ F/K (축별) |
| T5 | 축별 계단 응답 | 오버슈트 ≈ 0, T_s ≈ 5.8/ωn (Λ_ii 사용) |
| T12 | 중력 부호: τ = g(q)만 → 팔이 떠 있음 (반대 부호면 2배 빨리 떨어짐) | 10 s 드리프트 작음 |
| T13 | `gain_design.py` 출력이 9절 #7·#8 범위 계산과 일치 | 수동 계산과 동일 |

## 9. 이론 배경 — 민기님 문서 요약 (코드의 근거)

문서: 「작업공간 임피던스 제어 PD gain 설정.docx」(2026-11-02 검수 반영 + 민기님 메모 추가본). 괄호 안은 문서의 절 머리(MR 번호).

| # | 문서 항목 (절) | 핵심 식 | 코드에서 |
|---|---|---|---|
| 1 | 작업공간 동역학 (MR 8.6) | Λ(q) = (J M⁻¹ Jᵀ)⁻¹, 저속(c, J̇q̇ 무시) Λẍ + F_ext = ΛJM⁻¹(τ − g). F_ext = EE가 환경에 가하는 힘(MR 부호) | `crba` → 대칭화 `np.triu(M)+np.triu(M,1).T` → 팔 블록 + 손목 armature, J는 리프트 열 제외, `Lambda = inv(J M_inv Jᵀ + 1e-6 I)` |
| 2 | 토크 지령식 (MR 11.4.1·11.7.1, Khatib) | τ = Jᵀ(K(x_d − x) + D(ẋ_d − ẋ)) + g(q) + N(q)τ0 | `tau_task = J.T @ F_cmd`, `tau_cmd = tau_task + g + tau_null` |
| 3 | 영공간 (같은 절) | J̄ = M⁻¹JᵀΛ, N = I − JᵀJ̄ᵀ, ΛJM⁻¹Nτ0 = 0 | `J_bar_T = Lambda @ J @ M_inv`, `N_T = I − J.T @ J_bar_T`, τ0 = K_q(q_nom − q) − D_q q̇ (자세 유지) |
| 4 | 폐루프 오차식 (같은 절) | e = x_d − x, 목표 가속도 0 가정 → Λë + Dė + Ke ≈ F_ext | 6D 오차 `e = [p_d − p ; log3(R_d Rᵀ)]`, `edot = V_des − J q̇` |
| 5 | 고유진동수·감쇠 (MR 11.2.2) | Λ 대각 성분만 쓰는 근사: ωn = √(K/Λ), ζ = D/(2√(ΛK)) → **D = 2ζ√(ΛK)** | `D = diag(2*zeta*sqrt(diag(Lambda)*diag(K)))` 매 주기 재계산 → 입력은 **K와 ζ만**. ζ=1로 시작, 마찰이 감쇠를 더하므로 응답이 너무 느리면 낮춤(문서 메모) |
| 6 | 계산 예제 (MR 11.2.1·11.2.2) | Λ=4 kg, F=20 N, e_ss=0.02 m → K=1000 N/m, ωn≈15.81 rad/s, D≈126.5 N·s/m, ζ=1에서 T_s ≈ 5.8/ωn ≈ 0.37 s (4/(ζωn)은 ζ<1 근사) | T6 |
| 7 | 강성 설계 (MR 11.7.1) | 축별 K = diag(K_xy, K_xy, K_z). 리더 전 축 높게 / 팔로워 K_xy만 낮게 / K_z 둘 다 높게. **K_z ≥ m g / Δz_max**, **K_xy ≤ F_internal,max / Δx**(베이스 거리 오차가 먼저 주어짐), 하한 F_fric/δ(문서 메모) | `params.yaml` 프리셋 + `gain_design.py`(입력→범위 표) |
| 8 | 게인 물리적 제약조건 (MR 11.2.2·11.4.1) | 이산화 상한 [MR 외 경험칙] ωn ≤ 2πf/10 ≈ 62.8 rad/s → K_max ≈ Λ_min·3940. 마찰 하한 K_min ≥ F_friction,tip/δx, F_friction = J̄ᵀτ_stiction. 감쇠 상한(질량-댐퍼 이산화 안정) D < 2Λ/T | `gain_design.py` 경고 |
| 9 | 무게 보상 (강성 설계 메모 + 제약조건 절 ※) | τ += J_vᵀ[0, 0, m_box g/2]ᵀ → K_z는 무게 추정 오차만 감당. 충돌 확인: K_z ≥ 9810이면 Λ_min ≥ 2.5 kg 필요 | 상태머신에서 잡은 뒤 램프 온, 놓기 전 램프 오프 |
| 10 | 구현 골격 (MR 8.6·11.4.1·11.7.1 절의 코드 이미지) | 29줄 루프(g, Jacobian, crba 대칭화, Λ, 6D 오차, D, F_cmd, J̄ᵀ, N_T, 포화) | `impedance_node.py` task 모드와 같은 구조로 유지 |
| 11 | 모니터링 (MR 11.1·11.4.1) | 오차·감쇠 응답, **F̂_ext = Λë + Dė + Ke**(마찰 때문에 실물에선 참고용), τ_cmd 포화·떨림 | CSV 로그 + `plot_log.py`. F̂_ext를 쥐는 힘·내부력의 센서 없는 지표로 사용 |
| 12 | 자주 하는 실수 (같은 절) | ① K 단위(N/m vs N·m/rad) 섞지 말기 ② 속도는 차분 대신 측정 q̇로 J q̇, LPF는 노이즈 클 때만(지연 주의) ③ Pinocchio g(q)는 지탱 토크 → +g | K_pos·K_rot 분리, T12 |
| 13 | QnA | F/T 없이 → 토크 모드 임피던스(힘을 재지 않고 강성으로 관계 규정, Kt·마찰 한계). 고정 D면 Λ_max 기준, 우리는 매 주기 재계산. I 없음(와인드업) | 적분항 없음, D 재계산 |

문서에 없는 이론 근거(민기님 MR 손필기·이전 대화):
- 중력 보상 g(q) = RNEA(q, 0, 0) — MR 8.3 Newton–Euler(베이스 가속도에 −g). Pinocchio `computeGeneralizedGravity`가 이 계산
- PD + g 안정성: V = ½eᵀK_p e + ½q̇ᵀMq̇, V̇ = −q̇ᵀK_d q̇ ≤ 0 (Ṁ − 2C 반대칭) — MR 11.4.1. "왜 M·c를 안 넣나"의 근거
- τ = JᵀF — MR 5.2. 토크 → 전류 I = τ/(Kt·감속비·효율) — MR 11.8·8.9(실물 단계)

## 10. 게인 설계 절차 (9절 #5~#9를 코드로)

`gain_design.py`(새로 작성, Pinocchio로 Λ 계산) 입력 → 출력:
- 입력: 박스 잡는 자세 몇 개의 q, m_box, Δz_max, F_internal,max, Δx(베이스·팔 위치 오차), δ(쥐는 오프셋), μ, τ_stiction(실물 측정 전엔 0), 무게 추정 오차 비율, ζ
- 계산: 자세별 diag(Λ) → Λ_min·Λ_max, K_z 하한(무게 보상 유무 둘 다), K_xy 상한·하한, K_max(이산화), 토크 포화 확인(m g + K e_max ≤ F_max), D 예상값, ωn, T_s
- 출력: 축별 [하한, 상한, 추천값] 표 + 위반 경고 → `params.yaml`에 주석으로 근거와 함께 기록
- K_z > K_xy 순서 유지(교수님 의도)

## 11. 세션 끝날 때

`memory/STATE.md` 참빛 절(+ 새로 나온 개념 목록)과 `memory/LEDGER.md` 갱신 후 이 레포에 커밋·푸시(mingi-loop 규칙).
현대 레포에 낸 변경은 브랜치 이름·커밋을 STATE에 적는다.
