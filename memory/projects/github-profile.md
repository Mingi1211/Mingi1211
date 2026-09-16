# github-profile — 프로필 README 구축과 레포 정비

`Mingi1211/Mingi1211` (public) · 작업일 2026-09-02 · 출처: **Claude 대화 세션 (로컬 Windows 데스크톱 앱)**

> 이 레포가 기억 저장소가 되기 전, **프로필 README를 처음 만든 세션**의 기록이다.
> 이후 세션들이 "README에서 읽은 프로필"이라고 부르는 내용의 출처가 이 작업이다.

## 무엇을 했나

| 항목 | 결과 |
|---|---|
| 프로필 README | 새로 작성 → 사용자가 `Mingi1211/Mingi1211` 레포를 만들어 push (커밋 `6bca846`~`5a07555`) |
| 레포 리네임 | `PhysicalAI_Assignment_2024405002` → **`openvla-raccoonbot`** (Claude 제안, 사용자가 GitHub 웹에서 실행) |
| `sensor-logger` README | 비어 있던 README를 작성 → 사용자 push (`ae641e0`) |
| 이후 사용자 수정 | README에서 **stats 섹션 삭제** (`7a91282`, 사용자 본인 커밋) |

**README 구성 (사용자 선택으로 확정)**
- 언어: **영문 중심**
- 포지셔닝: 휴머노이드 **WBC** + Physical AI + 로봇 제어. **매니퓰레이션은 목표가 아니라 경유지**로 서술
- 프로젝트 카드: **OpenVLA × RaccoonBot 하나만** 깊게 (before/after 수치 표). `dreamlab-bootcamp`·`sensor-logger`는 카드에서 제외
- `05` 섹션: 처음엔 Claude가 추측으로 채운 `now` 체크리스트였음 → 사용자 확인 결과 **VLA 실기 구동(완료)만 사실**
  → `05 · what's next` 로 바꾸고, 방향은 사용자가 직접 말한 "휴머노이드 전신 동작"으로만 서술
- 톤: 네이비→시안 그라데이션(`#0D1B2A`→`#1B98E0`), 헤딩 `## ▍0N · 소문자`

## 왜 그렇게 했나

- 레퍼런스(`ohseohyune` 프로필)는 **구성만 참고하고 똑같이 하지 말 것** — 사용자 요구
- 레포가 3개뿐이라 프로젝트 나열보다 **대표 프로젝트 하나를 수치로 깊게** 보여주는 쪽이 강하다고 판단
- 레포 이름 `PhysicalAI_Assignment_<학번>`은 과제 제출용이라 대외 공개용으로 약함. GitHub이 리다이렉트를 걸어주므로 리네임 비용이 낮음
- `sensor-logger` README가 0바이트라 프로필에서 들어갔을 때 손해

## 막힌 것 / 주의

- **로컬 PC에 `gh` CLI 없음** → 당시 Claude는 push 불가, 사용자가 직접 push함
- 리네임 **전에** README 링크를 먼저 새 이름으로 바꿔두면 리네임 전까지 404 → 순서 안내가 필요했음
- `sensor-logger`를 클론한 뒤 `core.autocrlf false`를 걸었더니 **전 파일이 modified로 표시**됨
  (CRLF로 체크아웃된 상태에서 설정만 바꾼 탓). 설정 unset으로 복구, 내용 손상 없음
- ⚠️ `sensor-logger` README의 **"Built as a packaging exercise"는 Claude가 코드(Dockerfile + uv)를 보고 추론해 쓴 문장**이다.
  사용자가 목적을 직접 말한 적은 없다 → LEDGER에 `[정정]` 기록함

## 다음 액션

1. **[사용자가 답할 것]** ROS2 · C · MATLAB · STM32 사용 여부 — 근거가 없어 tech stack에서 뺐다. 쓴다면 배지 추가
2. **[사용자가 답할 것]** 프로필에 연락처(이메일 등) 공개 여부 — 전체 공개 페이지라 임의로 안 넣었다
