# Steps 1 & 2 — Read, audit, and plan against the canonical 8-PR sequence

**Step 1** (read & audit) and **Step 2** (plan) of the canonical Claude Code upgrade flow indexed by [`PROMPT.md`](../PROMPT.md). The 8-PR table is the canonical mapping of branches → scopes for a v2 upgrade pass; consumer repos pin a major and follow this exact sequence (skipping any PR whose scope is empty for the repo, with a one-line reason).

Hard ordering and practical execution sequencing live below the table. Step 0 (`prompt/00-version-check.md`) must pass before Step 1 begins. The 15 ground rules in [`prompt/01-ground-rules.md`](./01-ground-rules.md) — especially rules 9 (tiny commits), 11 (post-task self-check), and 12 (no PR without confirmation) — apply to every commit made under this sequence.

---

## Step 1 — Read and audit

Read every top-level file in the repo. Read the entrypoints of every code
directory. Build a mental model of:
  - What this project does (one sentence)
  - How it's built and deployed
  - What languages, frameworks, and external services it uses
  - What conventions exist (naming, structure, error handling)
  - What's missing that the checklist requires

## Step 2 — Plan

Post a single comment (or your initial Claude Code response) containing:
  - One-sentence project summary
  - Detected stack and deployment shape
  - Checklist results: for each item, mark ✓ / — / ⚠️ with a short reason
  - Proposed PR sequence using the **canonical 8-PR template** below;
    omit any PR whose scope doesn't apply to this repo and say so explicitly
  - Refactoring opportunities found (whether or not you'll act on them)

### Canonical 8-PR sequence for v2 upgrades

Follow this order unless the audit shows a PR has nothing to do (in which
case skip with a one-line reason). PRs are sequential — PR N+1 only opens
after PR N merges.

| # | Branch | Scope |
|---|---|---|
| 1 | `chore/v2-versioning-meta` | `VERSION` + `CHANGELOG.md` + `self-validate.yml` + (if applicable) `tag-release.yml` and `auto-tag.yml`. |
| 2 | `chore/v2-community-and-templates` | `templates/.github/` community files + tooling configs + expanded `.gitignore.example` + `templates/docs/` + badge block + new CLAUDE.md.tmpl sections. |
| 3 | `chore/v2-wiki-templates` | `templates/wiki/*.md` + new optional Wiki phase in PROMPT + new section 9 in checklist. |
| 4 | `chore/v2-ci-hardening` | least-privilege `permissions:` blocks + 40-char SHA pinning + `timeout-minutes` + cached lint/test tools + reusable lint-and-test + security-scan + release-please. |
| 5 | `chore/v2-prompt-hardening` | PROMPT.md ground rules 9–12 + Step 0 version check + canonical 8-PR sequence. |
| 6 | `chore/v2-checklist-expansion` | `UPGRADE_CHECKLIST.md` new sections (Security, A11y/Perf/SEO, Testing & Quality, Standards Versioning). |
| 7 | `chore/v2-dependabot-tighten` | `dependabot.yml` v2 expectations: limits, conventional-commit prefixes, labels, npm/pip dev-vs-prod split. |
| 8 | `chore/v2-readme-and-tag` | Root README "Next-level features (v2)" + standards-version badge; bump VERSION to `2.0.0`; cut CHANGELOG; tag `v2.0.0` and `v2`. |

**Hard ordering** (what must come before what):
- PR 1 first.
- PRs 2, 3, and 7 can run in parallel after PR 1.
- PR 4 needs PR 2 done first.
- Then PR 5 → PR 6 → PR 8, strictly sequential.

**Practical execution** (one PR at a time): PR 1 → 2 → 3 → 4 → 7 → 5 → 6 → 8.

Skip any PR whose scope is empty for this repo (e.g. no PWA code → PR 4's
PWA-relevant subsections drop out; no Python code → ruff/pytest configs
in PR 2 are skipped).

WAIT for user confirmation before opening any PR. The plan is the
deliverable for this step.
