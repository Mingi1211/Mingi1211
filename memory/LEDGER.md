# LEDGER — 사실·결정 로그

> **덧붙이기만 한다(append-only).** 기존 줄을 고치지 않는다.
> 사실이 바뀌면 새 줄에 `[정정]`으로 기록한다. 그래야 "언제 뭘 알았는지"가 남는다.
> 형식: `날짜 | 분류 | 내용 | 근거`

## 환경 (Claude Code 원격 세션)

| 날짜 | 분류 | 내용 | 근거 |
|---|---|---|---|
| 2026-09-15 | 환경 | **`kw.ac.kr` 전 도메인 egress 차단** — WebFetch 불가(EGRESS_BLOCKED). 광운대 정보는 WebSearch 스니펫으로만 수집 가능 | 직접 시도, ee/kupis/startup 모두 차단 |
| 2026-09-15 | 환경 | **LibreOffice(soffice)가 pptx를 못 연다** — 최소 pptx에서도 "source file could not be loaded". pptx 시각 QA에 못 씀 | 최소 파일로 재현 확인 |
| 2026-09-15 | 환경 | 한글 폰트 없음 → `apt-get install -y fonts-noto-cjk` 필요 | fc-list 확인 |
| 2026-09-15 | 환경 | `pptxgenjs`·`python-pptx`·`poppler-utils` 미설치. playwright는 `/opt/node22/lib/node_modules/playwright`에 전역 존재 | npm ls -g |
| 2026-09-15 | 환경 | `apt-get install poppler-utils`는 `apt-get update` 선행 필요(404) | 재현 |
| 2026-09-16 | 환경 | 사용자 PC는 **Windows / Ubuntu 24.04 듀얼부팅**. 평소 켜는 쪽은 Windows. `~/.claude`는 OS별로 따로라 **부팅 OS마다 sync 필요** | 사용자 진술 |
| 2026-09-16 | 환경 | Git Bash(MSYS)의 `pwd`는 `/c/Users/...` 를 준다. 윈도우 네이티브 Claude Code가 못 읽을 수 있어 `cygpath -m`으로 `C:/Users/...` 로 변환해 기록하도록 수정함 | sync-memory.sh |
| 2026-09-16 | 환경 | **사용자 로컬 PC는 Windows** — `bash` 없음. 로컬용 스크립트는 PowerShell(.ps1) 또는 Git Bash로 줄 것. README의 Ubuntu 24.04는 **원격 연구 환경**이지 로컬이 아니다 | 사용자 진술 |
| 2026-09-14 | 환경 | 로컬 Windows에 **한컴오피스 2024(Hwp.exe·COM 등록)** 설치돼 있으나 자동화 보안모듈(FilePathCheckerModule) 미등록 → COM으로 파일 열면 확인창에서 막힘. HWP는 바이너리 직접 편집으로 처리 (`docs/chambit-plan/`) | 레지스트리·Bin 폴더 확인 |
| 2026-09-14 | 환경 | 로컬 Python(Anaconda 3.13)에 `olefile`·`pyhwp`·`pywin32` 있음. `hwp5proc xml`은 원본 서식에서도 실패(pyhwp 버그), `hwp5proc models`는 동작 | 직접 실행 |
| 2026-09-14 | 환경 | 로컬 `gh` CLI 없음 → GitHub API는 curl로. **Taobao 페이지 WebFetch 불가.** 로컬 Read 도구는 PDF 렌더 불가(pdftoppm 없음) → `pypdf`로 텍스트 추출 | 직접 시도 |

## 광운대 사실 (조사 결과 캐시 — 모두 WebSearch 기반, 1차 확인 권장)

| 날짜 | 분류 | 내용 | 근거 |
|---|---|---|---|
| 2026-09-15 | 광운대 | **집현전**(중앙도서관 그룹스터디룸): 4~10인 14개실, **1일 2시간 제한**, 홈페이지+전용 앱 예약 | WebSearch |
| 2026-09-15 | 광운대 | **공학설계실습실**(전자정보공대): 예약 없이 이용, 학기 중 09:00–12:00 / 13:00–16:00 | WebSearch |
| 2026-09-15 | 광운대 | **광운창작소**(창업지원센터 메이커스페이스, 3D프린터): 온라인 예약 시스템 없음. 전화 02-941-9601 / 이메일 / 카카오 채널 | WebSearch |
| 2026-09-15 | 광운대 | 로봇학부 실습실·납땜 공간 개방시간: **웹에 공개 정보 없음.** 학과사무실 문의 필요 | WebSearch |
| 2026-09-15 | 광운대 | 졸업요건은 **수강신청 자료집 PDF 19~31p**에 있고, 학점 확인은 KLAS 별도 경로. 교육지원팀 02-940-5021 | WebSearch |
| 2026-09-15 | 광운대 | **KLAS에 졸업심사 기능이 존재한다** (사용자 확인). → 졸업요건 자가진단 주제 폐기 근거 | 사용자 진술 |
| 2026-09-15 | 광운대 | 마스코트 **우니**(하위 캐릭터 팡이), 상징동물 비마(飛馬) 재해석. 2021년 학부생 공모전 1위작 | WebSearch |
| 2026-09-15 | 광운대 | 마스코트 사용에 **「사용 확인 신청서」와 「2차 가공 사용 확인 신청서」가 별도로 존재** → 표정 변경은 2차 가공, 승인 필요 | news.kw.ac.kr/mascot |
| 2026-09-15 | 외부 | 에브리타임 **시간표 마법사** = 시간이 겹치지 않는 모든 조합 생성. **요일·시간 축만** 본다 | WebSearch |
| 2026-09-14 | 광운대 | **로봇인턴십(26-2)**: 참빛설계학기 비교과형, 일반선택 2학점 P/NP. 하반기 **총 40시간 이상** (OT 1·계획 2·선행연구 ≥5·프로젝트 ≥20·지도교수 미팅 ≥5·활동일지 4·중간보고 1·최종보고 2). 성과발표회 16주차 | 사용자 제공 `로봇연구실인턴십 프로그램 안내자료.pdf` |
| 2026-09-14 | 광운대 | 로봇인턴십 재료비: 팀당 **최대 100만원**, 20팀 내외. 신청 9/27, 선정 10/1, 안내 10/6(**구입은 10/6부터**). 구입신청서 → TA 승인 → 개인 선집행 → 매월 3일 증빙 | 같은 PDF |

## 사용자 레포 (2026-09-16 전수 확인)

| 날짜 | 분류 | 내용 | 근거 |
|---|---|---|---|
| 2026-09-16 | 레포 | `openvla-raccoonbot` — 피지컬AI 텀프로젝트. 7-D VLA 액션을 4-DoF 팔용 단계 머신으로 재매핑. 실기 grasp-lift 0.0122 m, 서버 요청 28→10, 스텝 811.7→581.2 ms | 레포 README·report.md |
| 2026-09-16 | 레포 | 그 프로젝트의 한계는 **fixed-layout 실기 실험**과 **100 step LoRA(성능 검증 아님)** — 본인이 보고서에 명시 | report.md §6 |
| 2026-09-16 | 레포 | `dreamlab-bootcamp` — 연구가 아니라 uv/tmux/Remote-SSH 숙달용 실습. PR #1이 `Dreamlemontree` 계정에서 옴 → **공동 사용 레포** | 커밋 로그 |
| 2026-09-16 | 레포 | `sensor-logger` — "packaging exercise". uv + Docker 재현성 연습 | README |
| 2026-09-16 | 레포 | `claude-routine` **빈 레포** (커밋 0). 기억 시스템과 겹치는지 여부는 판단 불가 | clone 시 empty repository |
| 2026-09-16 | 미확인 | `mygit` 용도 — README "mujoco" 한 줄인데 내용은 국내 주식 종목 목록. 불일치 | 레포 내용 |

## 결정

| 날짜 | 분류 | 내용 | 사유 |
|---|---|---|---|
| 2026-09-15 | 결정 | 팀 프로젝트 주제를 **`학기예보`**로 확정 | 권한 0·개인정보 0·콜드스타트 0, 기존 도구와 축이 다름 |
| 2026-09-15 | 결정 | 캐릭터는 **자체 제작 오리지널을 기본**으로, 우니는 승인 시 선택 스킨 | 우니 의존은 "외부 협조 불필요" 기준 위배 |
| 2026-09-15 | 결정 | 캐릭터 GIF는 **실제 인물·영상·음원·특정 안무를 일절 미사용** | IP 리스크 차단 |
| 2026-09-15 | 결정 | 교수 개인 평가·랭킹은 **기능 범위에서 명시 제외** | 명예훼손·윤리 리스크, 발표 방어 |
| 2026-09-16 | 결정 | 기억 시스템을 `Mingi1211/Mingi1211` 레포에 둔다 | 프로필 레포라 항상 접근 가능. 원격 세션은 `~/.claude`가 휘발됨 |
| 2026-09-16 | 결정 | 작업 브랜치를 PR 없이 `main`에 직접 병합 | 혼자 쓰는 프로필 레포라 PR 리뷰가 무의미. main에 있어야 클론·sync가 단순해짐 |

## 로컬 세션 `08a03da6` (2026-09-02~14, Windows 데스크톱 앱) — 2026-09-16 기록

> 다른 세션과 같은 날 동시에 기록해서, 충돌을 피하려고 섹션을 여기에 따로 둔다. 미확인 항목도 이 섹션 하단 표에 있다.

| 날짜 | 분류 | 내용 | 근거 |
|---|---|---|---|
| 2026-09-02 | 사실 | 사용자 **2001년생**, **2027년 8월 졸업(조기졸업) 예정** | 사용자 진술 |
| 2026-09-02 | 사실 | 서울대 DYROS 박재흥 교수 **2026-06-26 별세** | 한국경제·로봇신문 부고 (WebSearch) |
| 2026-09-02 | 판단 | 미국 **수업형 석사는 펀딩 사실상 없음**(GT 연 $6만+) → 부모님 지원 불가 조건에서 탈락. 미국은 **박사 직행**만 조건 충족(석사 없이 지원 가능) | GT ECE·Stanford EE 공식 문서 (WebSearch) |
| 2026-09-02 | 결정 | 모터 드라이버·QDD 액추에이터 하드웨어 트랙은 **하지 않는다** | 사용자 진술 "흥미 없음" |
| 2026-09-02 | 사실 | 사용자 궁극 목표 = 휴머노이드 동작 구현 **research engineer**(NVIDIA·Tesla급). 대학원은 수단 | 사용자 진술 |
| 2026-09-03 | 사실 | TOEFL(신 1–6 스케일) **R4.5 / L5.5 / W3.5 / S4.0 → overall 4.5** | 사용자 진술 |
| 2026-09-03 | 사실 | ETH 석사 영어 요건 TOEFL **5.0**(2026-01-21 이후 응시), **Home Edition 인정**, 섹션 최소 없음 | ETH language requirements 페이지 (WebSearch/Fetch) |
| 2026-09-03 | 결정 | TOEFL 재응시는 Home Edition이 아니라 **test center**로 | 사용자 진술 |
| 2026-09-05 | 결정 | 겨울방학 KAIST 인턴 대신 **현 연구실(박수한 교수님)에서 1년 몰입해 1저자 논문** — 교수님께 메일 | 교수님 제안(09-03 면담) 수용, 사용자 결정 |
| 2026-09-08 | 결정 | 연구실 People 페이지 관심분야: **Whole-Body Control · Sim-to-Real · VLA** 순. "풀스택" 표현 안 씀 | 대화에서 합의 |
| 2026-09-08 | 사실 | 교수님 지시: 해외 학회보다 **SCI급 저널**, KRoC 먼저 → **3/1 저널 투고**, 퀄리티 따라 IROS. 주제 **휴머노이드/모바일매니퓰레이터 전신제어·힘제어**, AI Worker·G1·사피엔스 공용 프레임워크, 캡스톤 연계 | 교수님 메일 (사용자가 원문 붙여넣음) |
| 2026-09-09 | 판단 | "URDF+YAML로 코드 재작성 없이 이기종 WBC"는 **mc_rtc가 이미 내세우는 기능** → 프레임워크 자체는 기여로 약함. 이식성 측정 → 원인 → 보정 규칙 구조를 권함 | mc_rtc 공식 문서 (WebSearch) |
| 2026-09-09 | 사실 | AI Worker **FFW-SG2** = 스워브 3륜(독립 조향·구동) + 양팔 7-DoF, Jetson AGX Orin, `ROBOTIS-GIT/ai_worker` 공개 | 사용자가 찾은 스펙 + WebSearch |
| 2026-09-12 | 사실 | 교수님 답장: "논문은 새로운 제안 + 근거", RA-L은 퀄리티 따라, **논문 스터디 참가 · 리스트 + 선정 이유 + 인상 먼저** | 교수님 메일 (사용자 붙여넣음) |
| 2026-09-12 | 사실 | 연구실 AI Worker는 **석사 진학 예정자 우선 배정** → 사용자는 못 쓴다고 가정 | 사용자 진술 |
| 2026-09-12 | 사실 | KRoC 2027 논문 마감 **11/26** | 사용자 진술 |
| 2026-09-13 | 결정 | 참빛설계 제안 **Little Apprentice**(아이가 가르치는 소형 휠 휴머노이드) — 반려 9안 거쳐 수렴. **→ 09-14 AlohaMini로 대체됨** | `projects/chambit-little-apprentice.md` |
| 2026-09-14 | 사실 | 로봇학실험4 과제 **AI 사용 허용**, 단 과한 주석·화려한 코드 금지 | 사용자 진술 (교수님 말씀 전달) |
| 2026-09-14 | 환경 | 로컬 **MATLAB R2024b** `C:/Program Files/MATLAB/R2024b`, `matlab -batch` 로 스크립트·Simulink 실행 가능. 사용자 MATLAB 작업 폴더 `C:/MATLAB` | 직접 실행 |
| 2026-09-14 | 환경 | Git Bash의 `python`(Anaconda)에 **python-docx·lxml 있음**, **PyMuPDF는 09-14에 `pip install pymupdf`로 설치** → PDF 페이지 PNG 렌더 가능 | 직접 실행 |
| 2026-09-14 | 환경 | Word COM `ExportAsFixedFormat`을 **한글 경로**로 Start-Job에서 돌리면 멈춤. docx를 **ASCII 경로로 복사 → `Documents.Open` 후 `SaveAs2(out,17)`** 로 2~9초에 성공 | 재현·해결 |
| 2026-09-14 | 환경 | python-docx로 OMML 수식 만들 때 같은 lxml 요소를 여러 번 append하면 **이동**돼 수식이 깨짐 → 매번 deepcopy | 재현·해결 |
| 2026-09-15 | 사실 | 사용자가 로실4 HW1 `.m`을 **직접 단순화**(비교 figure 2개, 70줄)하고 보고서 이미지 삽입·zip 생성 | 로컬 파일 타임스탬프·내용 확인 (09-16) |

| 날짜 | 분류 | 미확인 내용 |
|---|---|---|
| 2026-09-16 | 미확인 | PROFILE의 "DREAM Lab"과 대화 속 "박수한 교수님 동적제어연구실"이 같은 연구실인지 |
| 2026-09-16 | 미확인 | 참빛설계 주제가 Little Apprentice → AlohaMini로 바뀐 경위 |
| 2026-09-16 | 미확인 | 로실4 HW1 · 로봇제어 과제1 제출 여부, 제출본 |
| 2026-09-13 | 미확인 | Little Apprentice 예산 중 다이소몰 3품목 가격(검색 결과만), 형상 수치(65cm·0.2 m/s·토크 여유 34%)는 추정 |

| 날짜 | 분류 | 위 미확인의 확인 결과 | 근거 |
|---|---|---|---|
| 2026-09-16 | [정정] | **DREAM Lab = 박수한 교수님 동적제어연구실** (같은 곳) | 사용자 확인 |
| 2026-09-16 | [정정] | 참빛설계 주제가 AlohaMini로 바뀐 이유: **팀장(어재혁)이 제안**했고, **직접 설계하는 것(Little Apprentice)보다 난도가 할 만해서** | 사용자 확인 |
| 2026-09-16 | [정정] | **로봇학실험4 HW1 · 로봇제어 과제1 모두 제출 완료**. 로봇제어 제출본(원래 최종본 vs `_수정`)은 여전히 미확인 | 사용자 확인 |
| 2026-09-18 | 사실 | 교수님: 논문 정리는 **AI 없이 raw 형태로** 보내라. → 논문 리뷰 산출물은 Claude가 문장을 쓰지 말고 **형식·뼈대만** 잡아줄 것 | 사용자 전달 |

## 외부 조사 — AlohaMini (2026-09-14, repo 클론해서 1차 확인)

| 날짜 | 분류 | 내용 | 근거 |
|---|---|---|---|
| 2026-09-14 | 외부 | AlohaMini1: SO-ARM100/101 팔(5+1 DoF, 팔 부하 0.3 kg, 리프트 5 kg). AlohaMini2: AM-ARM200(6+1 DoF, 1 kg, 52 cm), 리프트 STS3095, 베이스 70 kg | `liyiteng/AlohaMini` README |
| 2026-09-14 | 외부 | AlohaMini2 BOM 합계 **~$1,097 / ¥7,548** (베이스 ¥2,475 · follower ×2 ¥3,320 · leader ×2 ¥1,646 · 체결 ¥107), 필라멘트 별도. 서보 32개(STS3215 25 + STS3095 7) | `AlohaMini2/docs/BOM.md` |
| 2026-09-14 | 외부 | README "120분 조립"은 **팔 조립 완료 전제의 베이스만**. 조립 가이드에 시간 추정 없음. 에폭시 접착·경화 단계 있음 | `assembly_guide.md` |
| 2026-09-14 | 외부 | **leader 서보는 5V** — AM-ARM 조립 가이드·lerobot profiles 일치. AlohaMini BOM의 7.4V(C046) 표기는 불일치 | `am-arm200/hardware_assembly.md`, `lerobot_alohamini/docs/alohamini/profiles.md` |
| 2026-09-14 | 외부 | lerobot 프로필: `alohamini2` = STS3215 바퀴 + 일반 팔 / `alohamini2pro` = **STS3250 바퀴** + HD 팔 → Pro 팔과 일반 베이스 혼용 시 맞는 프로필 없음 | `profiles.md` |
| 2026-09-14 | 외부 | 완제품: alohamini.com — 5-DOF DIY 키트 $1,499 / Pro 5-DOF 조립 $1,999 / Pro 6-DOF 조립 $2,699 (Taobao). PartaBot $1,099 품절·선주문. 공식 Taobao 상품 ID `1015799132286` | WebFetch(사이트), README |
| 2026-09-14 | 외부 | Taobao 조립 AM-ARM200 follower 팔(卓芸智能) ¥1,980/개, 2개 결제액 ₩829,375 (환산 약 210원/위안). 부품가(¥1,576) 대비 약 ¥400 비쌈 | 사용자 스크린샷 |

## 결정 — 참빛설계(AlohaMini)

| 날짜 | 분류 | 내용 | 사유 |
|---|---|---|---|
| 2026-09-14 | 결정 | 적용 스토리를 뷔페가 아닌 **1인 식당·트레이 정식집·휴게소**로. 뷔페 완전 대체는 다음 학기 캡스톤 | 사람 많은 환경은 SLAM이 어렵고 2개월 내 불가 (사용자 지시) |
| 2026-09-14 | 결정 | 인지 담당 불참에 따라 학습은 **트레이 파지 1과제(ACT)**, 배치·반납은 전신 제어, 식사완료는 테이블 번호 입력 | 3과제×50에피소드+모델 비교+인식은 3인·2개월에 무리 |
| 2026-09-14 | 결정 | 트레이 포함 총중량 **600 g 이하**로 목표 설정 | AlohaMini1 팔 부하 0.3 kg 기준 보수적. 버전 확정 시 재검토 |

## 2026-09-02 · 09-13 대화 세션 (로컬 Windows 데스크톱 앱) — 2026-09-16 인수인계로 기록

| 날짜 | 분류 | 내용 | 근거 |
|---|---|---|---|
| 2026-09-02 | 결정 | 프로필 README는 **영문 중심**, 포지셔닝 WBC + Physical AI + 제어, 프로젝트 카드는 **RaccoonBot 하나만** | 사용자 선택 (질문 응답) |
| 2026-09-02 | 사실 | 사용자는 **매니퓰레이션 자체엔 흥미가 크지 않다.** 목표는 휴머노이드 전신 동작 구현 | 사용자 진술 |
| 2026-09-02 | 결정 | `PhysicalAI_Assignment_<학번>` → **`openvla-raccoonbot`** 리네임 | Claude 제안 → 사용자 승인·실행. 과제 제출용 이름이라 대외용으로 약함 |
| 2026-09-02 | 결정 | README `05` 섹션을 `what's next`로. Claude가 추측으로 넣은 진행 항목 3개 삭제 | 사용자 확인 — 사실은 "VLA 실기 구동(완료)" 하나뿐 |
| 2026-09-02 | 사실 | README **stats 섹션은 사용자가 직접 삭제** | 커밋 `7a91282` |
| 2026-09-02 | 환경 | 로컬 Windows에 **`gh` CLI 없음.** credential helper = `manager`(GCM). 당시 push는 사용자가 PowerShell에서 직접 | `gh` 미설치 확인, `git config credential.helper` |
| 2026-09-02 | 환경 | 로컬 PDF 생성은 reportlab 5.0.1 + `C:/Windows/Fonts/malgun.ttf`(맑은 고딕)로 가능. poppler·pypdfium2·PyMuPDF 없음 → `Read` 도구로 PDF 렌더 불가, 브라우저 pane 썸네일로 확인 | 직접 확인 |
| 2026-09-02 | 환경 | reportlab 함정: ① PageTemplate 2개를 넣어도 **`NextPageTemplate`을 안 걸면 전 쪽이 첫 템플릿**(표지용 여백)을 씀 ② Paragraph `<font color>`는 `#` 포함 hex 필요 ③ 소제목 고아 방지는 `KeepTogether` | 재현 후 수정 |
| 2026-09-13 | 환경 | 로컬 Windows: LibreOffice·poppler·node·python-docx **없음**, pandoc·pypdf·**Microsoft Word 있음**. 쪽수 측정은 Word COM → `docx-page-fit` 스킬 | 직접 확인 |
| 2026-09-13 | 환경 | Git Bash에서 Python이 한글·`—`를 출력하면 cp949 오류 → `PYTHONIOENCODING=utf-8` 필요 | 재현 |
| 2026-09-13 | 환경 | Word COM 단순 호출에서 **숨은 Word 인스턴스가 멈춤(180s)**. 인자 전부 명시 + 별도 프로세스 watchdog으로 바꾼 뒤 정상. 사용자가 띄운 Word에는 붙지 않았음 | 1회 재현, PID로 확인 |
| 2026-09-13 | 결정 | 과제 분량 조정은 **원본을 덮어쓰지 않고 새 파일로.** 미완성 문항(설계·의견)은 Claude가 지어내지 않음 | 사용자 요구 · 사용자 아이디어 문항 |
| 2026-09-13 | 결정 | 분량 복원은 새 문장 작성이 아니라 **사용자 원문 문장에서 덜어내는 방식** | 요약 과정의 괄호 나열식 문장이 필자 문체와 어긋남 |
| 2026-09-14 | 사실 | 로봇제어 과제1 **최종본(원래 파일명 docx + PDF)은 사용자가 직접 생성.** PDF 5쪽, 1번 약 7,540자 · 2번 약 1,710자 | 2026-09-16 로컬 파일 직접 확인 |
| 2026-09-16 | [정정] | 위 2026-09-16 `sensor-logger` 줄의 "packaging exercise"는 사용자 진술이 아니다. **2026-09-02 Claude가 코드(Dockerfile + uv)를 보고 추론해 README에 쓴 표현**. 목적은 미확인 | 그 README를 작성한 대화 세션 |
| 2026-09-16 | 사실 | 프로필 README 자체가 **2026-09-02 Claude 대화 세션 산출물**. 다른 세션이 "README에서 읽은 프로필·스택"으로 쓰는 내용의 출처가 이것 | 커밋 `6bca846`~`5a07555` |
| 2026-09-16 | 사실 | 커밋 `2f67f0a`(참빛설계 기록)에 **동시에 작업 중이던 인수인계 세션의 `projects/github-profile.md`·`robot-control-hw1.md`가 함께 들어갔다.** 내용은 그 세션 작업본과 동일해 손실 없음. `C:/Mingi1211` 한 클론을 두 세션이 동시에 써서 생김 | `git show --stat 2f67f0a`, 작업 트리 diff 0 |
| 2026-09-16 | 환경 | **이 PC의 Git Bash `HOME` = `%APPDATA%\SPB_Data`** → `sync-memory.sh` 는 `SPB_Data\.claude` 에 썼고, Windows Claude Code가 읽는 `%USERPROFILE%\.claude` 에는 skills·CLAUDE.md가 **없다.** 로컬 Windows sync는 `sync-memory.ps1` 로 해야 한다. (09-16 LEDGER의 "sync 1회 실행 완료"는 실제로는 효과가 없었던 것) | Git Bash `echo $HOME`, PowerShell `Test-Path`, `CLAUDE_CONFIG_DIR` 미설정 |

| 2026-09-16 | [정정] | 위 Git Bash `HOME` 문제는 **스크립트 수정으로 해결**. `sync-memory.sh` 가 `USERPROFILE` 이 있고 `cygpath` 가 있으면 `%USERPROFILE%\.claude` 를 대상으로 삼는다. 리눅스(HOME) · Git Bash(USERPROFILE) 양쪽 실행 테스트 통과. 이제 두 스크립트 중 아무거나 써도 된다 | `scripts/sync-memory.sh`, 테스트 로그 |

| 2026-09-16 | 사실 | **로컬 Windows sync 성공.** Git Bash 출력 `대상: /c/Users/김민기/.claude`, 스킬 4개 + CLAUDE.md 포인터 기록됨. 로컬 Claude Code 세션은 이제 스킬 자동 로드 + STATE 경로 인지 상태 | 사용자가 붙여준 실행 출력 |

| 2026-09-18 | 결정 | 주제 범위를 **2기능**으로 확장: ① 학기 부담 진단·대안 조합 ② 관심분야 기반 수강 로드맵. 서비스명 가칭 `학업나침반` | 사용자 지시 |
| 2026-09-18 | 결정 | 대상 학부 **로봇·소프트웨어·정보융합** 3개. 역할은 PM 1 / 개발 3 / DB 2 / 디자인·기획 2 | 사용자 지시 |
| 2026-09-18 | 결정 | 부담 데이터는 **횟수가 아니라 주차(1~16) 시점**으로 저장(`load_event` 정규화). 시험기간 프로젝트 중복 같은 충돌 계산이 목적 | 설계 계획서 §2·§4 |
| 2026-09-18 | 환경 | **원격 세션은 사용자 로컬 Windows 경로에 접근할 수 없다.** 로컬 파일 작업은 로컬 Claude Code 세션에서 하거나 업로드받을 것 | `/mnt/c`·`/c` 부재 확인 |
| 2026-09-18 | 노하우 | 이 환경에서 **PDF는 HTML → Playwright `page.pdf()`** 로 만든다. LibreOffice는 여전히 불가. `@page{size:A4}` + Noto Sans CJK KR, `pdftoppm` 으로 시각 QA | 설계 계획서 제작 |

| 2026-09-18 | 결정 | 기술과경영 프로젝트를 **`Mingi1211/tech-management-team2` (private)** 로 분리. 프로필 레포에서는 `docs/deck`·`docs/plan`·`docs/team-project-topic.md`·`app/` 삭제. **기억 시스템(CLAUDE.md·memory·.claude/skills·scripts)은 프로필 레포에 남긴다** — 전 프로젝트 공용이라 옮기면 다른 작업에서 안 걸림 | 사용자 지시 |
| 2026-09-18 | 환경 | 레포 이름을 한글이 아닌 ASCII(`tech-management-team2`)로 지었다. 이번 세션에서 한글 파일명이 `pdftoppm`·LibreOffice에서 깨지는 걸 겪었고, 레포명은 URL·CLI·CI에 계속 등장한다 | 세션 경험 |
| 2026-09-18 | 환경 | **이 GitHub 통합은 `create_repository` 가 막혀 있다(403).** 새 레포는 사용자가 직접 만들고 `add_repo` 로 붙여야 한다 | 직접 시도 |
| 2026-09-18 | 사실 | 입력 폼 프로토타입 게시: <https://claude.ai/artifact/5KFsa4EYePQ8SfDqjf8bJW> · `db`+`downloads` 선언 · 조직 내부 전용 | Artifact publish |

| 2026-09-18 | 결정 | 부담 정규화를 **앱이 아니라 DB 트리거**로 한다. CSV import 로 `report` 를 넣어도 `load_event` 가 똑같이 생겨 프로토타입 데이터 이사가 공짜가 된다 | `db/schema.sql` |
| 2026-09-18 | 결정 | RLS: `report` 는 **insert 만 허용, select 불가**. 집계는 뷰(`v_week_load`)로만 공개. `anon key` 가 브라우저에 노출되기 때문 | `db/schema.sql` §5 |
| 2026-09-18 | 사실 | **아티팩트는 외부 host 로의 fetch 가 CSP 로 차단된다** → 아티팩트 폼은 Supabase 에 붙을 수 없다. 실배포 폼은 Vercel 에 올린 Next.js 페이지여야 한다 | artifact 페이지 계약 |
| 2026-09-18 | 노하우 | 이 환경에서 **SQL 검증 가능**: `apt-get install -y postgresql` → `pg_ctlcluster 16 main start` → `su postgres -c psql`. Supabase 전용 롤 `anon`·`authenticated` 는 직접 `create role ... nologin` 으로 만들어야 스키마가 끝까지 실행된다 | 스키마 검증 |

| 2026-09-19 | 결정 | 제출은 **브라우저 → Next API 라우트 → Supabase**. 브라우저가 Supabase 를 직접 치지 않는다. 키가 서버에만 남고 검증을 한곳에서 한다 | `app/api/reports/route.ts` |
| 2026-09-19 | 결정 | 주차 정규화(`weekOf`·`assignmentWeeksOf`)를 `lib/report.ts` 에 두고 **폼과 API 가 공유**한다. `db/schema.sql` 의 `week_of()` 와 값이 일치해야 한다 — 한쪽만 고치면 미리보기와 저장 결과가 어긋난다 | `lib/report.ts` |
| 2026-09-19 | [정정] | `v_week_load` 의 건수 컬럼이 총합이라 응답당 평균인 `load_score` 와 단위가 어긋났다. **전부 응답 1건당 평균으로 수정** | 로컬 PostgreSQL 확인 |
| 2026-09-19 | 노하우 | 이 환경에서 **Next.js API 라우트 검증법**: 목 서버(node http)를 띄워 `SUPABASE_URL` 을 거기로 돌리고 `next start` → curl 로 정상/비정상 제출 → 목이 받은 body 를 실제 PostgreSQL 스키마에 넣어 트리거까지 확인 | 이식 검증 |
| 2026-09-19 | 환경 | **`pkill -f "next start"` 가 Bash 툴 셸까지 끊는다**(exit 144). 백그라운드 프로세스 정리는 명령을 분리하거나 PID 를 직접 쓸 것 | 실제 발생 |

## 미확인 — 확인되면 `[정정]`으로 새 줄 추가할 것

| 날짜 | 분류 | 내용 |
|---|---|---|
| 2026-09-15 | 미확인 | 교명 광운(光云)의 '운'이 구름을 뜻한다는 한자 어원. 캐릭터 컨셉의 근거로 쓰고 있음 |
| 2026-09-14 | 미확인 | 卓芸智能이 AlohaMini 공식 Taobao 판매점인지 |
| 2026-09-14 | 미확인 | Pi 5 USB-A 4포트로 카메라 5대 + 팔 보드 2개 운용 가능 여부 (문서는 카메라별 별도 포트·허브 금지) |
| 2026-09-14 | 미확인 | Taobao 해외직구 영수증이 로봇인턴십 재료비 증빙으로 인정되는지 |
| 2026-09-14 | 미확인 | 부품 도착 2~3주·출력 80~120h는 추정치 (판매처 재고·실제 슬라이서 미확인) |
| 2026-09-13 | 미확인 | Word COM 첫 시도가 멈춘 원인 (Documents.Open 인자 부족인지, 보이지 않는 대화상자인지) |
| 2026-09-16 | 미확인 | 로봇제어 과제1 최종본이 2쪽 버전 대신 원문 길이 1번을 쓴 이유 · 제출 여부 · 마감일 |
| 2026-09-16 | 미확인 | 사용자의 ROS2 · C · MATLAB · STM32 사용 여부 (근거가 없어 프로필 스택에서 제외함) |
| 2026-09-16 | [정정] | 위 2026-09-02 "`gh` CLI 없음 → 당시 push는 사용자가 직접" 은 **push 불가를 뜻하지 않는다.** 로컬 Claude의 Bash에서 `GIT_TERMINAL_PROMPT=0 GCM_INTERACTIVE=never git push` 가 **인증 창 없이 성공**(GCM 캐시). 09-02엔 시도 없이 불가로 판단했던 것 | `7a58f26` push 성공 |

## 2026-09-19 — 배포·운영 (원격 세션)

| 날짜 | 분류 | 내용 | 근거 |
|---|---|---|---|
| 2026-09-19 | 사실 | **Vercel 배포 + Supabase 적재까지 한 번 관통 확인.** 사용자가 과목 1건 제출 → `report` · `load_event` 정상 생성 | Supabase 스크린샷 3장 |
| 2026-09-19 | 환경 | Vercel 환경변수의 환경 선택은 **체크박스가 아니라 단일 선택 드롭다운** — `Production and Preview` 를 고른다. ("셋 다 체크"라고 안내했던 것은 틀렸다) | 사용자 스크린샷, `docs/deploy.md` 수정 |
| 2026-09-19 | 노하우 | Supabase 에 `INSERT` 할 때 **`Prefer: return=representation` 은 SELECT 정책이 없으면 실패한다.** PostgreSQL 이 `RETURNING` 에 SELECT 권한을 요구하기 때문. **id 를 서버에서 만들고 `return=minimal`** 로 보낸다 | 로컬 PostgreSQL 로 두 가지 실패 모두 재현 |
| 2026-09-19 | 노하우 | 스키마를 두 번 돌리면 `42P07 relation already exists` 로 멈춘다 → `db/reset.sql` 선행 + seed 는 `on conflict do nothing`. **사용자가 SQL 을 반복 실행할 것을 전제로 스크립트를 짤 것** | 사용자 보고 후 재현·수정 |
| 2026-09-19 | 결정 | 과목명 **자유 입력을 W3 에 마스터 검색·선택으로 교체**하고, **QR 대량 배포는 W4 로 미룬다.** 순서를 바꾸면 한 주치 응답이 표기 차이(`자동제어1`/`자동제어 1`/`자동제어I`)로 쪼개진다 | `docs/todo.md` 고정 게이트 |
| 2026-09-19 | 사실 | 진단 기능은 **`v_week_load` 를 직접 읽는다. CSV 는 백업·대량입력 경로일 뿐**이다 | 사용자가 같은 오해를 두 번 물어봄 — 기록해 둔다 |
| 2026-09-19 | 환경 | **이 세션에 노션 커넥터가 없다.** 노션 갱신은 문서를 만들어 사용자가 붙여넣는 방식으로만 가능 | 커넥터 목록 확인 |
