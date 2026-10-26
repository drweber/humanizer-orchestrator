#!/usr/bin/env bash
# Refresh one vendored delegate from upstream and report what changed.
#   scripts/sync_delegates.sh <en|de|ru> [--apply]
# Without --apply it only reports. Upstream layouts differ and have moved
# before, so each delegate carries its own path map below.
set -euo pipefail

LANG_CODE="${1:-}"
APPLY="${2:-}"
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

case "$LANG_CODE" in
  en) REPO=https://github.com/blader/humanizer.git
      SKILL_SRC="SKILL.md";                      EXTRA="LICENSE" ;;
  de) REPO=https://github.com/marmbiz/humanizer-de.git
      SKILL_SRC="skills/humanizer-de/SKILL.md";  EXTRA="LICENSE NOTICE references scripts requirements-precise.txt" ;;
  ru) REPO=https://github.com/Vladimir-Human/humanizer-ru.git
      SKILL_SRC="skills/humanizer-ru/SKILL.md";  EXTRA="LICENSE skills/humanizer-ru/references:references skills/humanizer-ru/scripts:scripts" ;;
  *)  echo "usage: $0 <en|de|ru> [--apply]" >&2; exit 2 ;;
esac

DEST="$ROOT/delegates/$LANG_CODE"
SKILL_DEST="humanizer-$LANG_CODE.md"
TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT

git clone --depth 1 -q "$REPO" "$TMP/up"
NEW_COMMIT="$(cd "$TMP/up" && git rev-parse --short HEAD)"
OLD_COMMIT="$(cat "$DEST/COMMIT" 2>/dev/null || echo none)"
NEW_VERSION="$(sed -n 's/.*"version"[[:space:]]*:[[:space:]]*"\([^"]*\)".*/\1/p' "$TMP/up/.claude-plugin/plugin.json" 2>/dev/null | head -1)"

echo "delegate : $LANG_CODE"
echo "pinned   : $OLD_COMMIT"
echo "latest   : $NEW_COMMIT${NEW_VERSION:+  (v$NEW_VERSION)}"

if [ ! -f "$TMP/up/$SKILL_SRC" ]; then
  echo "ERROR: upstream moved its SKILL.md; expected $SKILL_SRC" >&2
  echo "       fix SKILL_SRC in this script before syncing." >&2
  exit 3
fi

if [ "$OLD_COMMIT" = "$NEW_COMMIT" ]; then
  echo "status   : up to date"
  exit 0
fi
echo "status   : behind"

# pattern numbering drift is the failure that breaks references/pattern-map.md silently
old_n="$(grep -cE '^#{2,4} [0-9]+\.' "$DEST/$SKILL_DEST" 2>/dev/null || echo 0)"
new_n="$(grep -cE '^#{2,4} [0-9]+\.' "$TMP/up/$SKILL_SRC" 2>/dev/null || echo 0)"
if [ "$old_n" != "$new_n" ]; then
  echo "WARNING  : pattern count changed $old_n -> $new_n; references/pattern-map.md must be rebuilt"
fi

echo
echo "--- changed ---"
diff -q "$DEST/$SKILL_DEST" "$TMP/up/$SKILL_SRC" >/dev/null 2>&1 || echo "differs: $SKILL_DEST"
for spec in $EXTRA; do
  src="${spec%%:*}"; dst="${spec##*:}"
  [ -e "$TMP/up/$src" ] || { echo "gone upstream: $src"; continue; }
  diff -rq "$DEST/$dst" "$TMP/up/$src" 2>/dev/null || true
done

if [ "$APPLY" != "--apply" ]; then
  echo
  echo "dry run. re-run with --apply to replace $DEST"
  exit 0
fi

# the upstream SKILL.md is renamed on vendoring: a nested SKILL.md would be
# read as a separate skill and the package would fail validation
rm -f "$DEST/$SKILL_DEST"
cp "$TMP/up/$SKILL_SRC" "$DEST/$SKILL_DEST"
for spec in $EXTRA; do
  src="${spec%%:*}"; dst="${spec##*:}"
  rm -rf "$DEST/$dst"
  [ -e "$TMP/up/$src" ] && cp -R "$TMP/up/$src" "$DEST/$dst"
done
find "$DEST" -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
echo "$NEW_COMMIT" > "$DEST/COMMIT"
[ -n "$NEW_VERSION" ] && echo "$NEW_VERSION" > "$DEST/VERSION"

echo
echo "applied. still to do by hand:"
echo "  1. update the '$LANG_CODE' row in VERSIONS.md (version $NEW_VERSION, commit $NEW_COMMIT, date)"
echo "  2. update the 'delegates' field in SKILL.md frontmatter"
echo "  3. spot-check references/pattern-map.md against upstream renumbering"
[ "$LANG_CODE" = "de" ] && echo "  4. smoke test: cd delegates/de && python3 scripts/humanizer_audit.py --file <file> --mode sachlich"
exit 0
