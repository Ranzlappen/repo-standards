# Migrating from repo-standards v2 → v3

This page is a per-repo migration log. The standards repo's own [`CHANGELOG.md`](https://github.com/Ranzlappen/repo-standards/blob/main/CHANGELOG.md) is the canonical "what changed in v3" reference; this page is the **applied-to-this-repo** companion.

## TL;DR

v3 is largely additive over v2.1. The structural change is that `PROMPT.md` is now a thin entry-point index over six modular files under `prompt/`, including the new **Phase 0** migration-planning layer. Most repos finish the migration in 5–6 PRs, *after* Phase 0 produces the tailored roadmap:

1. **Phase 0 (planning, no commits).** Paste the v3 [`PROMPT.md`](https://github.com/Ranzlappen/repo-standards/blob/main/PROMPT.md) into a Claude Code session; the first thing Claude does is run [`prompt/migration-planning.md`](https://github.com/Ranzlappen/repo-standards/blob/main/prompt/migration-planning.md) — produce the repo profile, must/should/could/skip score, resumable batch roadmap, AI / token / session / fair-use guardrails, and Dependabot mitigation audit. Wait for user confirmation before Step 0.
2. Versioning bump (`VERSION` → `3.0.0`, `.standards-version` → `3` or `3.0.0`, standards-version badge `v2` → `v3`).
3. Modular prompt adoption — no per-repo template change needed; consumers don't ship `prompt/` themselves, they fetch it from this repo.
4. Supply-chain baseline — copy `templates/.github/workflows/dependency-review.yml` and `workflow-summary.yml` (with their `*.properties.json` sidecars) into the consumer repo's `.github/workflows/`.
5. Quality-baseline expansion — wire Lighthouse CI + `lighthouserc.json` budgets (web projects only), enforce branch-protection per `GOVERNANCE.md` "Recommended branch-protection rules" with **admin no-bypass**, enable GitHub Discussions if the repo collects long-form Q&A.
6. CHANGELOG entry + tag.

## Breaking changes you should know about

* **Phase 0 runs before Step 0.** Claude pauses for user confirmation of the migration roadmap before doing anything else. This is a gate, not optional.
* **Standards-version major bumped 2 → 3.** Update `.standards-version` and the `Standards` badge URL in `README.md`. Without the bump, `prompt/00-version-check.md` refuses on a v2 → v3 mismatch.
* **`Migration-v1-to-v2.md` is no longer the current migration guide.** Step 0's reference now points at this page (`Migration-v2-to-v3.md`). Repos still on v1 must complete the v1 → v2 migration first using the legacy `Migration-v1-to-v2.md`.
* **Branch-protection on `main` is non-negotiable** for v3-compliant repos (per `UPGRADE_CHECKLIST.md` Section 12, **admin no-bypass**). Solo maintainers who want `main` write access keep admin-bypass on but document the deviation.
* **Dependency-review on every PR.** Repos that haven't already adopted `templates/.github/workflows/dependency-review.yml` need to add it; it's required as a status check on `main` per `templates/.github/GOVERNANCE.md`.

## Per-repo migration entries

Append one entry per repo as you migrate it. Keep entries terse — a few bullets each.

### `<repo-name>` — <YYYY-MM-DD>

* **Standards version**: v2.x.y → v3.0.0
* **Phase 0 deliverable link**: <URL to the Phase 0 comment / PR comment>
* **Roadmap shape**: <e.g. "canonical 8-PR sequence", "single-PR alternative", "custom batched per repo profile">
* **PR sequence used**: <e.g. "PRs 1–6 in the canonical order, PR 7 skipped (no PWA)">
* **Deviations**:
  * <e.g. "Skipped Lighthouse CI — repo is a CLI tool with no web surface.">
  * <e.g. "Branch-protection admin-bypass kept on — solo maintainer.">
* **Follow-ups**:
  * <issue link>

### `<repo-name>` — <YYYY-MM-DD>

* ...

---

## When the standards bump again (v3 → v4)

A future v4 page will live alongside this one (`Migration-v3-to-v4.md`). The pattern repeats: TL;DR, breaking changes, per-repo entries.

If you only ever consume one repo on a single standards version and never migrate, you can delete this page from your wiki — but keeping it is cheap and helps future you.
