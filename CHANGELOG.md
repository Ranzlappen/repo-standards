# Changelog

All notable changes to **repo-standards** are recorded here. Format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/) and the project uses [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

Consumer repos pin a major version (`v1`, `v2`, …) by referencing the matching git tag.

## [Unreleased]

## [2.0.0-rc.1] — 2026-05-08

### Added
- `VERSION` file at repo root declaring the current standards version.
- `CHANGELOG.md` at repo root.
- `.github/workflows/tag-release.yml` — manual `workflow_dispatch` helper that creates and pushes annotated tags from a GitHub runner (used to publish `v1.0.0` retroactively and `v2.0.0` / `v2` at release time).

### Notes
- This is the first release candidate of the v2 standards. Final v2.0.0 ships once all eight planned PRs land. See the v2 implementation plan for the full sequence.

[Unreleased]: https://github.com/Ranzlappen/repo-standards/compare/v2.0.0-rc.1...HEAD
[2.0.0-rc.1]: https://github.com/Ranzlappen/repo-standards/releases/tag/v2.0.0-rc.1
