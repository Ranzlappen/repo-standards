# Changelog

All notable changes to **repo-standards** are recorded here. Format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/) and the project uses [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

Consumer repos pin a major version (`v1`, `v2`, …) by referencing the matching git tag.

## [Unreleased]

### Added — PR 6: checklist expansion

- `UPGRADE_CHECKLIST.md` Section 10 — Security (CodeQL, secret scanning + push protection, Dependabot security alerts, SECURITY.md present, public-client-side-keys documented, .env hygiene, gitleaks-verified no-secrets-in-tracked-files).
- `UPGRADE_CHECKLIST.md` Section 11 — Accessibility / Performance / SEO (Lighthouse defaults Perf 80 / A11y 95 / BP 95 / SEO 90, accessible names, focus order, contrast, meta tags incl. Open Graph, sitemap.xml, robots.txt, manifest icons resolve). Skippable for non-web projects with a one-line reason.
- `UPGRADE_CHECKLIST.md` Section 12 — Testing & Quality (smoke tests, test command in CLAUDE.md, coverage thresholds matching pytest/vitest defaults, lint blocking in CI, Conventional Commits enforced via commit-msg hook, pre-commit installed by contributors, branch protection requires green CI, flaky tests get a label or issue rather than a TODO).
- `UPGRADE_CHECKLIST.md` Section 13 — Standards Versioning (.standards-version file, README badge, Upgrade-History wiki entry, CHANGELOG entry for standards-version-relevant changes, consumer-side references pinned to a tag, no mixed-version state).

### Changed

- `UPGRADE_CHECKLIST.md` "How to score a repo" — extended scoring to include sections 9 (Wiki) and 10–13 (Security, A11y, Testing, Versioning). Wiki and A11y skippable for non-applicable repos; Security and Standards Versioning non-negotiable for v2 compliance.

### Added — PR 5: PROMPT.md hardening

- `PROMPT.md` Step 0 — Standards version check preamble. Fetches the standards `VERSION` and the consumer repo's declared version (`.standards-version` file, README badge, or CLAUDE.md note); refuses on major mismatch, asks the user in offline-fallback mode, and proceeds otherwise.
- `PROMPT.md` ground rules 9–12 — Tiny commits (one file per response), Conventional Commits required, mandatory post-task self-check on every code-change commit, no PR opens without explicit user confirmation. These were the implicit rules followed throughout this v2 upgrade; codifying them so every downstream upgrade follows the same rhythm.
- `PROMPT.md` Step 2 — Canonical 8-PR sequence (`chore/v2-versioning-meta` through `chore/v2-readme-and-tag`) with branch names, per-PR scope, hard-ordering and practical-execution rules. Replaces the previous loose "1, 2, 3, optionally 4" guidance.

### Changed — PR 7: dependabot tightening

- `templates/.github/dependabot.yml` now applies the v2 expectations across every ecosystem entry: explicit `open-pull-requests-limit: 10`, `labels: ["dependencies", "<ecosystem>"]` for triage, conventional `commit-message` prefixes (`chore(deps)` / `chore(deps-dev)` plus `include: "scope"`), and dev-vs-prod group split for npm and pip (dev bumps no longer block prod review). The previously-bare `bundler` entry now matches the rest. Sub-app npm entry mirror-updated in the commented-out block so consumers uncomment a complete row.
- `UPGRADE_CHECKLIST.md` Section 2 (Repo hygiene) — the single dependabot bullet is now a sub-checklist mirroring the v2 dependabot.yml shape.

### Added — PR 4: CI hardening

- `templates/.github/workflows/lint-and-test.yml` — reusable `workflow_call` workflow with `language` input (node | python | static-html | mixed). Single entry point for lint+test across stacks.
- `templates/.github/workflows/security-scan.yml` — CodeQL static analysis (matrix on language, security-extended query suite) + Gitleaks full-history secret scan. Triggers on PR, push to main, and weekly Monday 06:00 UTC schedule.
- `templates/.github/workflows/release-please.yml` — Conventional-Commits-driven release-please integration. Disabled by default (`if: false`); maintainer enables explicitly.

### Changed — PR 4: existing workflows hardened

Every existing workflow now declares a least-privilege `permissions:` block, has every `uses:` line pinned to a 40-char commit SHA (with major-version trailing comment), and sets `timeout-minutes` on each job. Hardened workflows:

- `templates/.github/workflows/ci-node.yml` (timeout 15).
- `templates/.github/workflows/ci-python.yml` (timeout 15; lint/test tools now cached via `requirements-dev.txt`, no more inline `pip install`).
- `templates/.github/workflows/ci-static-html.yml` (timeout 10).
- `templates/.github/workflows/ci-android.yml` (timeout 30).
- `templates/.github/workflows/pages-deploy.yml` (timeout 15; permissions already correct, only SHA-pinning + timeout added).
- `.github/workflows/self-validate.yml` — SHA-pinned all `uses:` lines, **flipped the SHA-pinning lint job from soft warn to hard fail** (any non-SHA pin is now an `::error` and the job exits 1).
- `.github/workflows/tag-release.yml` — SHA-pinned `actions/checkout`.
- `.github/workflows/auto-tag.yml` — SHA-pinned `actions/checkout`.

### Changed — PR 4: checklist

- `UPGRADE_CHECKLIST.md` Section 3 (CI / GitHub Actions) tightened with the v2 requirements: workflow-scope `permissions:`, 40-char SHA-pin + trailing major-version comment, `timeout-minutes` per job (with default-by-stack values), pinned+cached lint/test tools, mandatory `security-scan.yml`, and reusable-workflow availability.

### Added — PR 3: wiki templates and Wiki seeding phase

- `templates/wiki/Home.md` — landing page with task-oriented "where to look" table.
- `templates/wiki/Architecture.md` — long-form architecture companion that defers to `CLAUDE.md` on disagreement.
- `templates/wiki/Upgrade-History.md` — append-only ledger of repo-standards upgrades.
- `templates/wiki/FAQ.md` — categorised FAQ skeleton (Using, Contributing, Operations, Standards).
- `templates/wiki/PWA-Safety.md` — links to `REFACTORING_GUIDE.md`'s PWA Refactor Addendum (single source of truth, no duplication).
- `templates/wiki/Migration-v1-to-v2.md` — per-repo migration log with v1 → v2 breaking-change summary.
- `templates/wiki/_Sidebar.md` — wiki sidebar grouped into Getting started / Architecture / Operations / Standards.
- `templates/wiki/_Footer.md` — single-line footer linking back to README, CLAUDE.md, Issues, and the standards version.
- `PROMPT.md` Step 4 (optional): Wiki seeding phase. Skipped by default; user-opt-in only. Manual paste via the GitHub web UI; no automated `.wiki.git` push.
- `UPGRADE_CHECKLIST.md` Section 9: Wiki (optional). Page-existence and structural invariants (append-only Upgrade-History, link-not-duplicate PWA-Safety, CLAUDE.md-wins Architecture).

### Added — PR 2: community files and tooling templates

- `templates/.github/PULL_REQUEST_TEMPLATE.md` — mirrors the PR description structure required by `PROMPT.md` Step 3, with optional PWA-specific verification block.
- `templates/.github/ISSUE_TEMPLATE/` — `config.yml` (no blank issues) plus YAML forms for bug, feature, question, and a Markdown `upgrade_request.md` that pre-fills the `@claude` upgrade flow.
- `templates/.github/CODE_OF_CONDUCT.md` — short stub linking to Contributor Covenant 2.1 (issue [#4](https://github.com/Ranzlappen/repo-standards/issues/4) tracks optional inlining).
- `templates/.github/CONTRIBUTING.md` — short contributor guide with inline conventional-commits cheat sheet.
- `templates/.github/SECURITY.md` — disclosure policy with private-reporting channel, response SLAs, supported-versions table.
- `templates/.github/FUNDING.yml` — sponsor-button skeleton, all platforms commented.
- `templates/.github/CODEOWNERS` — ownership-map skeleton with security-sensitive-paths section.
- `templates/.editorconfig` — cross-editor whitespace + encoding rules.
- `templates/.prettierrc` and `templates/.prettierignore` — Prettier formatting config.
- `templates/eslint.config.mjs` — ESLint 9 flat config starter.
- `templates/ruff.toml` — Ruff lint + format config.
- `templates/pyproject.toml.example` — Python project skeleton with pytest config.
- `templates/vitest.config.ts` — JS/TS testing starter.
- `templates/android-lint.xml` — Android Lint config.
- `templates/.pre-commit-config.yaml` — pre-commit hooks (hygiene, ruff, prettier, markdownlint, gitleaks, conventional-commit-msg).
- `templates/.markdownlint.json` — markdownlint config.
- `templates/.env.example` — documented environment-variable skeleton.
- `templates/docs/README.md` — starter folder explaining publishing options (plain Markdown / GitHub Pages + Jekyll / VitePress / MkDocs).

### Changed

- `templates/.gitignore.example` — expanded into seven well-commented sections (Secrets first, then Node/Vite, Python, JVM/Android, Static sites, Firebase/cloud, IDEs, OS noise, Misc) with explanatory comments per section.
- `templates/README.md.tmpl` — added a badge block (CI / License / Standards-version) and surfaced the LICENSE file with a one-sentence MIT summary instead of placeholder text.
- `templates/CLAUDE.md.tmpl` — added Conventional Commits, Testing, and Security & Secrets sections (template now 184 lines, still under the 200-line target).

## [2.0.0-rc.1] — 2026-05-08

### Added
- `VERSION` file at repo root declaring the current standards version.
- `CHANGELOG.md` at repo root.
- `.github/workflows/tag-release.yml` — manual `workflow_dispatch` helper that creates and pushes annotated tags from a GitHub runner (used to publish `v1.0.0` retroactively and `v2.0.0` / `v2` at release time).

### Notes
- This is the first release candidate of the v2 standards. Final v2.0.0 ships once all eight planned PRs land. See the v2 implementation plan for the full sequence.

[Unreleased]: https://github.com/Ranzlappen/repo-standards/compare/v2.0.0-rc.1...HEAD
[2.0.0-rc.1]: https://github.com/Ranzlappen/repo-standards/releases/tag/v2.0.0-rc.1
