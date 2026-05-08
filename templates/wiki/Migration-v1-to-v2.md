# Migrating from repo-standards v1 → v2

This page is a per-repo migration log. The standards repo's own [`CHANGELOG.md`](https://github.com/Ranzlappen/repo-standards/blob/main/CHANGELOG.md) is the canonical "what changed in v2" reference; this page is the **applied-to-this-repo** companion.

## TL;DR

v2 is additive over v1. Most repos finish the migration in 6–8 PRs:

1. Versioning + meta-CI scaffold (`VERSION`, `CHANGELOG.md`, `self-validate.yml`, `tag-release.yml`, `auto-tag.yml`).
2. Community files + tooling (issue forms, PR template, CoC, CONTRIBUTING, SECURITY, FUNDING, CODEOWNERS, `.editorconfig`, prettier, eslint, ruff, pyproject + pytest, vitest, android-lint, pre-commit, markdownlint, `.env.example`, expanded `.gitignore.example`, `docs/`).
3. Wiki templates (this folder).
4. CI hardening (least-privilege `permissions:`, SHA-pin every `uses:`, `timeout-minutes`, reusable `lint-and-test`, `security-scan`, `release-please`).
5. Dependabot tightening (limits, conventional-commit prefixes, labels, npm dev/prod split, github-actions ecosystem block).
6. PROMPT.md hardening (version preamble, tiny-commits rule, mandatory post-task self-check, canonical 8-PR sequence).
7. Checklist expansion (Security, A11y/Perf/SEO, Testing & Quality, Standards Versioning sections).
8. README "Next-level features" + version bump + tag.

## Breaking changes you should know about

* **`PROMPT.md` now refuses to upgrade unless the consumer's declared standards version matches.** Add a `.standards-version` file at the repo root containing the major version (e.g. `2`). Without it, Claude Code falls back to "latest major" and may emit a confirmation prompt.
* **CI workflows now require `permissions:` blocks.** Existing workflows without one will fail the new self-validate hard-fail rule once PR 4 merges.
* **`uses:` lines must be pinned to a 40-char SHA.** Major-version pins (`@v6`) get a soft warn during PR 1–3 and a hard fail from PR 4 onward.

## Per-repo migration entries

Append one entry per repo as you migrate it. Keep entries terse — a few bullets each.

### `<repo-name>` — <YYYY-MM-DD>

* **Standards version**: v1 → v2.0.0
* **PR sequence used**: <e.g. "PRs 1–8 in the canonical order">
* **Deviations**:
  * <e.g. "Skipped vitest config — repo is Python-only.">
  * <e.g. "Kept `start_url` in manifest as-is per PWA safety.">
* **Follow-ups**:
  * <issue link>

### `<repo-name>` — <YYYY-MM-DD>

* ...

---

## When the standards bump again (v2 → v3)

A future v3 page will live alongside this one (`Migration-v2-to-v3.md`). The pattern repeats: TL;DR, breaking changes, per-repo entries.

If you only ever consume one repo on a single standards version and never migrate, you can delete this page from your wiki — but keeping it is cheap and helps future you.
