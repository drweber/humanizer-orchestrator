# Pattern map

The three delegates number their patterns independently and **all three renumbered between the versions this project first vendored and the versions pinned now**: English went from 33 patterns to 26 with new names, Russian from 25 markers to 19, German kept its 72 with M-numbers. Findings keep their own delegate's identifier so they stay traceable upstream; this table is for cross-language comparison and for the degraded fallback when a delegate is missing.

**Pinned to the versions in `VERSIONS.md`.** A stale map is worse than no map, because a finding labelled with the wrong id sends the reader to a different pattern. After any delegate update, spot-check before trusting it. The scheduled sync workflow warns when a delegate's pattern headings change.

Alignment is approximate: where one project splits a concept the others merge, both entries appear.

| Concept | EN 3.1.0 | DE 5.28.2 | RU 4.1.5 |
|---|---|---|---|
| Negative parallelism, not X but Y | 1 | M8 | 2 |
| One-line closers, dramatic fragments | 2 | M51 | — |
| Aphorism formulas | 3 | M56 | — |
| Staged run-up, signposting | 4 | M33 | 1, 10 |
| Arguing with no one | 5 | — | — |
| Forced triads, rule of three | 6 | M9 | 8 |
| Repeated sentence openings, metronome rhythm | 7 | M55, M61 | 14 |
| Dashes | 8 | M16 | 16 |
| Stacked qualifiers, hedging | 9 | M41 | 17 |
| Hyphenated pairs | 10 | — | — |
| Passive voice, missing subjects | 11 | M39 | 4 |
| Bureaucratic register, канцелярит, Nominalstil | (in 11) | M58 | 4 |
| Overused AI words | 12 | M64 | — |
| Inflated significance | 13 | M1 | 3 |
| Vague connection or association | 14 | M10 | 6 |
| Shallow -ing riders | 15 | M10, M66 | 6 |
| Sales language, promotional tone | 16 | M2 | 18 |
| Borrowed authority, unnamed experts | 17 | M11 | 7 |
| Avoiding is, are, has | 18 | M65 | — |
| Bold as decoration | 19 | M13 | 15 |
| Decorative headings, emoji | 20 | M15 | 15 |
| Curly quotation marks, wrong quote form | 21 | M46 | — |
| Chatbot residue | 22 | M18 | 19 |
| Knowledge-limit disclaimers, gap-filling guesses | 23 | M19, M53 | 11 |
| Heading repeated in the first sentence | 24 | M34 | — |
| Writing about the document, diff-anchored prose | 25 | M52 | 11 |
| Re-explaining what the reader knows | 26 | — | 12 |
| Empty generalities | (in 26) | M44 | 12 |
| Connectives at every step | (in 4) | M62 | 13 |
| Moral or upbeat ending | (in 2) | M38 | 9 |
| Calques and false friends | — | M45 | 5 |
| Letter-style writing out of place | (in 22) | M17 | (in 19) |
| Placeholder text left in | (in 22) | M21 | (in 19) |
| Fabricated citation, invalid DOI | (global rule) | M26 | check_facts.py |
| Source does not support the claim | — | M42 | check_facts.py |
| Hidden Unicode, BOM, bidi controls | — | M43 | clean_paste.py |
| Vendor artefacts, utm tails, citation tokens | — | M24 | clean_paste.py |
| Decimal and date locale drift | — | M48 | — |
| Apostrophe errors | — | M49 | — |
| Synonym rotation for the same entity | — | M60 | — |
| Markdown residue in a non-Markdown target | (in 21) | M23, M57 | 15 |
| False agency, responsibility laundering | — | M70 | — |
| Retroactive pseudo-nuance | — | M71 | — |
| Pseudo-therapeutic validation | — | M72 | — |
| Modal particle anomaly | — | M63 | — |
| Register collapse | — | M69 | — |

## Owned by this orchestrator

Not in any delegate. See `references/technical-docs.md` and the artefact section of `SKILL.md`.

- Fabricated technical identifiers: flags, config keys, metric names, paths.
- Postmortems without timestamps; risks without owners or thresholds.
- Symmetric ADR trade-offs; migration guides with no rollback path.
- Mixed-language routing and cross-language misfiling.
- Homoglyph normalisation scoped to word-internal script mixing.
- Whitespace and paragraph density.
