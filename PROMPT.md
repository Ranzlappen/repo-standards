# Claude Code Upgrade Prompt

The standardized prompt for upgrading a Ranzlappen repo to the project's documentation, CI, and structural standards. Paste the entire **"Prompt to paste"** section below into a Claude Code session opened in the target repo, or into a GitHub issue tagged `@claude` if using the Claude Code GitHub Action.

The same prompt works in both flows.

## Modular structure

The actual rules, sequences, and step-by-step content live as seven focused files under [`prompt/`](./prompt/). `PROMPT.md` (this file) is the entry-point index — every cross-reference in `README.md`, `UPGRADE_CHECKLIST.md`, `REFACTORING_GUIDE.md`, and `templates/CLAUDE.md.tmpl` cites "`PROMPT.md` rule N" or "`PROMPT.md` Step N" (or "`PROMPT.md` Phase 0"), and those references land here and click through to the modular file.

The numbered files (`00`–`05`) are the canonical Step sequence. The unnumbered [`prompt/migration-planning.md`](./prompt/migration-planning.md) is **Phase 0** — the strategic-planning layer that runs *before* Step 0 and produces the tailored migration roadmap the rest of the flow executes.

| File | What's in it |
| --- | --- |
| [`prompt/migration-planning.md`](./prompt/migration-planning.md) | **Phase 0** — produce the tailored migration roadmap (repo profile + must/should/could/skip scoring + batch plan + AI-budget guardrails + Dependabot audit) before the version check. |
| [`prompt/00-version-check.md`](./prompt/00-version-check.md) | **Step 0** — refuse on major mismatch; the gate that keeps v3 rules off a v2 repo and vice versa. |
| [`prompt/01-ground-rules.md`](./prompt/01-ground-rules.md) | The **16 non-negotiable rules**: branching, behavior preservation, phased PRs, tiny commits, post-task self-check, plan-file hygiene, conflict / assumption-failure protocol, etc. |
| [`prompt/02-canonical-pr-sequence.md`](./prompt/02-canonical-pr-sequence.md) | **Step 1 + Step 2** — read & audit, then plan against the canonical 8-PR sequence with hard ordering and practical execution. |
| [`prompt/03-pr-description.md`](./prompt/03-pr-description.md) | **Step 3** — required PR description structure (Summary / Checklist coverage / Refactoring opportunities / Test plan). |
| [`prompt/04-wiki-seeding.md`](./prompt/04-wiki-seeding.md) | **Step 4** — optional, opt-in Wiki seeding via the GitHub web UI. |
| [`prompt/05-migration-debrief.md`](./prompt/05-migration-debrief.md) | **Step 5** — mandatory session-end debrief: what landed, what didn't and why, out-of-scope issues filed, follow-ups, repo-state delta. |

---

## Prompt to paste

```
You are upgrading this repository to **repo-standards v3.1.1** — the
self-dogfooding, AI-first standards toolkit at
https://github.com/Ranzlappen/repo-standards.

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
  - prompt/05-migration-debrief.md

## Phase 0 — Migration Planning & Smart Adoption (mandatory first step)

Per prompt/migration-planning.md, before touching any file:
  - Profile this repo's tech stack, size, complexity, architecture, and
    current state.
  - Score every UPGRADE_CHECKLIST.md item as must / should / could / skip
    by effort × value × risk for *this specific* project.
  - Produce a tailored migration roadmap respecting the canonical 8-PR
    sequence's hard ordering.
  - Surface AI / token / session / fair-use guardrails up front: each
    response under ~30% context, ~4-hour session cap, fair-use
    awareness, tiny resumable batches every batch ending with a clean
    commit + push so a session crash never loses work.
  - Audit Dependabot configuration against the v2 spam-mitigation rules
    and note any gaps.

Output the Phase 0 deliverable (profile + scoring table + roadmap +
guardrails ack + Dependabot status). WAIT for my explicit confirmation
before invoking Step 0. Clicking the **"Approve plan mode"** button — or
replying with "yes", "approved", "proceed", "confirmed", "go ahead", or
similar — counts as explicit confirmation.

## Non-negotiable ground rules (apply to every response)

The full 16 rules live in prompt/01-ground-rules.md. Headlines:

1. Behavior preservation (rule 2). Keep 100% of original functionality,
   user flows, UI, storage keys, URLs, deployment shape, observable
   behavior. Analyze the target repo *before* editing. Flag a
   "Repo-specific risks / edge-cases" subsection in every PR description
   and post-task self-check ("None observed" acceptable; heading
   mandatory).
2. Conflict / assumption failure protocol (rule 16). If any
   assumption from the Phase 0 plan or a later step proves wrong,
   or an unexpected problem hits mid-execution, STOP. Don't
   self-decide a workaround, don't silently alter the plan, don't
   skip steps. State the failed assumption + the exact issue,
   propose 2–3 concrete options with trade-offs, and wait for
   explicit confirmation before continuing.
3. Tiny commits (rule 9). One file (or one inseparable pair) per
   response, one Conventional Commit per change.
4. Post-task self-check (rule 11). Mandatory after every code-change
   commit — both drift-detection (per templates/CLAUDE.md.tmpl) and
   mechanical verification (files exist, YAML/JSON parses, links
   resolve, line-count delta matches the plan, no template placeholders
   remain in tracked files outside templates/).
5. Plan-file hygiene (rule 15). Never bloat plans with completed work
   — start fresh or actively prune.
6. Out-of-scope findings (rule 13). Auto-file a labeled GitHub issue by
   default; opt out via the repo variable
   DISABLE_OUT_OF_SCOPE_ISSUES=true.
7. No PR opens without explicit user confirmation (rule 12).
   Conventional Commits only.
8. Operating mode default = canonical 8-PR sequence (rule 14). The
   single-PR alternative mode is opt-in for focused work that would
   otherwise produce ≤3 PRs.

## After Phase 0 confirms

Run prompt/00-version-check.md (Step 0). On major mismatch, refuse and
tell the user. Then follow Steps 1–2 in
prompt/02-canonical-pr-sequence.md (read & audit + plan the canonical
8-PR sequence), Step 3 in prompt/03-pr-description.md (PR description
structure for every approved PR), and — if the user opts in — Step 4
in prompt/04-wiki-seeding.md (manual Wiki seeding via the GitHub web
UI), and finally Step 5 in prompt/05-migration-debrief.md (mandatory
session-end debrief unless the user explicitly skips it).

## Final note on adaptation

If anything in the standards genuinely doesn't fit this project, say so
in the Phase 0 plan and propose how to handle it. The standards are
meant to be lived with, not enforced robotically. If your audit reveals
something that should be added to UPGRADE_CHECKLIST.md or the templates
themselves, mention it — it's a separate PR against the standards repo.

Begin now with Phase 0 — produce the migration plan and wait for my
explicit confirmation before invoking Step 0.
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
