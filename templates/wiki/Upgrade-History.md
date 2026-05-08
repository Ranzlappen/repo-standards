# Upgrade history

A timestamped record of repo-standards upgrades applied to **<PROJECT_NAME>**. Entries are append-only: never edit a past entry, only add a new one.

The newest entry is at the top.

## Conventions

Each entry includes:

* **Date** (ISO format, UTC).
* **From → To** standards versions.
* **Triggered by** — issue/PR link or "manual".
* **Scope** — which categories the upgrade touched (Docs / Hygiene / CI / Refactor / PWA-Safety / Wiki).
* **Notes** — anything notable: deviations from defaults, deferred items, follow-up issues.

The repo's `.standards-version` file always reflects the most recent **To**.

---

## <YYYY-MM-DD> — v? → v?

* **Triggered by**: <issue/PR link or "manual">
* **Scope**: <Docs / Hygiene / CI / Refactor / PWA-Safety / Wiki>
* **Notes**:
  * <one-line summary of the change>
  * <one-line summary of the change>

<!--
Earliest entry typically reads:

## YYYY-MM-DD — initial v1 adoption

* **Triggered by**: <issue link>
* **Scope**: Docs, Hygiene, CI
* **Notes**:
  * Adopted README, CLAUDE.md, LICENSE, .gitignore, dependabot.yml.
  * CI: <which workflow templates were copied in>.
  * No refactor needed (codebase under 800 LOC per file).
-->
