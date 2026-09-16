---
name: docx-page-fit
description: 워드(docx) 과제·보고서를 정해진 쪽수에 맞출 때 사용한다. "1쪽으로 요약해줘" "2쪽 딱 되게 맞춰" "분량 줄여/늘려" "표지 제외 N쪽" "워드 쪽수 확인" 같은 요청에 해당한다. 원본 서식을 유지한 채 본문만 교체하는 절차, 로컬 Windows에서 Word로 실제 쪽수를 재는 스크립트, 요약·복원할 때 필자 문체를 지키는 원칙을 담고 있다.
---

# docx-page-fit — 워드 문서를 정확한 쪽수에 맞추기

2026-09-13 로봇제어 과제 #1에서 **같은 작업을 두 번(1쪽 요약 → 2쪽 복원)** 해서 만든 스킬.
사례 기록: `memory/projects/robot-control-hw1.md`

## 원칙 — 먼저 지킬 것

1. **원본은 덮어쓰지 않는다.** 항상 새 파일명으로 저장한다. 사용자가 원본을 Word로 열어두고 있는 경우가 많다
2. **쪽수 기준을 확인한다.** 이 사용자는 "표지 제외"로 센다. 애매하면 현재 쪽수를 먼저 재서 "늘려야 하나 줄여야 하나"로 판별한다
3. **미완성 문항은 지어내지 않는다.** 설계·의견 문항은 사용자의 것이다. 원문 그대로 두고 보고한다
4. **사용자가 직접 고친 문장은 보존한다.** 다시 손댈 때는 수정본을 기준으로 삼고, 수정된 문단 XML을 통째로 유지한다
5. **요약·복원은 원문 문장에서 덜어내는 방식을 우선한다.** 새 문장을 지어 붙이면 필자 문체와 어긋난다.
   특히 `분야(회사 A, 회사 B), 분야(…)` 식 괄호 나열과 가운뎃점(·) 나열은 원문 서술체와 가장 크게 튄다
6. 고친 오타·사실 오류는 **요약본에서만** 고치고 무엇을 고쳤는지 보고한다

## 절차

```
1. pandoc -t markdown --wrap=none 원본.docx          # 내용 파악
2. unzip → skills/docx/scripts/merge_runs.py          # 쪼개진 run 병합 (텍스트 검색 가능하게)
3. 최상위 블록 목록 출력 — 블록 번호·pPr·첫 run rPr·앞 30자
   → 표지 끝(페이지 나누기) / 문항 제목(numPr) / 본문 문단 템플릿 pPr·rPr 확보
4. 교체 스크립트: 경계 블록을 텍스트로 assert 한 뒤 x[:시작] + 새 문단 + x[끝:]
   - 원본 un/ 은 읽기 전용으로 두고 매 빌드마다 work/ 로 복사 (재실행 시 assert가 깨지지 않게)
   - [Content_Types].xml 을 zip 첫 항목으로
5. validate.py 새파일.docx --original 원본.docx
6. Word로 실제 쪽수 측정 (아래 스크립트) → 모자라면 원문 복원, 넘치면 덜어내기 → 반복
7. 마지막 쪽이 한 줄 여유뿐이면 "제출 전 PDF로 변환해 쪽수 확인" 을 권고
```

**분량 감 (A4, 여백 상 1701/하·좌·우 1440 twips, 바탕 10pt, 왼쪽 들여쓰기 800)**
본문 약 **2,500~2,700자/쪽**. 문단 하나 추가마다 반 줄~한 줄 손실. 1줄 ≈ 13pt, 약 55자.

## 로컬 Windows 환경 제약 (2026-09-13 확인)

| 있음 | 없음 |
|---|---|
| pandoc, pypdf, reportlab, **Microsoft Word** | LibreOffice(soffice), poppler(pdftoppm), node, python-docx, pypdfium2, PyMuPDF |

- → 스킬 기본 절차의 `soffice → pdftoppm` 렌더링은 **안 된다.** 쪽수는 Word COM으로 잰다
- Git Bash의 Python 출력은 cp949라 한글·`—` 출력에서 죽는다 → **`PYTHONIOENCODING=utf-8`** 필수
- `Read` 도구로 PDF를 못 본다(pdftoppm 없음). 브라우저 pane에서 `file:///` 로 열면 **썸네일로 레이아웃 확인은 가능**,
  내부 클릭은 안 되고 `#page=` 는 무시될 때가 많다

## Word로 쪽수 재기 — 반드시 이 방식으로

**직접 `New-Object -ComObject Word.Application` 후 `Documents.Open(path, $false, $true, $false)` 로 열었을 때
숨은 Word가 멈춰 180초 타임아웃**이 났다. 아래처럼 인자를 전부 명시하고 **별도 프로세스 + watchdog**으로 돌린 뒤로는 정상.
(멈춘 정확한 원인은 **[미확인]**)

`wordpages.ps1`
```powershell
param([string]$Path, [string]$Pdf)
$ErrorActionPreference = 'Stop'
$word = New-Object -ComObject Word.Application
try {
    if ($word.Documents.Count -gt 0) { throw "attached to an existing Word instance; aborting" }
    $word.Visible = $false; $word.DisplayAlerts = 0; $word.AutomationSecurity = 3
    $doc = $word.Documents.Open($Path, $false, $true, $false, "", "", $false, "", "", 0, [Type]::Missing, $false, $false, 0, $true)
    $doc.Repaginate()
    $pages = $doc.ComputeStatistics(2)
    $end = $doc.Content; $end.Collapse(0)
    $vpos = $end.Information(6)          # 마지막 줄의 쪽 상단 기준 세로 위치(pt)
    if ($Pdf) { $doc.ExportAsFixedFormat($Pdf, 17) }
    $doc.Close($false)
    "pages=$pages endVerticalPos(pt)=$vpos"
} finally { $word.Quit(); [System.Runtime.InteropServices.Marshal]::ReleaseComObject($word) | Out-Null }
```

실행 (watchdog — **사용자가 이미 띄운 Word PID는 절대 죽이지 않는다**)
```powershell
$before = @(Get-Process WINWORD -ErrorAction SilentlyContinue | ForEach-Object Id)
$p = Start-Process powershell.exe -ArgumentList @('-NoProfile','-ExecutionPolicy','Bypass','-File',"$dir\wordpages.ps1",'-Path',"$dir\out.docx") `
     -RedirectStandardOutput "$dir\wp_out.txt" -RedirectStandardError "$dir\wp_err.txt" -PassThru -WindowStyle Hidden
if (-not $p.WaitForExit(75000)) {
    Stop-Process -Id $p.Id -Force -Confirm:$false
    Get-Process WINWORD -ErrorAction SilentlyContinue | Where-Object { $before -notcontains $_.Id } | Stop-Process -Force -Confirm:$false
    "TIMEOUT"
} else { Get-Content "$dir\wp_out.txt" -Raw }
```

- `-ArgumentList` 에 **빈 문자열 `''` 을 넣으면 Start-Process가 거부**한다. PDF가 필요 없으면 `-Pdf` 인자 자체를 빼라
- **쪽이 꽉 찼는지 판정**: 사용 가능한 하단 = 쪽 높이 842pt − 하단 여백(1440 twips = 72pt) = **770pt**.
  `endVerticalPos` 가 **~740pt 이상이면 거의 꽉 찬 것**. 문서 끝에 빈 문단이 있으면 그 줄 위치가 나온다는 점을 감안할 것
- 판정이 이상하면 원본부터 같은 스크립트로 재서 사용자 체감 쪽수와 맞는지 교차 확인한다
