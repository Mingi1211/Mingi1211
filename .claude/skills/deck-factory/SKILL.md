---
name: deck-factory
description: 발표 덱(pptx)이나 UI 프로토타입 목업을 만들 때 사용한다. HTML로 앱 화면을 그려 스크린샷으로 뽑고 그걸 슬라이드에 넣는 파이프라인, 한글 폰트 설치, LibreOffice가 안 될 때의 시각 QA 우회법, pptxgenjs 함정을 담고 있다. "PPT 만들어줘" "목업 보여줘" "프로토타입 화면" "슬라이드" 요청에 해당한다.
---

# deck-factory — 목업 → 스크린샷 → 덱 파이프라인

2026-09 `학기예보` 덱(10장) 제작에서 확립. **말로 설명하는 슬라이드보다 렌더된 화면 한 장이 이긴다.**

## 환경 준비 (원격 세션은 매번 필요)

```bash
apt-get install -y fonts-noto-cjk          # 한글 폰트. 안 깔면 두부(□□□)
apt-get update -qq && apt-get install -y -qq poppler-utils   # pdftoppm. update 선행 필수(404)
pip install --quiet python-pptx defusedxml Pillow lxml
cd <작업디렉토리> && npm install pptxgenjs   # playwright는 전역에 이미 있음
```

- playwright 경로: `require('/opt/node22/lib/node_modules/playwright')` — 로컬 설치 불필요
- 작업은 스크래치패드에서. 최종 산출물만 레포로 복사

## 1단계 — HTML로 화면을 그린다

한 HTML 파일에 화면들을 `id`를 붙인 컨테이너로 나열하고, JS로 반복 요소(차트 막대, 캐릭터 표정)를 생성한다.
**캐릭터·아이콘은 인라인 SVG로 코드에서 그린다** — 이미지 파일 불필요, 저작권 클린, 표정 변형은 path 교체로 끝.

```js
// 무드(표정)와 팔 자세를 분리해두면 애니메이션 프레임을 공짜로 얻는다
function ch(mood, size, armOverride){ ... arms[armOverride || mood] ... }
```

## 2단계 — Playwright로 요소별 스크린샷

```js
const { chromium } = require('/opt/node22/lib/node_modules/playwright');
const b = await chromium.launch();
const p = await b.newPage({ deviceScaleFactor: 2, viewport:{width:1400,height:1000} });
await p.goto('file://' + __dirname + '/mock.html');
await p.waitForTimeout(600);
for (const id of ids) (await p.$('#'+id+' > *')).screenshot({ path: id+'.png' });
```

**함정**
- 컨테이너가 `display:block`이면 뷰포트 전체 폭으로 찍힌다 → **안쪽 자식(`#id > *`)을 찍는다**
- 그래도 가장자리에 1~2px 배경이 샌다 → **찍은 뒤 사방 3px 크롭**
  ```python
  im.crop((3,3,w-3,h-3)).save(f)
  ```
- 슬라이드 배경색과 이미지 배경색을 **정확히 같은 값**으로 맞추면 이음매가 안 보인다

## 3단계 — pptxgenjs로 덱 생성

`anthropic-skills:pptx` 스킬의 함정 목록을 먼저 읽을 것. 추가로 실전에서 걸린 것:

- **한글 폰트는 `맑은 고딕`** 으로 지정 (한국 윈도우 PowerPoint 표준). 안전 폰트 목록은 라틴 기준이라 한글엔 무의미
- 색상 hex에 `#` 금지, 8자리 금지 → 파일 손상
- `addText`마다 `isTextBox: true`, 도형과 정렬할 땐 `margin: 0`
- 이미지는 **원본 비율대로** 배치. 스크립트로 검산할 것:
  ```python
  ideal_h = set_w * img_h / img_w   # set_h와 0.06" 이내여야 함
  ```
- 슬라이드 하단 여백 최소 0.35". 세로로 긴 폰 목업은 높이를 먼저 정하고 폭을 역산
- 발표자 노트는 `slide.addNotes("...")`

## 4단계 — 검증 (LibreOffice가 고장난 환경에서)

```bash
python3 <pptx-skill>/scripts/office/validate.py deck.pptx   # 스키마·관계·차트 검사
```

**⚠️ 이 환경의 `soffice`는 pptx를 못 연다** (최소 파일에서도 실패 확인). PDF 변환 QA 경로가 막혀 있다.
대신 **pptx의 실제 좌표를 python-pptx로 읽어 HTML로 재현**하고 Playwright로 찍는다:

```python
from pptx import Presentation
P = 100.0                      # 1인치 = 100px
x = shape.left / 914400 * P    # EMU → px
# 도형은 div, 그림은 base64 img, 텍스트는 절대배치 div + 점선 outline(박스 경계 확인용)
# 정렬 매핑 주의: PP_ALIGN LEFT=1, CENTER=2, RIGHT=3
```

이 방법으로 **텍스트 오버플로·겹침·여백 부족**을 실제로 잡아낼 수 있다. 눈으로 전 슬라이드를 본다.

내용 검증은 python-pptx로 텍스트를 덤프해 오타·자리표시자·**숫자 불일치**를 확인한다.
(실제로 슬라이드 간 "한 단계"/"두 단계", "87점"/"82점" 불일치를 여기서 잡았다.)

## 5단계 — 파일명 주의

**한글 파일명은 `soffice`·`pdftoppm`에서 깨진다.** 변환이 필요하면 ASCII 사본(`deck.pptx`)을 만들어 쓰고,
사용자에게 전달하는 최종본만 한글 이름으로 둔다.

## 덱 구성 원칙 (사용자 취향)

- **글을 최대한 뺀다.** 슬라이드당 제목 + 짧은 주석 3개 정도
- 프로토타입 화면을 **크게** 넣고 번호 원 + 한 줄 설명을 옆에 단다
- **before/after 비교**를 꼭 한 장 넣는다. 가장 설득력 있다
- 어두운 표지·마무리 + 밝은 본문 (샌드위치)
- 액센트 줄무늬·제목 밑줄 금지 (AI 티가 난다)
- 마지막 장은 "왜 이게 안전한가" 3카드 + "다음 회의까지" 액션

## 재사용 자산

`docs/deck/prototype-mock.html` — 학기예보 목업 원본. 캐릭터 SVG 생성 함수, 16주 막대 차트,
폰 프레임, 공유 카드, 파이프라인 다이어그램이 들어 있다. **새 프로젝트는 여기서 복사해 시작한다.**
