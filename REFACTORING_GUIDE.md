# Refactoring Guide: Single-File Projects → Modular

How to split big single-file projects (HTML, JS, Python) into modules **without changing behavior**. Behavior preservation is the contract — if anything looks, feels, or acts different after the refactor, the refactor is wrong.

This guide is referenced by [`UPGRADE_CHECKLIST.md`](./UPGRADE_CHECKLIST.md) section 5.

---

## When to refactor

Only when **all three** are true:

1. The file is over ~800 lines, **and**
2. The project is still being actively worked on, **and**
3. Future edits are likely to span multiple "concerns" (e.g. UI + storage + networking).

A 1500-line single-file project that is "done" and rarely touched is fine. Don't churn for the sake of it. The cost of a refactor is paid in bugs (regressions) and time; the value is paid out only across future edits.

If you skip the refactor, document the decision in CLAUDE.md so the next session doesn't propose it again.

---

## The contract: zero behavior change

Before starting:

1. **Open the file in the browser** (for HTML projects) and walk through every visible feature. Take screenshots of every distinct screen / state.
2. **Note any non-visible behavior** — keyboard shortcuts, localStorage keys, service worker registrations, IndexedDB schemas, network calls, console output.
3. **List every external dependency** loaded via `<script src=...>` or CDN — these stay loaded the same way after the refactor.
4. Record the file's **byte size and line count** before and after — the refactored output should be roughly equivalent in total bytes (slight overhead from imports is fine).

After refactoring:

5. Walk through the same checklist. Every screenshot must reproduce. Every shortcut still works. Every storage key has the same name and shape.
6. If anything is different — even a slightly different animation timing — the refactor regressed. Either fix the regression or revert.

This contract is non-negotiable. The user's stated value of these projects is "working as-is, hosted somewhere, mobile-first". A refactor that adds a build step or changes the deployment URL has not preserved behavior.

---

## PWA Refactor Addendum (mandatory if the project is a PWA)

Apply this section automatically whenever the repo contains **any** of:

* A `sw.js`, `service-worker.js`, or any file registered via `navigator.serviceWorker.register(...)`
* A `manifest.json`, `manifest.webmanifest`, or `<link rel="manifest" ...>` tag
* A `.well-known/assetlinks.json` (indicates a TWA / Android app binding)
* Calls to `Notification.requestPermission()`, `navigator.vibrate()`, `caches.open(...)`, IndexedDB, or any persistent storage API beyond simple localStorage

If any of those are present, the project has installed users whose data and app shell live in their browsers. A careless refactor will silently destroy their data, break the offline experience, or invalidate the installed Android/iOS app. None of that is recoverable for the affected user — they have to uninstall, lose history, and reinstall.

The rules below are non-negotiable defaults. Apply them automatically. Only stop and ask the user when a rule cannot be followed (e.g. an asset must move and there's a manifest reference to it, but the user explicitly asked to reorganize that path).

### Step 1 — Pre-refactor PWA inventory (run before touching any code)

Produce a `pwa-inventory.md` artifact in the PR description with these sections:

1. **Storage keys** — grep the entire codebase for `localStorage.`, `sessionStorage.`, `indexedDB.`, `caches.open(`, and any Firebase RTDB/Firestore paths. List every key/path string. These are now treated as a public API of the app.
2. **Schema versions** — find any `version`, `schemaVersion`, `MIGRATION_VERSION`, or migration-pipeline constant. Record current value.
3. **Service worker** — file path, registration scope, current `CACHE_NAME` (or equivalent), full precache list, presence/absence of `skipWaiting()` and `clients.claim()`.
4. **Manifest paths** — every `start_url`, `scope`, `icons[].src`, `screenshots[].src`, `shortcuts[*].url`, and `id`.
5. **TWA binding** — does `.well-known/assetlinks.json` exist? If yes, record the SHA-256 fingerprint(s) it contains and the package name.
6. **Permissions requested** — Notification, vibration, geolocation, persistent-storage, push, etc., and the user gesture each is tied to.
7. **External dependencies** — every CDN script tag, every dynamically imported URL.

This inventory becomes the post-refactor verification checklist. Every item must round-trip identically.

### Step 2 — Apply these rules automatically (no user prompt needed)

**Storage keys are sacred.** Never rename a key during a refactor. If `tickedTasks` was the key before, it is the key after. The refactored module exports a constant, but its value is byte-identical to what was there. If you genuinely believe a rename improves the code, that is a separate PR with an explicit data migration — never bundled with structural refactoring.

**Migration code is preserved byte-for-byte.** Extract migration logic into its own module in its own commit, with no rewrites. The set of versions handled, the order of migrations, the field-rename logic, and the schema-version constant must all be identical. If the original had `if (v < 5) migrateV4ToV5(data)`, the refactored version has the exact same call.

**Service worker stays at the same path.** GitHub Pages does not let you set the `Service-Worker-Allowed` header, so `sw.js` cannot move without losing scope. Keep it where it was. If the original was at `/sw.js`, the refactored project has it at `/sw.js`. The internal contents may be modularized using `importScripts(...)` or ES-module SWs (`{ type: 'module' }` in registration) but the *file path* is fixed.

**Bump `CACHE_NAME` on every refactor commit that changes precached file paths.** If the cache was `ticked-v3` and the refactor introduces `/js/storage.js` where there was none before, bump to `ticked-v4`. Update the precache list to match the new structure. This is the single most common PWA-refactor bug — old SW + new HTML + missing files = white screen for installed users.

**Add `self.skipWaiting()` and `self.clients.claim()` if missing.** A refactor commit is the right moment to add these (they don't change behavior for first-time visitors but ensure installed users get the new SW immediately). If they're already there, leave them.

**Update `manifest.json` paths in the same commit that moves the referenced asset.** If you move `icon-192.png` from `/` to `/assets/icons/`, the manifest update is in the same commit. Never split across commits — the intermediate state is broken.

**Never touch `manifest.json`'s `start_url`, `scope`, or `id`.** These bind installed apps to the project. Changing them invalidates the install on every user's home screen — it doesn't update, it stops working until they reinstall. If a refactor would require changing them, **stop and ask the user**.

**Never touch `.well-known/assetlinks.json`.** TWAs are bound to the SHA-256 fingerprint in this file. Changing it breaks the Android app for every user. If a refactor would touch this file, **stop and ask the user**.

**Permission prompts stay tied to the same user gesture.** If `Notification.requestPermission()` was called from a click handler on the "Enable Notifications" button, it stays in a click handler on that same button. Do not move it to module-load time — browsers block prompts not tied to a gesture and the feature silently breaks.

**ES-module service workers need explicit registration update.** If the SW itself is converted to use `import` statements, the registration call must change to `navigator.serviceWorker.register('/sw.js', { type: 'module' })`. Do this in the same commit, or don't convert the SW.

### Step 3 — Post-refactor verification (automatic, included in PR description)

Walk through the inventory from Step 1, item by item. The PR description includes a checklist with each line marked ✓:

* Every storage key still exists, with the same name
* Schema version constant has the same value
* SW file is at the same path
* `CACHE_NAME` bumped, precache list matches new file layout
* `skipWaiting` and `clients.claim` present
* Manifest paths all resolve to existing files
* `start_url`, `scope`, `id` unchanged
* `assetlinks.json` unchanged (if present)
* Permission requests still fire from the same gestures
* All CDN scripts still loaded the same way

If any line is not ✓, the PR is not ready. Fix or revert.

### When to actually stop and ask the user

Apply everything above without asking. The narrow list of cases that genuinely require user input:

* A storage key, schema version, `start_url`, `scope`, `id`, or `assetlinks.json` *must* change to complete the refactor (almost never true — usually means the refactor scope is wrong)
* The deployed URL would change
* A tracked asset must be deleted, not just moved
* You discover the project's PWA manifest is broken in `main` (separate fix PR, not bundled)

Everything else is the AI's call. Do it, document it in the PR, move on.

---

## Strategy: incremental, one module at a time

**Don't** rewrite the whole file in one pass. **Do** extract one cohesive section at a time, commit each, verify behavior holds.

A typical sequence:

1. Add section comment headers throughout the original file (`/* === SECTION: storage === */`, `/* === SECTION: timer === */`). Commit. No behavior change.
2. Extract the smallest, most independent section first (usually pure utilities — formatters, math helpers). Commit.
3. Extract the next-most-independent section. Commit.
4. Continue until the entry point file is small (typically a UI bootstrapper) and everything else lives in its own module.
5. Run the visual + behavioral checklist one final time.

Commit frequently. Each commit should leave the project in a working, deployable state.

---

## HTML / JS single-file projects

These projects (`ticked`, `worldmap`, `twitch-mood-radar`) use no bundler and are deployed as a single HTML file to GitHub Pages. The refactor must preserve that deployment shape: **one HTML entry point, no build step required for deployment**.

### Use native ES modules

Modern browsers support ES modules natively via `<script type="module">`. No bundler, no npm, no build step. This is the right tool here.

**Before** (single file):

```html
<!DOCTYPE html>
<html>
<head><style>/* 800 lines of CSS */</style></head>
<body>
  <!-- markup -->
  <script>
    // 2000 lines of JS doing many things
  </script>
</body>
</html>
```

**After** (entry point + modules):

```html
<!DOCTYPE html>
<html>
<head><link rel="stylesheet" href="./styles/main.css"></head>
<body>
  <!-- markup -->
  <script type="module" src="./js/main.js"></script>
</body>
</html>
```

```
project-root/
├── index.html              # entry point, ~50 lines
├── js/
│   ├── main.js             # bootstrapper — wires modules to DOM
│   ├── storage.js          # localStorage / IndexedDB helpers
│   ├── timer.js            # timer engine
│   ├── notifications.js    # service worker + Notification API
│   └── ui/
│       ├── swipe.js        # swipe-to-delete
│       └── theme.js        # dark/light toggle
└── styles/
    ├── main.css            # imports the others
    ├── tokens.css          # CSS custom properties (colors, spacing)
    ├── layout.css          # grid, flex, structural rules
    └── components.css      # buttons, inputs, cards
```

### Splitting rules for JS

- **One responsibility per module.** A module about storage doesn't touch the DOM. A module about UI doesn't touch the network.
- **Use named exports** for everything. Default exports make refactoring harder later.
- **Always include the `.js` extension** in import paths — native ESM requires it (`import { foo } from './bar.js'`, not `./bar`).
- **No circular imports.** If A imports B and B imports A, extract the shared piece into C.
- **Keep `main.js` thin.** It should mostly be `import` statements followed by `init()` calls.

### Splitting rules for CSS

- **`tokens.css`** holds only `:root { --c-accent: ... }` style custom property definitions. Nothing else.
- **`layout.css`** holds structural rules (grid, flex, positioning). No colors, no fonts.
- **`components.css`** holds reusable component styles (buttons, cards, inputs).
- Use `@import url('./tokens.css');` at the top of `main.css` to compose them. Note the request count tradeoff: more files = more requests on first load. For small projects this is irrelevant.

### Local dev for HTML projects

Native ES modules **don't work over `file://`** due to CORS. Local dev needs a static server. Two phone-friendly options to document in CLAUDE.md:

1. **GitHub Codespaces** — runs in browser, has a built-in preview server. Works on mobile.
2. **GitHub Pages preview** — push to a `preview` branch, view the deployed URL.

For phone-only workflows, GitHub Pages preview is usually the right answer. Document this in CLAUDE.md.

### Specific suggestions for the user's projects

Apply the above pattern with these proposed splits:

**`ticked`** (timestamped log + process tracker):
- `storage.js` — localStorage schema, migration pipeline, the v5 → vN migration logic
- `timer.js` — timestamp engine, checkpoint logic
- `notifications.js` — service worker, permission flow, scheduling
- `ui/swipe.js` — swipe-to-delete with haptic feedback
- `ui/checkpoints.js` — checkpoint rendering and interaction
- `main.js` — bootstrapper

**`worldmap`** (D3 globe with Equal Earth projection):
- `data.js` — node descriptions, connection data
- `projection.js` — Equal Earth setup, zoom/pan
- `layers/technology.js`, `layers/migration.js`, etc. — one file per layer
- `ui/bottom-sheet.js` — mobile bottom sheet
- `main.js` — bootstrapper

**`twitch-mood-radar`** (Twitch chat sentiment dashboard):
- `twitch.js` — IRC WebSocket connection
- `sentiment.js` — sentiment scoring engine
- `physics.js` — bubble physics engine
- `charts.js` — Chart.js wrappers
- `ui/dashboard.js` — layout and DOM updates
- `main.js` — bootstrapper

These are **proposals**. The actual splits should follow the natural seams in the existing code — don't force a structure that fights the project.

---

## Python single-file projects

For `discord-musicbot` and similar:

```
discord-musicbot/
├── bot.py                  # entry point — discord.Client, event handlers
├── cogs/                   # discord.py cog pattern
│   ├── music.py
│   ├── queue.py
│   └── admin.py
├── services/
│   ├── youtube.py          # external API wrappers
│   └── audio.py
├── utils/
│   └── formatting.py
├── requirements.txt
└── .env.example            # documented env vars, no real secrets
```

Same rules: one responsibility per module, no circular imports, behavior unchanged.

---

## What the upgrade PR should produce

When refactoring is part of the upgrade pass, the PR description should include:

1. **Before/after line counts** per file.
2. **Module map**: which functions/classes from the original now live where.
3. **Behavior verification checklist**: which features were tested, with screenshot diffs if visual.
4. **Deployment unchanged**: confirm the deployed URL, build command, and external dependencies are identical.
5. **Followups**: anything noticed during refactoring that's worth doing next but wasn't in scope.

If a refactor introduces *any* behavior change (even a justified improvement), it goes in a **separate PR** layered on top of the refactor PR. Refactor and feature changes never mix.
