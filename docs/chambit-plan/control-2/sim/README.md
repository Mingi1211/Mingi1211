# 2번 하위 제어 — Gazebo 시뮬 세팅 (Ubuntu에서 실행)

Windows Claude가 2026-10-27에 작성. **아직 한 번도 실행해 보지 않은 코드**다 — Ubuntu에서 첫 실행 때 오류를 고쳐 가며 쓴다.
일정은 Notion "주간 일정" 캘린더가 정본. 배경은 `../HANDOFF_ubuntu_1026.md`.

## 파일

| 파일 | 역할 |
|---|---|
| `setup_sim.py` | ai_worker 설정 패치: 팔 14축에 effort 인터페이스(use_sim일 때만), effort 컨트롤러 2개 + 그리퍼 위치 컨트롤러 2개 추가. 원본 `.orig` 백업, `--restore`로 복구 |
| `impedance_node.py` | 토크 제어 노드 (Pinocchio). 모드 `spring` / `gravity` / `task`(6D 작업공간 임피던스 + null-space + Λ 감쇠 + 5차 궤적 + 리더/팔로워 + Cyclo 입력) |
| `params.yaml` | 게인·모드·프레임 (Gazebo 시작용 추정치) |
| `tools.sh` | `effort_on/off`, `goal`, `imp_run`, `imp_mode` 단축 명령 |
| `list_frames.py` | 팔 관절·프레임·질량 확인 (ee_frame 이름 검증) |
| `plot_log.py` | 노드가 남긴 CSV(`~/impedance_logs/`) → 그래프 |

## 0. 한 번만

```bash
pip install pin   # 또는 sudo apt install ros-jazzy-pinocchio  (python3 -c "import pinocchio" 로 확인)
sudo apt install -y ros-jazzy-ros-gz ros-jazzy-gz-ros2-control ros-jazzy-ros2-controllers python3-vcstool
# ai_worker 빌드는 ../HANDOFF_ubuntu_1026.md "오늘 시작 명령" 참고
python3 setup_sim.py --ws ~/ros2_ws/src/ai_worker
cd ~/ros2_ws && colcon build --symlink-install --packages-select ffw_description ffw_bringup && source install/setup.bash
```

## 1. 매번 실행 (터미널 3개, 모두 `source ~/ros2_ws/install/setup.bash`)

```bash
# T1
ros2 launch ffw_bringup ffw_sg2_follower_ai_gazebo.launch.py
# T2  (팔이 위치 제어로 서 있는 상태에서 노드 먼저)
source tools.sh && imp_run
# T3
source tools.sh
python3 list_frames.py          # 처음 한 번: end_effector_r_link 있는지, 질량 확인
effort_on r                     # 오른팔 위치 → effort 전환 (이때부터 노드 토크가 팔을 잡음)
effort_off r                    # 문제 생기면 즉시 원래 위치 제어로
```

## 2. 캘린더 단계별

| 날짜 | 할 일 | 명령 |
|---|---|---|
| 10/28(수) 관절 1개 스프링 | `params.yaml` mode: spring, spring_joint: 4 | `imp_mode spring` → GUI에서 팔꿈치에 힘 주면 밀렸다 돌아옴 |
| 10/30(금) 한 팔 중력 보상 | mode: gravity, Kq를 0에 가깝게 | 팔이 그 자리에 떠 있으면 성공. 처지면 g(q) 부호·관절 순서 확인 |
| 11/3(화) 작업공간 임피던스 | mode: task | `goal r 0.35 -0.20 0.85 3` → 손이 5차 궤적으로 이동 |
| 11/4(수) null-space·Λ | `K_null`, `armature_wrist`, `zeta` 바꿔 비교 | 팔꿈치 흘러내림 유무, 감쇠 그래프 |
| 11/5(목) 양팔 리더-팔로워 | sides: [r, l], preset_r leader / preset_l follower | `effort_on both` |
| 11/3·11/8 Cyclo 연결 | source: cyclo (Cyclo 실행 + `arm_*_controller` 비활성 상태) | Cyclo MoveL 목표 → FK → x_d |

그래프: `python3 plot_log.py ~/impedance_logs/<파일>.csv`

## 3. 처음에 막힐 가능성이 큰 곳 (확인 순서)

1. `forward_command_controller`가 effort 인터페이스를 못 잡음 → `ros2 control list_hardware_interfaces`에서 `arm_r_joint1/effort`가 보이는지. 안 보이면 xacro 패치(`MINGI_EFFORT`)가 빌드에 반영됐는지
2. gz_ros2_control이 위치↔effort 전환을 거부 → 전환 대신 처음부터 effort만 쓰도록 `arm_r_controller` 스포너를 launch에서 빼는 방법
3. 노드에서 `프레임 ... 없음` → `list_frames.py` 결과로 `ee_frame_r` 수정
4. 팔이 바로 떨어짐 → 노드가 먼저 떠 있고 `/joint_states`를 받는지, 토크 부호, `tau_max`가 너무 작은지
5. 진동 → `zeta`↑, `K_*`↓, `rate` 100 Hz 유지

## 4. 실물로 옮길 때 (아직 안 함)

- xacro의 effort 인터페이스는 **use_sim일 때만** 들어가게 했다 → 실물 bringup은 영향 없음
- 실물은 팔 gpio의 `Goal Position → Goal Current`, `Operating Mode 3 → 0`이 추가로 필요 (허락 받은 뒤, 관절 1개부터)
- `params.yaml`의 토크 한계·게인은 실물에서 낮게 시작. 명령 끊김 시 팔이 떨어지므로 받침·E-Stop 필수
