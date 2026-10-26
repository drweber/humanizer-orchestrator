#!/usr/bin/env bash
# Package self-check. Run locally or in CI; exits non-zero on any failure.
set -uo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"
fail=0
note() { printf '%-42s %s\n' "$1" "$2"; }
bad()  { note "$1" "FAIL: $2"; fail=1; }

# 1. exactly one SKILL.md, at the root
n=$(find . -name SKILL.md -not -path "./.git/*" | wc -l | tr -d ' ')
[ "$n" = "1" ] && [ -f SKILL.md ] && note "single SKILL.md at root" "ok" \
  || bad "single SKILL.md at root" "found $n (nested ones are read as separate skills)"

# 2. frontmatter name and description budget
name=$(sed -n 's/^name: *//p' SKILL.md | head -1)
[ "$name" = "humanizer" ] && note "frontmatter name" "ok ($name)" || bad "frontmatter name" "got '$name'"
desc=$(awk '/^description: \|/{f=1;next} f&&/^[a-z_]+:/{exit} f' SKILL.md | wc -c | tr -d ' ')
[ "$desc" -gt 0 ] && [ "$desc" -le 1024 ] && note "description <=1024 chars" "ok ($desc)" \
  || bad "description <=1024 chars" "$desc"

# 3. delegates present and pinned
for d in en de ru; do
  [ -f "delegates/$d/humanizer-$d.md" ] && [ -s "delegates/$d/COMMIT" ] \
    && note "delegate $d" "ok $(cat delegates/$d/VERSION 2>/dev/null) @$(cat delegates/$d/COMMIT)" \
    || bad "delegate $d" "missing entrypoint or COMMIT"
done

# 4. scripts compile
for f in scripts/*.py; do
  python3 -m py_compile "$f" 2>/dev/null && note "compile $(basename "$f")" "ok" || bad "compile $(basename "$f")" "syntax error"
done
for f in scripts/*.sh; do
  bash -n "$f" 2>/dev/null && note "parse $(basename "$f")" "ok" || bad "parse $(basename "$f")" "syntax error"
done

# 5. our own docs obey our own rules
python3 scripts/normalize_whitespace.py --check --target md SKILL.md README.md VERSIONS.md NOTICE.md references/*.md >/dev/null 2>&1 \
  && note "whitespace clean" "ok" || bad "whitespace clean" "run normalize_whitespace.py"
python3 scripts/strip_watermarks.py --check SKILL.md README.md VERSIONS.md NOTICE.md references/*.md >/dev/null 2>&1 \
  && note "no paste artefacts" "ok" || bad "no paste artefacts" "run strip_watermarks.py"

# 6. german linter runs from the vendored path
( cd delegates/de && printf 'Ein kurzer Satz zum Testen der Linter.\n' > /tmp/_hz_smoke.md \
  && python3 scripts/humanizer_audit.py --file /tmp/_hz_smoke.md --mode sachlich >/dev/null 2>&1 ) \
  && note "de linter smoke" "ok" || bad "de linter smoke" "humanizer_audit.py did not run"

find . -name "__pycache__" -exec rm -rf {} + 2>/dev/null
echo
[ "$fail" = "0" ] && echo "validate: PASS" || echo "validate: FAIL"
exit $fail
