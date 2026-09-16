# BOOTSTRAP — 다른 프로젝트에서 이 기억을 쓰는 법

> **먼저 알아야 할 것: 기억은 자동으로 따라오지 않는다.**
> Claude Code가 파일을 자동 로드하는 경로는 정해져 있고, 이 레포에 둔 파일은
> **이 레포에서 연 세션에서만** 자동 로드된다. 다른 프로젝트에서 쓰려면 연결이 필요하다.

## 자동 로드되는 경로 (원리)

| 경로 | 언제 로드되나 |
|---|---|
| `<레포>/CLAUDE.md` | 그 레포 세션에서 **항상** |
| `<레포>/.claude/skills/*/SKILL.md` | 그 레포 세션에서 **설명이 맞을 때** |
| `~/.claude/CLAUDE.md` | 그 PC의 **모든** 세션에서 항상 |
| `~/.claude/skills/*/SKILL.md` | 그 PC의 **모든** 프로젝트에서 |

→ **결론: 전 프로젝트에서 쓰려면 `~/.claude/` 에 있어야 한다.**
다만 Claude Code 웹/원격 세션은 컨테이너가 매번 새로 만들어져 `~/.claude/`가 휘발된다.
그래서 **정본은 이 레포에 두고, 환경에 따라 아래 셋 중 하나로 연결한다.**

---

## 방법 A — 로컬 PC · 권장 (한 번만 하면 모든 프로젝트에 적용)

### Windows (사용자 기본 환경)

`bash`가 없다. 아래 둘 중 하나를 쓴다.

**A-1. Git Bash — 권장.** Git for Windows에 딸려 오므로 이미 설치돼 있다.
시작 메뉴에서 "Git Bash"를 열고:

```bash
git clone https://github.com/Mingi1211/Mingi1211.git ~/repos/mingi-memory
bash ~/repos/mingi-memory/scripts/sync-memory.sh
```

**A-2. PowerShell.** Git Bash를 안 쓸 때.

```powershell
git clone https://github.com/Mingi1211/Mingi1211.git $env:USERPROFILE\repos\mingi-memory
powershell -ExecutionPolicy Bypass -File $env:USERPROFILE\repos\mingi-memory\scripts\sync-memory.ps1
```

> `-ExecutionPolicy Bypass`가 필요한 이유: 윈도우는 기본적으로 서명 없는 `.ps1` 실행을 막는다.
> 이 옵션은 **그 한 번의 실행에만** 적용되고 시스템 설정을 바꾸지 않는다.

둘 다 `%USERPROFILE%\.claude\skills\` 에 스킬을 복사하고 `%USERPROFILE%\.claude\CLAUDE.md` 에 포인터를 넣는다.

### Linux / macOS

```bash
git clone https://github.com/Mingi1211/Mingi1211.git ~/repos/mingi-memory
bash ~/repos/mingi-memory/scripts/sync-memory.sh
```

### 듀얼부팅이면 OS마다 한 번씩

`~/.claude`는 **OS별로 따로** 존재한다. Windows에서 돌렸다고 Ubuntu 쪽에 적용되지 않는다.
**부팅한 OS마다 한 번씩** 실행해야 한다. 레포 클론도 각각 필요하다.

### 이후 갱신

레포가 바뀔 때마다 같은 스크립트를 다시 실행한다. 내부에서 `git pull`을 하므로 클론은 최초 1회면 된다.

스크립트가 하는 일: 최신 커밋을 받아 `.claude/skills/*`를 `~/.claude/skills/`로 복사하고,
`~/.claude/CLAUDE.md`에 기억 파일 위치를 가리키는 블록을 넣는다. 마커로 감싸므로 **여러 번 실행해도 중복되지 않는다.**

> *(Linux / macOS 한정)* 심볼릭 링크(`ln -s`)로 걸면 `git pull`만으로 동기화되지만,
> 링크된 스킬 디렉터리가 인식되는지는 버전에 따라 다를 수 있다. 확실한 쪽은 위의 복사 방식이다.

---

## 방법 B — Claude Code 웹 / 원격 세션

컨테이너가 휘발되므로 **세션마다** 둘 중 하나를 한다.

1. **세션 소스에 `Mingi1211/Mingi1211`를 추가한다** (권장).
   그러면 그 레포의 `CLAUDE.md`와 스킬이 로드된다.
2. 또는 세션 첫 메시지에 아래를 붙여넣는다.

---

## 방법 C — 어떤 환경에서도 통하는 최후 수단

새 세션 **첫 메시지에 이 한 덩어리를 복붙**한다.

```
작업 전에 내 기억 저장소부터 붙여줘.
저장소: https://github.com/Mingi1211/Mingi1211

1. 이 레포를 이 세션에 추가(add_repo)하고 클론해줘
2. memory/STATE.md 와 memory/PROFILE.md 를 읽어줘
3. .claude/skills/ 아래 스킬 목록을 확인하고, 이번 작업에 맞는 걸 써줘
4. 작업이 끝나면 STATE.md / LEDGER.md 를 갱신해서 그 레포에 커밋·푸시해줘
```

> 이 문단을 메모 앱이나 브라우저 북마크에 저장해두면 매번 타이핑할 필요가 없다.

---

## 갱신 흐름

```
어느 세션에서든 작업
      ↓
memory/STATE.md · LEDGER.md 갱신, 새 노하우는 SKILL.md 에
      ↓
Mingi1211/Mingi1211 에 커밋·푸시        ← 정본은 항상 여기 하나
      ↓
로컬 PC 에서 sync-memory.sh 실행        ← 로컬 세션에도 반영
```

**정본은 항상 이 레포 하나다.** `~/.claude/`에 있는 건 사본이므로,
거기서 직접 고치지 말고 레포에서 고친 뒤 다시 동기화한다.

---

## 스크립트가 안 될 때

| 증상 | 원인 / 대응 |
|---|---|
| `bash: command not found` | 윈도우 PowerShell에서 `.sh`를 돌린 것. A-1(Git Bash) 또는 A-2(`.ps1`) 사용 |
| `이 시스템에서 스크립트를 실행할 수 없으므로` | 실행 정책. `powershell -ExecutionPolicy Bypass -File ...` 로 실행 |
| `git: 명령을 찾을 수 없습니다` | Git for Windows 미설치 → <https://git-scm.com/download/win> |
| `~/.claude/CLAUDE.md` 한글이 깨짐 | 스크립트는 UTF-8(BOM 없음)로 쓴다. 메모장으로 저장하면 깨질 수 있으니 VS Code로 열 것 |
| `~/.claude/CLAUDE.md` 경로가 `/c/Users/...` 로 적힘 | Git Bash의 MSYS 경로. 현재 스크립트는 `cygpath -m`으로 `C:/Users/...` 로 바꿔 적는다. 옛 버전으로 돌렸다면 **최신 스크립트로 다시 실행**할 것 |
| 스크립트 자체가 안 되면 | **수동으로 해도 된다.** `.claude/skills/` 의 폴더 3개를 `%USERPROFILE%\.claude\skills\` 로 복사하고, `%USERPROFILE%\.claude\CLAUDE.md` 에 STATE.md 경로를 가리키는 문장 몇 줄을 직접 적으면 끝이다 |

## 확인 방법

**아무 폴더에서나** Claude Code를 새로 열고 이렇게 물어본다.

> "내 STATE.md에 뭐라고 적혀 있어?"

- **진행 중인 프로젝트(학기예보) 이야기가 나오면** → 성공
- **파일을 못 찾는다고 하면** → 연결 실패. `~/.claude/CLAUDE.md`를 열어 경로가 실제로 존재하는지 확인한다.
  경로가 `/c/Users/...` 형태면 최신 스크립트로 다시 실행할 것
- **읽기 권한을 물어보면** → 정상이다. 작업 폴더 밖 파일이라 그렇다. 승인하면 된다

### 무엇이 자동이고 무엇이 아닌가

| | 자동인가 |
|---|---|
| 스킬 3개 로드 (`~/.claude/skills/`) | ✅ 설명이 맞으면 자동 |
| `~/.claude/CLAUDE.md` 로드 | ✅ 매 세션 자동 |
| STATE.md **읽기** | △ CLAUDE.md의 지시를 따라 읽지만, 폴더 밖 접근이라 승인이 필요할 수 있다 |
| STATE.md **갱신** | ❌ **지시일 뿐 강제가 아니다.** 중요한 작업 뒤에는 "기억 갱신해줘" 한마디 하는 게 확실하다 |
| 웹/모바일 세션 | ❌ `~/.claude`가 없다. 방법 B 또는 C 필요 |
