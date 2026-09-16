#!/usr/bin/env bash
# 이 레포의 스킬·기억을 ~/.claude/ 로 동기화한다 (로컬 PC 전용).
# 정본은 항상 이 레포다. ~/.claude/ 쪽을 직접 고치지 말 것.
set -euo pipefail

REPO="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
DEST="${HOME}/.claude"
MARK_BEGIN="<!-- mingi-memory:begin -->"
MARK_END="<!-- mingi-memory:end -->"

echo "정본: ${REPO}"
git -C "${REPO}" pull --ff-only || echo "  (pull 생략 — 오프라인이거나 로컬 변경 있음)"

mkdir -p "${DEST}/skills"
for dir in "${REPO}"/.claude/skills/*/; do
  [ -d "${dir}" ] || continue
  name="$(basename "${dir}")"
  rm -rf "${DEST}/skills/${name}"
  cp -r "${dir}" "${DEST}/skills/${name}"
  echo "  스킬 동기화: ${name}"
done

# ~/.claude/CLAUDE.md 에 포인터 블록을 넣는다 (있으면 교체, 없으면 추가)
BLOCK="${MARK_BEGIN}
## 내 기억 저장소

정본: ${REPO}  (GitHub: Mingi1211/Mingi1211)

- 세션을 시작하면 **\`${REPO}/memory/STATE.md\`** 를 먼저 읽는다.
- 사용자 고정 정보는 \`${REPO}/memory/PROFILE.md\`.
- \"전에 왜 이렇게 정했지?\" 는 \`${REPO}/memory/LEDGER.md\` 를 grep 한다.
- 의미 있는 작업을 했으면 **세션 종료 시 STATE.md / LEDGER.md 를 갱신하고 그 레포에 커밋**한다.
- 상세 운영 규칙은 \`mingi-loop\` 스킬.
${MARK_END}"

touch "${DEST}/CLAUDE.md"
if grep -qF "${MARK_BEGIN}" "${DEST}/CLAUDE.md"; then
  python3 - "$DEST/CLAUDE.md" "$MARK_BEGIN" "$MARK_END" "$BLOCK" <<'PY'
import sys, re
path, b, e, block = sys.argv[1:5]
s = open(path, encoding='utf-8').read()
s = re.sub(re.escape(b) + r'.*?' + re.escape(e), block.replace('\\', r'\\'), s, flags=re.S)
open(path, 'w', encoding='utf-8').write(s)
PY
  echo "  ~/.claude/CLAUDE.md 포인터 갱신"
else
  printf '\n%s\n' "${BLOCK}" >> "${DEST}/CLAUDE.md"
  echo "  ~/.claude/CLAUDE.md 포인터 추가"
fi

echo "완료. 새 세션부터 적용된다."
