# Repo Upgrade Checklist

The standard audit. Every Ranzlappen repo should pass every applicable item. "Applicable" depends on the project's language and shape — items marked **(if applicable)** can be skipped with a one-line note explaining why.

This checklist is meant to be run by Claude Code via [`PROMPT.md`](./PROMPT.md), but can also be used as a manual review.

---

> **Standards version.** This checklist applies to the version of `repo-standards` recorded in [`VERSION`](./VERSION) at the root of this repo. Consumer repos pin a major version (`v1`, `v2`, …) by referencing the matching git tag.

## 1. Documentation

- [ ] **`README.md` exists** at repo root, follows the [README template](./templates/README.md.tmpl).
- [ ] README opens with a one-sentence description of what the project is and who it's for.
- [ ] README has a **"Quick Reference" table** ("I want to... → Do this") for the most common tasks.
- [ ] README has a **"Project Structure"** section with a tree showing the top two levels.
- [ ] README explains how to **run the project locally** (or, if no local setup is needed, says so explicitly).
- [ ] README is written assuming the reader is operating from a phone via the GitHub web UI when possible. Long terminal-only flows are flagged as "developer-only".
- [ ] **`CLAUDE.md` exists** at repo root, follows the [CLAUDE.md template](./templates/CLAUDE.md.tmpl).
- [ ] CLAUDE.md is **under ~200 lines / ~10 KB**. Long CLAUDE.md files get partially ignored by Claude — prune ruthlessly.
- [ ] CLAUDE.md ends with the standard **"Post-task self-check"** block (keeps docs in sync after every change).
- [ ] **`LICENSE` exists** (MIT unless there's a specific reason).
- [ ] If README and CLAUDE.md disagree on architecture, **CLAUDE.md wins** and the README is updated.

## 2. Repo hygiene

- [ ] **`.gitignore`** is appropriate for the project's language(s). No build artifacts, secrets, IDE config, or OS noise committed.
- [ ] No secrets, API keys, or credentials in tracked files. Public client-side keys (e.g. Firebase config) are okay if security is enforced server-side, but this is documented in CLAUDE.md.
- [ ] No files larger than ~5 MB unless justified (and then ideally via Git LFS).
- [ ] **`.github/dependabot.yml`** exists with weekly schedule and the v2 expectations applied per ecosystem:
  - [ ] explicit `open-pull-requests-limit` (default: 10).
  - [ ] `labels: ["dependencies", "<ecosystem>"]` for triage.
  - [ ] `commit-message` with `prefix: "chore(deps)"` (and `prefix-development: "chore(deps-dev)"` where the ecosystem distinguishes dev/prod) plus `include: "scope"`.
  - [ ] groups split production vs development for npm and pip (so dev bumps don't block prod review and vice versa); minor + patch grouped, majors land one-per-PR.
  - [ ] explicit `package-ecosystem: "github-actions"` block with the same limits / labels / prefixes as npm.
- [ ] Default branch is `main`.
- [ ] Repo has a **non-empty description** on its GitHub page.
- [ ] Repo has **topics/tags** set (language, framework, broad category).

## 3. CI / GitHub Actions (if applicable)

- [ ] At least one workflow exists in `.github/workflows/`.
- [ ] Workflows are **scoped by `paths` filters** so unrelated changes don't trigger irrelevant runs.
- [ ] **Concurrency control** is configured per workflow (cancel-in-progress for CI, queue for deploys).
- [ ] **Every workflow declares a `permissions:` block** at workflow scope — least privilege (`contents: read` is the default for non-deploying CI). Jobs override per-step where they need more.
- [ ] **Every `uses:` action is pinned to a 40-char commit SHA**, with a trailing comment naming the major version (e.g. `actions/checkout@de0fac2e4500dabe0009e67214ff5f5447ce83dd  # v6`). Major-version pins (`@v6`) and floating refs (`@main`) are rejected. Self-validate enforces this as a hard fail.
- [ ] **Every job declares `timeout-minutes`.** Defaults: Node 15, Python 15, static-html 10, Android 30, Pages-deploy 15, security-scan-codeql 30, security-scan-gitleaks 5.
- [ ] Node version (or other runtime version) is **pinned and consistent** across all jobs.
- [ ] **Lint/test tools are pinned and cached** (e.g. ruff/pytest in `requirements-dev.txt`, not inline `pip install ruff` per step). Cache keys include the dependency-pin file.
- [ ] Required secrets are **named in the workflow comment** and documented in CLAUDE.md.
- [ ] If the repo has multiple sub-projects, CI uses **per-app jobs gated on path filters** (see `website/.github/workflows/ci.yml` for the pattern).
- [ ] **A `security-scan.yml` workflow exists** with CodeQL + gitleaks, triggered on PRs, push-to-main, and a weekly schedule.
- [ ] **Reusable workflow available** (`lint-and-test.yml`) for projects that want a single callable lint+test entry point.

## 4. Project structure

- [ ] No file over **800 lines** unless it's data, generated code, or genuinely cohesive (e.g. a CSS theme). If a source file exceeds 800 lines, refactoring is flagged — see [`REFACTORING_GUIDE.md`](./REFACTORING_GUIDE.md).
- [ ] If a refactor PR was opened in this upgrade pass, its Test plan enumerates before/after evidence per [`PROMPT.md`](./PROMPT.md) rule 2's five buckets — UI, URLs, Storage, Deployment shape, External dependencies — using the **Behavior-preservation evidence** sub-block in the shared [PR template](./templates/.github/PULL_REQUEST_TEMPLATE.md). For PWA repos, Section 6 below is the expansion of the **Storage** and **External dependencies** buckets.
- [ ] Folder names are **consistent** (kebab-case for assets, the project's idiomatic case for source).
- [ ] No mystery directories without a README or comment explaining their purpose.
- [ ] Generated artifacts (`dist/`, `_site/`, `node_modules/`, `__pycache__/`) are not tracked.

## 5. Single-file project audit (if the repo is one big HTML/JS/Python file)

For projects like `ticked`, `worldmap`, `twitch-mood-radar`:

- [ ] The single file is **under 800 lines total**, or
- [ ] A refactor plan exists (proposed in the upgrade PR) that splits it into modules per [`REFACTORING_GUIDE.md`](./REFACTORING_GUIDE.md), or
- [ ] CLAUDE.md explicitly explains why the single-file structure is intentional and lists the internal section anchors.
- [ ] The HTML file's `<style>` and `<script>` blocks have **clear section comments** (`/* === SECTION: <name> === */`) so future edits are scoped.

## 6. PWA / installed-user safety (if applicable)

This section applies automatically if the repo contains **any** of: `sw.js`, `service-worker.js`, `manifest.json`, `manifest.webmanifest`, `<link rel="manifest">`, `.well-known/assetlinks.json`, or any code calling `navigator.serviceWorker.register`, `Notification.requestPermission`, `caches.open`, IndexedDB, `localStorage`, or `sessionStorage`. See the **PWA Refactor Addendum** in [`REFACTORING_GUIDE.md`](./REFACTORING_GUIDE.md) for the full handling rules.

- [ ] **Pre-refactor inventory** (`pwa-inventory.md`) is included in the refactor PR description, listing: storage keys, schema versions, SW path + `CACHE_NAME` + precache list, manifest paths, TWA `assetlinks.json` fingerprints (if present), permission requests, and external CDN dependencies.
- [ ] **Storage keys unchanged.** Every key/path string from the inventory exists in the refactored code with the same value.
- [ ] **Migration code preserved byte-for-byte.** Schema-version constant unchanged; migration order, version numbers, and field-rename logic are identical.
- [ ] **Service worker file path unchanged.** If it was `/sw.js`, it is still `/sw.js`.
- [ ] **`CACHE_NAME` bumped** in any commit that changes the precache file list. Precache list updated to match new module paths.
- [ ] **`self.skipWaiting()` and `self.clients.claim()` present** in the SW (added if missing — does not change first-time-visitor behavior, but ensures installed users get the new SW immediately).
- [ ] **Manifest paths resolve.** Every `start_url`, `scope`, `id`, `icons[].src`, `screenshots[].src`, and `shortcuts[*].url` points to an existing file.
- [ ] **`start_url`, `scope`, and `id` unchanged** from the inventory (changing them invalidates installed apps on every user's home screen).
- [ ] **`.well-known/assetlinks.json` unchanged** if present (changing it breaks bound TWAs).
- [ ] **Permission requests stay tied to the same user gestures** they were tied to before (browsers block prompts not tied to a click/tap).
- [ ] **ES-module SWs** (if the SW itself uses `import`) are registered with `{ type: 'module' }` in the same commit that converts them.
- [ ] If the SW registration's `scope` option is set explicitly, it is unchanged.

If any item cannot be satisfied without breaking installed users, the refactor scope is wrong — revert the offending change rather than asking the user to accept data loss.

## 7. Tests (if applicable)

- [ ] If the project has business logic, **at least a smoke test** exists.
- [ ] Test command is documented in CLAUDE.md under "Build & Development".
- [ ] CI runs tests for the relevant app on every PR.

## 8. Refactoring opportunities flagged

The upgrade pass should produce a short **"Refactoring opportunities"** section in the PR description, listing things noticed but not done in the same PR. Examples:

- Functions over 60 lines
- Duplicated logic across files
- Outdated dependencies that need a manual migration
- Dead code (unreachable, commented-out blocks)
- Magic numbers / strings that should be named constants
- Mixed concerns in a single module (UI + state + I/O)

These are **proposals**, not part of the upgrade PR. They become future work.

## 9. Wiki (optional)

Wiki content is optional. A repo without a wiki is not "downgraded" — it just doesn't get the long-form companion docs that complement README and CLAUDE.md. If the wiki **is** populated:

- [ ] **Wiki is enabled** on the repo (Settings → Features → Wikis).
- [ ] **`Home.md` exists** with a "where to look" task-oriented table.
- [ ] **`Architecture.md` exists** and explicitly states that `CLAUDE.md` wins on disagreement (single source of truth for architecture).
- [ ] **`FAQ.md` exists** with categorised entries; recurring questions are graduated to README/CLAUDE.md rather than living forever in FAQ.
- [ ] **`Upgrade-History.md` exists** and is append-only (newest entry on top).
- [ ] **`PWA-Safety.md` exists** if the repo is a PWA, and links to `REFACTORING_GUIDE.md`'s PWA Refactor Addendum rather than duplicating the rules.
- [ ] **`Migration-v1-to-v2.md` (or current major) exists** with the per-repo migration entry recorded.
- [ ] **`_Sidebar.md` and `_Footer.md` exist** and stay short (long sidebars push content below the fold).

Wiki seeding is performed manually via the GitHub web UI per `PROMPT.md` Step 4 — the upgrade flow does not push to `<repo>.wiki.git` automatically.

## 10. Security

- [ ] **CodeQL is enabled** for the repo's primary language(s). For projects using the v2 templates, this means `templates/.github/workflows/security-scan.yml` is copied in and the language matrix matches what's in the repo.
- [ ] **Secret scanning is on** (Settings → Code security and analysis → Secret scanning) with push protection enabled.
- [ ] **Dependabot security alerts** are enabled (Settings → Code security and analysis → Dependabot alerts + Dependabot security updates).
- [ ] **`SECURITY.md` exists** at `.github/SECURITY.md` (or repo root) with a private-reporting channel — GitHub private vulnerability reporting preferred, email fallback.
- [ ] **Public client-side keys are documented** in `CLAUDE.md` under "Security & Secrets" if the project ships any (e.g. Firebase web config). Documentation explicitly says they're public-by-design and points at the server-side rule that secures the data.
- [ ] **`.env` is `.gitignore`d**; `.env.example` is committed; documented variables list `<SECURITY_CONTACT_EMAIL>` rotation cadence.
- [ ] **No secrets, API keys, or unredacted credentials in tracked files** (verified by gitleaks in the security-scan workflow on every PR + push to main + weekly schedule).

## 11. Accessibility, Performance, SEO (web projects only)

Skip this section for non-web projects (CLI tools, Discord bots, libraries) with a one-line note.

- [ ] **Lighthouse baseline** captured for the production URL. Defaults: Performance ≥ 80, Accessibility ≥ 95, Best Practices ≥ 95, SEO ≥ 90. Tune per project; don't lower without a recorded reason.
- [ ] **Accessibility audit basics**: every interactive element has an accessible name (button text, `aria-label`, or `alt` attribute), focus order is logical, contrast ratio ≥ 4.5:1 for body text, no keyboard traps. PWAs additionally need to handle the back-button correctly when modals are open.
- [ ] **Meta tags** present in `<head>`: `<title>`, `<meta name="description">`, `<meta name="viewport" content="width=device-width, initial-scale=1">`, charset, and Open Graph (`og:title`, `og:description`, `og:image`) for shareability.
- [ ] **`sitemap.xml`** present at site root for any site with more than ~5 distinct pages, and is referenced from `robots.txt`.
- [ ] **`robots.txt`** present at site root, explicit about which paths bots should and shouldn't crawl.
- [ ] **PWA manifest icons resolve** (every `icons[].src` exists). Lighthouse's installability audit catches this; running it locally before merge is the cheapest gate.

## 12. Testing & Quality

- [ ] **At least a smoke test exists** for any project with business logic. "Does the entry point start without crashing?" is a valid smoke test for the smallest projects; richer behavior gets richer tests.
- [ ] **Test command is documented in `CLAUDE.md`** under "Build & Development" (or the project's equivalent), so a new contributor can run tests without guessing.
- [ ] **Coverage thresholds set** for projects with `pyproject.toml`/pytest or `vitest.config.ts`. Defaults: lines / statements / functions ≥ 80%, branches ≥ 75%. Tune per project; don't lower without a recorded reason.
- [ ] **Lint runs in CI** on every PR. Defaults: ruff for Python, ESLint for JS/TS, ktlint or detekt for Kotlin, html-validate for static HTML. Failures are blocking.
- [ ] **Conventional Commits enforced locally** via the `commit-msg` hook in `templates/.pre-commit-config.yaml` (CI re-checks the merge commit).
- [ ] **Pre-commit installed** by contributors (`pre-commit install`) — documented in `CONTRIBUTING.md`.
- [ ] **Test failures are blocking**: PR can't merge with red CI. Branch protection on `main` requires the CI workflow to pass.
- [ ] **Flaky tests are flagged with a label or skip**; chronic flakes get an issue instead of a `// TODO: fix flaky` comment that never gets addressed.

## 13. Standards Versioning

- [ ] **`.standards-version` file at repo root** containing one line with the major version this repo follows (e.g. `2`). Read by `PROMPT.md` Step 0 to gate upgrade runs.
- [ ] **Standards-version badge in `README.md`** above the fold:
  `[![Standards](https://img.shields.io/badge/repo--standards-v2-informational)](https://github.com/Ranzlappen/repo-standards)`.
- [ ] **`Upgrade-History.md` wiki page** records the migration entry for the most recent upgrade (per section 9 — Wiki).
- [ ] **`CHANGELOG.md` entry** dated and version-stamped for any change that introduces, removes, or alters a standards-version-relevant requirement (e.g. dropping support for an older Node version).
- [ ] **Pinned dependency on the standards repo** is at a tag, not `main`. PROMPT.md fetches `VERSION` from `Ranzlappen/repo-standards/main` (always-current); but consumer-side references in CONTRIBUTING.md, badges, etc. point at `v2` (or a specific `v2.0.0`) so a future v3 doesn't silently break docs.
- [ ] **No mixed-version state**: every reference in this repo to "repo-standards" cites the same major. Don't ship a v2 PROMPT result with a v1 README badge.

---

## How to score a repo

A repo is "upgraded" when:

1. All applicable boxes in sections 1–4 are checked.
2. Section 5 is addressed (refactor or justification).
3. Section 6 is addressed if applicable (PWA inventory + verification, or noted as N/A with reason).
4. Section 7 is addressed (tests exist or are explicitly deferred with a note).
5. Section 8 produced a refactoring-opportunities list, even if empty.
6. Section 9 (Wiki) is addressed if the wiki is populated, or skipped with a one-line note.
7. Section 10 (Security) — all items checked. CodeQL + secret scanning + Dependabot alerts are non-negotiable for v2 compliance.
8. Section 11 (A11y/Perf/SEO) is addressed for web projects, or skipped with a one-line reason for non-web projects.
9. Section 12 (Testing & Quality) — at minimum, smoke tests + lint in CI + Conventional Commits enforced.
10. Section 13 (Standards Versioning) — `.standards-version` file present, README badge present, no mixed-version state.

The upgrade PR description should include this checklist with each item explicitly marked `✓`, `—` (not applicable, with reason), or `⚠️` (deferred, with reason).
