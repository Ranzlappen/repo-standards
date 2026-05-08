# Contributing to Ranzlappen Repo Standards

Thanks for considering a contribution. This repo is the source of the standards every other Ranzlappen repo adopts, so changes here ripple downstream — read [`README.md`](../README.md), [`PROMPT.md`](../PROMPT.md) (and the modular files under `prompt/`), and the relevant section of [`UPGRADE_CHECKLIST.md`](../UPGRADE_CHECKLIST.md) before opening a PR.

## Quick links

- [Open issues](../../issues) — bug reports, feature ideas, "the standards say X but should they say Y?".
- [Pull requests](../../pulls) — submit changes for review.
- [Code of Conduct](./CODE_OF_CONDUCT.md) — how we treat each other.
- [Governance](../templates/.github/GOVERNANCE.md) — roles, decision-making, branch-protection rules. (The template lives under `templates/`; this repo follows it directly.)
- [Security policy](./SECURITY.md) — how to report vulnerabilities privately.

## How to propose a change

1. **Open an issue first** for anything beyond a typo fix or a checklist clarification. The standards repo is a coordination point — aligning on the *what* avoids re-doing downstream work.
2. **Branch from `main`** with a short, descriptive name: `chore/v3-…`, `docs/clarify-rule-2`, `feat/scorecard-badge`. The canonical 8-PR sequence in [`PROMPT.md`](../PROMPT.md) Step 2 is the per-major upgrade flow; standalone changes use plain Conventional-Commits-shaped branch names.
3. **Keep PRs small.** One focused change per PR. The standards repo's own v2 → v3 upgrade landed as five batched commits on a single branch — that rhythm is documented in `prompt/02-canonical-pr-sequence.md` (after Batch 2 modularization) and is itself an option, not the default.
4. **Match the existing style.** `self-validate.yml` runs actionlint, lychee (offline link check), the SemVer assertion on `VERSION`, and the SHA-pinning lint on every `uses:` line. All four must be green before review.
5. **Update docs in the same PR** when behavior, scopes, or rule numbers change. Drift between `PROMPT.md`, `UPGRADE_CHECKLIST.md`, and `templates/CLAUDE.md.tmpl` is the single biggest source of pain — catch it in the same commit.

## Conventional commits

This project uses [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/). Short summary:

- `feat: …` — a new standard, template, or rule that consumers will adopt.
- `fix: …` — a bug fix in an existing rule, template, or workflow.
- `docs: …` — documentation only (README, CHANGELOG, REFACTORING_GUIDE clarifications).
- `refactor: …` — restructuring without changing semantics (Batch 2's `prompt/` split is the canonical example).
- `chore: …` — build, deps, tooling, anything not user-visible. Includes `chore(release): …` for version bumps.
- `ci: …` — changes to `.github/workflows/`.

Recommended scopes for changes in this repo: `dogfood`, `prompt`, `wf`, `docs`, `meta`, `checklist`, `security`, `governance`. Breaking changes (rule renumberings, template-shape changes that downstream repos can't trivially absorb) get a `!` and a `BREAKING CHANGE:` footer — they trigger a major-version bump.

## Pull request checklist

The PR template surfaces these automatically. Repeated here for reference:

- [ ] No accidental rule semantics change unless the PR explicitly says otherwise.
- [ ] Every cross-reference between `PROMPT.md` / `UPGRADE_CHECKLIST.md` / `templates/CLAUDE.md.tmpl` / `templates/README.md.tmpl` / `REFACTORING_GUIDE.md` updated together.
- [ ] CHANGELOG entry added under `[Unreleased]` for any rule-bearing change.
- [ ] CI green (actionlint + lychee + semver + SHA-pinning + workflow-properties pairing).
- [ ] No secrets, credentials, or unredacted personal data committed.
- [ ] Conventional commit message on the merge commit (squash-merge default).

## Reviewing

The repo owner is the sole maintainer at present (see [`CODEOWNERS`](./CODEOWNERS)). Triage target is one week; a PR sitting longer is in noise rather than ignored — ping the issue or PR.

## Community standards

Because this project is hosted on GitHub, contributions are governed by **three** community standards in addition to this repo's own [`CODE_OF_CONDUCT.md`](./CODE_OF_CONDUCT.md):

1. The [GitHub Community Guidelines](https://docs.github.com/en/site-policy/github-terms/github-community-guidelines) — what's expected of all GitHub users.
2. The [GitHub Acceptable Use Policies](https://docs.github.com/en/site-policy/acceptable-use-policies/github-acceptable-use-policies) — what GitHub disallows on its platform (spam, harassment, illegal content, malware, doxxing, etc.).
3. This repo's [Code of Conduct](./CODE_OF_CONDUCT.md) and [Security policy](./SECURITY.md).

Maintainers will close, hide, or report contributions that violate any of the three. Reporting routes: CoC concerns to the routes in `CODE_OF_CONDUCT.md`; platform-policy concerns to GitHub Trust & Safety via [github.com/contact/report-content](https://github.com/contact/report-content).

## License

By contributing, you agree that your contributions will be licensed under this repository's [MIT License](../templates/LICENSE).
