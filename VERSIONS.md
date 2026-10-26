# Vendored delegate versions

Each delegate is a self-contained directory. Updating one means replacing that directory and editing two lines. Nothing imports code across delegate boundaries, so they update independently and a stale delegate degrades only its own language.

## Pinned

| Language | Upstream | Version | Commit | Licence | Vendored |
|---|---|---|---|---|---|
| en | [blader/humanizer](https://github.com/blader/humanizer) | 3.1.0 | `8c307f3` | MIT | 2026-10-26 |
| de | [marmbiz/humanizer-de](https://github.com/marmbiz/humanizer-de) | 5.28.2 | `9248315` | MIT AND CC-BY-SA-4.0 | 2026-10-26 |
| ru | [Vladimir-Human/humanizer-ru](https://github.com/Vladimir-Human/humanizer-ru) | 4.1.5 | `9b1d29f` | MIT | 2026-10-26 |

Each delegate also carries `delegates/<lang>/VERSION` and `delegates/<lang>/COMMIT`, so a diff against upstream is possible without consulting this table.

## The automatic route

`.github/workflows/sync-delegates.yml` runs every morning at 05:00 UTC, checks all three upstreams, and opens one pull request per delegate that moved. It applies the sync and runs `scripts/validate.sh` before opening the PR, so a broken refresh never reaches review.

It deliberately does not merge. Vendored third-party content gets a human read, and an upstream renumbering silently invalidates `references/pattern-map.md`, which no script can repair. When the pattern count changes, the sync script prints a warning and the PR body carries it.

Two things must be enabled once in repository settings for this to work: Actions must be allowed to create pull requests, and the workflow needs `contents: write` plus `pull-requests: write`, which the file already declares. Note also that GitHub disables scheduled workflows in a public repository after sixty days without commits; a manual run from the Actions tab re-arms it.

Run it on demand from the Actions tab with `workflow_dispatch`, optionally naming a single delegate.

## Updating one delegate by hand

```bash
scripts/sync_delegates.sh de            # dry run, shows what changed
scripts/sync_delegates.sh de --apply
./scripts/validate.sh
```

Then, in all cases:

1. Update the row in the table above: version, commit, date.
2. Update the `delegates` field in `SKILL.md` frontmatter.
3. Spot-check `references/pattern-map.md`. This is the step that breaks silently.
4. For German, confirm the linters still run: `cd delegates/de && python3 scripts/humanizer_audit.py --file <some.md> --mode sachlich`.

## Upstream layouts differ and have moved

This is the trap that broke the first sync script, so the path map lives in `scripts/sync_delegates.sh` per delegate rather than being assumed:

| | instructions | references | scripts |
|---|---|---|---|
| en | `SKILL.md` at repo root | none | none |
| de | `skills/humanizer-de/SKILL.md` | `references/` at root | `scripts/` at root |
| ru | `skills/humanizer-ru/SKILL.md` | `skills/humanizer-ru/references/` | `skills/humanizer-ru/scripts/` |

The sync script fails loudly rather than vendoring a wrong file if an upstream `SKILL.md` is not where it expects.

## One rename on vendoring

Each upstream ships its instructions as `SKILL.md`, and a nested `SKILL.md` inside a skill directory is read as a separate skill. On vendoring each is renamed to `delegates/<lang>/humanizer-<lang>.md`. Nothing else is modified. The sync script does this automatically; `scripts/validate.sh` fails if a stray `SKILL.md` appears anywhere but the root.

## What is vendored per delegate

**en** — `humanizer-en.md` and its licence. Self-contained: no references, no tooling.

**de** — `humanizer-de.md`, `references/` (10 files, `patterns.md` is the large one), `scripts/` (15 files), `requirements-precise.txt`, licence and notice. The scripts are dependency-free; `requirements-precise.txt` covers the optional spaCy path for `--precise` only, and nothing here installs it.

**ru** — `humanizer-ru.md`, `references/` (`patterns.md`, `examples.md`), `scripts/` (`clean_paste.py`, `check_facts.py`), licence. The upstream `eval/` corpus is not vendored: it is large, it exists to benchmark that project, and it has no role here.

## Own scripts

Not vendored, maintained here:

| Script | Purpose |
|---|---|
| `scripts/strip_watermarks.py` | NBSP family, variation selectors, leftover citation tokens, homoglyph normalisation scoped to word-internal script mixing |
| `scripts/normalize_whitespace.py` | Blank-line collapse with `md`, `plain` and `commit` targets |
| `scripts/sync_delegates.sh` | Upstream refresh with per-delegate path maps and renumbering warning |
| `scripts/validate.sh` | Package self-check, also used by CI |

All are idempotent and offer `--check`, which exits 1 on findings so they work as pre-commit hooks.
