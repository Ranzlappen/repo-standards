# Changelog

All notable changes to **repo-standards** are recorded here. Format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/) and the project uses [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

Consumer repos pin a major version (`v1`, `v2`, …) by referencing the matching git tag.

## [Unreleased]

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
