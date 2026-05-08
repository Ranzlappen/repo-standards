# `docs/` starter

This folder is the documentation home for **<PROJECT_NAME>**. The repo's `README.md` covers what the project is and how to use it; everything more detailed (architecture, ADRs, API reference, runbooks) lives here.

## What goes here

- `architecture.md` — system shape, key flows, why the project is structured this way.
- `adr/` — Architecture Decision Records, one file per decision (`0001-use-vitest.md`).
- `api/` — generated or hand-written API reference if the project ships an API.
- `runbooks/` — operational guides ("the deploy is failing", "rotate the API key").
- `images/` — diagrams and screenshots referenced by other docs.

Anything in `docs/` that's also valuable to someone reading the GitHub repo cold should still be linked from the root `README.md`. The folder is a destination, not a hiding place.

## Publishing options

The standards repo doesn't pick a static-site generator for you. Three common options, ordered by overhead:

### 1. Plain Markdown on GitHub (zero config)

Default. Files render natively at `https://github.com/<OWNER>/<REPO>/blob/main/docs/`. Best for projects with a few docs and no need for search, sidebars, or theming.

### 2. GitHub Pages with a Jekyll theme

Turn on Pages, point it at the `docs/` folder, optionally add a `_config.yml` with `theme: jekyll-theme-cayman` (or similar). Free hosting at `<owner>.github.io/<repo>/`. No build step beyond what Pages does for you.

### 3. A dedicated documentation site

Pick exactly one — don't ship two:

- **VitePress** (Node, Vue-based). Lightweight, fast HMR, good for code-heavy docs. Add `package.json` deps and a `.vitepress/config.ts`.
  - Reference: <https://vitepress.dev/>
- **MkDocs Material** (Python). Rich theme, great for API docs and search out of the box. Add a `mkdocs.yml` at the repo root.
  - Reference: <https://squidfunk.github.io/mkdocs-material/>

Both deploy to GitHub Pages via a workflow. The `templates/.github/workflows/pages-deploy.yml` starter handles the publish step; you only add the build step.

## Release & publish automation

If this project uses [`release-please.yml`](../.github/workflows/release-please.yml) for Conventional-Commits-driven releases, the workflow ships three opt-in post-release publish jobs gated on repo variables:

| Trigger | Repo variable | Action |
| --- | --- | --- |
| Push to `main` with Conventional Commits | `RELEASE_PLEASE_ENABLED=true` | Open / update a release PR; on merge, cut the GitHub Release. |
| ↳ Release created | `PUBLISH_NPM_ENABLED=true` | `npm publish --provenance` via npm OIDC. |
| ↳ Release created | `PUBLISH_PYPI_ENABLED=true` | PyPI publish via OIDC trusted publishing. |
| ↳ Release created | `PUBLISH_GHCR_ENABLED=true` | Multi-arch container to `ghcr.io/<owner>/<repo>`. |

Configure the OIDC trust policy on each external service *before* setting the corresponding variable to `true` — until then, the publish jobs short-circuit and a release-please run that cuts a release simply doesn't trigger them.

## OpenSSF Scorecard badge

The `scorecard` job in [`security-scan.yml`](../.github/workflows/security-scan.yml) publishes the project's score weekly. Add the badge to your `README.md`:

```markdown
[![OpenSSF Scorecard](https://api.securityscorecards.dev/projects/github.com/<OWNER>/<REPO>/badge)](https://securityscorecards.dev/viewer/?uri=github.com/<OWNER>/<REPO>)
```

Replace `<OWNER>/<REPO>`. The first run after enabling Scorecard takes ~10 minutes to publish before the badge resolves.

## Workflow summary system

`templates/.github/workflows/workflow-summary.yml` is a reusable workflow that produces a structured, AI-parsable Markdown summary of a CI run — status, per-job durations, warnings, errors, annotations — emitted to `$GITHUB_STEP_SUMMARY` and optionally posted as a sticky PR comment keyed by an HTML-comment marker (so repeat runs update the same comment instead of stacking).

The Markdown shape is committed to: identical headings, identical table columns, sorted annotations. Humans skim it; AI agents (Claude reviewing CI failures, Copilot suggesting fixes, internal triage bots) parse it without ad-hoc heuristics.

**Wire into a per-repo workflow:**

```yaml
name: CI
on: [pull_request]

jobs:
  lint-test:
    uses: ./.github/workflows/lint-and-test.yml
    with:
      language: node

  summarize:
    needs: [lint-test]
    if: ${{ always() }}
    uses: ./.github/workflows/workflow-summary.yml
    with:
      workflow-name: CI
      post-pr-comment: true
    permissions:
      contents: read
      actions: read
      pull-requests: write
      checks: read
```

`if: ${{ always() }}` is critical — the summary should fire even when the upstream jobs fail, otherwise the PR comment never updates with the failure detail. The required `permissions:` block declares `pull-requests: write` (for the comment) and `checks: read` (to fetch annotations); leave them off and the workflow short-circuits the relevant step.

**Output shape:**

```markdown
## CI — run #42

**Status:** ❌ failure
**Total duration:** 3m 12s
**Jobs:** 2
**Warnings:** 1
**Errors:** 3

### Jobs

| Job | Status | Duration | Annotations |
| --- | --- | --- | --- |
| lint-test | ❌ failure | 1m 47s | 4 |
| summarize | ✅ success | 0s | 0 |

### Warnings (1)

- `src/foo.ts:12` — unused import _(in job: lint-test)_

### Errors (3)

- `src/bar.ts:7` — missing semicolon _(in job: lint-test)_
- ...
```

The trailing `<sub>` tag in the actual output names the workflow that generated the summary, so a stale or hand-edited comment is distinguishable from an automated one.

## When to graduate from option 1 → 2 → 3

- Stay on **plain Markdown** while there are <10 doc files and no search.
- Move to **GitHub Pages + Jekyll** when you want a custom URL, a theme, or better mobile rendering.
- Move to **VitePress / MkDocs** when you want full-text search, a sidebar/TOC, or versioned docs.

Don't pre-emptively pick option 3 for a project that doesn't have option-1-worth of content yet.
