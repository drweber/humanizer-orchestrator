#!/usr/bin/env bash
# Package the skill for upload to Claude Desktop / claude.ai, or for
# unzipping into ~/.claude/skills/. The archive root is the skill folder,
# which is what the upload expects.
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
OUT="${1:-$ROOT/dist}"
NAME=humanizer

"$ROOT/scripts/validate.sh" >/dev/null || { echo "validate failed, not packaging" >&2; exit 1; }

rm -rf "$OUT/$NAME" "$OUT/$NAME.zip" "$OUT/$NAME.skill"
mkdir -p "$OUT/$NAME"
cd "$ROOT"
for p in SKILL.md README.md NOTICE.md VERSIONS.md LICENSE references scripts delegates; do
  cp -R "$p" "$OUT/$NAME/"
done
find "$OUT/$NAME" \( -name "__pycache__" -o -name "*.pyc" -o -name ".DS_Store" -o -name "*.bak" \) -exec rm -rf {} + 2>/dev/null || true

cd "$OUT"
zip -qr "$NAME.zip" "$NAME" -x "*/.git/*"
cp "$NAME.zip" "$NAME.skill"
tar -czf "$NAME.tar.gz" "$NAME"
shasum -a 256 "$NAME.zip" "$NAME.skill" "$NAME.tar.gz" > SHA256SUMS.txt
rm -rf "$OUT/$NAME"

echo "built in $OUT:"
ls -lh "$NAME.zip" "$NAME.skill" "$NAME.tar.gz" | awk '{print "  "$5, $9}'
