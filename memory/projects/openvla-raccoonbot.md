# openvla-raccoonbot — 피지컬AI 텀프로젝트

`Mingi1211/openvla-raccoonbot` (public) · 최종 커밋 2026-05-31 `9228384 REPORT`
문서: 레포 루트 `README.md`(290줄, 상세) · `report.md`(제출용 보고서)

## 무엇을 했나

수업 제공 RaccoonBot OpenVLA 예제를 받아 **데이터셋과 client 코드를 직접 고쳐** 동작 범위를 넓힌 프로젝트.
파이프라인 전체를 한 번 관통시켰다: MuJoCo demonstration 생성 → RLDS/TFDS 변환 → LoRA 테스트 →
OpenVLA server/client 연결 → 실기 실행.

**핵심 문제**: OpenVLA는 7-D 액션 `[dx,dy,dz,droll,dpitch,dyaw,gripper]`을 내는데 RaccoonBot은 사실상 4-DoF.
baseline client에서는 gripper command가 계속 0 근처라 **목표에 도달해도 물체를 잡지 못했다.**

**해결**: 액션을 그대로 실행하지 않고 **단계 머신으로 재매핑**.
`approach → descend → close → lift` (grasp/lift), `approach → descend → push` (push).
추가로 `--request_every_n_steps` 로 추론 호출을 스케줄링.

## 한 일

- 데이터셋 확장 — episode 20개(train 18 / val 2), task `grasp` 7 + `push` 13, 색상 4종 각 5개, **고유 instruction 14개**
- 오브젝트 형상 추가 — `Raccoon_multishape_objects.xml` (red=cylinder, blue=cube, green=sphere, yellow=cylinder)
- RLDS → TFDS 재빌드, **100 step short LoRA** 테스트 (파이프라인 검증 목적)
- 전 스텝 계측 → CSV (raw vs assisted action, latency, motion time, gripper cmd, lift 거리)

## 결과

| 항목 | baseline | 개선 후 |
|---|---|---|
| cylinder grasp-and-lift (MuJoCo) | 실패 (gripper 안 닫힘) | red **0.0162 m** / blue **0.0159 m** |
| 28-step episode 당 서버 요청 | 28 | **10** (ratio 0.357) |
| 평균 스텝 시간 | 811.7 ms | **581.2 ms** |
| 실기 RaccoonBot grasp-lift | — | **0.0122 m** (`gripper_cmd=1.0` 확인) |

미학습 오브젝트/태스크 일반화: `blue cube lift` 0.0120 m ✅ · `green sphere push` 0.0104 m ✅ ·
`red cylinder push` 0.0090 m · **`green sphere lift`는 떨어져서 실패 처리**

## 한계 (본인이 보고서에 명시한 것)

- 실기 실험은 **fixed-layout** — 카메라로 임의 위치 물체를 찾는 방식이 아님 (target 대략 x=0, y=17 cm 고정)
- LoRA는 **100 step short test만** — 학습에 따른 성능 향상을 확인한 것이 아니다
- sphere lift 실패에서 **물체 형상에 따라 gripper 접촉·pitch 제어가 중요**함을 확인
- 후속 아이디어: 형상 다양한 demonstration 확대, 관절 범위 내 작은 pitch offset으로 미끄러운 물체 grasp 안정성 비교

## 레포 구조 메모

- `client_improvements/` — 개선 코드 + `evidence/` (CSV·로그·mp4·png 실험 증거)
- `openvla/`, `dlimp_openvla/` — 업스트림 코드 벤더링
- README가 참조하는 `Mujoco/` 경로 일부는 이 레포에 없다 (별도 환경에 있었던 듯)

## 설명 자료 PDF (2026-09-02 · Claude 대화 세션)

"누가 뭘 했고 뭐가 나아졌냐고 물으면" 답할 용도로 만든 **A4 4쪽 한국어 PDF**.
로컬 `Documents/RaccoonBot_OpenVLA_설명자료.pdf` — **이 레포에는 없다.** reportlab 생성 스크립트는 세션 스크래치패드에만 있었다(영구 보존 아님).

| 쪽 | 내용 |
|---|---|
| 1 | 한 줄 요약 · 문제(7D vs 4DOF) · 한 일 ①데이터셋 ②TFDS/LoRA ③단계 매핑 |
| 2 | ④계측 · before/after 표 · **pitch를 안 따라간 이유**(`th4 = -(th2+th3) - 90°` 고정)와 sphere lift 실패 분석 |
| 3 | 한계 4가지 · **예상 질문과 답 6개** |
| 4 | 말하기 대본 — 30초 버전 원문 · 3분 버전 순서표 |

**프레이밍 결정**
- 핵심 주장을 "학습"이 아니라 **"모델 출력과 하드웨어 사이 간극을 메운 실행 계층"** 에 둠 — LoRA 100 step으로 학습 성과를 주장하면 첫 질문에 무너진다
- **한계를 먼저 말하도록** 예상 질문 앞에 배치
- 가장 날카로운 질문 "결국 사람이 짠 규칙이 움직인 것 아닌가"에 대한 답: 절반 인정 + 증명한 것(VLA 출력을 실행 가능한 형태로 변환)과 증명하지 않은 것(자율 인식)의 경계를 직접 긋기
- 마지막 답("다음에 뭘 할 건가")은 **whole-body 제어로 확장**으로 연결 — 프로필 README `what's next` 와 같은 방향

**원본 README에서 이 PDF를 만들며 새로 확인한 사실** (앞 절에 없던 것)
- `droll/dpitch/dyaw` 는 직접 추종하지 않는다. 실기 IK에서 4번 관절을 위 식으로 계산해 gripper가 **항상 아래를 향하도록 고정** — 가변 pitch는 4번 관절 범위·충돌 검증이 필요해 보류
- sphere lift 실패의 최대 lift 값은 **약 0.0022 m**. 원인 분석: 곡면 접촉점이 좁음 + 접근 위치 오차 + 고정 pitch

**열린 것**
- **[사용자가 답할 것]** PDF 2쪽(§04 pitch·sphere 분석)을 Claude가 요약하며 뉘앙스를 바꾼 곳이 없는지 확인 요청 → 답 없음
- **[사용자가 답할 것]** 같은 내용으로 발표 슬라이드가 필요한지 → 답 없음
