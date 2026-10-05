# Cyclo 실습 + MR 공부 가이드 — 10/5(월) ~ 10/8(목)

위에서부터 순서대로 따라가면 됩니다. 오늘은 **실험 하나 → 그 실험에 나온 MR 개념 하나**를 번갈아 합니다. 방금 본 동작을 바로 교재 식으로 확인하는 순서입니다.

| 표시 | 뜻 |
|---|---|
| **명령** | 그대로 복사해서 붙여 넣습니다 |
| **✔ 성공** | 이렇게 나오면 다음으로 넘어갑니다 |
| **✗ 안 되면** | 먼저 해 볼 것. 그래도 안 되면 단계 번호와 에러를 Claude에게 붙여 주세요 |
| **📸 / 🎥** | 캡처하거나 녹화할 것 (발표자료 재료) |
| **✍ 기록** | 빈칸에 직접 적습니다. 수요일 정리와 목요일 발표에 그대로 씁니다 |
| **📖 MR** | 교재 읽기. 지금은 **영문 PDF 쪽수**(`~/Downloads/MR.pdf`) — 한글판은 절 번호로 찾으세요 (아래 "MR 읽기 지도") |

목표 수준: 구조와 개념을 이해하고, 돌려 본 것을 설명할 수 있는 정도.
원본 매뉴얼: `~/cyclo_study/1주차 정기미팅_cyclo 공부 매뉴얼.docx` (PART·STEP 번호는 매뉴얼 기준)

---

## 시간표 한눈에 (17:45 재조정 — 실습·Notion 끝, 남은 건 개념·코드 공부)

실습(C1·C2·C4·C5)과 영상, Notion "실습" 페이지 정리까지 끝났습니다. 남은 건 **MR 개념 + 코드 연결 공부**와 **현대 공유용 1장**입니다.
오늘 밤 4시간에 다 넣지 않고 **화·수 저녁으로 나눴습니다.** 쉬는 시간을 넣었고, 막히면 다음 날로 넘겨도 되는 단계에는 *(넘겨도 됨)* 을 붙였습니다.
아래 순서는 이 문서의 위→아래 순서와 같습니다.

**월요일 밤 (20:00–24:00)** — Windows에서 이어서 해도 됨 (코드 읽기·MR·Notion만 남음)

| 시간 | 할 일 | 종류 |
|---|---|---|
| 20:00–20:10 | **현대 미팅 준비** — Notion 실습 페이지 + 말할 포인트 3개 | 정리 |
| 20:10–20:40 | **MR-2** 작업공간 속도 제어 (11.3.3, 3.2.3.3) | 📖 30분 |
| 20:40–21:10 | **🔍 C1 코드** | 🔍 30분 |
| 21:10–21:20 | 휴식 | |
| 21:20–21:45 | **🔍 C2 코드 + MR-5** 힘 계층 (8.3, 11.4) | 🔍📖 25분 |
| 21:45–22:20 | **MR-3** 자코비안 · 특이점 (5.1, 5.3) | 📖 35분 |
| 22:20–22:30 | 휴식 | |
| 22:30–23:00 | **🔍 C4 코드** | 🔍 30분 |
| 23:00–23:40 | **MR-4** 역기구학 (6.2, 6.3) *(넘겨도 됨 → 화요일)* | 📖 40분 |
| 23:40–24:00 | 마무리 | |

**화요일 저녁 (2–3시간)** — 현대 미팅 후

| 시간 | 할 일 |
|---|---|
| (밀린 것) | 월요일에 못 한 🔍 C4 코드 등 |
| (밀렸으면) 40분 | **MR-4** 역기구학 (6.2, 6.3) |
| 40분 | **MR-6** MR ↔ Cyclo 요약표 + 코드 흐름 표 |
| 20분 | 현대 피드백 정리 |
| 20분 | Claude에게 오늘 필기 Notion 정리 요청 → 검토 |

**수요일 (2–3시간)** — 태블릿 정리 → PDF → Claude가 목요일 발표자료 제작

| 시간 | 할 일 |
|---|---|
| 50분 | **F1** 그림 3장 |
| 50분 | **F2** 예상 질문 6개 내 말로 |
| 30분 | **F3·F4** 다음 주 계획 + PDF 내보내기 |

**더 밀리면 빼는 순서**: ① MR-5 → ② MR-3의 5.1.4·5.3 → ③ MR-4의 6.2 → ④ F2 질문을 6개에서 4개(1·3·7·10)로. 🔍 C1·C4 코드, MR-2·MR-3의 5.1은 빼지 않습니다.

---

## 0. 시작 전에 알아 둘 것

### 이미 끝난 것 (10/5 12:30, Claude가 확인)

| 매뉴얼 단계 | 상태 | 비고 |
|---|---|---|
| STEP 1 ROS 2 설치 | 끝남 | Jazzy |
| STEP 2 미니 Cyclo용 venv | **생략** | PART B를 하지 않으므로 |
| STEP 3 AI Worker 모델 | 끝남 | `~/cyclo_study/ai_worker` |
| PART B 미니 Cyclo | **생략** | Windows에서 낸 수치(E6·E7, E8·E9)만 인용 |
| STEP 8 Cyclo 빌드 | 끝남 | `~/cyclo_ws`가 아니라 **`~/ros2_ws`** 사용 |
| STEP 9 브리지 venv | 끝남 | `~/cyclo_study/venv_ros` (mujoco 3.14.0) |

화면 없이 미리 돌려 본 결과입니다(**10/5 16:40 브리지 버그 수정 후 재검증**). 오늘 이 근처 숫자가 나오면 정상입니다. 로그는 `~/cyclo_study/verified/`에 있습니다. (버그 있던 때 로그는 `verified/old_bug/`)

| 실험 | 미리 돌린 결과 |
|---|---|
| C1 기본 이동 | 목표까지 **5.6 mm** 남음 (x −4.6, y +0.4, z −3.3 mm) |
| C2 중력 보상 | **0.0 mm** (처짐이 사라짐) |
| C4 자기충돌 | 오른손 (0.30, 0.03, 0.86)에서 멈춤, 왼손이 (0.40, 0.17, 0.84)로 비켜남 |
| C5 도달 불가 | x 0.80 목표 → 0.60까지 뻗고 멈춤 |

### 만들어 둔 실행 스크립트 (`~/cyclo_study`)

| 파일 | 쓰는 터미널 | 하는 일 |
|---|---|---|
| `env.sh` | 모두 | ROS·Cyclo 환경을 불러오고 `~/cyclo_study`로 이동 |
| `t1_bridge.sh 이름 [옵션]` | T1 | MuJoCo 창을 띄우고 로봇 역할을 합니다. 끝나면 `이름.csv` 저장 |
| `t2_cyclo.sh [옵션]` | T2 | 실제 Cyclo 컨트롤러(MoveL) 실행 |
| `send.sh c1 / c3 / c4 / c5` | T3 | 목표 자세 보내기 |
| `fk.sh` | T3 | Cyclo가 계산한 양손 위치 출력 |

### MR 읽기 지도

> ⚠️ **쪽수 안내 (임시)**: 아래 "영문 PDF 쪽"은 `~/Downloads/MR.pdf`(2017년 5월 영문 프리프린트) 기준입니다. **한글판은 쪽수가 다릅니다.**
> 절 번호(9.2.1 등)와 식 번호((9.8) 등)는 같으므로, 한글판에서는 **목차에서 절 번호로 찾으세요.**
> 한글판 목차를 받으면 Claude가 아래 "한글판 쪽" 칸과 가이드 전체를 한글판 쪽수로 바꿉니다.

| 절 | 한글판 쪽 | 영문 PDF 쪽 | Cyclo에서 만나는 곳 | 언제 |
|---|---|---|---|---|
| 9.1–9.2 궤적 생성, **식 (9.7)–(9.8)** | 9.2.1 = **461** | 343–348 | `rotationCubic`, `cubicVector` (movel 노드 411–420행) | MR-1 |
| 11.3.3 작업공간 속도 제어, **식 (11.18)** | ? | 437–438 | `computeDesiredVelocity` (343행) | MR-2 |
| 3.2.3.3 회전의 행렬 로그 | ? | 103– | 자세 오차, `rotationCubic`의 `log()` | MR-2 |
| 5.1 자코비안 (5.1.1, 5.1.2, 5.1.4, 5.1.5) | ? | 196–206 | `computeFrameJacobian(LOCAL_WORLD_ALIGNED)` | MR-3 |
| 5.3 특이점 | ? | 209–213 | `weight_damping` | MR-3 |
| 6.2 수치 IK (Newton–Raphson) | ? | 244–249 | Cyclo가 *쓰지 않는* 방식 (비교 대상) | MR-4 |
| 6.3 역속도 기구학, **식 (6.7)** | ? | 250–252 | QP 비용 (`vr_controller.cpp` 113행) | MR-4 |
| 8.3 RNEA | ? | 309–313 | C2 `--gravcomp` | MR-5 |
| 11.4.1 단일 관절 토크 제어 (중력 보상) | ? | 439–446 | C2 해석, 현대 임피던스와 연결 | MR-5 |

**이번에 안 읽는 것** (다음 주 이후): 4.1 순기구학(PoE), 3.3 트위스트·Adjoint, 7장 닫힌 연쇄(양팔 협동 운반 때), 9.3–9.4, 11.4.2 이후.

### 매뉴얼에서 틀린 곳 5가지 (미팅 전에 꼭 기억)

1. **Cyclo는 측정값이 아니라 자기 명령값으로 적분합니다.**
   `ai_worker_movel_controller_node.cpp:382` → `q_feedback = q_desired_`. 측정값 `q_`는 리프트 축에만 씁니다(383–385행). 최신 main도 같습니다.
   매뉴얼의 "q_d = q_측정 + q̇Δt", "E8 = Cyclo식 적분"은 틀린 설명입니다.
2. **특이점 제약은 슬롯만 있고 구현이 안 돼 있습니다.**
   QP에 slack 1개와 제약 1행이 잡혀 있지만, `setIneqConstraint()`가 그 행을 채우지 않습니다. 특이점 대응은 `weight_damping`(감쇠)만 합니다.
3. **감쇠 최소자승(DLS, λ²I)은 MR 본문에 없습니다.**
   MR 6.3은 의사역행렬과 가중 의사역행렬까지만 다룹니다. DLS는 그 의사역행렬이 특이점에서 커지는 문제를 막으려고 실무에서 더하는 항입니다. "MR 6.3의 확장"이라고 말해야 정확합니다.
4. **워크스페이스는 `~/ros2_ws`입니다.** 매뉴얼의 `~/cyclo_ws`가 아닙니다.
5. **브리지(`cyclo_mujoco_bridge.py`)에 버그가 있었습니다 — 10/5 16:40 수정.**
   관절 종류 비교(`m.jnt_type[j] in (...)`)가 MuJoCo 3.14에서 항상 False라 `/joint_states`에 **관절이 0개** 실렸습니다. Cyclo는 측정값을 전부 0으로 읽었고, 두 번째 명령부터 팔이 "내린 자세"로 리셋됐습니다(C4에서 오른팔이 떨어졌다 다시 올라감).
   `int()`로 비교하도록 고쳤습니다(34행 근처). 원본은 `cyclo_mujoco_bridge.py.orig`.
   **확인법**: T1을 켜면 `MuJoCo 브리지 시작: 관절 31개 발행`이 나와야 합니다. `0개`면 수정 전 파일입니다.
   수정 전 측정값(C1 8.9 mm, C2 4.4 mm, 16:35 C4 영상)은 쓰지 않습니다.

---

# 월요일 밤 (20:00–24:00) — 내일 미팅 준비 먼저, 그다음 개념·코드

**결과물**: 현대 미팅 포인트 메모 + MR 노트(11.3.3, 3.2.3.3, 5.1, 5.3, 8.3) + C1·C2·C4 코드 노트.

실습 단계(C1·C2·C4·C5)는 끝났습니다. 내용은 맨 아래 부록과 Notion "실습" 페이지에 있습니다.

---

## STEP E1. 현대 미팅 준비 (월 20:00–20:10)

별도 1장은 만들지 않습니다. **Notion "실습" 페이지를 위에서부터 보여 주며 영상(C4 → C1 → C5) 위주로 상황을 공유**하면 됩니다. MR 개념은 머릿속에 있는 만큼 말로 짧게.

Notion 페이지에 다 있지만 **현대 쪽에 따로 짚어 줄 포인트 3개**만 메모해 두세요.

1. **Cyclo는 위치 명령까지만 낸다 → 그 아래가 현대 몫.** C2에서 하위 계층에 중력 보상만 넣었더니 5.6 → 0.0 mm. 현대의 임피던스·전류 제어가 들어갈 자리가 바로 여기.
   → 물어볼 것: 현대 제어기는 **어떤 입력**을 받나요? (위치 명령 / 목표 힘 / 둘 다)
2. **실기로 옮길 때 주의점.** Cyclo는 측정값이 아니라 자기 명령값으로 계산을 이어 감(382행) → 실제 처짐·외력을 상위에서 모름. 시뮬의 위치 액추에이터와 실제 DYNAMIXEL 내부 제어도 다름.
3. **협동 운반과의 연결.** Cyclo의 `bimanual_movel`(두 손이 가상 물체를 잡은 채 상대 자세 유지)이 2대 협동 운반과 같은 문제. **Cyclo를 기준선으로 쓸지, 별도 IK를 만들지** 같이 정하기.

(시간이 되면) 진행 중 막혔던 것 한 줄: MuJoCo 브리지 버그를 찾아 고친 뒤 다시 측정함.

---

## 📖 MR-2. 작업공간 속도 제어 — 11.3.3 + 3.2.3.3 (월 20:10–20:40, 30분)

**왜 지금**: C1에서 Cyclo가 매 10 ms마다 "손을 어느 속도로 움직일지" 정했습니다. 그 규칙이 이 절입니다.

| 읽을 곳 | 영문 PDF 쪽 | 읽는 법 |
|---|---|---|
| 11.3 도입 + 11.3.1 단일 관절 | 431–435 | **훑기 (5분)**. "앞먹임(feedforward) + 오차 피드백" 구조만 잡습니다 |
| 11.3.3 Task-Space Motion Control | 437–438 | **정독 (12분)**. 식 (11.16) 읽고, **식 (11.18)에 집중** |
| 3.2.3.3 Matrix Logarithm of Rotations | 103– | **8분**. log(R) = 회전축 × 각도. 식 유도는 건너뛰고 결과만 |

**식 (11.18)이 Cyclo의 `computeDesiredVelocity`(343행)입니다.** (적분항 K_i = 0)

```
MR (11.18)   [ω; ṗ] = [ω_d; ṗ_d] + K_p · X_e,     X_e = [ log(RᵀR_d) ;  p_d − p ]
                     └ 앞먹임 ┘   └ 오차 피드백 ┘

Cyclo 343행  desired_vel = feedforward + kp × [ p_goal − p ;  axis·angle(R_goal Rᵀ) ]
             kp_position = kp_orientation = 50  (ai_worker_config.yaml 7행)
```

자세 오차를 MR은 손끝 좌표계(RᵀR_d)로, Cyclo는 world 좌표계(R_goal Rᵀ)로 씁니다. 같은 오차를 다른 좌표계에서 쓴 것뿐입니다.

✍ **노트 (11.3.3)**
- ① 정의: ________________________________
- ② 식: (11.18) ________________________________
- ③ 어디서: movel 노드 343행, C1에서 2초 동안 매 10 ms

✍ **답해 보기** (예상 질문 6번): v_d = v_ff + kp·e에서 각 항의 역할은? kp가 작으면?
> 앞먹임이 궤적을 따라가게 하고, 피드백이 남은 오차를 줄입니다. kp가 작으면 뒤처집니다(Windows 실험 E3: 최종 오차 3.5 mm).

---

## 🔍 C1 코드 — 명령 하나가 관절 명령이 되기까지 (월 20:40–21:10, 30분)

**목표**: 방금 C1에서 보낸 `/r_goal_move` 한 줄이 Cyclo 안에서 거치는 다섯 단계를 코드로 따라갑니다. MR-1(9.2), MR-2(11.3.3)에서 본 식이 **어느 줄**인지 찾는 게 핵심입니다.

주 파일: `ai_worker_movel_controller_node.cpp` (Ctrl+P → `ai_worker_movel_controller_node`)

### ① 명령이 도착하면 — 288–306행 `rightMoveLCallback`

```cpp
295  syncArmStateToFeedback(right_arm_joints_, q_desired_);   // 오른팔 명령값을 측정값으로 맞춤
299  kinematics_solver_->updateState(q_desired_, qdot_);
300  right_movel_start_pose_ = kinematics_solver_->getPose(r_gripper_name_);  // 시작 자세 = 지금 손 위치 (순기구학)
301  right_movel_goal_pose_  = poseMsgToEigen(msg->pose);                     // 목표 = 보낸 (0.35, -0.20, 0.85)
302  right_active_motion_duration_ = commandDurationSeconds(msg->time_from_start);  // T = 2 s
```

- **이 함수는 계산을 하지 않습니다.** 시작·목표·시간만 기억하고 끝납니다. 계산은 100 Hz 타이머(④~⑤)가 합니다.
- 295행이 중요합니다. 측정값을 쓰는 건 **명령이 도착하는 이 순간뿐**입니다. 이후에는 ⑤의 명령값으로 계속 갑니다.

### ② 2초짜리 궤적 만들기 — 404–429행 (매 10 ms) ↔ **MR (9.7)–(9.9)**

```cpp
404  if (right_movel_trajectory_active_ && right_elapsed < right_active_motion_duration_) {
405    linear_ref   = cubicDotVector<3>(elapsed, 0, T, p_start, p_goal, 0, 0);  // ṗ_ref  (앞먹임 속도)
410    position_ref = cubicVector<3>   (elapsed, 0, T, p_start, p_goal, 0, 0);  // p(s)   ← (9.7)
415    rotation_ref = rotationCubic    (elapsed, 0, T, R_start, R_goal);        // R(s)   ← (9.8)
419    angular_ref  = rotationCubicDot (...);                                   // ω_ref  (앞먹임 각속도)
428    right_desired_vel = computeDesiredVelocity(right_gripper_pose_, pose_ref, linear_ref, angular_ref);
430  } else {
434    right_desired_vel = computeDesiredVelocity(right_gripper_pose_, right_movel_goal_pose_);  // T 이후: 목표에 고정
```

(코드를 읽기 쉽게 줄였습니다. 실제 코드는 네임스페이스와 변수 이름이 깁니다.)

- 보간 함수 본체는 `type_define.hpp` (Ctrl+P → `type_define`)에 있습니다.
  - **126행 `cubic()`**: 끝 속도를 0으로 넣으면 MR (9.9)–(9.11)의 s(t) = 3(t/T)² − 2(t/T)³과 같습니다.
  - **290행 `rotationCubic()`**: `rotation_0 * ((rotation_0.transpose() * rotation_f).log() * tau).exp()` → **MR (9.8) 그대로**입니다.
- 2초가 지나면(430행 이후) 앞먹임 없이 목표 자세만 피드백으로 붙잡습니다.

### ③ 손끝 목표 속도 — 343–361행 `computeDesiredVelocity` ↔ **MR (11.18)**

```cpp
352  position_error    = goal.translation() - current.translation();      // p_d − p
353  rotation_error    = goal.linear() * current.linear().transpose();    // R_d Rᵀ
354  angle_axis_error(rotation_error);                                    // log → 축 × 각도 (MR 3.2.3.3)
358  desired_vel.head<3>() = feedforward_linear  + kp_position_    * position_error;    // ṗ = ṗ_d + Kp·(p_d − p)
359  desired_vel.tail<3>() = feedforward_angular + kp_orientation_ * orientation_error; // ω = ω_d + Kp·log(...)
```

- 결과는 6개 숫자(선속도 3 + 각속도 3)입니다. 아직 "손끝을 이렇게 움직이고 싶다"일 뿐, 관절 이야기는 없습니다.

### ④ 손끝 속도 → 관절 속도 (QP) — 470–492행 ↔ **MR 5.1, 6.3** (저녁 MR-3, MR-4)

```cpp
471  desired_task_velocities[r_gripper_name_] = right_desired_vel;   // 오른손 목표 속도
472  desired_task_velocities[l_gripper_name_] = left_desired_vel;    // 왼손도 들어감! (명령 없으면 "제자리 유지")
479  right_weight.head<3>().setConstant(weight_position_);           // W 위치 = 10
480  right_weight.tail<3>().setConstant(weight_orientation_);        // W 자세 = 1
487  damping = Ones(dof) * weight_damping_;                          // 감쇠 = 0.1
492  qp_controller_->getOptJointVel(optimal_velocities);             // QP 풀기 → 관절 속도 q̇ (31개)
```

QP 안쪽은 `vr_controller.cpp`의 **113–133행 `setCost`**입니다 (Ctrl+P → `vr_controller`).

```cpp
119  J_i = robot_data_->getJacobian(link_name);                        // 손마다 자코비안 (6×31)
130  P += 2.0 * J_iᵀ * W * J_i;                                        // ‖J q̇ − v_d‖²_W 를 풀어 쓴 것
132  q += -2.0 * J_iᵀ * W * xdot_desired;
```

- 지금은 "자코비안으로 손끝 속도와 관절 속도를 잇는 최소제곱 문제"라는 것만 잡고 넘어갑니다. 식의 뜻은 **MR-3(자코비안)과 MR-4(6.3)**에서 채웁니다.
- 472행이 C4의 복선입니다. 왼손에 명령을 안 줘도 **두 손이 늘 한 문제 안에 같이 들어 있습니다.**

### ⑤ 적분하고 내보내기 — 382, 499, 569–574행

```cpp
382  q_feedback = q_desired_;                                      // 측정값이 아니라 지난 주기의 명령값
499  q_desired_ = q_feedback + optimal_velocities * time_step_;    // q ← q + q̇·0.01
574  arm_r_pub_->publish(trajectory);                               // 오른팔 7개 + 그리퍼 → .../joint_trajectory
```

여기서 Cyclo의 일은 끝납니다. 그다음은 브리지(`cyclo_mujoco_bridge.py` 47–53행 `apply_trajectory`)가 받아서 MuJoCo 액추에이터 목표(`ctrl`)에 넣습니다.

### 직접 확인 (2분, C1을 다시 켜 둔 상태에서만 · 선택)

Cyclo가 실제로 내보내는 값(⑤)을 봅니다. 숫자 8개 = 오른팔 7개 + 그리퍼입니다.

```bash
ros2 topic echo --once /leader/joint_trajectory_command_broadcaster_right/joint_trajectory
```

설정값(③④)이 실제로 읽혔는지 봅니다.

```bash
ros2 param get /ai_worker_movel_controller kp_position
```

✍ **노트**: 다섯 단계를 한 줄씩. 각 줄 끝에 MR 식 번호.
1. 명령 도착: ________________________ (288)
2. 궤적: ________________________ (404–429, MR 9.7–9.9)
3. 손끝 속도: ________________________ (343, MR 11.18)
4. 관절 속도: ________________________ (492, MR 5.1·6.3)
5. 적분·발행: ________________________ (499)

✍ **답해 보기**: C1에서 Cyclo 계산(`fk.sh`)으로는 목표에 도착했는데, MuJoCo 실제 손은 왜 몇 mm 모자랐나? 위 다섯 단계 중 어디 때문인가?
> 힌트: ⑤의 382행. 그리고 바로 다음 C2.

---

## 휴식 (21:10–21:20)

---

## 🔍 C2 코드 — 처짐은 어디서 생기고, 어디서 보상하나 (월 21:20–21:35, 15분)

**목표**: C1의 처짐과 C2의 개선이 **Cyclo가 아니라 그 아래 계층**에서 일어난다는 걸 코드 세 군데로 확인합니다.

### ① 처짐이 생기는 곳 — MuJoCo 위치 액추에이터

파일: `~/cyclo_study/ai_worker/ffw_description/mujoco/ffw_sg2/ffw_sg2.xml` (Ctrl+P → `ffw_sg2.xml`)

```xml
24  <default class="YM080-230-R099-RH">                                 ← 클래스 이름이 실제 DYNAMIXEL-Y 모델명
25    <position kp="3000" kv="80" forcerange="-61.4 61.4"/>
438 <position name="arm_r_joint1" joint="arm_r_joint1" class="YM080-230-R099-RH" .../>
```

위치 액추에이터가 내는 힘은 **τ = kp·(목표 − 현재) − kv·속도**입니다. 멈춰 있을 때 중력 토크 τ_g를 버티려면 τ_g = kp·Δq만큼 **각도 오차 Δq가 남아야** 합니다.
→ 처짐 Δq = τ_g / kp. kp가 유한한 이상 처짐은 0이 되지 않습니다. 실기의 DYNAMIXEL 위치 제어도 같은 원리입니다(내부 P 게인).

### ② Cyclo는 그 처짐을 모른다 — `ai_worker_movel_controller_node.cpp` 382행

```cpp
382  Eigen::VectorXd q_feedback = q_desired_;    // 측정값 q_ 가 아니라 명령값
```

Cyclo는 처진 팔이 아니라 **자기가 낸 명령 자세**로 다음 계산을 합니다. 그래서 C1에서 `fk.sh`(Cyclo 계산)는 목표에 도착했다고 나오고, MuJoCo 실제 위치만 처져 있었습니다.

### ③ 보상하는 곳 — `cyclo_mujoco_bridge.py` 63–67행 (Ctrl+P → `cyclo_mujoco_bridge`)

```python
63  def step(self):
65      if self.gravcomp:                                                    # τ_ff = g(q) + C(q,q̇)q̇ (RNEA)
66          self.d.qfrc_applied[self.arm_dof] = self.d.qfrc_bias[self.arm_dof]
67      mujoco.mj_step(self.m, self.d)
```

- `qfrc_bias` = MuJoCo가 매 스텝 계산하는 **중력 + 코리올리·원심력 토크**입니다. MR 8.3 RNEA가 구하는 c(θ,θ̇) + g(θ)와 같은 양입니다.
- 이걸 팔 관절에 그대로 더하면 액추에이터가 중력을 버틸 필요가 없어집니다 → Δq가 줄어듦 → **C1 → C2 오차 감소.**
- Cyclo 코드는 한 줄도 안 바뀌었습니다. **바뀐 건 브리지(= 실로봇의 하위 제어기 자리)뿐입니다.**

### 정리 그림 (노트에 그대로)

```
Cyclo (위치 명령, 382행: 처짐 모름)
   │ q_desired
   ▼
하위 제어  τ = kp(q_d − q) − kv·q̇  [+ g(q) ← C2에서 추가]   ← 현대의 임피던스·전류 제어가 들어갈 자리
   │
   ▼
팔 (중력) → 처짐 Δq = τ_g / kp
```

✍ **답해 보기**: 실기에서 처짐을 줄이는 방법 두 가지는? (힌트: 위 그림의 kp, 그리고 [+ g(q)])

---

## 📖 MR-5. 힘 계층 — 8.3, 11.4 (월 21:35–21:45, 10분 · C2 코드 바로 이어서)

방금 본 C2 코드(`qfrc_bias`)의 이론 쪽입니다. **시간이 밀렸으면 건너뜁니다.** Notion 실습 페이지 C2에 핵심 식 (11.38)은 이미 들어가 있습니다.

**왜 읽나**: C2의 `--gravcomp`가 무엇을 더했는지, 그리고 현대의 임피던스 제어가 Cyclo 아래 어디에 붙는지 알기 위해서입니다.

| 읽을 곳 | 영문 PDF 쪽 | 읽는 법 |
|---|---|---|
| 8.3 도입 + 8.3.2 알고리즘 | 309, 312 | **알고리즘 박스만 (5분)**. τ = M(θ)θ̈ + c(θ,θ̇) + g(θ)를 링크마다 재귀로 계산한다는 것 |
| 11.4.2.2 Centralized Multi-joint Control | 450 | **식 (11.38)–(11.39)만 (5분)**. PD + 중력 보상 → 오차 0으로 수렴 = C2의 0.0 mm |
| 11.4.1 단일 관절 토크 제어 | 439–446 | 시간 남으면 훑기 |

✍ **노트 (8.3 / 11.4.1)** — 한 줄씩:
- RNEA: ________________________________
- 중력 보상: ________________________________ (C1 ___ → C2 ___ mm, 재측정 값)

---

## 📖 MR-3. 자코비안 · 특이점 — 5.1, 5.3 (월 21:45–22:20, 35분)

**왜 지금**: (11.18)로 만든 "손끝 속도"를 "관절 속도"로 바꾸려면 자코비안이 필요합니다. 오후 C4에서 두 팔이 함께 움직인 것도 자코비안 위에서 푼 결과입니다. 바로 다음 🔍 C4 코드에서 확인합니다.

| 읽을 곳 | 영문 PDF 쪽 | 읽는 법 |
|---|---|---|
| 5.1 도입 + 5.1.1 Space Jacobian | 196–200 | **정독 (12분)**. 예제 계산은 훑기 |
| 5.1.2 Body Jacobian | 201–203 | **정독 (8분)** |
| 5.1.4 Space와 Body의 관계 | 205 | **5분**. J_s = [Ad] J_b 한 줄 |
| 5.1.5 Alternative Notions | 205–206 | **5분**. "손끝 원점 속도 + 고정 좌표계 축" 같은 다른 표현도 있다는 것 |
| 5.3 Singularity Analysis | 209–213 | **5분**. 그림 위주. "rank가 떨어지면 어떤 방향으로 못 움직인다" |
| 5.4 조작성 | 214– | 건너뜁니다 |

**Cyclo는 어느 자코비안을 쓰나?** `kinematics_solver.cpp:190`

```cpp
pinocchio::computeFrameJacobian(model_, data, q, link_index, LOCAL_WORLD_ALIGNED, J);
```

`LOCAL_WORLD_ALIGNED` = 속도를 **손끝 원점**에서 재고, **world 축**으로 표현합니다.
- space 자코비안(5.1.1): 원점이 world → 다름
- body 자코비안(5.1.2): 축이 손끝 좌표계 → 다름
- → **둘 다 아닌 중간 표현.** 5.1.5의 "다른 표현"이고, (11.18)의 (ω, ṗ)와 같은 생각입니다.

AI Worker 한쪽 팔은 7관절이므로 J는 **6×7**입니다. 행(6)보다 열(7)이 많아 남는 자유도가 1개 있습니다 → MR-4에서 다룹니다.

✍ **노트 (5.1)**
- ① 정의: ________________________________
- ② 식: V = J(θ)θ̇ ________________________________
- ③ 어디서: `kinematics_solver.cpp:190`, QP 비용 `vr_controller.cpp:113`

✍ **노트 (5.3)** — 한 줄: ________________________________

✍ **답해 보기** (예상 질문 1번): space / body 자코비안 차이는? Cyclo는 어느 쪽?

---

## 휴식 (22:20–22:30)

---

## 🔍 C4 코드 — 충돌 거리 → CBF 제약 → 왼손이 비키는 이유 (월 22:30–23:00, 30분)

**목표**: C4 영상에서 "명령을 안 받은 왼손이 왜 비켰나"를 코드 세 군데로 설명할 수 있게 됩니다. 방금 MR-3(자코비안)을 읽은 상태라 ②가 읽힙니다.

### ① 두 손은 늘 같은 문제 안에 있다 — `ai_worker_movel_controller_node.cpp` 471–472행

```cpp
471  desired_task_velocities[r_gripper_name_] = right_desired_vel;   // 오른손: 왼손 자리로 가라
472  desired_task_velocities[l_gripper_name_] = left_desired_vel;    // 왼손: 지금 자리에 있어라 (C4 1단계 목표)
```

QP의 변수 q̇는 **로봇 전체 관절 31개**입니다. 오른팔·왼팔을 따로 풀지 않습니다.

### ② 두 손 사이 거리와 그 기울기 — `kinematics_solver.cpp` 250–335행 (Ctrl+P → `kinematics_solver`)

```cpp
265  pinocchio::computeDistances(model_, data_, geom_model_, geom_data_, q_);   // 링크 쌍마다 최소 거리 d
311  pA = dist_res.nearest_points[0];  pB = dist_res.nearest_points[1];          // 두 링크에서 가장 가까운 두 점
313  n = (pB − pA) / ‖pB − pA‖;                                                  // 두 점을 잇는 방향
329  JA = J_jointA.topRows<3>() − skew(rA) * J_jointA.bottomRows<3>();          // 점 A의 속도 자코비안
330  JB = J_jointB.topRows<3>() − skew(rB) * J_jointB.bottomRows<3>();          // 점 B의 속도 자코비안
332  grad = (nᵀ * (JB − JA))ᵀ;                                                   // ∂d/∂q
```

(코드를 읽기 쉽게 줄였습니다.)

- **329–330행** = 강체 위의 한 점 속도 **v_p = v + ω × r**을 자코비안으로 쓴 것입니다. MR-3에서 읽은 5.1 자코비안(관절 속도 → 속도)을 "손끝"이 아니라 "가장 가까운 점"에 적용한 것뿐입니다.
- **332행**: 두 점이 서로 멀어지는 속도 = nᵀ(v_B − v_A) = nᵀ(J_B − J_A) q̇. 즉 `grad`는 "관절을 이렇게 움직이면 거리가 얼마나 변하나"(ḋ = gradᵀ q̇)입니다.
- J_A는 오른팔 관절에, J_B는 왼팔 관절에 값이 있습니다 → **`grad`에는 양팔 관절이 다 들어 있습니다.** 여기가 ③의 핵심입니다.

### ③ CBF 제약으로 넣기 — `vr_controller.cpp` 200–216행

```cpp
201  pair_results = robot_data_->getCollisionPairDistances(true, ...);   // ② 호출 (기울기 포함)
205  A_ineq 의 한 행 = res.grad.transpose();                             // gradᵀ q̇
209  + slack (1.0)                                                       // 불가능할 때만 조금 어김
211  if (res.distance <= collision_buffer_) {                            // 5 cm 안에 들어왔을 때만
212    l_ineq = −cbf_alpha_ * (res.distance − collision_safe_distance_); //   하한 = −α(d − 0.02)
```

합치면:

```
gradᵀ q̇ + s  ≥  −α (d − d_safe)        (d ≤ 0.05 m일 때)
   = ḋ
```

- **CBF 읽는 법**: h = d − d_safe ≥ 0을 지키고 싶습니다. ḣ = ḋ ≥ −α·h이면 h가 0에 가까워질수록 "다가가는 속도"의 허용치도 0이 되어 넘지 않습니다.
- 같은 모양이 바로 위 186–198행 **관절 한계**에도 있습니다: q̇ + s ≥ −α(q − q_min). 거리 d 대신 관절각 q일 뿐입니다.

### ④ 그래서 왼손이 비킨다

QP는 비용(오른손은 목표로, 왼손은 제자리에)을 최소화하면서 ③의 제약을 지켜야 합니다. ②에서 `grad`에 **양팔 관절이 모두 들어 있으므로**, ḋ를 지키는 방법은 두 가지가 섞입니다.

- 오른손을 덜 보내기 (오른손 추종 비용 ↑)
- 왼손을 바깥으로 비키기 (왼손 유지 비용 ↑)

가중치가 같으므로(`weight_position` 10 = 10) QP는 **둘을 섞은 해**를 냅니다. 그래서 C4 기록에서 오른손이 약 7 cm 모자라고, 왼손이 약 8 cm 비켜났습니다.
팔마다 따로 IK를 풀었다면 왼손은 꼼짝하지 않고 오른손만 멈췄을 겁니다. **이것이 whole-body control입니다.**

✍ **노트**: 세 줄로
1. 거리와 기울기: ________________________ (kinematics_solver.cpp 332, MR 5.1)
2. CBF 제약: ________________________ (vr_controller.cpp 211–213)
3. 왼손이 비킨 이유: ________________________

✍ **답해 보기** (예상 질문 8번): `cbf_alpha`를 50에서 5로 줄이면 C4에서 무엇이 달라질까?
> 힌트: α가 작으면 h가 클 때도 ḣ 허용치가 작습니다 → 더 멀리서부터 천천히 다가갑니다.

---

## 📖 MR-4. 역기구학 — 6.2, 6.3 (월 23:00–23:40, 40분 · 넘겨도 됨 → 화요일)

**왜 지금**: 앞의 MR-3에서 "손끝 속도 = J × 관절 속도"를 봤습니다. 이번엔 반대로 **원하는 손끝 속도에서 관절 속도를 구하는 법**입니다. 이게 Cyclo QP가 푸는 문제입니다.

| 읽을 곳 | 영문 PDF 쪽 | 읽는 법 |
|---|---|---|
| 6.2 Numerical IK — 6.2.1 Newton–Raphson | 244 | **훑기 (5분)** |
| 6.2.2 Numerical IK Algorithm | 245–249 | **알고리즘 박스만 정독 (10분)**. 예제는 건너뜀 |
| 6.3 Inverse Velocity Kinematics | 250–252 | **정독 (25분)**. 식 (6.7) 의사역행렬, 여유 자유도, 가중 의사역행렬(질량행렬로 가중) |

**6.2와 Cyclo의 차이** — Cyclo는 6.2(반복해서 수렴)를 쓰지 않고 **6.3(속도를 한 번 풀기)을 100 Hz로 반복**합니다.

```
MR 6.2   θ ← θ + J†(θ)·V_err   를 오차가 0이 될 때까지 반복         (한 번 부를 때 여러 번 계산)
MR 6.3   θ̇ = J†(θ)·V_d   (6.7)                                       (한 번)
Cyclo    매 10 ms: 현재 자세에서 6.3을 한 번 → θ += θ̇·Δt → 다음 주기
```

**6.3 → Cyclo QP로 가는 세 단계** (`vr_controller.cpp:113` `setCost`)

| 단계 | 식 | 근거 |
|---|---|---|
| ① 의사역행렬 | θ̇ = J†V_d. 7관절이면 해가 여러 개 → 그중 ‖θ̇‖가 가장 작은 것 | MR 6.3 식 (6.7) |
| ② 가중 의사역행렬 | 관절마다 다른 가중치로 최소화 | MR 6.3 (PDF 251) |
| ③ 감쇠 + 제약 | min ‖Jθ̇ − V_d‖²_W + w_d‖θ̇‖² + 관절 한계·충돌 제약 | **MR 밖** — Cyclo QP |

①에 감쇠만 더한 것이 DLS(Windows 미니 Cyclo의 `solve_dls`), 거기에 제약까지 더한 것이 Cyclo QP입니다. 그래서 **"DLS는 제약 없는 QP"**입니다.

남는 1자유도(MR-3에서 본 6×7): 6.3의 "최소 노름 해"처럼 Cyclo도 감쇠 항(‖θ̇‖ 최소)이 정합니다. 팔꿈치 자세 유지 같은 별도 작업은 없습니다 → 확장 지점.

✍ **노트 (6.2–6.3)**
- ① 정의: ________________________________
- ② 식: (6.7) ________________________________
- ③ 어디서: `vr_controller.cpp:113`, C5(특이점 근처에서 slack)

✍ **답해 보기** (예상 질문 2번): 왜 Newton–Raphson이 아니라 미분 IK인가?

---

## STEP E2. 마무리 (월 23:40–24:00)

- [ ] 영상 3개(`~/Videos/Screencasts/` c1·c4·c5)와 Notion 실습 페이지 영상이 재생되는지 확인합니다.
- [ ] 내일 가져갈 것: Notion 실습 페이지 링크, 영상 3개(C1, C4, C5), 포인트 메모 3개
- [ ] 내일 물어볼 질문을 1–2개 적습니다. 예: "현대 쪽 임피던스 제어는 어떤 입력(위치 명령인지, 목표 힘인지)을 기대하나요?"
- [ ] CSV가 다 있는지 확인합니다.

```bash
ls ~/cyclo_study/*.csv
```

---

# 화요일

## 오전 — 현대 미팅

- [ ] Notion 실습 페이지와 영상으로 공유합니다. 영상은 **C4 → C1 → C5** 순서를 추천합니다.
- [ ] 피드백은 노트에 그대로 적습니다.

## 저녁 (2–3시간)

- [ ] 월요일에 밀린 것부터 (예: 🔍 C4 코드)
- [ ] 📖 MR-4 (월요일에 못 했으면, 위 월요일 섹션)
- [ ] 📖 MR-6 + 코드 흐름 표 (아래)
- [ ] 현대 피드백 정리 (20분)
- [ ] Claude에게 "오늘 필기 Notion에 정리해줘" 요청 → 검토 (20분)

---

## 📖 MR-6. MR ↔ Cyclo 한 쪽 요약 + 코드 흐름 (화 저녁, 40분)

오늘 MR 노트(MR-1 ~ MR-5)를 **한 쪽 표**로 옮깁니다. 이 표가 수요일 태블릿 정리와 목요일 발표 4번 슬라이드의 원본이 됩니다.

| MR 절 · 식 | 한 줄 의미 | Cyclo 코드 | 오늘 실험 |
|---|---|---|---|
| 9.2, (9.7)–(9.8) | | movel 노드 411–420 | C1 |
| 11.3.3, (11.18) | | movel 노드 343 | C1, C2 |
| 3.2.3.3 | | type_define.hpp 290 | — |
| 5.1, 5.1.5 | | kinematics_solver.cpp 190 | C4 |
| 5.3 | | `weight_damping` | C5 |
| 6.3, (6.7) | | vr_controller.cpp 113 | C4, C5 |
| MR 밖: QP · CBF · slack | | vr_controller.cpp 150, 168 | C4, C5 |
| 8.3 / 11.4.1 | | (Cyclo 밖, 브리지 `--gravcomp`) | C2 |

- [ ] 표 완성 (빈칸은 내 말로)

---

## (참고) D1 코드 흐름 표 — MR-6에서 같이 씁니다

MR-6 시간(22:15–22:40)에 아래 MR-6 표와 **함께** 채웁니다. 🔍 C1·C2·C4에서 코드를 이미 다 봤으니 새로 읽지 않고, 흩어진 노트를 이 표 한 장으로 모읍니다.

읽기 도우미: [지난 보고서](https://claude.ai/code/artifact/3f56857b-20b4-4e67-96c7-c44cbcfbf308)의 2·4·5절

| # | 파일 : 줄 | 볼 것 | MR | 노트에 적을 한 줄 |
|---|---|---|---|---|
| ① | `cyclo_motion_controller_ros/config/ai_worker_config.yaml` : 7–19 | `kp_position 50`, `weight_*`, `cbf_alpha 50`, `/r_goal_move` | — | 오늘 쓴 토픽과 숫자가 여기 있다 |
| ② | `ai_worker_movel_controller_node.cpp` : 288 | `rightMoveLCallback` — 시작·목표 자세 저장 | — | 명령이 들어오면 시작·목표를 기억 |
| ③ | 같은 파일 : 411–420 | `cubicVector`, `rotationCubic` | **9.2, (9.7)–(9.8)** | 위치 직선 + 자세 log/exp, 3차 s(t) |
| ④ | 같은 파일 : 343 | `computeDesiredVelocity` | **11.3.3, (11.18)** | v_d = v_ff + kp·e |
| ⑤ | `kinematics_solver.cpp` : 190 | `computeFrameJacobian(LOCAL_WORLD_ALIGNED)` | **5.1, 5.1.5** | 손끝 원점, world 축 |
| ⑥ | `vr_controller.cpp` : 113 / 150 / 168 | `setCost` / `setBoundConstraint` / `setIneqConstraint` | **6.3 (6.7) + MR 밖** | 비용 = 추종 + 감쇠 + slack, 제약 = 속도 한계 + CBF |
| ⑦ | `ai_worker_movel_controller_node.cpp` : 382, 499 | `q_feedback = q_desired_` → `q_desired_ += q̇·Δt` | 수치 적분 | 명령값 기준 적분 → C1 처짐의 원인 |

(②③④⑦은 `cyclo_motion_controller_ros/src/nodes/ai_worker/`, ⑤⑥은 `cyclo_motion_controller_core/src/` 아래에 있습니다.)

- [ ] ①–⑦을 노트에 한 줄씩 적었다
- [ ] 노트 맨 아래에 이 그림을 손으로 그립니다 (**수요일 그림 ②의 초안**). 상자 옆에 MR 절 번호를 붙입니다.

```
/r_goal_move ─► 보간 ─► v_d = v_ff + kp·e ─► QP(OSQP) ─► q += q̇·Δt ─► 관절 명령 ─► MuJoCo
               (9.2)       (11.3.3)          (5.1, 6.3)    (적분)
                  ▲                                            │
                  └──────── 명령값(q_desired_)으로 다음 주기 ◄──┘
```

---

# 수요일 (2–3시간) — 태블릿 정리 → PDF

**결과물**: 태블릿 노트 PDF 1개. Claude가 이걸로 목요일 발표자료를 만듭니다.
MR은 새로 읽지 않습니다. 월요일 노트와 MR-6 표를 옮겨 적으며 다시 봅니다.

## STEP F1. 그림 3장 (50분)

| 쪽 | 그림 | 넣을 것 |
|---|---|---|
| 1 | **시스템 구성** | 세 박스: T2 Cyclo ↔ T1 브리지 ↔ MuJoCo. 화살표에 토픽 이름 (`/r_goal_move`, `/joint_states`, `.../joint_trajectory`). "브리지 = 실로봇 follower 역할" |
| 2 | **MoveL 한 주기** | STEP D1 맨 아래 그림 정리본 + 상자마다 MR 절·식 번호 (9.2 (9.8) / 11.3.3 (11.18) / 5.1 · 6.3 (6.7) / 적분) |
| 3 | **QP 식** | 아래 식 + CBF·slack 한 줄씩 + MR-6 표 |

3쪽에 옮길 식:

```
변수  x = [q̇, slack들]
비용  Σ ‖J_i q̇ − v_d,i‖²_W + w_d ‖q̇‖² + ρ·Σ slack        (W 위치 10 / 자세 1, w_d 0.1, ρ 1000)
제약  q̇_min ≤ q̇ ≤ q̇_max                                    (속도 한계)
      q̇ + s ≥ −α (q − q_min),   −q̇ + s ≥ −α (q_max − q)     (관절 한계 CBF, α 50)
      ∇dᵀ q̇ + s ≥ −α (d − d_safe)   [d ≤ 0.05일 때]          (자기충돌 CBF, d_safe 0.02)

CBF   h ≥ 0을 지키려면 ḣ ≥ −α·h → 경계에 가까울수록 다가가는 속도도 0에 가까워짐   (MR 밖)
slack 제약끼리 충돌해도 QP가 풀리게. 평소 0, 불가능할 때만 조금 어김 (C5)          (MR 밖)
DLS   제약을 빼고 W = I, w_d = λ²이면 DLS 식과 같음 → "DLS는 제약 없는 QP"         (MR 6.3의 확장)
```

## STEP F2. 예상 질문 6개 — 내 말로 (50분)

매뉴얼 PART F의 13개 중 이 6개만 합니다. 뼈대를 보고 **자기 말로 2–3줄**씩 적습니다. 월요일 "✍ 답해 보기"에 적은 것을 다듬으면 됩니다.

| # | 질문 | 답의 뼈대 | MR |
|---|---|---|---|
| 1 | space / body 자코비안 차이? Cyclo는? | space = 고정 좌표계에서 본 twist, body = 손끝 좌표계. Cyclo는 `LOCAL_WORLD_ALIGNED`(손끝 원점, world 축) → 둘 사이 (kinematics_solver.cpp:190) | 5.1.1, 5.1.2, 5.1.5 |
| 2 | 왜 Newton–Raphson이 아니라 미분 IK? | 100 Hz마다 현재 자세에서 한 번 선형화해 속도를 구함. 반복 수렴이 필요 없고, 제약을 QP로 넣기 쉬움 | 6.2 vs 6.3 |
| 3 | 특이점은 어떻게 막나? | J의 계수가 떨어지면 q̇ 폭주. Cyclo는 감쇠 항(`weight_damping`)으로 대응. 특이점 제약 슬롯은 있지만 구현 안 됨 → 확장 지점 | 5.3 |
| 7 | QP 비용과 제약을 말해 보라 | STEP F1 3쪽 식. OSQP 표준형 ½xᵀPx + qᵀx, l ≤ Ax ≤ u | 6.3 + MR 밖 |
| 8 | CBF가 뭔가? α는? | ḣ ≥ −αh. α가 크면 경계 가까이까지 빠르게, 작으면 일찍 감속. C4에서 확인 | MR 밖 |
| 10 | **(정정)** Cyclo는 무엇을 기준으로 적분하나? | 측정값이 아니라 **자기 명령값** (382행 `q_feedback = q_desired_`). 그래서 Cyclo는 처짐을 모르고, 처짐은 하위 위치 제어가 결정 (C1). 아래 계층에 중력 보상을 넣으면 줄어듦 (C2) → 힘 계층이 들어갈 자리 | 8.3, 11.4.1 |

## STEP F3. 현대 피드백 + 다음 주 (15분)

- [ ] 한 쪽에: 현대 피드백 요약 / 다음 주 할 일 2–3개
  - 예: 실로봇에서 같은 C1 명령 비교, `bimanual_movel`로 가상 물체 운반(**MR 7장 닫힌 연쇄**, 3.3 Adjoint), 중력 보상 → 임피던스 위치

## STEP F4. PDF로 내보내고 Claude에게 넘기기 (15분)

- [ ] 태블릿 노트를 PDF로 내보냅니다.
- [ ] 이 폴더에 넣습니다:

```bash
mkdir -p ~/cyclo_study/handoff_thu
```

넣을 것: 노트 PDF, `media/`의 영상·캡처, 현대 1장 PDF, (있으면) `C1_bridge.png`·`C2_bridge.png`

- [ ] Claude에게 이렇게 보냅니다:
  > `~/cyclo_study/handoff_thu` 에 정리본 넣었어. 매뉴얼 PART F 8장 구성으로 목요일 발표자료 만들어줘.

---

# 이번에 하지 않는 것

시간이 부족하면 아래는 빼도 됩니다. 발표에서 물으면 "다음 단계"로 답합니다.

- 미니 Cyclo 재실행 (Windows 수치만 인용)
- 기준 대비 실측 그래프·정량 분석
- C6 파라미터 바꾸기, C7 FK 일치 비교
- MR 4.1, 3.3, 7장, 9.3–9.4, 11.4.2 이후
- `bimanual_movel` 실행 (협동 운반 시연은 다음 주)

**시간이 밀릴 때 빼는 순서**: ① MR-5 → ② C3 → ③ MR-3의 5.1.4·5.3 → ④ MR-4의 6.2 → ⑤ 🔍 C2 코드(그림만 노트에 옮기기). 실험 C1·C4, MR-1·MR-2, 🔍 C1·C4 코드는 빼지 않습니다.

---

# 부록 — 끝난 단계 (참고용)

## ✅ 월요일 오후에 끝낸 실습 (참고용)

14:00–16:45에 끝냈습니다. C1 영상은 그대로 씁니다(정지 상태에서 명령 하나라 버그 영향 없음). C1·C2 **숫자**와 C4 영상은 STEP R에서 다시 합니다. 원래 단계 내용은 맨 아래 부록에 있습니다.

---

## 🔁 STEP R. 브리지 수정 후 다시 하기 (16:45–17:05)

정정 5번의 브리지 버그 때문에 C1·C2 숫자와 C4 영상을 다시 만듭니다. **C1·C2는 녹화 없이 숫자만**, C4만 녹화합니다.

- [ ] **확인**: T1을 켰을 때 `MuJoCo 브리지 시작: 관절 31개 발행`. `0개`가 나오면 Claude에게 알려 주세요.

**R1. C1 숫자 (3분, 녹화 없음)**

```bash
./t1_bridge.sh C1
```

T2 `./t2_cyclo.sh` → T3 `./send.sh c1` → 5초 뒤 T2·T1 끄기 → T3:

```bash
./venv_ros/bin/python plot_bridge.py --log C1.csv --target 0.35 -0.20 0.85 --out C1
```

✔ 5–6 mm 근처. 부록 C1의 ✍ 기록 칸(⚠️ 표시)에 새 값을 적습니다.

**R2. C2 숫자 (3분, 녹화 없음)**

```bash
./t1_bridge.sh C2 --gravcomp
```

T2 `./t2_cyclo.sh` → T3 `./send.sh c1` → 5초 뒤 T2·T1 끄기 → T3:

```bash
./venv_ros/bin/python plot_bridge.py --log C2.csv --target 0.35 -0.20 0.85 --out C2
```

✔ 0 mm 근처. 아래 STEP C2의 ✍ 기록 칸에 적습니다. (C2 단계 자세한 설명은 바로 아래 STEP C2)

**R3. C4 재녹화 (15분)** → 아래 **STEP C4**를 처음부터 그대로 합니다. 이전 영상(16-35-13)은 지우거나 `old_` 를 붙여 두세요.

---

## STEP C2. 중력 보상 — 설명·기록용 (실행은 STEP R2)

**보여 줄 것**: 처짐은 아래 계층에서 중력 보상(feedforward)을 넣으면 준다 → 현대의 임피던스 제어가 들어갈 자리.

- [ ] **T1** (옵션 `--gravcomp` 추가):

```bash
./t1_bridge.sh C2 --gravcomp
```

- [ ] **T2**:

```bash
./t2_cyclo.sh
```

- [ ] **T3**:

```bash
./send.sh c1
```

✔ C1과 같은 움직임이고, 끝에서 처짐이 거의 없습니다.

- [ ] 5초 뒤 **T2 Ctrl+C → T1 Ctrl+C**
- [ ] **T3**:

```bash
./venv_ros/bin/python plot_bridge.py --log C2.csv --target 0.35 -0.20 0.85 --out C2
```

✔ 0 mm 근처면 정상입니다. (수정 전 브리지에서는 4.4 mm가 나왔습니다 — 버그 때문)

✍ **기록**: 목표와의 거리 C1 5.6 mm → C2 0.0 mm
**설명할 수 있어야 하는 것**
> 오차가 거의 절반으로 줄었는데 지금 바꾼 것은 하위 계층이다. 즉, 상위계층인 cyclo에서는 $$\dot{x}_{\text{cmd}} = \dot{x}_{\text{ref}} + K_p (x_{\text{ref}} - x)[cite: 1, 2]$$ 이렇게 작업 공간 feedforward에 비례오차 피드백 제어기를 사용한다. 317-382행에서 확인할 수 있듯이 cyclo는 실제 센서값이 아닌 자신이 보낸 명령값을 기준으로 적분하여 위치 지령을 내보낸다.
바뀐 점은 --gravcomp이다. 방금은 위치제어만 존재해서 위치 오차에 비례하는 복원 토크를 내보냈지만 실제 팔 링크 질량에 의해 중력 토크가 아래로 끌어당겨 정지 상태를 유지하려면 중력과 평형을 이루어야 하므로 중력 처짐 편차 $$q_{\text{desired}} - q = \frac{g(q)}{K_p} \neq 0 \implies \text{말단 오차 8.9 mm 발생}[cite: 1, 2]$$ 가 남는다.
그런데 --gravcomp를 활성화하면 mujoco 시뮬레이터 내부에서 MR 8.3에 해당하는 RNEA(recursive newton-euler algorithm)를 통해 현재 자세에서의 동역학 토크 $h(q, \dot{q}) = c(q, \dot{q}) + g(q)$를 계산하여 모터에 직접 feedforward로 더해준다. 즉, $$\tau = K_p (q_{\text{desired}} - q) + \tilde{g}(q)[cite: 2]$$ 으로 토크 수식이 바뀌고 MR 식 11.38형식과 같다. 이렇게 되면 중력을 지탱하는 부담을 $\tilde{g}(q)$ 항이 담당하여 모터의 위치 제어기가 중력을 버티기 위해 오차를 남겨두지 않게 된다. 중력 처짐이 상쇄되어 오차는 4.4mm로 대폭 감소할 수 있게 된다.
그럼 구조적으로 왜 위치 명령 아래에 힘 계층을 사용할까? 그에 대한 해답은 순수 기구학 기반 제어의 한계이다. cyclo는 상위 계층으로 모터 질량, 링크 관성, 중력 등 물리적 세계의 힘을 알지 못하고 기구학적 위치와 속도만 계산한다. 이는 액추에이터가 힘을 내지 못하면 정밀한 직선 궤적(MoveL)을 계산하더라도 실제 로봇은 중력에 주저않는다는 의미이다. 계층적 제어 아키텍처를 다시 정리하면 상위에서 cyclo가 작업 공간 직선 경로 생성을 하고 qp 기반 목표 관절 위치와 속도 지령을 만든다. 하위 단계에서는 $M(q)\ddot{q} + c(q,\dot{q}) + g(q)$ 동역학 모델을 바탕으로 중력과 외력을 상쇄하는 토크 feedforward를 생성해내서 상위 기구학 알고리즘은 그대로 쓰고, 하위에 중력 보상(힘 계층)을 추가하는 것만으로 추종 성능을 향상시킬 수 있다.
그럼에도 남은 4.4mm 오차는 왜 있을까? 중력 토크가 이상적으로 상쇄되었다 하더라도, 관절의 마찰력이나 링크와 감속기의 미세 탄성 변형, 제어 이산화 주기 및 솔버의 수치 오차 등 복합적으로 작용하여 잔여 편차가 남게 된다.

> ⚠️ **[정정 10/5 16:45 — Notion 옮길 때 반영]**
> - 4.4 mm는 브리지 버그 때문에 남은 값이었습니다. 수정 후 C2 = **0.0 mm** → 중력 보상만으로 처짐이 사라집니다.
> - 따라서 "남은 4.4 mm 오차는 왜 있을까?" 문단(마찰·탄성·이산화 오차)은 **이 시뮬레이션에는 해당하지 않습니다.** 이 MuJoCo 모델에는 그런 오차 요인이 거의 없기 때문입니다. 실기에서는 그 요인들이 실제로 남으므로, "실로봇에서는 잔여 오차가 생길 것"으로 바꿔 쓰면 맞습니다.
> - "말단 오차 8.9 mm" → 재측정한 C1 값(약 5.6 mm)으로, "절반으로 줄었다" → "사라졌다"로.
> - "317-382행" → 382–388행 (`ai_worker_movel_controller_node.cpp`).

---

## STEP C4. 자기충돌 회피 🎥 — 미팅 핵심 장면 (STEP R3, 16:50–17:05)

**보여 줄 것**: 두 팔을 하나의 QP로 같이 풀고, 충돌 제약(CBF)을 지킨다.

- [ ] **T1**:

```bash
./t1_bridge.sh C4
```

- [ ] **T2**:

```bash
./t2_cyclo.sh
```

- [ ] MuJoCo 화면을 **두 손이 다 보이게 정면에서** 잡습니다.
- [ ] 🎥 **녹화 시작**
- [ ] **T3**:

```bash
./send.sh c4
```

이 명령은 두 단계로 자동 진행됩니다.
1. 두 손을 가슴 앞에 모읍니다. 왼손 (0.35, +0.10), 오른손 (0.35, −0.10)
2. 3초 뒤 오른손을 **왼손이 있는 자리** (0.35, +0.10)로 보냅니다.

✔ 오른손이 왼손에 닿기 전에 멈춥니다.
✔ **왼손이 바깥쪽으로 비켜납니다.** 이게 이 장면의 핵심입니다.
✔ 2단계 동안 오른팔은 **아래로 떨어지지 않고** 높이(z ≈ 0.85)를 유지한 채 옆으로 이동합니다.
✗ 오른팔이 순간적으로 아래로 툭 떨어졌다가 다시 올라가면 → 브리지 버그입니다. T1 로그가 `관절 31개`인지 확인하세요.

- [ ] 멈추고 3초 뒤 🎥 **녹화 정지**
- [ ] 📸 **캡처 3**: 두 손이 떨어져 멈춘 장면
- [ ] **T3**:

```bash
./fk.sh
```

- [ ] **T2 Ctrl+C → T1 Ctrl+C**

✍ **기록**
- 오른손 멈춘 곳: x 0.298 y 0.031 z 0.858 (목표는 0.35, 0.10, 0.85)
- 왼손 비켜난 곳: x 0.400 y 0.167 z 0.843 (원래 0.35, 0.10, 0.85)

**설명할 수 있어야 하는 것** — 왜 왼손이 움직였나?
> 한 마디로 설명한다면 Whole-body QP 기반 통합을 해서 최적화했기 때문이다. cyclo는 양팔, 리프트, 머리 등 로봇의 자유도를 분리하지 않고 2차 계획법 즉, 하나의 qp로 목적함수와 제약조건으로 통합하여 최적 관절 속도를 구한다. 이때 목적함수는 태스크 오차와 관절 움직임 비용을 최소화하도록 구성된다.
양팔 간 충돌 회피 제약은 CBF 부등식 제약을 설명하는데, 두 손 사이 거리에 대해 다음과 같은 제어 장벽 함수 기반 안전 부등식 제약이 걸려 있다. 

저녁 MR-3(5.1)과의 연결: `∇d`는 "거리 d를 관절각으로 미분한 것"이라 자코비안과 같은 종류의 양입니다. Pinocchio가 거리와 함께 계산해 줍니다.$$\nabla d(q)^T \dot{q} \ge -\alpha (d(q) - d_{\text{safe}})$$ 여기서 $\nabla d(q)^T \dot{q}$는 시간에 따른 거리의 변화율($\dot{d}$)을 의미한다. 오른손이 왼손이 있던 목표 위치($x=0.35, y=0.10$)로 접근하면서 두 손 사이 거리 $d$가 안전 한계($d_{\text{safe}}$)에 근접하자, 솔버는 두 손이 더 이상 가까워지지 않도록($\dot{d} \ge \dots$) 양팔 관절 전체의 속도 조합을 구속한다.
케이스는 두 가지가 있을 것이다. 오른손이 진입을 멈추거나 왼손이 바깥으로 비켜주는 것인데, QP솔버가 판단하기에 오른손의 목표 추종 오차 패널티와 왼손을 움직이는 비용을 저울질했을 때, 오른손은 목표에 덜 가고 남은 안전 거리는 왼손을 밀어내어 확보하는 것이 전체 비용 관점에서 최적이라고 판단한 것이다.

파라미터(`ai_worker_config.yaml`): `collision_buffer 0.05 m`(이 거리 안에서 제약 시작), `collision_safe_distance 0.02 m`, `cbf_alpha 50`

---

## STEP C5. 도달 불가능한 목표 🎥 (17:05–17:15)

**보여 줄 것**: 손이 닿지 않는 곳을 줘도 QP가 깨지지 않는다. (이유는 Notion 실습 페이지 C5 — 추종은 비용, 감쇠 항, 관절 한계. slack은 보험)

- [ ] **T1**:

```bash
./t1_bridge.sh C5
```

- [ ] **T2**:

```bash
./t2_cyclo.sh
```

- [ ] 🎥 **녹화 시작**
- [ ] **T3**:

```bash
./send.sh c5
```

✔ 오른팔을 앞으로 최대한 뻗고 멈춥니다. 떨거나 튀지 않습니다.

- [ ] 🎥 **녹화 정지** → **T3** `./fk.sh` → **T2 Ctrl+C → T1 Ctrl+C**

✍ **기록**: 목표 x 0.80 → 실제 x 0.602 (미리 돌린 값 0.60)

**설명할 수 있어야 하는 것**
> 일단 원래 목표는 0.80이었는데 0.602에서 멈췄다. 그 이유는 기구학적 한계와 특이점으로 MR 5.3 singularity에 나오는 내용인데, 로봇팔을 전방으로 완전히 뻗은 자세는 최대 도달 한계에 도달하는 상태로 기구학적 특이점이다. 특이점 부근에서는 jacobian rank가 떨어지거나 특이값이 0에 매우 가까워지는데, 일반적인 역기구학(의사역행렬 DLS 등)으로 도달 불가능한 목표를 무리하게 추종하려고 하면, $\dot{q} = J^{\dagger} v$ 연산에서 jacobian inverse matrix 폭증으로 관절 속도가 극단적으로 튀어 비정상적인 발산이 발생한다.
cyclo에서는 $$\min_{\dot{q}, s} \quad \frac{1}{2} \dot{q}^T W \dot{q} + \frac{1}{2} \rho s^T s$$ 이렇게 2차 계획법 QP 최적화로 정식화하여, 목표 추종 등 주요 제약식마다 완충용 슬랙 변수 s를 포함해 문제를 상황에 따라 약간 위반이나 타협이 허용되는 유연한 제약조건으로 만든다. 해당 식은 다음과 같이 동작한다. 평상시는 $s \approx 0$ 으로 솔버가 s=0을 유지하며 목표 속도를 완벽히 추종한다. 목표가 물리적 도달 한계 밖에 있어 제약 조건을 수학적으로 만족할 수 없는 상태가 되면, 솔버는 벌점  $\rho \Vert{}s\Vert{}^2$ 를 감수하면서 s를 조금씩 열어 제약을 완화한다. 이렇게 하면 관절 한계와 특이점 안전 영역을 침범하지 않는 선에서 물리적으로 허용 가능한 최대 한계까지 최선의 도달값을 내며 부드럽게 멈추게 된다. 참고로 일반 DLS나 역기구학만으로는 도달 불가능한 목표 추종 시 특이점에서 역행렬 폭증으로 관절 속도가 튄다. cyclo는 높은 패널티가 걸린 슬랙 변수 덕분에 불가능한 상황에서만 제약을 유연하게 어기며 로봇팔의 안전 확보, 도달 가능한 최대 한계에서 안정적으로 정지한다.

---

## STEP A3. 파일 정리 (19:30–19:40, C1 코드 마무리와 함께)

오후가 밀리면 여기서 바로 저녁으로 넘어갑니다. 이 단계는 저녁 시간표에 넣어 뒀습니다.

- [ ] 영상 이름 바꾸기 (`~/Videos/Screencasts/`) → `C1_기본이동.webm`, `C4_자기충돌.webm`, `C5_도달불가.webm`
- [ ] 영상·캡처를 한 폴더로 모으기:

```bash
mkdir -p ~/cyclo_study/media && cp ~/Videos/Screencasts/*.webm ~/cyclo_study/media/ && cp ~/Pictures/Screenshots/*.png ~/cyclo_study/media/ 2>/dev/null; ls ~/cyclo_study/media
```

- [ ] (시간이 남으면) **C3 보간 없이 이동**: C1과 같은 방법으로 켜고 `./send.sh c3`. MR-1의 s(t) 없이 바로 목표를 향합니다. VR·마커로 실시간 조종할 때 쓰는 방식입니다.

---

## STEP A0. 터미널 3개 준비 (14:00–14:10)

- [ ] 터미널을 3개 엽니다. 이름을 붙이면 편합니다(우클릭 → 제목 설정): **T1 브리지 / T2 Cyclo / T3 명령**
- [ ] 세 터미널 모두에서:

```bash
cd ~/cyclo_study
```

- [ ] 녹화 길이 제한을 풉니다. GNOME 기본값이 30초로 잘릴 수 있습니다. 한 번만 하면 됩니다.

```bash
gsettings set org.gnome.settings-daemon.plugins.media-keys max-screencast-length 0
```

✔ 아무 출력 없이 끝나면 성공입니다.

- [ ] MR PDF를 열어 둡니다. 실험 사이사이에 계속 씁니다.

```bash
xdg-open ~/Downloads/MR.pdf
```

---

## STEP A1. MuJoCo 창이 뜨는지 확인 (14:10–14:20)

이 단계만 Claude가 미리 확인하지 못했습니다(제 쪽에서는 화면에 접근이 안 됨).

- [ ] **T1**:

```bash
./t1_bridge.sh test
```

✔ MuJoCo 창이 뜨고 AI Worker가 바닥에 서 있습니다. T1에 `MuJoCo 브리지 시작: 관절 31개 발행`이 나옵니다.
✔ 마우스: 왼쪽 드래그 = 회전, 오른쪽 드래그 = 이동, 휠 = 확대. **오른팔이 잘 보이는 각도로 맞춰 두세요.** 이 각도로 녹화합니다.

✗ 창이 안 뜨고 에러가 나면 → 에러 전체를 Claude에게 붙여 주세요. 영상은 화면 없이 렌더링하는 방식으로 바꿀 수 있습니다.
✗ `No module named rclpy` → `env.sh`를 거치지 않은 것입니다. 반드시 `./t1_bridge.sh`로 실행하세요.

- [ ] 확인했으면 T1에서 **Ctrl+C**로 끕니다.

---

## STEP A2. 녹화 연습 (14:20–14:30)

- [ ] **PrtSc** 키를 누릅니다 → 화면 아래에 도구가 뜹니다.
- [ ] 오른쪽의 **영상(캠코더) 아이콘**을 눌러 녹화 모드로 바꿉니다.
- [ ] **영역 선택**으로 MuJoCo 창 + T3 터미널이 같이 들어오게 잡습니다.
  명령을 치는 장면과 로봇이 움직이는 장면이 한 화면에 들어오면 발표 때 설명하기 좋습니다.
- [ ] 가운데 동그란 버튼으로 시작 → 5초 뒤 **화면 오른쪽 위 빨간 정지 버튼**으로 멈춥니다.

✔ `~/Videos/Screencasts/`에 `.webm` 파일이 생깁니다. 한 번 재생해 봅니다.

```bash
ls ~/Videos/Screencasts/
```

- [ ] 연습 파일은 지워도 됩니다.

---

## 📖 MR-1. 궤적 생성 — 9.1–9.2 (14:30–14:55, 25분)

**왜 지금**: 바로 다음 C1에서 손이 "2초에 걸쳐 직선으로" 갑니다. 그 2초짜리 움직임을 만드는 식입니다.

| 읽을 곳 | 영문 PDF 쪽 | 읽는 법 |
|---|---|---|
| 9.1 Definitions | 343 | **정독 (5분)**. 경로 θ(s)와 시간 스케일링 s(t)를 나누는 이유 |
| 9.2.1 Straight-Line Paths | 344–346 | 스크루 경로(9.5–9.6)는 훑고, **식 (9.7)–(9.8)을 정독 (10분)** |
| 9.2.2 Time Scaling — 3차 다항식 | 346–347 | **식 (9.9)–(9.11) 정독 (8분)**. 5차는 "가속도까지 0" 한 줄만 |
| 9.2.2의 사다리꼴·S-curve | 348– | 건너뜁니다 |

**식 (9.7)–(9.8)은 Cyclo 코드 그대로입니다.**

```
MR (9.7)  p(s) = p_start + s·(p_end − p_start)
MR (9.8)  R(s) = R_start · exp( log(R_startᵀ R_end) · s )

Cyclo     cubicVector(...)                                     ← 위치
          rotation_0 * ((rotation_0.transpose() * rotation_f).log() * tau).exp()   ← 자세 (type_define.hpp:290)
```

`s`(코드에서는 `tau`)를 3차 다항식으로 만드는 게 9.2.2입니다: s(t) = 3(t/T)² − 2(t/T)³

✍ **노트 (9.1–9.2)**
- ① 정의: 로봇 말단 좌표계 시작 형상에서 목표 형상까지 이동할 때 3차원 위치는 작업 공간의 최단 유클리드 직선으로 이동시키고 회전(자세)은 고정된 단일 회전축에 대해 일정한 각속도로 단조 회전하도록 분리하여 정의한 경로
- ② 식: $p(s) = p_{\text{start}} + s(p_{\text{end}} - p_{\text{start}})$
$R(s) = R_{\text{start}} \exp\left( \log(R_{\text{start}}^T R_{\text{end}}) s \right) \quad (s \in [0, 1])$
- ③ 어디서: C1의 2초 이동, movel 노드 411–420행

✍ **답해 보기**: 위치와 자세를 왜 따로 보간하나? 회전행렬을 성분별로 섞으면 왜 안 되나?
> 먼저 위치와 자세를 따로 보간하는 이유는 SE(3) 전체를 단일 screw motion으로 한 번에 보간하면 말단 원점이 공간상 직선이 아닌 나선이나 원호 궤적을 그리며 휘어지게 된다. 따라서 공구 끝점이 작업 공간상 정확한 3차원 직선을 유지하도록 위치 벡터는 선형 보간으로 처리하고, 자세는 행렬 로그를 취해 회전축과 회전각으로 변환한 뒤 각도만 s만큼 스케일링하여 SO(3) 제약을 완벽히 유지하도록 분리한다.
회전행렬을 성분별로 섞으면 안 되는 이유는 먼저 회전행렬은 직교성과 행렬식이 1이어야 하는 기하학적 제약 조건을 만족해야 강체의 물리적 자세를 표현할 수 있다.두 회전행렬의 성분을 선형 보간하거나 평균을 내면 열벡터들이 단위 길이를 유지하지 못하고 서로 직교하지 않게 되며, SO(3)에 속하지 않아 물리적인 회전 자체로 성립할 수 없다.

---

## STEP C1. 기본 이동 🎥 (14:55–15:20)

**보여 줄 것**: ROBOTIS의 Cyclo 코드를 한 줄도 고치지 않고, 실로봇 대신 MuJoCo 로봇을 움직였다.

- [ ] **T1**:

```bash
./t1_bridge.sh C1
```

- [ ] MuJoCo 창이 뜨고 로봇이 자리를 잡으면(약 3초) **T2**:

```bash
./t2_cyclo.sh
```

✔ T2에 `AI Worker MoveL Controller initialized successfully!`가 나옵니다.
✔ 노란 글씨 `Collision model for the robot may not be perfect!`는 경고일 뿐이니 무시합니다.

- [ ] **T3**에서 연결을 확인합니다.

```bash
source env.sh && ros2 topic hz /joint_states
```

✔ `average rate: 100.0` 근처가 나옵니다. **Ctrl+C**로 멈춥니다.
✗ 아무것도 안 나오면 → T1이 꺼진 것입니다. T1부터 다시 켜세요.

- [ ] 📸 **캡처 1**: T1·T2·T3이 모두 보이는 화면 (세 프로그램이 같이 도는 구성 사진)
- [ ] 🎥 **녹화 시작** (STEP A2 방법)
- [ ] **T3**:

```bash
./send.sh c1
```

✔ T3에 `보냄 /r_goal_move → (0.35, -0.20, 0.85), T=2 s`가 나옵니다.
✔ MuJoCo에서 **오른팔이 2초 동안 앞으로 들립니다.** 방금 읽은 3차 시간 스케일링이라 출발과 도착이 부드럽습니다.

- [ ] 팔이 멈추고 3초 뒤 🎥 **녹화 정지**
- [ ] 📸 **캡처 2**: 도착한 자세
- [ ] **T3**에서 Cyclo가 계산한 손 위치를 확인합니다.

```bash
./fk.sh
```

- [ ] 끄기: **T2 Ctrl+C → T1 Ctrl+C** (T1을 꺼야 `C1.csv`가 저장됩니다)
- [ ] **T3**에서 실제로 도착한 위치(MuJoCo)를 확인합니다.

```bash
./venv_ros/bin/python plot_bridge.py --log C1.csv --target 0.35 -0.20 0.85 --out C1
```

✔ `최종 위치 [...] · 목표와의 거리 ○.○ mm`가 나옵니다. 5–6 mm 근처면 정상입니다(브리지 수정 후). (그래프 `C1_bridge.png`도 같이 생기지만 오늘은 보지 않아도 됩니다.)

✍ **기록**
- Cyclo가 계산한 오른손(`fk.sh`): x 0.350 y -0.200 z 0.850
- MuJoCo 실제 오른손: x 0.3454 y -0.1996 z 0.8467
- 목표와의 거리: 5.6 mm

✗ 팔이 안 움직이면 → T3에서:

```bash
ros2 topic echo --once /leader/joint_trajectory_command_broadcaster_right/joint_trajectory
```

나오면 브리지 문제, 안 나오면 Cyclo 문제입니다. 결과와 T2 로그를 Claude에게 붙여 주세요.

**설명할 수 있어야 하는 것** — 왜 목표와 몇 mm 차이가 나나?
> Eigen::VectorXd q_feedback = q_desired_;
if (lift_joint_index_ >= 0 && lift_joint_index_ < q_feedback.size()) {
  q_feedback[lift_joint_index_] = q_[lift_joint_index_];
}

kinematics_solver_->updateState(q_feedback, qdot_);
right_gripper_pose_ = kinematics_solver_->getPose(r_gripper_name_);

실제 코드 317-324행을 보면 q_ 라는 엔코더 측정 각도가 들어온다. 이걸 그대로 기구학 상태 갱신에 사용하지는 않고 직전 루프 계산된 명령값인 q_desired_를 q_feedback으로 사용한다.(리프트 관절만 예외적으로 센서값 그대로) 즉, 노드가 계산하고 퍼블리시하는 현재 그리퍼 자세인 right_gripper_pose_는 실제 로봇팔 물리적 위치가 아니라 이상적인 기구학 명령값 누적 위치이다.

cyclo_motion_controller::common::Vector6d AIWorkerMoveLController::computeDesiredVelocity(...)
{
  ...
  const Eigen::Vector3d position_error = goal_pose.translation() - current_pose.translation();
  const Eigen::Matrix3d rotation_error = goal_pose.linear() * current_pose.linear().transpose();
  ...
  desired_vel.head<3>() = feedforward_linear + kp_position_ * position_error;
  desired_vel.tail<3>() = feedforward_angular + kp_orientation_ * orientation_error;
  return desired_vel;
}

254-268행과 349행을 보면 이동 중이나 이동 완료 후 목표치와의 편차를 줄이기 위해 피드백을 kp_position*position_error로 계산한다. 여기서 current_pose로 들어가는 값이 right_gripper_pose_이다. 결과적으로 q_desired_가 목표 지점 관절각에 도달하면 current_pose==goal_pose가 되어 position_error=0이 된다.

Eigen::VectorXd optimal_velocities;
if (!qp_controller_->getOptJointVel(optimal_velocities)) { ... }

q_desired_ = q_feedback + optimal_velocities * time_step_;
publishTrajectory(q_desired_);
377-383행은 QP 솔버 최적화 및 적분 부분이다.QP 솔버가 계산한 최적 관절 속도 optimal_velocities를 이전 명령값 q_feedback에 시간 적분하여 새로운 목표 관절각 q_desired_를 생성해 모터 컨트롤러에 지령으로 넣는다.여기서도 목표 도달하면 optimal_velocities=0이 되어 q_desired_는 정기구학 목표(이 경우 [0.350, -0.200, 0.850]에 수렴하여 고정)

그래서 실제 시뮬레이션에서 8.9mm 오차가 발생하는 이유는 뭘까?
첫번째는 상위 루프인 cyclo 노드에서 로봇팔이 물리적인 중력을 받아 밑으로 처지는 것을 q_ 센서 피드백을 사용해 루프에 반영하지 않고 feedforward로 처리한다. fk.sh 상에서는 목표치에 정확히 도착한 것처럼 판정되는 것이다.
두번째는 하위 루프인 Mujoco/모터 액추에이터의 중력 처짐이다. cyclo가 내보낸 관절각은 mujoco, 실제라면 dynamixel 모터 pid 제어기로 전달될텐데 지령각과 실제 측정각 차이에 비례하는 복원 토크를 낸다. 하지만 로봇팔 링크 질량 때문에 중력 토크가 작용한다. 이 중력을 버티고 정지해 있으려면 모터가 중력과 크기가 같고 방향이 반대인 토크가 출력되어야 하는데 편차가 발생한다. Steady-state error라고도 부르는 평형상태에서 발생하는 정상상태 오차이다.
실제 데이터와의 일치성을 확인해보면 수직 하강 방향으로 -7.6mm, x방향 -4.6mm, y방향 +0.4mm로 팔이 아래로 처지며 링크가 약간 뒤로 당겨지는 상황이 연출됐다고 보면 된다. 즉, 중력에 의한 처짐 현상과 정확히 일치한다.

> ⚠️ **[정정 10/5 16:45 — Notion 옮길 때 반영]**
> - 분석 내용(382행 명령값 적분 → Cyclo는 처짐을 모름 → 하위 위치제어의 정상상태 오차)은 **그대로 맞습니다.**
> - 숫자만 바꿉니다. 8.9 mm는 브리지 버그 때문이었고, 수정 후 C1 = **5.6 mm** (x −4.6, y +0.4, **z −3.3 mm**). 재측정 값으로 교체하세요.
> - 줄 번호: 317–324 → **382–388**, 254–268·349 → **404–434, 343–361**, 377–383 → **491–500**
> - "feedforward로 처리한다" → "처짐을 루프에 반영하지 않는다(모르는 채 명령만 낸다)"

---


---

# 막혔을 때

| 증상 | 해결 |
|---|---|
| MuJoCo 창이 안 뜸 | 에러를 Claude에게 붙여 주세요. 화면 없이 렌더링하는 방식으로 바꿀 수 있습니다 |
| T2가 `initialized` 뒤 조용함 | 정상입니다. 명령을 기다리는 중입니다 |
| T2에 `Joint states timed out` | T1이 꺼졌습니다. T1을 다시 켜면 자동으로 복구됩니다 |
| `./send.sh`가 안 끝남 | T2(Cyclo)가 안 켜져 있습니다. 명령을 받을 쪽이 생길 때까지 기다리는 중입니다 |
| 팔이 안 움직임 | STEP C1의 ✗ 확인 명령 |
| 로봇이 넘어지거나 흔들림 | T2 → T1 순서로 끄고 다시 켭니다. 베이스가 바퀴로 서 있어서 큰 동작에서 흔들릴 수 있습니다 |
| 녹화가 30초에서 끊김 | STEP A0의 `gsettings` 명령 |
| MR 쪽수가 안 맞음 | 이 PDF는 인쇄 쪽수 + 18 = PDF 쪽수입니다. PDF 뷰어의 쪽 번호 입력란에 PDF 쪽수를 넣으세요 |
| 그래도 안 됨 | 그 실험은 `verified/`에 미리 돌린 로그가 있으니 숫자는 그걸로 쓰고 넘어갑니다. 막힌 지점을 정확히 적어 두는 것도 보고 내용입니다 |
