# Repo Upgrade Checklist

The standard audit. Every Ranzlappen repo should pass every applicable item. "Applicable" depends on the project's language and shape — items marked **(if applicable)** can be skipped with a one-line note explaining why.

This checklist is meant to be run by Claude Code via [`PROMPT.md`](./PROMPT.md), but can also be used as a manual review.

---

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
- [ ] **`.github/dependabot.yml`** exists with weekly schedule. Minor+patch updates grouped to reduce PR noise.
- [ ] Default branch is `main`.
- [ ] Repo has a **non-empty description** on its GitHub page.
- [ ] Repo has **topics/tags** set (language, framework, broad category).

## 3. CI / GitHub Actions (if applicable)

- [ ] At least one workflow exists in `.github/workflows/`.
- [ ] Workflows are **scoped by `paths` filters** so unrelated changes don't trigger irrelevant runs.
- [ ] **Concurrency control** is configured per workflow (cancel-in-progress for CI, queue for deploys).
- [ ] **Action versions are pinned** to a major version at minimum (e.g. `actions/checkout@v6`, not `@main`).
- [ ] Node version (or other runtime version) is **pinned and consistent** across all jobs.
- [ ] Required secrets are **named in the workflow comment** and documented in CLAUDE.md.
- [ ] If the repo has multiple sub-projects, CI uses **per-app jobs gated on path filters** (see `website/.github/workflows/ci.yml` for the pattern).

## 4. Project structure

- [ ] No file over **800 lines** unless it's data, generated code, or genuinely cohesive (e.g. a CSS theme). If a source file exceeds 800 lines, refactoring is flagged — see [`REFACTORING_GUIDE.md`](./REFACTORING_GUIDE.md).
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

---

## How to score a repo

A repo is "upgraded" when:

1. All applicable boxes in sections 1–4 are checked.
2. Section 5 is addressed (refactor or justification).
3. Section 6 is addressed if applicable (PWA inventory + verification, or noted as N/A with reason).
4. Section 7 is addressed (tests exist or are explicitly deferred with a note).
5. Section 8 produced a refactoring-opportunities list, even if empty.

The upgrade PR description should include this checklist with each item explicitly marked `✓`, `—` (not applicable, with reason), or `⚠️` (deferred, with reason).
