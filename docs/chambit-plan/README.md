# 참빛설계학기 계획서(서식 1-2) HWP 생성 스크립트

한글 프로그램 없이 HWP 5.0 바이너리를 직접 고쳐서 계획서 2~7번을 채운다. (2026-09-14)

| 파일 | 역할 |
|---|---|
| `content2.py` | **계획서 본문 전부** (프로그램명·요약·목표·지원동기·활동내용·팀원표·13주 계획·결과물). 내용 수정은 여기만 |
| `build2.py` | 원본 서식을 읽어 셀 문단 교체, 주차 행 추가(4→13행), 글자모양(나눔고딕OTF 9pt 검정)·문단모양 추가 후 저장 |
| `hwplib.py` | 레코드 파서/라이터, raw deflate |
| `dump.py` | 레코드·글자모양 덤프 (검증용) |

## 실행 (Windows, pywin32·olefile 필요)

```bash
# 원본 서식을 같은 폴더에 orig.hwp 로 복사한 뒤
python build2.py out2.hwp
```

원본 서식 파일은 레포에 없다 — 사용자 Downloads의 `[서식 1-2] 참빛설계학기 계획서(비교과형).hwp`.

## 알아낸 것 (다시 할 때 필요)

- 본문 전체가 **행 32개짜리 표 하나**. 셀은 `LIST_HEADER`의 (row, col)로 찾는다
- 행 추가 = `TABLE` 레코드의 nRows·행별 셀 수 배열 수정 + 이후 셀 row 인덱스 시프트
- 새 문단은 `PARA_LINE_SEG`를 **생략**(한글이 열 때 재계산하게 함)
- 문단 여백·들여쓰기 값은 **pt×200** 단위 (내어쓰기 -1200 ≈ 6pt)
- CFB 저장은 `pythoncom.StgCreateDocfile` 사용 (olefile은 같은 크기로만 덮어쓰기 가능)
- **한글에서 열어 확인한 적은 없다.** pyhwp 파서로 구조만 검증함

## Linux에서 저장하기 (2026-10-13 추가)

`pythoncom`이 없는 원격(Linux) 세션에서는 `cfbwrite.py`의 `write_cfb(path, {"BodyText/Section0": bytes, ...}, root_clsid)` 로 저장한다.
원본 스트림을 그대로 넣으면 olefile 기준 **바이트 단위로 동일하게** 왕복된다. pyhwp는 이 환경에서 빌드 실패.

> ⚠️ **olefile은 헤더 오류를 그냥 넘긴다.** 첫 버전은 헤더 offset 68(첫 DIFAT 섹터)에 0을 써서 **한글에서 '파일 손상'** 이 났다(2026-10-13). 반드시 `0xFFFFFFFE`.
> 저장 후에는 FAT 체인·DIFAT·미니스트림을 직접 검사하는 엄격 검사를 돌릴 것 (olefile 통과 ≠ 한글 통과)
- 수정·새 문단에도 `PARA_LINE_SEG`를 1개(textStart 0) 남기고 줄정보 수=1로 둔다 (지우지 않음)

- 셀 문단은 `LIST_HEADER`와 **같은 레벨**이다. 셀 범위는 "다음 같은 레벨 `LIST_HEADER` 전까지"로 잡아야 한다
- 기존 문단 글자 교체: `PARA_TEXT` 교체 + `PARA_HEADER` nchars 갱신 + 뒤쪽 `PARA_CHAR_SHAPE` 위치 이동 + `PARA_LINE_SEG` 삭제(줄정보 수 0)
- 원래 레코드를 찾을 때 `list.index`는 **값 비교**라 같은 내용의 빈 문단을 잘못 잡는다 → `is`로 찾을 것

## 그림 넣기·줄 정보 (2026-10-13)

- `hwppic.py` — 글자처럼 취급 그림(gso → `$pic` 개체요소 → 그림 레코드) + BinData. pyhwp `hwp5proc models`로 파싱 검증,
  **한글에서 열림 확인은 사용자 몫**
- pyhwp는 pip 빌드가 안 되지만 `pip download --no-binary :all: pyhwp` 후 `src`를 PYTHONPATH에 넣으면
  `hwp5proc models <파일> BodyText/Section0` 로 **레코드 구조 검증기**로 쓸 수 있다
- 셀 안 긴 문단은 `PARA_LINE_SEG`를 **줄마다** 넣는다(줄 높이 1000·간격 600·피치 1600 = 10pt 160%).
  줄 하나짜리 seg를 넣었을 때 사용자가 "양쪽 정렬로 맞춰 달라"고 함 → 한글이 seg를 레이아웃 캐시로 쓰는 것으로 추정
- 글자 폭 추정: Noto Sans CJK 한글 0.92em(맑은 고딕 대용). 문단 모양 bit7=1이면 한글 **글자 단위** 줄나눔
- 셀 글자를 바꿀 때 원래 칸의 회색 안내 글자모양(예: "(단과)" 49번)이 남아 일부가 흐리게 보였다 → 값 칸은 글자모양을 하나로 강제
