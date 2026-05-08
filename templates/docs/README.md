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

## When to graduate from option 1 → 2 → 3

- Stay on **plain Markdown** while there are <10 doc files and no search.
- Move to **GitHub Pages + Jekyll** when you want a custom URL, a theme, or better mobile rendering.
- Move to **VitePress / MkDocs** when you want full-text search, a sidebar/TOC, or versioned docs.

Don't pre-emptively pick option 3 for a project that doesn't have option-1-worth of content yet.
