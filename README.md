# Ranzlappen Repo Standards

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
| [`templates/.github/`](./templates/.github/) | Community files: PR template, issue forms (bug / feature / question / upgrade-request), CODE_OF_CONDUCT, CONTRIBUTING, SECURITY, FUNDING, CODEOWNERS. |
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
| [`templates/LICENSE`](./templates/LICENSE) | MIT, matching the website repo. |

## How to use it (phone-friendly)

**Option A — Claude Code GitHub Action (recommended for mobile).**
Install the action in each repo once. Then to upgrade a repo, open a new issue and paste the contents of [`PROMPT.md`](./PROMPT.md) with `@claude` at the top. Claude opens a PR. You review and merge from the GitHub mobile app. Zero terminal.

**Option B — Claude Code session directly.**
In any repo, run `claude` (or open the Claude Code Android app and connect to a `claude remote-control` session on a machine you control), then paste [`PROMPT.md`](./PROMPT.md). Claude works locally and pushes a branch.

The prompt is identical for both. Pick the flow that fits where you are.

## Repo upgrade order (recommended)

The template hardens fastest if you do small, similar repos first:

1. **Single-file HTML** — `worldmap`, `ticked`, `twitch-mood-radar` (validates the static-HTML CI workflow + refactoring guide)
2. **Smaller utilities** — `Exif`, `gadget`, `intuino`, `court-procedure-guide` (depends on what they are)
3. **Larger projects** — `discord-musicbot` (Python), `synth-piano`, `polyvote`
4. **Android** — `D2app` last (different stack, may need its own CLAUDE.md variant)

After the first repo, expect to tweak the templates here based on what you learn. That's the point of having the standards in their own repo: change once, re-run.

## License

MIT.
