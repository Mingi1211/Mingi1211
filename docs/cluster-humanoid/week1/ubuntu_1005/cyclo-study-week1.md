---
name: cyclo-study-week1
description: "민기's Cyclo/MR study week of 2026-10-05 — where the guide, notes, and pending tasks live"
metadata:
  node_type: memory
  type: project
  originSessionId: 69dbe073-4cb2-47c2-b856-71f6987256f0
  modified: 2026-10-05T07:27:55.136Z
---

2026-10-05(월)~10-08(목) Cyclo 실습 + Modern Robotics 공부. 화(10/6) 현대 미팅, 목(10/8) 정기 미팅.
- 작업 폴더 `~/cyclo_study`, 따라가기 가이드 `~/cyclo_study/GUIDE.md` (사용자가 C1 구간 등에 본인 필기를 붙여 넣음 — 덮어쓰지 말 것)
- Cyclo는 `~/ros2_ws` (매뉴얼의 `~/cyclo_ws` 아님). 실험 스크립트 t1_bridge.sh / t2_cyclo.sh / send.sh / fk.sh
- `cyclo_mujoco_bridge.py` 관절 0개 버그(mujoco 3.14 enum 비교) 10/5 16:40 수정. 수정 전 측정값(C1 8.9, C2 4.4 mm, 16:35 C4 영상)은 무효 → 수정 후 C1 5.6, C2 0.0 mm. 사용자 필기에 정정 메모(⚠️ [정정 …])를 달아 둠 — Notion 옮길 때 반영. C1 기록은 사용자가 직접 재측정값(z 0.8467, 5.6 mm)으로 덮어씀(10/5 17:00경) → Notion에는 C1 = 5.6 mm, C2 = 0.0 mm(사용자 재측정 10/5 확인)만 쓰고 수정 전 값(8.9/4.4)은 넣지 않음. 버그·재측정 경위는 한 줄 정도로만. 사용자 C2 노트의 '남은 4.4 mm 오차' 문단은 Claude 정정 메모대로 '시뮬레이션에선 0 mm(처짐 소멸), 마찰·탄성·이산화 잔여오차는 실기에서 생길 것'으로 바꿔 반영
- 사용자가 가진 MR은 한글판(쪽수 다름, 9.2.1 = 461쪽). `~/Downloads/MR.pdf`는 영문 2017 프리프린트(인쇄쪽+18=PDF쪽). 한글판 목차 받으면 쪽수 매핑 예정
- Notion '실습' 페이지(DreamLab 학부연구생/김민기 진행상황/실습, app.notion.com/p/3f059c1c337e80ceada0c94688c8241a)에 10/5 C1·C2·C4·C5 정리 완료(10/5 17:40, Chrome에서 마크다운 paste 이벤트 + 파일 입력 가로채기로 업로드). 형제 페이지 'MR 개념'이 사용자 필기 형식 기준. 정정 메모 내용은 반영 완료
- 남은 요청 예정: ① 남은 필기(MR-2 이후, 코드 단계)를 Notion으로 옮기기 ([[notion-note-editing-style]]) ② 수요일 `~/cyclo_study/handoff_thu` 정리본으로 목요일 발표자료 제작

**Why:** 세션이 끊겨도 이어서 작업하기 위해.
**How to apply:** 이 주 작업 요청이 오면 GUIDE.md와 이 메모부터 확인.
