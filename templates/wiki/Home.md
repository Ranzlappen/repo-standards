# <PROJECT_NAME> Wiki

Welcome. This wiki is the long-form companion to the repo's [`README.md`](https://github.com/<OWNER>/<REPO>/blob/main/README.md) and [`CLAUDE.md`](https://github.com/<OWNER>/<REPO>/blob/main/CLAUDE.md). The README is the front door; the wiki is everything that doesn't fit there without bloating it.

## Where to look

| I want to... | Page |
| --- | --- |
| Understand how the project is shaped | [Architecture](./Architecture) |
| See what changed across standards versions | [Upgrade-History](./Upgrade-History) |
| Migrate from repo-standards v1 to v2 | [Migration-v1-to-v2](./Migration-v1-to-v2) |
| Find an answer to a common question | [FAQ](./FAQ) |
| Refactor a PWA without breaking installed users | [PWA-Safety](./PWA-Safety) |

## How this wiki is organised

* **Conceptual pages** (Architecture, FAQ, PWA-Safety) explain the *why* behind decisions and link out to the canonical docs in the repo.
* **Operational pages** (Upgrade-History, Migration-v1-to-v2) are timestamped and append-only. Don't edit history; add a new entry.
* **Sidebar** ([`_Sidebar.md`](./_Sidebar)) controls the left-hand navigation. **Footer** ([`_Footer.md`](./_Footer)) shows on every page.

## Contributing

The wiki lives at <https://github.com/<OWNER>/<REPO>/wiki> and is editable through the GitHub web UI. Edits are recorded with the editor's GitHub identity but don't go through PR review — keep changes incremental and surface large rewrites via an issue first.

If you want a change to be *enforceable* (style guide, naming convention, etc.), put it in [`CLAUDE.md`](https://github.com/<OWNER>/<REPO>/blob/main/CLAUDE.md). Wiki pages are reference; CLAUDE.md is law.

---

> **About these templates.** The pages in this wiki started life as `templates/wiki/` in the [repo-standards v2](https://github.com/Ranzlappen/repo-standards) toolkit. Replace the `<PROJECT_NAME>`, `<OWNER>`, and `<REPO>` placeholders, edit out anything that doesn't apply, and delete this paragraph.
