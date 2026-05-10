# `docs/` — long-form documentation for repo-standards

This folder is the long-form documentation home for **Ranzlappen Repo Standards** itself. The root [`README.md`](../README.md) is the front door (what the repo is, how to use it, the badge wall); [`PROMPT.md`](../PROMPT.md) and the [`prompt/`](../prompt/) modular files are the canonical Claude Code upgrade prompt; [`UPGRADE_CHECKLIST.md`](../UPGRADE_CHECKLIST.md) is the audit; this folder is for everything else worth writing down.

It's deliberately empty at the v3.0 cut. The folder exists so future how-tos, ADRs, migration guides, and runbooks have a known home rather than getting wedged into `README.md` or sprinkled across issues.

## Where docs live (this repo's map)

| Surface | What's in it |
| --- | --- |
| [`README.md`](../README.md) | Front door — what the project is, badge wall, "What's in here" table, how-to-use-it flows, community standards. |
| [`PROMPT.md`](../PROMPT.md) | Entry-point index for the canonical upgrade prompt. Thin (~80 lines). |
| [`prompt/`](../prompt/) | Modular source of the upgrade prompt — Step 0 / 16 ground rules / Steps 1–2 / Step 3 / Step 4 / Step 5. Each file is independently fetchable. |
| [`UPGRADE_CHECKLIST.md`](../UPGRADE_CHECKLIST.md) | The audit Claude Code runs against any repo. Pass/fail items grouped by category. |
| [`REFACTORING_GUIDE.md`](../REFACTORING_GUIDE.md) | How to split big single-file projects without changing behavior. PWA Refactor Addendum lives here. |
| [`SPONSORS.md`](../SPONSORS.md) | Sponsorship thank-you doc + boundaries. |
| [`CHANGELOG.md`](../CHANGELOG.md) | Notable changes per release. Keep-a-Changelog format. |
| [`.github/`](../.github/) | This repo's live community files (CoC, CONTRIBUTING, SECURITY, FUNDING, CODEOWNERS) + meta-CI workflows. Dogfood instances of the same templates downstream consumers adopt. |
| [`templates/`](../templates/) | The boilerplate downstream consumers copy into their own repos. Don't edit a template expecting it to apply to *this* repo — the live copies are at the root. |
| `docs/` (this folder) | Long-form how-tos, ADRs, migration guides, runbooks. Currently empty at v3.0; populate as the need arises. |

## When to add a file here

Add to `docs/` when a piece of writing is:

- **Too long for `README.md`** (more than one screen worth of detail).
- **Stable enough to be discoverable** (not a one-off conversation that belongs in a Discussion or issue).
- **Cross-referenced from multiple surfaces** (a how-to that the README, the checklist, and a PR description all point at).

Examples that *would* belong here once written:

- `docs/migration-v2-to-v3.md` — the consumer-side guide for upgrading a v2 repo to v3 (counterpart to the wiki's `Migration-v1-to-v2.md`).
- `docs/adr/0001-modular-prompt.md` — Architecture Decision Record for splitting `PROMPT.md` (Batch 2 of v3).
- `docs/adr/0002-workflow-summary-system.md` — ADR for the AI-parsable workflow-summary contract (Batch 3 of v3).
- `docs/runbooks/cut-a-release.md` — step-by-step for cutting a tag, including the local self-validate gates and the PR template.
- `docs/runbooks/rotate-a-pinned-sha.md` — when an upstream action releases a security fix, how to find + update the SHA + verify the lint stays green.

Examples that *don't* belong here:

- One-off Q&A → use [GitHub Discussions](https://github.com/Ranzlappen/repo-standards/discussions).
- Bug reports / feature requests → use [Issues](https://github.com/Ranzlappen/repo-standards/issues).
- The 16 ground rules / the canonical 8-PR sequence / the audit checklist → those have their own dedicated files at the root, don't duplicate.

## Anything in `docs/` that's also valuable cold should still be linked from `README.md`

`docs/` is a destination, not a hiding place. If a doc here would help a first-time visitor, link it from the root `README.md` "What's in here" table.

## Difference from `templates/docs/`

- **`docs/`** (this folder) is the **live** doc home for the standards repo itself.
- **`templates/docs/`** is the **boilerplate** that downstream consumers copy into their own repos. It ships a publishing-options guide (plain Markdown / GitHub Pages / VitePress / MkDocs), the OpenSSF Scorecard badge snippet, and the Workflow summary system snippet — all framed as "how to start your project's docs".

The two folders never share content. Edits to `templates/docs/` propagate downstream on the next consumer upgrade; edits to `docs/` stay here.
