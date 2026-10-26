# Routing

Step 2. Decide language, genre, scope and delegate ownership before any delegate loads. Getting this wrong is worse than a missed pattern: it applies one language's rules to another's grammar.

## 1. Language of each passage

Decide per passage, not per document. A passage is a paragraph, a list, a heading with its body, or a table cell block.

Signals, in order of reliability: script (Cyrillic to Russian), diacritics and ß (German), noun capitalisation mid-sentence with German function words, vocabulary otherwise.

Passages under roughly fifteen words are often ambiguous. Inherit the language of the surrounding passage rather than guessing, and say so if the choice affected a finding.

## 2. Never restyled, in any language

Treat as quotation. Do not route to a delegate at all.

- Code blocks, inline code, YAML and TOML frontmatter, JSON, config fragments.
- Identifiers: file paths, flags, keys, environment variables, metric names, cluster and service names, branch names, Jira keys.
- UI labels, error messages and log lines, including German ones inside English prose.
- Direct quotations with their original punctuation and quote marks.
- Legal and regulatory wording, standard names, clause references.
- Link targets. Link text is prose; the URL is not.

## 3. Genre gates, checked before style work

The Russian delegate encodes these most explicitly and the logic applies in all three languages.

| Genre | Consequence |
|---|---|
| Contract, normative act, policy under audit | Artefact removal only. No stylistic editing. Bureaucratic register is mandatory here. |
| Academic and scientific | Passive voice, hedging and explicit connectives are conventions, not tells. |
| Fiction, poetry, literary essay | Dashes, triads and complex syntax may be deliberate. Style patterns need corroboration from a second category. |
| Journalism, column, opinion | Triads and parallelism can be craft. Count them only in combination. |
| Marketing, blog, social | Full catalogue applies. |
| Operational and engineering docs | Full catalogue plus `technical-docs.md`, but lists, tables and clipped imperatives are correct register. |

If the text predates November 2022, check only artefacts and sources; the style catalogue does not apply.

## 4. Delegate ownership

| Segment | Delegate | Mode |
|---|---|---|
| Russian prose | `delegates/ru/` | genre first, then its decision tree |
| German prose | `delegates/de/` | `locker`, `sachlich` or `formal`; default `sachlich` and say so |
| English prose | `delegates/en/` | its own invocation mode |
| Mixed sentence, one language dominant with quoted foreign material | dominant language's delegate; quoted material untouchable | — |
| Genuine code-switching mid-clause | flag for the user, do not silently pick | — |

Never hand a passage to a delegate for a different language, even when the document is overwhelmingly in that other language.

## 5. Cross-language findings, which belong to the host language

- **Denglisch inside English prose.** An English-pass finding. The German delegate would not see it.
- **Anglicisms inside German prose.** German delegate, M45, which separates hard calques from false friends; `eventuell` meaning *eventually* and `aktuell` meaning *actually* are the canonical cases.
- **Calques inside Russian prose.** Russian delegate, its pattern 5.
- **Locale drift.** Belongs to the host language of the document, not of the number. `07/28/2026` in a German document is a German finding.
- **An English document written by a German or Russian speaker.** Nominalstil and канцелярит transfer into English as noun-heavy constructions with no actor. An English-pass finding even though the mechanism is imported.

## 6. Report assembly

1. Group findings by language, keeping each delegate's own identifiers.
2. Deduplicate where two delegates flagged the same span. Keep the finding from the delegate that owns the span.
3. Compute document-level observations across the whole file, not per segment.
4. State segment counts in the header so the reader knows what was routed where.

If one language accounts for the whole document, drop the segmentation reporting and produce a plain single-language report.
