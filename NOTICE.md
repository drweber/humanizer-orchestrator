# Licences and attribution

This project is an orchestrator around three independent humanizer projects, vendored under `delegates/`. Their pattern catalogues are their authors' work, not this project's. Each delegate directory keeps its own upstream `LICENSE`; those files are authoritative. Pinned versions in `VERSIONS.md`.

## delegates/en — blader/humanizer 3.1.0

MIT, Copyright (c) 2025 Siqi Chen. https://github.com/blader/humanizer

Provides the English catalogue of 26 patterns, the invocation modes, the draft to audit to final loop, the never-invent-facts rule, voice calibration, the false-positive list and the signs-of-human-writing list. Based on the English Wikipedia page *Wikipedia:Signs of AI writing* by WikiProject AI Cleanup, CC BY-SA 4.0.

## delegates/de — marmbiz/humanizer-de 5.28.2

MIT AND CC-BY-SA-4.0, Copyright (c) 2026 Martin Moeller, with portions Copyright (c) 2025 Siqi Chen as a derivative of blader/humanizer. https://github.com/marmbiz/humanizer-de

Provides the German catalogue of 72 patterns with HIGH/MEDIUM/LOW severity, the Locker/Sachlich/Formal mode matrix, the multi-pass pipeline, Claim-Lock and Persona-Lock, the false-positive carve-outs with calibration data, and the dependency-free linters under `delegates/de/scripts/`. Based on the German Wikipedia pages on recognising AI-generated content, CC BY-SA 4.0.

The CC BY-SA 4.0 term applies to the Wikipedia-derived material in `delegates/de/references/patterns.md` and the corresponding catalogue tables. Redistribution of that material carries the same licence.

## delegates/ru — Vladimir-Human/humanizer-ru 4.1.5

MIT, Copyright (c) 2026 Vladimir. https://github.com/Vladimir-Human/humanizer-ru

Provides the Russian catalogue of 19 patterns, the genre-gated decision tree, the quantitative thresholds that refuse an authorship verdict, the untrusted-input isolation rules, and the `clean_paste.py` and `check_facts.py` scripts. Based on the Russian Wikipedia page on signs of generated text and the English *Signs of AI writing*, CC BY-SA 4.0.

The upstream `eval/` directory, including its benchmark corpus, is not vendored.

## delegates/text-hygiene — guillaumemeyer/watermarks-remover 0.7.0

MIT, Copyright (c) 2026 Guillaume Meyer and contributors. https://github.com/guillaumemeyer/watermarks-remover

Vendored from that project's `clean-user-facing-text` skill, which is self-contained and needs no service: the invisible and format-character table including tag characters, noncharacters, private-use areas and exotic spaces, NFKC normalisation, per-hit confidence levels, and the stylometry scorer. The `mark-classes.md` and `removal-matrix.md` references come from the same project's `remove-ai-marks` skill.

Not vendored from it: the `remove-ai-marks` HTTP client and its service, the Docker images, the benchmark corpora, and the `stealer/` module.

## This orchestrator

MIT. Original material, claiming no part of the above:

- `SKILL.md`: routing, arbitration between conflicting delegate rules, global rules, artefact-cleanup pipeline, whitespace policy, unified output contract.
- `references/routing.md`: language segmentation, genre gates applied across all three languages, cross-language finding ownership.
- `references/input-isolation.md`: untrusted-input handling, generalised from the Russian delegate to all three languages.
- `references/pattern-map.md`: crosswalk between the three numbering schemes.
- `references/technical-docs.md`: engineering and operational document tells, covered by none of the delegates.
- `references/house-rules.md`: this author's own conventions.
- `scripts/strip_watermarks.py` (homoglyph normalisation; the rest of its original character handling was retired in favour of the text-hygiene delegate), `scripts/normalize_whitespace.py`, `scripts/sync_delegates.sh`, `scripts/validate.sh`.
- The GitHub Actions workflows.

## Shared ancestry

All three delegates descend from WikiProject AI Cleanup material, and the German one descends additionally from blader/humanizer. That common root is why the three catalogues align as closely as `references/pattern-map.md` shows, and why the arbitration section is short: the disagreements concentrate in language-specific typography and register, not in the substance patterns.
