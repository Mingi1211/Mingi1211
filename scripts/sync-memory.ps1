#Requires -Version 5.1
<#
  이 레포의 스킬·기억을 %USERPROFILE%\.claude\ 로 동기화한다 (Windows 전용).
  정본은 항상 이 레포다. ~/.claude 쪽을 직접 고치지 말 것.

  실행:
    powershell -ExecutionPolicy Bypass -File .\scripts\sync-memory.ps1
#>

$MarkBegin = '<!-- mingi-memory:begin -->'
$MarkEnd   = '<!-- mingi-memory:end -->'

$Repo       = Split-Path -Parent $PSScriptRoot
$Dest       = Join-Path $env:USERPROFILE '.claude'
$SkillsSrc  = Join-Path $Repo '.claude\skills'
$SkillsDest = Join-Path $Dest 'skills'

Write-Host "정본: $Repo"

if (-not (Test-Path $SkillsSrc)) {
    Write-Host "오류: $SkillsSrc 가 없다. 레포 루트에서 실행했는지 확인할 것." -ForegroundColor Red
    exit 1
}

# 최신 커밋 받기 (실패해도 계속 — 오프라인이거나 로컬 변경이 있을 수 있다)
git -C $Repo pull --ff-only
if ($LASTEXITCODE -ne 0) { Write-Host "  (pull 생략 - 오프라인이거나 로컬 변경 있음)" }

# 스킬 복사
New-Item -ItemType Directory -Force -Path $SkillsDest | Out-Null
Get-ChildItem -Path $SkillsSrc -Directory | ForEach-Object {
    $target = Join-Path $SkillsDest $_.Name
    if (Test-Path $target) { Remove-Item -Recurse -Force $target }
    Copy-Item -Recurse -Force $_.FullName $target
    Write-Host "  스킬 동기화: $($_.Name)"
}

# ~/.claude/CLAUDE.md 에 포인터 블록 삽입 (있으면 교체, 없으면 추가)
# 작은따옴표 here-string이라 백틱·$가 그대로 남는다. __REPO__만 치환한다.
$template = @'
<!-- mingi-memory:begin -->
## 내 기억 저장소

정본: __REPO__  (GitHub: Mingi1211/Mingi1211)

- 세션을 시작하면 **`__REPO__\memory\STATE.md`** 를 먼저 읽는다.
- 사용자 고정 정보는 `__REPO__\memory\PROFILE.md`.
- "전에 왜 이렇게 정했지?" 는 `__REPO__\memory\LEDGER.md` 를 검색한다.
- 의미 있는 작업을 했으면 **세션 종료 시 STATE.md / LEDGER.md 를 갱신하고 그 레포에 커밋**한다.
- 상세 운영 규칙은 `mingi-loop` 스킬.
<!-- mingi-memory:end -->
'@
$block = $template.Replace('__REPO__', $Repo)

$ClaudeMd = Join-Path $Dest 'CLAUDE.md'
if (-not (Test-Path $ClaudeMd)) { New-Item -ItemType File -Path $ClaudeMd -Force | Out-Null }

$content = [System.IO.File]::ReadAllText($ClaudeMd, [System.Text.Encoding]::UTF8)

if ($content.Contains($MarkBegin)) {
    $pattern = [regex]::Escape($MarkBegin) + '.*?' + [regex]::Escape($MarkEnd)
    $content = [regex]::Replace($content, $pattern, $block.Replace('$', '$$'), 'Singleline')
    Write-Host "  ~/.claude/CLAUDE.md 포인터 갱신"
} else {
    $content = $content.TrimEnd() + "`r`n`r`n" + $block + "`r`n"
    Write-Host "  ~/.claude/CLAUDE.md 포인터 추가"
}

# UTF-8 (BOM 없음) 으로 저장 — 한글이 깨지지 않게
$utf8NoBom = New-Object System.Text.UTF8Encoding($false)
[System.IO.File]::WriteAllText($ClaudeMd, $content, $utf8NoBom)

Write-Host "완료. 새 세션부터 적용된다." -ForegroundColor Green
