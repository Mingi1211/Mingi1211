# HANDOFF — Ubuntu → Windows (2026-10-05 18:00)

Ubuntu Claude Code 세션(10/5 12:00–18:00)에서 Cyclo 실습과 Notion 실습 페이지 정리까지 끝냈다.
**지금부터 Windows에서 MR 개념 공부 → Notion 정리, Cyclo 코드 공부를 이어서 한다.** 실습(ROS·MuJoCo 실행)은 더 하지 않는다.

## Windows Claude가 먼저 할 것

1. 이 파일 → `claude_memory/` 두 파일 → `cyclo_study/GUIDE.md` 순서로 읽는다.
2. 사용자 정보: 호칭 "민기님", 한국어, 결론 먼저. 10/6(화) 오전 현대 미팅, 10/8(목) 정기 미팅.
3. GUIDE.md의 Ubuntu 경로는 아래처럼 바꿔 읽는다.

| GUIDE.md에 적힌 경로 (Ubuntu) | 이 묶음에서 |
|---|---|
| `~/ros2_ws/src/cyclo_control/` | `cyclo_control_src/` |
| `~/cyclo_study/` | `cyclo_study/` |
| `~/cyclo_study/ai_worker/ffw_description/mujoco/ffw_sg2/ffw_sg2.xml` | `cyclo_study/ffw_sg2.xml` |
| `~/Downloads/MR.pdf` | Google Drive의 `MR.pdf` (같이 올려 둠) |

`code -g 파일:줄` 같은 명령은 Windows에서도 VS Code가 설치돼 있으면 그대로 쓸 수 있다(경로만 바꿔서).

## 지금까지 한 것 (10/5, Ubuntu)

- Cyclo(cyclo_control `8d982a0`, 수정 없음) + MuJoCo AI Worker2(FFW-SG2) 브리지로 실습 C1·C2·C4·C5 완료
  - C1 기본 이동: Cyclo 계산은 목표에 정확히 도착, MuJoCo 실제 손은 **5.6 mm** 처짐 (x −4.6, y +0.4, z −3.3 mm)
  - C2 중력 보상(`--gravcomp`): **0.0 mm**
  - C4 자기충돌: 오른손 목표 약 9 cm 앞에서 정지, 명령 없는 왼손이 약 8 cm 비켜남 (fk: R (0.298, 0.031, 0.858), L (0.400, 0.167, 0.843))
  - C5 도달 불가(x 0.80): x 0.602, z 0.926에서 발산 없이 정지
- 영상 C1·C4·C5, 그래프 C1·C2 → Notion "실습" 페이지에 업로드 완료
- Notion "실습" 페이지 작성 완료: https://app.notion.com/p/3f059c1c337e80ceada0c94688c8241a
  (DreamLab 학부연구생 / 김민기 진행상황 / 실습). **사용자가 직접 일부 고쳤고, C4·C5 설명은 본인 말로 고쳐 쓰는 중 → 덮어쓰지 말 것**
- 형식 기준 페이지 "MR 개념": https://app.notion.com/p/MR-3f059c1c337e803b92a9d2303117cba3 (9.2까지 사용자가 작성)

## 남은 일 (자세한 단계는 GUIDE.md "시간표 한눈에")

| 언제 | 할 일 |
|---|---|
| 월 20:00–24:00 | 현대 미팅 포인트 메모 → MR-2 → 🔍 C1 코드 → 🔍 C2 코드 + MR-5 → MR-3 → 🔍 C4 코드 → MR-4(넘겨도 됨) |
| 화 오전 | 현대 미팅: Notion 실습 페이지 + 영상(C4 → C1 → C5), 포인트 3개는 GUIDE.md STEP E1 |
| 화 저녁 2–3h | 밀린 것 → MR-6 요약표 + 코드 흐름 표 → 현대 피드백 → 필기를 Notion "MR 개념"(또는 사용자가 정한 페이지)에 정리 |
| 수 2–3h | 태블릿 정리(그림 3장, 예상 질문 6개) → PDF → Claude가 목요일 발표자료 제작 (매뉴얼 PART F 8장 구성) |

## 코드에서 확인한 사실 (발표·필기에서 틀리기 쉬운 것)

모두 `cyclo_control_src/` 기준 줄 번호.

| 사실 | 근거 |
|---|---|
| 팔은 측정값이 아니라 **직전 명령값**으로 적분. 측정값은 리프트만 | `ai_worker_movel_controller_node.cpp` 382–388, 499 |
| MoveL 명령이 올 때만 오른팔 상태를 측정값으로 맞춤 | 같은 파일 295 |
| 손끝 목표 속도 $v_d = v_{ff} + K_p e$, 자세 오차 = axis-angle of $R_{goal}R^T$ = MR 식 (11.18) | 같은 파일 343–361 |
| 궤적: 위치 3차 보간, 자세 $R_0\exp(\log(R_0^TR_f)\,s)$ = MR 식 (9.7)–(9.8) | 같은 파일 404–434, `type_define.hpp` 126, 290 |
| QP 비용: $\sum\lVert J_i\dot q - v_{d,i}\rVert^2_W + \dot q^TW_d\dot q + \rho\mathbf 1^Ts$ (slack 벌점은 **일차식**) | `vr_controller.cpp` 113–148 |
| 제약: 속도 한계(bound), 관절 한계 CBF, 자기충돌 CBF($d\le0.05$일 때) | 같은 파일 150, 168–216 |
| **특이점 제약은 자리만 있고 미구현** → 특이점 대응은 감쇠 항뿐 | 같은 파일 생성자(슬롯 할당) vs `setIneqConstraint` |
| 자코비안은 `LOCAL_WORLD_ALIGNED` (space·body 둘 다 아님) | `kinematics_solver.cpp` 190 |
| 충돌 거리 기울기 $\nabla d^T = n^T(J_B - J_A)$ → 양팔 관절 모두 포함 | 같은 파일 329–332 |
| 목표 추종은 **제약이 아니라 비용** → 도달 불가여도 QP 해 존재 (C5) | `vr_controller.cpp` setCost |
| 감쇠 최소자승(DLS)은 MR 본문에 없음. MR 6.3은 의사역행렬·가중 의사역행렬까지 | MR 6.3 |
| C2의 0.0 mm ↔ MR 11.4.2.2 식 (11.38) PD+중력 보상, (11.39) 이후 오차→0 | MR PDF 450 |

## MR 교재

- 사용자는 **한글판**을 갖고 있다. 쪽수가 영문과 다름(예: 9.2.1 직선 경로 = 한글판 461쪽). 절·식 번호는 같다.
- 영문 `MR.pdf`(2017-05 프리프린트, modernrobotics.org 공개본)는 **인쇄 쪽수 + 18 = PDF 쪽수**. GUIDE.md의 "영문 PDF 쪽"은 이 기준.
- 한글판 목차 사진을 받으면 GUIDE.md "MR 읽기 지도"의 "한글판 쪽" 칸을 채우기로 했다.

## Notion 작업 방법 (Claude용 메모)

- Notion 커넥터가 연결돼 있으면 그걸 쓴다. 없으면 Claude in Chrome으로 한다(Ubuntu에서는 이 방법으로 성공).
  - 쓸 위치의 빈 블록을 클릭 → `javascript_tool`로 `new ClipboardEvent('paste', {clipboardData: dt})`(dt에 `text/plain` 마크다운) 디스패치 → 제목·표·코드 블록·목록·인라인 `$…$`·블록 `$$…$$` 수식이 그대로 변환된다. 마크다운은 `String.raw` 템플릿에 넣고 백틱은 `§`로 썼다가 `replaceAll`.
  - 영상·이미지: `/동영상`, `/이미지` 블록 → `HTMLInputElement.prototype.click`을 가로채 Notion이 만드는 file input을 DOM에 붙잡아 두고 → `file_upload`(이 세션이 읽을 수 있는 경로의 파일만, 한 번에 10 MB 이하). 끝나면 원래 `click` 복원.
  - 블록 삭제: 블록 핸들 클릭 → Esc → Delete.
- 쓰는 방식: `claude_memory/notion-note-editing-style.md` — 사용자 문장을 살리고 **틀린 것만 첨삭**, 짧고 명료하게, 장황한 AI식 설명 금지. 형식은 "MR 개념" 페이지를 따른다.
- 사용자가 직접 고치겠다고 한 부분(실습 페이지 C4·C5 설명)은 건드리지 않는다.

## 이 묶음의 파일

| 경로 | 내용 |
|---|---|
| `cyclo_study/GUIDE.md` | 따라가기 가이드(남은 일정 포함). 부록에 사용자 실습 필기 원본과 ⚠️ 정정 메모 |
| `cyclo_study/HANDOFF_windows_to_ubuntu_1005.md` | 이전(Windows→Ubuntu) 핸드오프 |
| `cyclo_study/1주차 정기미팅_cyclo 공부 매뉴얼.docx`, `manual.txt` | 원본 매뉴얼(정정 사항은 GUIDE.md "매뉴얼에서 틀린 곳" 참고) |
| `cyclo_study/cyclo_mujoco_bridge.py` | **수정본** 브리지(관절 0개 버그 수정, 34행 근처) |
| `cyclo_study/*.csv`, `C1_bridge.png`, `C2_bridge.png` | 실습 로그와 그래프 |
| `cyclo_study/ffw_sg2.xml` | MuJoCo 모델(C2 코드 공부: 24–25, 438행) |
| `cyclo_study/*.sh`, `plot_bridge.py` 등 | Ubuntu 실행 스크립트(참고용, Windows에서는 실행 안 함) |
| `cyclo_control_src/` | cyclo_control `8d982a0` 소스(메시·서드파티 제외). GUIDE.md 줄 번호와 일치 |
| `claude_memory/` | Ubuntu Claude가 남긴 메모 2개 |
