# Ranzlappen Repo Standards

A portable toolkit for upgrading my repos to a consistent, high-quality baseline. Distilled from the [`website`](https://github.com/Ranzlappen/website) repo, which is the working reference implementation.

This repo answers two questions:

1. **What does a "good" Ranzlappen repo look like?** → see the [templates](./templates/) and the [`UPGRADE_CHECKLIST.md`](./UPGRADE_CHECKLIST.md).
2. **How do I bring an existing repo up to that bar with Claude Code?** → paste [`PROMPT.md`](./PROMPT.md) into a Claude Code session opened in that repo, or open an issue tagging `@claude` with the same prompt.

## What's in here

| File | Purpose |
| --- | --- |
| [`UPGRADE_CHECKLIST.md`](./UPGRADE_CHECKLIST.md) | The audit Claude Code runs against any repo. Pass/fail items grouped by category. |
| [`REFACTORING_GUIDE.md`](./REFACTORING_GUIDE.md) | How to split big single-file projects into modules without changing behavior. |
| [`PROMPT.md`](./PROMPT.md) | The standardized Claude Code prompt. One prompt, applied repo by repo. |
| [`templates/CLAUDE.md.tmpl`](./templates/CLAUDE.md.tmpl) | Skeleton CLAUDE.md based on the website repo's structure. |
| [`templates/README.md.tmpl`](./templates/README.md.tmpl) | Skeleton README with the "Quick Reference" pattern. |
| [`templates/.github/dependabot.yml`](./templates/.github/dependabot.yml) | Weekly dependency updates, sensible groupings. |
| [`templates/.github/workflows/`](./templates/.github/workflows/) | CI starters for Node, Python, static HTML, and Android. |
| [`templates/.gitignore.example`](./templates/.gitignore.example) | Combined .gitignore for Node + Python + JVM + macOS noise. |
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
