# Architecture

This page is the long-form companion to the **Architecture** section in [`CLAUDE.md`](https://github.com/<OWNER>/<REPO>/blob/main/CLAUDE.md). When the two disagree, **`CLAUDE.md` wins** — it's the authoritative source. Treat this page as background and rationale.

## At a glance

<2–4 sentence overview of what this project does and how it's shaped.>

```
<repo-root>/
├── <key file or folder>      # what it is
├── <key file or folder>      # what it is
├── <subfolder>/
│   └── <key file>            # what it is
└── ...
```

## Modules

<For each significant module / sub-app, a heading and 1–2 paragraphs covering:
  - What problem it solves
  - Where it lives (`path/`)
  - Public surface (entry point file, exported functions, HTTP routes — whatever applies)
  - Dependencies on other modules (or "stand-alone")
  - Why it's its own module instead of folded into something else>

### `<module-1>`

<...>

### `<module-2>`

<...>

## Cross-cutting concerns

* **Storage and persistence** — <where data lives, how it's namespaced. Cross-link `CLAUDE.md` "Storage / data conventions".>
* **Authentication and authorisation** — <which boundary enforces what. If client-side keys are public by design, say so and point at the server-side rule that secures the data.>
* **Error handling** — <project's error-handling conventions: fail-fast, fail-soft, retry, etc.>
* **Logging / observability** — <where logs go, how to read them in production.>
* **Internationalisation** — <if applicable, how strings are sourced and translated.>

## Deployment shape

<One paragraph describing what's deployed where:
  - Hosting target(s)
  - Build pipeline summary (link to the workflow files)
  - URL structure
  - Manual rollback procedure if any>

## Why these choices

<Short list of decisions worth remembering. Each entry: what we chose, what we considered, why we picked this. Keep to ~5 entries — anything more belongs in an ADR file under `docs/adr/`.>

* **<Choice 1>** — <one-paragraph rationale>.
* **<Choice 2>** — <...>

## Where to learn more

* [`CLAUDE.md`](https://github.com/<OWNER>/<REPO>/blob/main/CLAUDE.md) — current architecture (authoritative).
* [`docs/`](https://github.com/<OWNER>/<REPO>/tree/main/docs) — ADRs and longer-form notes.
* [Upgrade-History](./Upgrade-History) — how the architecture has evolved.
