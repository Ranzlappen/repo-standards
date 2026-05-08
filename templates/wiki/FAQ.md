# FAQ

Common questions about **<PROJECT_NAME>**. Add new entries at the bottom of the relevant section. If a question keeps coming back, promote the answer to [`README.md`](https://github.com/<OWNER>/<REPO>/blob/main/README.md) or [`CLAUDE.md`](https://github.com/<OWNER>/<REPO>/blob/main/CLAUDE.md) — the FAQ is for things that *should* be obvious but aren't, not for primary documentation.

## Using the project

### How do I run it locally?

See the **Developer Setup** section in [`README.md`](https://github.com/<OWNER>/<REPO>/blob/main/README.md). If those steps don't work for you, [open a question issue](https://github.com/<OWNER>/<REPO>/issues/new/choose) — we'd rather fix the docs than have you guess.

### Where does my data live?

<One paragraph naming the storage backend (localStorage, IndexedDB, Firebase, Postgres, etc.) and pointing at the relevant CLAUDE.md "Storage / data conventions" entry.>

### How do I export / back up my data?

<...>

### Why does feature X behave the way it does?

<Add entries here as feature questions accumulate. Link out to specific code or docs where useful.>

## Contributing

### How do I propose a feature?

[Open a feature-request issue](https://github.com/<OWNER>/<REPO>/issues/new/choose). Problem-first; the form prompts for it.

### My PR is failing CI — what now?

Read the failing job's log first. Common causes:

* **Lint failures** — run `<lint command>` locally; many auto-fix with `--fix`.
* **Test failures** — confirm the failing test reproduces locally; if not, it may be flaky.
* **Workflow validation** — for any change under `.github/workflows/`, the workflow YAML must be valid; `actionlint` catches most issues.

### What's the commit-message format?

[Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/). The pre-commit `commit-msg` hook (see [`.pre-commit-config.yaml`](https://github.com/<OWNER>/<REPO>/blob/main/.pre-commit-config.yaml)) enforces this locally. Short summary in [`CLAUDE.md`](https://github.com/<OWNER>/<REPO>/blob/main/CLAUDE.md) under "Conventional Commits".

## Operations

### How do I rotate a secret / API key?

<Project-specific. Reference `CLAUDE.md` "Required secrets" and explain the exact rotation path.>

### How do I roll back a deploy?

<Project-specific.>

### Where do logs live in production?

<...>

## Standards and tooling

### What version of repo-standards is this on?

Check the [`.standards-version`](https://github.com/<OWNER>/<REPO>/blob/main/.standards-version) file at the repo root. The full upgrade history lives in the [Upgrade-History](./Upgrade-History) page.

### Why this folder structure?

See [Architecture](./Architecture) for the long form, [`CLAUDE.md`](https://github.com/<OWNER>/<REPO>/blob/main/CLAUDE.md) for the authoritative current shape.
