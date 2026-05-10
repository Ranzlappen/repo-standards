# Phase 0 — Migration planning & smart adoption

This is **Phase 0** of the canonical Claude Code upgrade flow indexed by [`PROMPT.md`](../PROMPT.md). It runs **before Step 0** (version check) and produces the strategic plan the rest of the flow executes against.

Why split this out? `UPGRADE_CHECKLIST.md` is 13 sections and ~200 line-items deep. Running every item against a 5k-LoC static site wastes the user's tokens, attention, and (when running via the GitHub Action) Anthropic API credits. A 200-line script doesn't need branch-protection-on-`main` quite the way a production PWA does. Phase 0 profiles the target repo, scores every checklist item by **effort × value × risk**, drops what doesn't apply, and packages the rest into resumable batches sized to fit a single Claude session.

The output of Phase 0 is the migration roadmap. Steps 1–4 of [`prompt/02-canonical-pr-sequence.md`](./02-canonical-pr-sequence.md) and beyond execute against that roadmap.

---

## When Phase 0 runs

- Always, on every upgrade pass, **before Step 0**.
- The output is posted as the **first** comment on the planning issue (GitHub Action flow) or as the **first** session response (direct Claude Code flow).
- The rest of the flow does **not** start until the user explicitly confirms the roadmap.

---

## 1. Repo profiling

Before scoring anything, build a structured profile of the target repo.

**Tech stack inference.** Read `package.json`, `pyproject.toml`, `Gemfile`, `build.gradle` / `build.gradle.kts`, `go.mod`, `Cargo.toml`, `index.html`, `manifest.json`, `service-worker.js` / `sw.js`. Catalogue: language(s), framework(s), build tool, deploy target.

**Project type.** One of:
- **PWA** — has manifest + service worker + cache strategy. Section 6 of the checklist applies in full.
- **Static-HTML site** — single or few HTML files, no build step (`worldmap`, `ticked`). Section 5 (single-file audit) applies.
- **Backend service** — exposes an HTTP/RPC interface or runs as a daemon.
- **Library** — published to npm / PyPI / Maven / etc., no end-user runtime of its own. Section 11 (A11y/Perf/SEO) is N/A.
- **CLI** — entrypoint is `bin/`, `__main__`, or similar. Section 11 is N/A.
- **Mobile / Android** — has `android/` or `AndroidManifest.xml`. Section 11 is N/A; SW/manifest items in Section 6 are N/A.
- **Repo-of-standards / docs-only** — like `repo-standards` itself. Most of Sections 5–7 are N/A.

**Size bucket.** Approximate with `find . -name '*.<ext>' -not -path './node_modules/*' -not -path './.git/*' | xargs wc -l` for the repo's primary extensions.
- **Small:** < 5k LoC.
- **Medium:** 5k – 50k LoC.
- **Large:** > 50k LoC.

**Complexity signals.**
- **Workflows count** — how many `.github/workflows/*.yml` files? (More than 5 → "complex CI".)
- **Dependency count** — direct deps in `package.json` / `pyproject.toml` / etc. (More than 50 → "heavy ecosystem".)
- **Mono vs. single** — multiple sub-apps under one repo? If yes, CI needs path-filtered jobs per app (per checklist Section 3).
- **Has GitHub Pages** — `_config.yml` or `gh-pages` branch present.
- **Has a deploy step** — workflows reference `peaceiris/actions-gh-pages`, `firebase deploy`, `vercel`, `cloudflare/wrangler-action`, etc.

**Owner profile.**
- **Solo** — single contributor, no Code Owners.
- **Small team** — 2–5 contributors, may have Code Owners.
- **Org-scale** — out of scope for this profiling pass; assume the org's own playbook overrides.

Output: a 5–8 line profile summary at the top of the Phase 0 artifact.

---

## 2. Score every checklist item

For each line in `UPGRADE_CHECKLIST.md` sections 1–13, assign three labels.

**Effort.**
- **S** — under 5 minutes. Single-file edit, no logic change. (Adding a badge, renaming a file, copying a template.)
- **M** — under 30 minutes. Multi-file edit or one new workflow. (Adding `dependency-review.yml`, wiring a Lighthouse CI baseline.)
- **L** — 2 hours or more. Real refactor, new test suite, behavior-affecting migration. (Splitting a 1200-line file per `REFACTORING_GUIDE.md`, adding coverage gates to a project that has no tests.)

**Value.**
- **S** — cosmetic or marginal. (A badge nobody clicks, an `assets/` folder rename.)
- **M** — hardening. (Branch protection rules, OpenSSF Scorecard, pre-commit hooks.)
- **L** — non-negotiable. (Secret scanning on, CodeQL on, `.standards-version` present, license file present, no committed secrets.)

**Risk.**
- **S** — zero-risk doc edit. Markdown only, no behavior change, no CI impact.
- **M** — low-risk config / CI change. May fail CI once until tuned, but no user-facing impact.
- **L** — behavior-affecting. Touches the SW, the precache list, storage keys, deploy config, or anything Section 6 (PWA) covers. Requires the `pwa-inventory.md` discipline.

**Bucket.**
- **must** — high value (L) AND low/medium risk (S/M). Ships in the first batches.
- **should** — medium value (M) AND any risk. Ships after the musts.
- **could** — low value (S) AND low effort (S). Ships if there's session budget left.
- **skip** — not applicable to this stack / project type. State the reason in one line per skip.

Output: a Markdown table with columns `Item | Effort | Value | Risk | Bucket | Notes`. Items batched together (e.g. all the `dependabot.yml` sub-items in checklist Section 2) collapse to one row with a parent-item summary.

---

## 3. Tailored migration roadmap

Order the **must** and **should** items into resumable batches. Each batch is one PR (canonical 8-PR mode) or one commit on a long-lived feature branch (single-PR mode — see [`templates/CLAUDE.md.tmpl`](../templates/CLAUDE.md.tmpl) "Alternative Operating Mode").

**Batch sizing.** Default 5–8 commits per batch, target ~1 hour of work per batch. Smaller batches (2–3 commits) are fine for risky items; larger batches (10+) compromise resumability.

**Inter-batch dependencies.** Note hard ordering — mirror the hard-ordering block from [`prompt/02-canonical-pr-sequence.md`](./02-canonical-pr-sequence.md):
- Versioning + meta first.
- Community + templates and CI hardening can run in parallel after that.
- Prompt / checklist hardening waits for community + templates.
- Final README + tag bump waits for everything.

State each dependency as "Batch N+1 needs Batch N done first" so the user knows what they can re-order vs. not.

**Output:** an ordered list of batches, each with its commits, its dependencies, and its expected runtime.

---

## 4. AI / token / session / fair-use guardrails

Phase 0 is also where the AI tooling's own constraints get surfaced. Failing to do this is how a session crashes mid-PR-7 and loses context that can't be rebuilt.

**Token budget per turn.** Keep each response under ~30% of the model's context window. Summarize long tool-result dumps (full-repo `find`, large file reads) in-context and discard the raw output once consumed. Respect compaction — if the harness compacts, restate the current batch goal in the next turn so the compacted summary doesn't lose the thread.

**Session length.** Cap continuous work at ~4 hours per session. Beyond that, accuracy degrades and the user loses the ability to review at the same pace Claude generates. Recommend a break + resume on a fresh session with the plan file (preserved across sessions per [`prompt/01-ground-rules.md`](./01-ground-rules.md) rule 15) as the resume point.

**Fair use.** Stay within Anthropic's API usage policy. If the GitHub Action flow hits rate limits, distribute work across sessions (one PR per session) rather than blocking on a single long-running run.

**Tiny resumable batches.** Every batch ends with a clean commit + push. Surface this guarantee to the user up front: "if my session crashes, the worst case is you lose at most one batch's worth of in-progress edits — the previously-committed batches are safe in git." This is the operational reason Phase 0 produces small batches even when the technical scope of an upgrade is large.

---

## 5. Dependabot PR spam mitigation

Dependabot, with default settings, generates one PR per dependency update. On a busy repo this means 20+ PRs per week — spam that nobody reviews and that ends up auto-merged or auto-closed without scrutiny. The [`templates/.github/dependabot.yml`](../templates/.github/dependabot.yml) shipped from v2 already implements the spam-mitigation rules below; Phase 0's job is to confirm they're applied to **this** repo.

**Required configuration** (verify each in the target repo's `.github/dependabot.yml`):

- **Grouping** — `groups:` block per ecosystem. Minor + patch updates land in **one** PR per group, per week. Majors land one per PR for individual review.
- **Weekly schedule** — `interval: "weekly"` on every entry. Daily produces too much noise.
- **`open-pull-requests-limit: 10`** — caps the queue depth so Dependabot doesn't pile up 50 open PRs during a slow review week.
- **Labels** — `dependencies` + ecosystem tag (`npm`, `python`, `github-actions`, etc.) so triage filters and the auto-merge workflow can find Dependabot PRs.
- **Conventional-commit prefixes** — `prefix: "chore(deps)"` for production deps, `prefix-development: "chore(deps-dev)"` for dev deps (where the ecosystem distinguishes), `include: "scope"` so the package name lands in the commit subject.
- **Dev / prod split** — separate groups per `dependency-type` for npm and pip so dev-tool bumps don't block prod-dep review and vice versa.

**Auto-merge** is **not** a `dependabot.yml` feature — it's a separate concern. Recommend (in the Phase 0 output) one of:
- GitHub's native **"Allow auto-merge"** repo setting + branch-protection required-status-checks. Author enables auto-merge on the PR; the merge fires when CI is green. Patch + minor only; majors stay manual.
- A workflow-side **labeled-auto-merge** action that watches `dependencies` + `chore(deps)` patch/minor PRs and enables auto-merge on them.

**`CODEOWNERS`** — a `*` line in `.github/CODEOWNERS` ensures every Dependabot PR lands in a human's review queue. Without this, Dependabot PRs sit unassigned and rot.

If any of these are missing in the target repo, **Phase 0 promotes them into the migration roadmap** (typically as part of the same batch as the rest of Section 2 / Section 3 hygiene work).

---

## 6. Output artifact

Phase 0 produces a single Markdown document containing:

1. **Repo profile** — the 5–8 line summary from Section 1.
2. **Scoring table** — the must / should / could / skip table from Section 2.
3. **Migration roadmap** — the ordered batches from Section 3, with inter-batch dependencies and expected runtime.
4. **Guardrails acknowledgement** — one line confirming the session-budget, fair-use, and tiny-resumable-batches guarantees from Section 4.
5. **Dependabot mitigation status** — confirmation that the rules in Section 5 are present in the target repo's `dependabot.yml`, or a callout that they need to land as part of the roadmap.

**In the GitHub Action flow:** post this as the first comment on the issue. Wait for the user to reply with "approved" (or a redlined version of the roadmap) before invoking Step 0.

**In the direct Claude Code flow:** post this as the first response in the session. Wait for the user to confirm before invoking Step 0.

**What counts as confirmation (both flows):** clicking the **"Approve plan mode"** button — or replying with "yes", "approved", "proceed", "confirmed", "go ahead", a 👍 reaction on the plan comment, or similar — counts as explicit confirmation.

After confirmation, hand off to [`prompt/00-version-check.md`](./00-version-check.md) and proceed through the canonical flow.

---

## 7. Conflict / Assumption Failure Protocol (execution-phase reminder)

The roadmap Phase 0 produces is a *prediction*. Reality during execution will sometimes contradict it — a file the plan assumed exists doesn't, a CI check gates the merge in an unexpected way, a `git push` is rejected, an audit uncovers behavior the profiling missed.

When that happens, the protocol is **non-negotiable** (rule 16 in [`prompt/01-ground-rules.md`](./01-ground-rules.md)):

> **Conflict / Assumption Failure Protocol** (critical safety rule)
> If at any point during execution you discover that an assumption in the Phase 0 plan or any later step was wrong, or you encounter an unexpected problem, **do not make any self-decided compromises or adjustments**. Immediately stop, clearly state the exact issue and the assumption that failed, propose 2–3 concrete options with trade-offs, and wait for my explicit confirmation before proceeding. Never silently alter the plan, skip steps, or decide on a workaround yourself.

This protocol overrides every other rule when they conflict (including rule 8 "Default to autonomy"). The Phase 0 deliverable should explicitly acknowledge that this protocol is in effect — add one line to the **Guardrails acknowledgement** in Section 6 confirming "Conflict / assumption-failure protocol acknowledged: any plan deviation stops for explicit confirmation."
