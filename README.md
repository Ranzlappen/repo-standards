# Ranzlappen Repo Standards

[![Standards](https://img.shields.io/badge/standards-v2.1.1-informational)](./VERSION)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](./templates/LICENSE)
[![Self-validate](https://github.com/Ranzlappen/repo-standards/actions/workflows/self-validate.yml/badge.svg)](https://github.com/Ranzlappen/repo-standards/actions/workflows/self-validate.yml)

A portable toolkit for upgrading my repos to a consistent, high-quality baseline. Distilled from the [`website`](https://github.com/Ranzlappen/website) repo, which is the working reference implementation.

This repo answers two questions:

1. **What does a "good" Ranzlappen repo look like?** → see the [templates](./templates/) and the [`UPGRADE_CHECKLIST.md`](./UPGRADE_CHECKLIST.md).
2. **How do I bring an existing repo up to that bar with Claude Code?** → paste [`PROMPT.md`](./PROMPT.md) into a Claude Code session opened in that repo, or open an issue tagging `@claude` with the same prompt.

## What's in here

| File | Purpose |
| --- | --- |
| [`VERSION`](./VERSION) | Current standards version (semver). Consumer repos pin a major via git tag (`v1`, `v2`, …). |
| [`CHANGELOG.md`](./CHANGELOG.md) | Notable changes per release. Keep-a-Changelog format. |
| [`UPGRADE_CHECKLIST.md`](./UPGRADE_CHECKLIST.md) | The audit Claude Code runs against any repo. Pass/fail items grouped by category. |
| [`REFACTORING_GUIDE.md`](./REFACTORING_GUIDE.md) | How to split big single-file projects into modules without changing behavior. |
| [`PROMPT.md`](./PROMPT.md) | The standardized Claude Code prompt. One prompt, applied repo by repo. |
| [`.github/workflows/`](./.github/workflows/) | This repo's own meta-CI: `self-validate.yml` lints docs/templates; `tag-release.yml` is a manual `workflow_dispatch` helper for publishing tags. |
| [`templates/CLAUDE.md.tmpl`](./templates/CLAUDE.md.tmpl) | Skeleton CLAUDE.md based on the website repo's structure. |
| [`templates/README.md.tmpl`](./templates/README.md.tmpl) | Skeleton README with the "Quick Reference" pattern. |
| [`templates/CHANGELOG.md.tmpl`](./templates/CHANGELOG.md.tmpl) | Keep-a-Changelog skeleton for downstream repos. |
| [`templates/.github/`](./templates/.github/) | Community files: PR template, issue forms (bug / feature / question / upgrade-request), CODE_OF_CONDUCT, CONTRIBUTING, GOVERNANCE, SECURITY, FUNDING, CODEOWNERS. |
| [`templates/.github/dependabot.yml`](./templates/.github/dependabot.yml) | Weekly dependency updates, sensible groupings. |
| [`templates/.github/workflows/`](./templates/.github/workflows/) | CI starters for Node, Python, static HTML, and Android. |
| [`templates/.editorconfig`](./templates/.editorconfig) | Cross-editor whitespace + encoding rules. |
| [`templates/.prettierrc`](./templates/.prettierrc) + [`.prettierignore`](./templates/.prettierignore) | Prettier formatting config and ignore list. |
| [`templates/eslint.config.mjs`](./templates/eslint.config.mjs) | ESLint 9 flat config starter. |
| [`templates/ruff.toml`](./templates/ruff.toml) | Ruff (Python lint + format) config. |
| [`templates/pyproject.toml.example`](./templates/pyproject.toml.example) | Python project skeleton with pytest + coverage config. |
| [`templates/vitest.config.ts`](./templates/vitest.config.ts) | Vitest starter for JS/TS testing. |
| [`templates/android-lint.xml`](./templates/android-lint.xml) | Android Lint config (drop into `app/lint.xml`). |
| [`templates/.pre-commit-config.yaml`](./templates/.pre-commit-config.yaml) | pre-commit hooks: hygiene, ruff, prettier, markdownlint, gitleaks, conventional-commit-msg. |
| [`templates/.markdownlint.json`](./templates/.markdownlint.json) | markdownlint config used by the pre-commit hook. |
| [`templates/.env.example`](./templates/.env.example) | Documented environment-variable skeleton. |
| [`templates/.gitignore.example`](./templates/.gitignore.example) | Combined .gitignore in named sections (Secrets, Node/Vite, Python, JVM/Android, Static sites, IDE, OS noise). |
| [`templates/docs/`](./templates/docs/) | Starter folder for project docs with publishing-options guide. |
| [`templates/.cursorrules`](./templates/.cursorrules) | Cursor IDE pointer file — defers to CLAUDE.md as architecture source of truth. |
| [`templates/ai/AI_TEAM_PLAYBOOK.md`](./templates/ai/AI_TEAM_PLAYBOOK.md) | Multi-AI coordination doc (Claude Code / Cursor / Copilot / Codex coexistence). |
| [`templates/wiki/`](./templates/wiki/) | GitHub Wiki templates: Home, Architecture, FAQ, Upgrade-History, PWA-Safety, Migration-v1-to-v2, _Sidebar, _Footer. |
| [`templates/LICENSE`](./templates/LICENSE) | MIT, matching the website repo. |

## Next-level features (v2)

What v2 adds on top of v1, in five sentences:

- **Versioned standards.** A repo declares which major it follows in `.standards-version`; PROMPT.md's Step 0 refuses to upgrade a v1 repo with v2 rules (or vice versa), and `auto-tag.yml` watches `VERSION` so each release tag is automatic.
- **Tiny-commit rhythm.** PROMPT.md ground rules 9–12 codify one file per response, Conventional Commits, mandatory post-task self-check, and explicit confirmation before any PR opens — the same rhythm this repo's own v2 upgrade followed end to end.
- **Hardened CI everywhere.** Every workflow declares least-privilege `permissions:`, every `uses:` line is pinned to a 40-char SHA (with a major-version trailing comment), every job has `timeout-minutes`, lint/test tools are pinned and cached, and a self-validate workflow hard-fails any future regression on those rules.
- **Security and quality baked in.** New `security-scan.yml` runs CodeQL + gitleaks on every PR, push to main, and weekly schedule; new `lint-and-test.yml` is a single reusable workflow with a `language` input; new `release-please.yml` ships disabled-by-default for projects that want Conventional-Commits-driven releases.
- **Phone-friendly batteries.** Templates ship for community files (PR template, four issue forms, CoC, CONTRIBUTING, SECURITY, FUNDING, CODEOWNERS), language tooling (.editorconfig, prettier, ESLint flat config, ruff, pyproject + pytest, vitest, android-lint, pre-commit, markdownlint, .env.example), an expanded named-section `.gitignore.example`, a `docs/` starter, and a full GitHub Wiki layout (`Home`, `Architecture`, `FAQ`, `Upgrade-History`, `PWA-Safety`, `Migration-v1-to-v2`, plus sidebar and footer).

The full canonical PR sequence to upgrade a repo from v1 to v2 lives in [`PROMPT.md`](./PROMPT.md) Step 2; the matching audit lives in [`UPGRADE_CHECKLIST.md`](./UPGRADE_CHECKLIST.md) sections 1–13.

## Next-level features (v2.1)

v2.1 is the polish release. It shipped in two waves: an initial cut focused on the rule-2 evidence chain and rule-11 split, then a complete final polish adding nine new feature areas. Both waves are bundled under the single `[2.1.0]` entry in [`CHANGELOG.md`](./CHANGELOG.md).

### v2.1 — Initial cut

- **Rule-2 evidence chain.** PROMPT.md rule 2 ("behavior preservation") now enumerates five observable-behavior buckets — UI, URLs, Storage, Deployment shape, External dependencies — and puts the burden of proof on the refactor. REFACTORING_GUIDE.md names `pwa-inventory.md` as the rule-2 evidence artifact for PWA refactors; the shared PR template gains a tickable **Behavior-preservation evidence** sub-block for non-PWA refactors; UPGRADE_CHECKLIST.md Section 4 audits that any refactor PR opened during an upgrade pass carried that evidence.
- **Self-check canonicalized.** PROMPT.md rule 11 splits the post-task self-check into (a) drift-detection (the existing CLAUDE.md.tmpl block) and (b) mechanical verification with five enumerated checks: files exist, YAML/JSON parses, links resolve, line-count delta matches the plan, no template placeholders remain in tracked files outside `templates/`.

### v2.1 — Complete Final Polish

- **A — Rule-2 non-negotiable repo-specific tailoring.** Rule 2 now mandates 100% original functionality preserved, target-repo analysis *before* editing, and a "Repo-specific risks / edge-cases" subsection in every PR description and post-task self-check. Echoed in REFACTORING_GUIDE.md, UPGRADE_CHECKLIST.md, templates/README.md.tmpl, templates/CLAUDE.md.tmpl.
- **B — Fully automated release & package publishing.** `release-please.yml` ships three opt-in publish jobs gated on layered repo variables: `PUBLISH_NPM_ENABLED` (npm OIDC), `PUBLISH_PYPI_ENABLED` (PyPI OIDC), `PUBLISH_GHCR_ENABLED` (GHCR multi-arch + provenance + SBOM). Existing `RELEASE_PLEASE_ENABLED` gate kept. Documented as an automation matrix in this README.
- **C — `templates/.github/GOVERNANCE.md`.** Sustainable solo-or-small-team OSS governance template covering descriptive roles, lazy-consensus decision-making, contribution lifecycle, and recommended branch-protection rules with the exact GitHub UI checkboxes that match v2.0's required status checks.
- **D — AI-native support.** `templates/.cursorrules` (Cursor IDE pointer) and `templates/ai/AI_TEAM_PLAYBOOK.md` (multi-AI coordination doc covering Claude Code / Cursor / Copilot / Codex). CLAUDE.md template gains an "AI readiness" subsection; README template gains an "AI tooling" subsection.
- **E — Workflow metadata.** Every workflow in `templates/.github/workflows/` now ships with a `*.properties.json` companion (name, description, iconName, categories, filePatterns) — same schema as github/starter-workflows. `self-validate.yml` hard-fails on any missing or orphan sidecar.
- **F — OpenSSF Scorecard.** New `scorecard` job in `security-scan.yml` runs weekly + on `branch_protection_rule` events + on push-to-main, publishes results to securityscorecards.dev, uploads SARIF to the Security tab. Badge snippet in `templates/docs/README.md`.
- **G — GitHub Template repository documentation.** Root README explains when to enable the Template-repository feature (new-repo starters) vs. when to keep using `PROMPT.md` (existing-repo upgrades), with a 6-step consumer onboarding sequence. UPGRADE_CHECKLIST.md Section 13 audits awareness.
- **H — Stale-issue/PR housekeeping (opt-in).** New `templates/.github/workflows/stale.yml` gated on `STALE_ENABLED=true`. Defaults: issues 60d → 7d, PRs 90d → 14d, broad exemption labels.
- **I — GitHub Community Guidelines + Acceptable Use audit.** CONTRIBUTING.md, root README, and templates/README.md.tmpl now explicitly bind contributions to the GitHub Community Guidelines, GitHub Acceptable Use Policies, and the repo's Code of Conduct, with reporting routes named.
- **K — Out-of-scope auto-issue (opt-out) + Single-PR alternative mode.** CLAUDE.md template + PROMPT.md rules 13–14: out-of-scope findings auto-file a labeled GitHub issue (opt out via `DISABLE_OUT_OF_SCOPE_ISSUES=true`); a single-feature-branch / single-PR mode is sanctioned for focused work that would otherwise produce ≤3 PRs (open draft early, subscribe to PR activity, commits accumulate, ready-for-review at completion).
- **L — Plan Management & Clean State Rule.** PROMPT.md rule 15 + `templates/CLAUDE.md.tmpl` "Plan Management & Clean State Rule" section + `UPGRADE_CHECKLIST.md` Section 13 audit bullet — when a long Claude session reopens plan mode, the rule mandates a fresh plan file or active pruning of completed sections, never appending new phases to a plan that already contains shipped work.

### Release & publish automation matrix

`templates/.github/workflows/release-please.yml` ships disabled-by-default and gated on layered repo variables. Set each variable to `true` only when its trust setup is in place; everything else short-circuits.

| Trigger | Repo variable | Action |
| --- | --- | --- |
| Push to `main` with Conventional Commits | `RELEASE_PLEASE_ENABLED=true` | Open / update a release-please PR; on merge, cut the GitHub Release + tag. |
| ↳ Release created (above) | `PUBLISH_NPM_ENABLED=true` | `npm publish --provenance` via npm OIDC trusted publishing (no `NPM_TOKEN`). |
| ↳ Release created (above) | `PUBLISH_PYPI_ENABLED=true` | `pypa/gh-action-pypi-publish` via PyPI OIDC trusted publishing (no `PYPI_API_TOKEN`). |
| ↳ Release created (above) | `PUBLISH_GHCR_ENABLED=true` | `docker buildx` multi-arch image to `ghcr.io/<owner>/<repo>` with provenance + SBOM. |

OIDC trust setup lives outside this repo: configure the npm package settings, the PyPI publishing account, or the GHCR token scope before flipping the variable. The workflow file's header comment lists the exact pages.

## How to use it (phone-friendly)

**Option A — Claude Code GitHub Action (recommended for mobile).**
Install the action in each repo once. Then to upgrade a repo, open a new issue and paste the contents of [`PROMPT.md`](./PROMPT.md) with `@claude` at the top. Claude opens a PR. You review and merge from the GitHub mobile app. Zero terminal.

**Option B — Claude Code session directly.**
In any repo, run `claude` (or open the Claude Code Android app and connect to a `claude remote-control` session on a machine you control), then paste [`PROMPT.md`](./PROMPT.md). Claude works locally and pushes a branch.

The prompt is identical for both. Pick the flow that fits where you are.

## Repo upgrade order (recommended)

Each repo upgrade follows the canonical 8-PR sequence in [`PROMPT.md`](./PROMPT.md) Step 2. The order in which you upgrade *repos* is your call; the template hardens fastest if you do small, similar repos first:

1. **Single-file HTML** — `worldmap`, `ticked`, `twitch-mood-radar` (validates the static-HTML CI workflow + refactoring guide)
2. **Smaller utilities** — `Exif`, `gadget`, `intuino`, `court-procedure-guide` (depends on what they are)
3. **Larger projects** — `discord-musicbot` (Python), `synth-piano`, `polyvote`
4. **Android** — `D2app` last (different stack, may need its own CLAUDE.md variant)

After the first downstream upgrade, expect to tweak the templates here based on what you learn. That's the point of having the standards in their own repo: change once, re-run.

## Use as a GitHub Template repository

This repo is structured as a **GitHub Template repository** — a one-click starter for new repos. Once enabled (`Settings → General → Template repository → ☑ Template repository`), the repo page gains a green **"Use this template"** button alongside `Code`. Clicking it creates a new repository pre-populated with this repo's tracked files but with a fresh git history (no commit log carried over).

**When to use it:** spinning up a brand-new project that should ship with the v2.1 baseline (community files, workflow templates, dependabot config, pre-commit hooks, governance, AI-tooling sidecars, etc.) on day one — instead of running [`PROMPT.md`](./PROMPT.md) against an empty repo and waiting for the 8-PR sequence to complete.

**When to keep using `PROMPT.md` instead:** for **existing** repos. The template flow is a clean-slate clone; the upgrade flow is for repos with code, history, and behavior that must be preserved (per [`PROMPT.md`](./PROMPT.md) rule 2).

**What downstream consumers do after "Use this template":**

1. Rename `templates/CLAUDE.md.tmpl` → `CLAUDE.md` at the repo root, fill in the placeholders.
2. Rename `templates/README.md.tmpl` → `README.md` at the repo root, fill in the placeholders.
3. Move workflow templates from `templates/.github/workflows/` to `.github/workflows/` and delete the ones that don't apply.
4. Move community files from `templates/.github/` to `.github/`.
5. Run `pre-commit install` once locally (if pre-commit is part of the chosen toolchain).
6. Open the first PR — `self-validate.yml` should be green out of the gate.

The `templates/` folder is intentionally left in the new repo as a reference; delete it once the consumer no longer needs the originals.

## Community standards

Contributions to this repo are governed by three layered standards: the [GitHub Community Guidelines](https://docs.github.com/en/site-policy/github-terms/github-community-guidelines), the [GitHub Acceptable Use Policies](https://docs.github.com/en/site-policy/acceptable-use-policies/github-acceptable-use-policies), and the [Contributor Covenant 2.1](https://www.contributor-covenant.org/version/2/1/code_of_conduct/) referenced from [`templates/.github/CODE_OF_CONDUCT.md`](./templates/.github/CODE_OF_CONDUCT.md). The same three apply to every downstream repo built from these templates — see [`templates/.github/CONTRIBUTING.md`](./templates/.github/CONTRIBUTING.md) for the contributor-facing version and the reporting routes.

## License

MIT.
