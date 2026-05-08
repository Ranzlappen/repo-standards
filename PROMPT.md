# Claude Code Upgrade Prompt

The standardized prompt for upgrading a Ranzlappen repo to the project's documentation, CI, and structural standards. Paste the entire **"Prompt to paste"** section below into a Claude Code session opened in the target repo, or into a GitHub issue tagged `@claude` if using the Claude Code GitHub Action.

The same prompt works in both flows.

## Modular structure

The actual rules, sequences, and step-by-step content live as six focused files under [`prompt/`](./prompt/). `PROMPT.md` (this file) is the entry-point index — every cross-reference in `README.md`, `UPGRADE_CHECKLIST.md`, `REFACTORING_GUIDE.md`, and `templates/CLAUDE.md.tmpl` cites "`PROMPT.md` rule N" or "`PROMPT.md` Step N" (or "`PROMPT.md` Phase 0"), and those references land here and click through to the modular file.

The numbered files (`00`–`04`) are the canonical Step sequence. The unnumbered [`prompt/migration-planning.md`](./prompt/migration-planning.md) is **Phase 0** — the strategic-planning layer that runs *before* Step 0 and produces the tailored migration roadmap the rest of the flow executes.

| File | What's in it |
| --- | --- |
| [`prompt/migration-planning.md`](./prompt/migration-planning.md) | **Phase 0** — produce the tailored migration roadmap (repo profile + must/should/could/skip scoring + batch plan + AI-budget guardrails + Dependabot audit) before the version check. |
| [`prompt/00-version-check.md`](./prompt/00-version-check.md) | **Step 0** — refuse on major mismatch; the gate that keeps v3 rules off a v2 repo and vice versa. |
| [`prompt/01-ground-rules.md`](./prompt/01-ground-rules.md) | The **15 non-negotiable rules**: branching, behavior preservation, phased PRs, tiny commits, post-task self-check, plan-file hygiene, etc. |
| [`prompt/02-canonical-pr-sequence.md`](./prompt/02-canonical-pr-sequence.md) | **Step 1 + Step 2** — read & audit, then plan against the canonical 8-PR sequence with hard ordering and practical execution. |
| [`prompt/03-pr-description.md`](./prompt/03-pr-description.md) | **Step 3** — required PR description structure (Summary / Checklist coverage / Refactoring opportunities / Test plan). |
| [`prompt/04-wiki-seeding.md`](./prompt/04-wiki-seeding.md) | **Step 4** — optional, opt-in Wiki seeding via the GitHub web UI. |

---

## Prompt to paste

```
You are upgrading this repository to match the standards defined at:
  https://github.com/Ranzlappen/repo-standards

Before doing anything else, fetch and read these files from that repo:
  - README.md
  - UPGRADE_CHECKLIST.md
  - REFACTORING_GUIDE.md (includes the mandatory PWA Refactor Addendum)
  - templates/CLAUDE.md.tmpl
  - templates/README.md.tmpl
  - prompt/migration-planning.md
  - prompt/00-version-check.md
  - prompt/01-ground-rules.md
  - prompt/02-canonical-pr-sequence.md
  - prompt/03-pr-description.md
  - prompt/04-wiki-seeding.md

Then audit THIS repository against UPGRADE_CHECKLIST.md and produce one or more
pull requests that bring it into compliance.

Run Phase 0 first per prompt/migration-planning.md — produce the repo profile,
the must/should/could/skip scoring of UPGRADE_CHECKLIST.md, the tailored batch
roadmap with AI-budget guardrails, and the Dependabot mitigation status. WAIT
for user confirmation of the Phase 0 deliverable before invoking Step 0.

Then follow prompt/00-version-check.md. On a major mismatch, refuse and
tell the user.

Then follow prompt/01-ground-rules.md (the 15 non-negotiable rules — they
apply for every commit, every PR, every Step below).

Then follow Steps 1–2 in prompt/02-canonical-pr-sequence.md (read & audit,
then post the plan). WAIT for user confirmation before opening any PR.

For each approved PR, follow prompt/03-pr-description.md (PR description
structure) — and rule 12 (no PR opens without explicit user confirmation).

prompt/04-wiki-seeding.md is Step 4 — optional, opt-in only. Skipped by
default unless the user explicitly says "seed the wiki".

Final note on adaptation: if anything in the standards genuinely doesn't
fit this project, say so in the plan and propose how to handle it. The
standards are meant to be lived with, not enforced robotically. If your
audit reveals something that should be added to UPGRADE_CHECKLIST.md or
the templates themselves, mention that too — it's a separate PR against
the standards repo.

Begin with Phase 0 in prompt/migration-planning.md.
```

---

## Notes on the two flows

**GitHub Action flow (recommended for phone):**
- Open a new issue in the target repo with the title "Upgrade to repo standards" and the prompt above as the body, with `@claude` at the very top.
- Claude posts a plan as a comment.
- Reply to confirm the plan or adjust scope.
- Claude opens PRs sequentially. Review and merge each from the GitHub mobile app.

**Direct Claude Code session:**
- `cd` into the repo (or open it in the Claude Code Android app via `claude remote-control`).
- Paste the prompt.
- Same flow — plan, then PRs.

If you want Claude to handle the standards repo itself (not the target repo), just say "this is the standards repo, audit it for self-consistency instead" — the audit still applies.
