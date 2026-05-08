# PWA Safety

If **<PROJECT_NAME>** ships any of these, treat it as a PWA with installed users whose data lives in their browsers — and never refactor without following the PWA Safety rules:

* a `sw.js` / `service-worker.js` (or any file registered via `navigator.serviceWorker.register`)
* a `manifest.json` / `manifest.webmanifest` / `<link rel="manifest">`
* a `.well-known/assetlinks.json` (TWA / Android binding)
* calls to `Notification.requestPermission`, `caches.open`, `IndexedDB`, `localStorage`, `sessionStorage`, or `navigator.vibrate`

## Where the rules live

The complete, authoritative rules are the **PWA Refactor Addendum** in [`REFACTORING_GUIDE.md`](https://github.com/<OWNER>/<REPO>/blob/main/REFACTORING_GUIDE.md#pwa-refactor-addendum-mandatory-if-the-project-is-a-pwa). This wiki page intentionally **does not duplicate them** — there's exactly one source of truth and it's that file.

The matching pass/fail audit lives in section 6 of [`UPGRADE_CHECKLIST.md`](https://github.com/<OWNER>/<REPO>/blob/main/UPGRADE_CHECKLIST.md).

## Why a separate page

Two reasons this gets its own wiki page rather than just being a link from `Home.md`:

1. **It's the most consequential file in the wiki.** A botched PWA refactor silently destroys data on every installed user's device. Anything that prevents that is worth surfacing.
2. **Search-engine and in-repo discovery.** People hitting "PWA service worker safe refactor" should land here and immediately be redirected to the canonical rules — even if they didn't know there was a refactoring guide.

## Pre-refactor inventory

Before any refactor that could touch PWA surface area, produce a `pwa-inventory.md` artifact in the PR description per [`REFACTORING_GUIDE.md` Step 1](https://github.com/<OWNER>/<REPO>/blob/main/REFACTORING_GUIDE.md#step-1--pre-refactor-pwa-inventory-run-before-touching-any-code). Inventory items:

1. Storage keys (every `localStorage.`, `sessionStorage.`, `indexedDB.`, `caches.open(`).
2. Schema versions and migration code.
3. Service worker file path, scope, `CACHE_NAME`, precache list, `skipWaiting` / `clients.claim` presence.
4. Manifest `start_url`, `scope`, `id`, every icon/screenshot/shortcut path.
5. `assetlinks.json` SHA-256 fingerprints (if present).
6. Permissions requested and the user gestures they're tied to.
7. External CDN scripts.

## When to stop and ask

Most decisions during a PWA refactor are autonomous. The narrow exceptions where the refactor must pause and ask:

* A storage key, schema version, `start_url`, `scope`, `id`, or `assetlinks.json` *must* change.
* The deployed URL would change.
* A tracked asset must be deleted (not moved).
* `main` is broken in a way unrelated to the refactor.

Anything else: decide, document in the PR, move on.

---

*This page exists in every Ranzlappen repo that adopts repo-standards v2 and may be a PWA. Single source of truth lives in `REFACTORING_GUIDE.md`.*
