# Engineering documents

Read alongside the delegate when the text is a README, runbook, postmortem, ADR, PR description, commit message, incident update or Notion page, in any language. None of the three delegates covers this ground, and it is where a reviewer spots machine output fastest.

## The rule that outranks everything here

**Never invent a technical identifier.** No flag, config key, environment variable, metric name, API parameter, version or file path that is not in the source or verified. A fabricated `--enable-locality-aware-routing` looks exactly like a real flag, survives review, and fails in production. If one is needed and unavailable, describe the behaviour and mark `[VERIFY]`.

Same for numbers. A postmortem needs figures, but the figures come from the author.

## Structural tells

- **Purpose preamble.** "This document aims to provide a comprehensive overview of…" Say what the thing is, or delete the section.
- **Reassurance close.** "By following these steps you can ensure a smooth deployment." Delete.
- **A conclusion section in an operational document.** Runbooks do not conclude.
- **Heading restated as its first sentence.**
- **A benefits section** in a document about how to do a thing.
- **Symmetric ADR trade-offs:** two bullets for, two against, each generic enough to fit any pair of technologies. A real ADR is asymmetric, because one option is usually better and the content worth writing down is the specific cost of choosing it.
- **Every list exactly three items.**
- **Diff-anchored prose.** Documentation describing what changed rather than what is. Correct in a changelog, wrong in a README.

## Content tells

- **Postmortems without timestamps.** A real postmortem is timestamps, commands run, and what was believed at each point. Phase narration means nobody wrote down what happened.
- **Risks without owners or thresholds.** Who watches, at what number, and what do they do then?
- **Blameless turned actor-free.** A blameless postmortem still says which system did what.
- **Alert entries with no action.** If it does not say what to do, it is a description, not a runbook.
- **Migration guides with no rollback.** If no rollback path exists, that is the most important sentence in the document, and it is usually the missing one.

## PR descriptions and commit messages

- Restating the diff in prose. The reviewer can read the diff; they cannot read why.
- No reason for the change and no statement of what breaks if it is wrong.
- Chat residue in a commit body.
- Markdown that will not render where it is going.

Useful shape: what changed, why, what could break, how it was tested.

## CVs and self-descriptions

- Unfalsifiable claims: passionate, results-driven, proven track record, thrives in fast-paced environments.
- The job advert restated in synonyms.
- Achievements with no number, no timeframe, no scale.
- Enthusiasm substituting for evidence.

Replacement shape: what you were responsible for, at what scale, with a number, plus one thing that went wrong and what you did. Every specific comes from the person, never from the editor.

## What to leave alone

- **Lists, tables and numbered steps.** A runbook is steps. A comparison is a table.
- **Clipped imperatives inside procedures.** "No restart needed" is correct register in step 4.
- **Repeated identifiers.** The synonym-rotation rule is stricter here, not looser: call the same thing the same name every time. Never vary `production-galaxy` into "the production environment" for elegance.
- **Terminology and version numbers.**
- **Hedges that reflect real uncertainty.** "We think the trigger was the stuck CNI pod, but we could not reproduce it" is honest.
- **Consistent headings and sensible bolding.**
