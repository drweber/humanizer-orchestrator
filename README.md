# humanizer-orchestrator

A Claude skill that removes the signs of AI-generated writing from text in **English, German and Russian**, and writes prose that does not carry them in the first place.

It is an orchestrator. It carries no pattern catalogue of its own: it routes each passage to a vendored language specialist, arbitrates where their rules contradict each other, and adds the layers none of them cover.

## Install

```bash
# Claude Code
unzip humanizer.zip -d ~/.claude/skills/

# Claude Desktop / claude.ai
# Settings > Capabilities > enable "Code execution and file creation",
# then Customize > Skills > + > upload the zip
```

Build the zip from a checkout with `scripts/build_zip.sh`, or clone straight into `~/.claude/skills/humanizer`. No dependencies: the vendored linters are standard-library Python 3.

## Delegates

Each is the native authority for its language, based on that language's own Wikipedia guidance rather than a translation of the English one.

| Language | Upstream | Catalogue |
|---|---|---|
| English | [blader/humanizer](https://github.com/blader/humanizer) 3.1.0 | 26 patterns |
| German | [marmbiz/humanizer-de](https://github.com/marmbiz/humanizer-de) 5.28.2 | 72 patterns, HIGH/MEDIUM/LOW, plus working linters |
| Russian | [Vladimir-Human/humanizer-ru](https://github.com/Vladimir-Human/humanizer-ru) 4.1.5 | 19 patterns, genre gates, count thresholds |

They are vendored at pinned commits under `delegates/`, not installed as separate skills, so that this orchestrator is the single entry point. A scheduled workflow keeps them current by pull request.

## What the orchestrator adds

**Arbitration**, because the three genuinely contradict each other. The sharpest case is the dash: English treats it as a universal connector to be removed, German requires the spaced Gedankenstrich and treats the unspaced English em dash as the tell, Russian treats тире as mandatory in a copula-less sentence. A dash policy never crosses a segment boundary, so a mixed-language file legitimately ends up with dashes in its German and Russian passages and none in its English prose.

**Mixed-language routing.** Segment first, then route. A Russian paragraph never goes to the German delegate because the file is mostly German. Quoted strings, identifiers, UI labels and error messages stay in their own language and are not restyled at all.

**Artefact and homoglyph cleanup**, run before analysis because invisible characters distort the German rhythm metrics. Homoglyphs are normalised automatically but only inside a single word, where the majority script wins — so `cоnfig` with a Cyrillic `о` becomes Latin while `конфиг` is untouched. Inside a URL or bare domain a mixed-script word is reported and left alone: rewriting a hostname changes where the link points, and a mixed-script domain is a phishing signal for a human to look at.

**Engineering documentation**, covered by no delegate: postmortems without timestamps, symmetric ADR trade-offs, risks without owners, migration guides with no rollback, and fabricated flags or config keys.

**Untrusted-input isolation**, generalised from the Russian delegate to all three languages, because the input is always text someone else may have written and it arrives in the same channel as instructions.

**Global rules that outrank every delegate:** never invent facts, technical identifiers or personal experience; never trade quality for a detector score; a null edit is a valid result.

## Tooling

```bash
./scripts/validate.sh                                          # package self-check

python3 delegates/ru/scripts/clean_paste.py FILE --in-place    # citation tokens, utm tails, zero-width
python3 scripts/strip_watermarks.py FILE                       # NBSP family, selectors, homoglyphs
python3 scripts/normalize_whitespace.py --target md FILE       # blank-line collapse

cd delegates/de && python3 scripts/humanizer_audit.py --file FILE --mode sachlich
```

Every script is idempotent and takes `--check`, which exits 1 on findings, so they work as pre-commit hooks. `strip_watermarks.py` refuses source files without `--force`, because a cleaner that hunts citation tokens will corrupt a regex literal that legitimately contains them.

## On watermarks

The cleanup removes characters that are defects in their own right: they break grep, diffs, terminals and CI, and they leak into commits.

It does not remove statistical watermarks such as SynthID-text, which are carried in the distribution of token choices rather than in characters. No character-level pass touches them, and this project makes no claim otherwise.

## Updating delegates

`.github/workflows/sync-delegates.yml` checks all three upstreams every morning and opens one pull request per delegate that moved, after running the full self-check. It never merges: vendored third-party content gets a human read, and an upstream renumbering silently invalidates `references/pattern-map.md`, which no script can repair. All three renumbered between the first vendoring and the versions pinned now, so this is a real failure mode rather than a hypothetical one.

Manual route and the per-delegate path maps are in `VERSIONS.md`.

## Licences

Three MIT projects vendored under `delegates/`, each keeping its own `LICENSE`; the German one is additionally CC-BY-SA-4.0 for its Wikipedia-derived catalogue. All three descend from WikiProject AI Cleanup material published under CC BY-SA 4.0. This orchestrator is MIT. Full attribution in `NOTICE.md`.
