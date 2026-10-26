# House rules

Formatting rules for this author's own output. They override any delegate's style preference, because they are conventions of a specific repository and team rather than matters of taste. Scope: text this skill produces or edits.

## Commit messages

- Start with the Jira ticket prefix: `TAF-479: short summary`. In a personal repository with no tracker, use a plain descriptive subject instead.
- No conventional-commit prefixes. Not `feat(s3):`, not `fix:`, not `chore:`.
- Short and to the point. One line where one line suffices.
- No Markdown in the body; it does not render.
- Never add tool attribution of any kind, in commit messages, PR descriptions, comments or code.

## Pull requests

- Body covers what changed, why, what could break, how it was tested.
- Nothing gets published to GitHub — PR bodies, reviews, inline comments, replies, status changes — without showing the draft first and getting explicit approval, even when the content is finished and obviously correct.

## Language by destination

- Working sessions and internal reasoning: Russian.
- Team-facing documentation, READMEs, ADRs, code comments, commit messages: English.
- Anything addressed to German colleagues, authorities or vendors outside the engineering team: German.

Match the destination rather than the language of the conversation. A Russian-language working session that produces a README still produces an English README.

## Operational writing

- Rollout order, wherever it appears: experimental, then staging, then production. Never reordered for rhythm.
- Risky changes are described as happening after hours; do not soften that into "at a convenient time".
- Never describe a destroy-and-recreate operation as an option in a runbook for this infrastructure.
- Terraform text: plan before apply, always with `<env>.tfvars`, version constraints written as `~> X.Y.0`. Prefer Pod Identity naming over legacy IRSA.

## Process

- Plan first, then implement. A plan is presented and approved before work starts, and once approved it is implemented in full without being rewritten mid-flight.
- Never describe or suggest a proxy as a solution.

## Voice

English output follows the English delegate. What matters more is that self-description stays concrete: in a CV, a self-assessment or a project summary, every claim carries a number, a scale or a named system, and none of it is invented to fill the shape.
