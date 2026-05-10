# Changelog

All notable changes to **repo-standards** are recorded here. Format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/) and the project uses [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

Consumer repos pin a major version (`v1`, `v2`, …) by referencing the matching git tag.

## [Unreleased]

### Added

- `.github/workflows/auto-tag.yml` (live root only — no template counterpart) — three new downstream jobs (`build`, `release`, `provenance`) chained off the existing `auto-tag` job. When VERSION bumps and a new tag is created, the workflow now also (a) packs a curated source tarball `repo-standards-templates-vX.Y.Z.tar.gz` from `templates/`, `prompt/`, `scripts/`, `docs/`, and the top-level standards docs (`LICENSE`, `README.md`, `CHANGELOG.md`, `VERSION`, `PROMPT.md`, `UPGRADE_CHECKLIST.md`, `REFACTORING_GUIDE.md`); (b) creates a GitHub Release at the new tag via `softprops/action-gh-release` (pinned to `3bb12739c298aeb8a4eeaf626c5b8d85266b0e65 # v2.6.2`) with the tarball + sha256 attached; (c) generates SLSA Level 3 provenance via the official `slsa-framework/slsa-github-generator/.github/workflows/generator_generic_slsa3.yml` reusable workflow (pinned to `f7dd8c54c2067bafc12ca7a55595d5ee9b75204a # v2.1.0`), signed via Sigstore Fulcio with a Rekor transparency-log entry, and uploads the `.intoto.jsonl` to the same Release. Lifts the OpenSSF Scorecard Packaging check from `-1` to `10` and the Signed-Releases check to `10` once five signed releases exist. Workflow scope remains `contents: read`; each new job declares its own least-privilege permissions block (Token-Permissions stays at `10 / 10`). Verify a release locally with [`slsa-verifier verify-artifact --provenance-path <name>.intoto.jsonl --source-uri github.com/Ranzlappen/repo-standards --source-tag vX.Y.Z <tarball>`](https://github.com/slsa-framework/slsa-verifier).
- `prompt/05-migration-debrief.md` — new mandatory **Step 5** of the canonical Claude Code upgrade flow. Produces a single Markdown debrief at the end of every migration pass: shipped PRs, deferred scope with reasons, out-of-scope issues filed, follow-ups, and `.standards-version` delta. Roll-up of information already produced during the pass (per-PR descriptions from Step 3, self-checks from rule 11, auto-issues from rule 13, Phase 0 scoring table) — explicitly not a re-audit. Skipped only on explicit user signal. Indexed in `PROMPT.md`'s modular-structure table; covered by the dogfood audit's `[6/8] Modular prompt files` section.

### Changed

- `PROMPT.md` modular-structure table extended from 6 → 7 prompt files; "six focused files" → "seven focused files"; step range `(00–04)` → `(00–05)`; embedded prompt-to-paste fetch list adds `prompt/05-migration-debrief.md`; "After Phase 0 confirms" closing paragraph names Step 5 with the mandatory-by-default qualifier.
- `prompt/01-ground-rules.md` preamble: step range citation updated from "Step (0–4)" to "Step (0–5)" to reflect the new Step 5. Rule range remains 1–16 — no rule additions or renumbering in this entry; rule 16 (Conflict / Assumption Failure Protocol) shipped separately in v3.0.5.
- `prompt/04-wiki-seeding.md`: cross-references the Step 5 debrief as the source of the `Upgrade-History` entry's Headline / Scope / Notes blocks. Single source of truth when both Step 4 and Step 5 are taken.
- `scripts/dogfood-audit.py`: section `[6/8]` enumeration adds `"05-migration-debrief"`; module docstring bumped from "all 6 prompt/*.md" to "all 7"; total audit count moves from 33 → 34 PASS.
- Surface-reference cleanup pass across narrative docs that v3.0.5's rule-16 addition + PR #35's Step-5 addition both missed: `README.md` (rows 41 + 123), `docs/README.md` (rows 13 + 42), and `prompt/02-canonical-pr-sequence.md` (line 5). All five sites bumped from "15 ground rules" → "16 ground rules" and, where they enumerated the canonical Step sequence, extended through Step 5 (Migration debrief). `02-canonical-pr-sequence.md`'s "especially relevant" callout adds rule 16 alongside the existing rules 9/11/12 since rule 16 is itself an execution-time / per-commit rule. Surface-only — no behaviour, audit, or rule-numbering change.
- `.github/SECURITY.md` supply-chain commitments table: the **Signed releases via sigstore / cosign** row flipped from `in flight` → `live` and the mechanism column rewritten to point at the new `provenance` job in `auto-tag.yml` (Sigstore Fulcio + Rekor transparency log) with the verifier command line. The **SLSA build provenance** row flipped from `in flight (target Level 3)` → `live (Level 3)` and rewritten to credit the same job. Both rows now describe shipped behaviour rather than aspirational plumbing. No change to the other rows or to the score-floor / out-of-scope sections.

### Fixed

- `templates/.github/workflows/security-scan.yml` and `templates/.github/workflows/ci-static-html.yml`: `gitleaks/gitleaks-action` pin converged on the commit-SHA form (`ff98106e4c7b2bc287b24eaf42907196329070c7`) the live `.github/workflows/security-scan.yml` already uses; both templates previously pinned the equivalent annotated-tag-object SHA (`dcedce43c6f43de0b836d1fe38946645c9c638dc`). GitHub recommends commit-SHA pins for actions; this is notation cleanup with zero behaviour change.

### Tracked separately

- Issue [#33](https://github.com/Ranzlappen/repo-standards/issues/33) — re-evaluate `gitleaks-action` Node-20 deprecation after the 2026-06-02 GitHub Actions runner cutover. Deferred replacement plan preserved inline in the issue body for reactive execution if the forced Node-24 migration breaks the action; high-confidence prediction is no-op (action is a thin wrapper around the `gitleaks` Go binary).

## [3.0.5] — 2026-05-09

Hotfix on top of v3.0.4. Lifts the live OpenSSF Scorecard score from `5.9 / 10` (below the repo's stated `≥ 7.0` floor in `templates/.github/SECURITY.md` + `templates/.github/GOVERNANCE.md`) by fixing the `Token-Permissions` regression (currently scoring `0 / 10`). Two live-root workflows — `auto-tag.yml` and `tag-release.yml` — declared `permissions: contents: write` at workflow scope. Scorecard's [Token-Permissions check](https://github.com/ossf/scorecard/blob/main/docs/checks.md#token-permissions) flags any non-`read` workflow-scope permission as a violation; the fix is to scope the `contents: write` to the only job in each workflow that actually needs it (the tag-create + tag-push step). No semantic change to any rule, prompt file, governance doc, or checklist item — `prompt/00-version-check.md` still expects major `3`; consumers pinned to the `v3` major-tag pick up everything in this release on their next workflow run.

### Fixed

- `.github/workflows/auto-tag.yml` (live root only — no template counterpart) — workflow-scope `permissions: contents: write` re-scoped to `permissions: contents: read`. The `auto-tag:` job now declares `permissions: contents: write` job-locally where it actually executes `git tag -a` + `git push origin <tag>` + the `git push --force origin v<MAJOR>` for the moving major-version pointer. Closes the OpenSSF Scorecard `Token-Permissions` regression flagged at https://api.scorecard.dev/projects/github.com/Ranzlappen/repo-standards.
- `.github/workflows/tag-release.yml` (live root only — no template counterpart) — same shape: workflow-scope `permissions: contents: write` re-scoped to `permissions: contents: read`; the `tag:` job now declares `permissions: contents: write` job-locally where it executes `git tag -a` + `git push origin <tag>` (with optional `--force` per workflow_dispatch input).

### Changed

- `VERSION` bumped from `3.0.4` to `3.0.5`.
- `.standards-version` bumped from `3.0.4` to `3.0.5` (kept aligned with `VERSION`).
- Root `README.md` standards badge bumped from `v3.0.4` to `v3.0.5`.
- Root `README.md` "Upgrade any repo to vX" headline + body bumped from `v3.0.4` to `v3.0.5`.
- `PROMPT.md` master prompt banner bumped from `repo-standards v3.0.4` → `repo-standards v3.0.5` (line 27).
- Confirmation-language polish across the prompt surface: `PROMPT.md` (Phase 0 master block), `prompt/01-ground-rules.md` (rule 12), `prompt/migration-planning.md` (Section 6 output artifact), `prompt/02-canonical-pr-sequence.md` (Step 1–2 PR-open gate), `templates/.github/ISSUE_TEMPLATE/upgrade_request.md` (step 3), and `templates/wiki/Migration-v2-to-v3.md` (Phase 0 step) now explicitly state that clicking the "Approve plan mode" UI button — or replying with "yes", "approved", "proceed", "confirmed", "go ahead", or (in GitHub-issue contexts) a 👍 reaction on Claude's plan comment — counts as the explicit confirmation those gates require. Reduces plan-mode stalls in Claude Code on the web where the agent previously treated UI-button approval as ambiguous.
- New **rule 16 — Conflict / Assumption Failure Protocol** added to `prompt/01-ground-rules.md`, with mirrored entries in `PROMPT.md`'s master headlines (new headline #2, existing #2-7 renumbered to #3-8) and `prompt/migration-planning.md` (new Section 7 execution-phase reminder). When any Phase 0 assumption fails or an unexpected problem hits mid-execution, Claude must stop, state the failure, propose 2–3 options with trade-offs, and wait for explicit confirmation — never silently alter the plan, skip steps, or self-decide a workaround. Critical-safety rule; overrides every other rule (including rule 8 "Default to autonomy") when they conflict. Append-only addition (rule numbering 1–15 unchanged) so existing `PROMPT.md rule N` cross-references in `UPGRADE_CHECKLIST.md`, `REFACTORING_GUIDE.md`, `templates/CLAUDE.md.tmpl`, and `README.md` stay valid.

### Migration notes

- **No consumer action required.** The two re-scoped workflows are live-root only (`.github/workflows/auto-tag.yml` and `.github/workflows/tag-release.yml`), not part of the downstream-facing `templates/.github/workflows/` set. Downstream consumers don't ship these workflows; this is purely a self-compliance lift on the standards repo itself.
- **Live OpenSSF Scorecard score** before this release: `5.9 / 10` (verified live at `https://api.scorecard.dev/projects/github.com/Ranzlappen/repo-standards`). Two further low-scoring checks remain — `Branch-Protection` (currently `3 / 10`) and `Code-Review` (currently `0 / 10`) — but both require GitHub Settings → Rules → Rulesets edits the maintainer performs separately (require ≥1 approval + dismiss stale + require branches up-to-date + uncheck "Allow administrators to bypass"). With those UI fixes in place + this release's Token-Permissions fix + a fresh Scorecard run, the aggregate is expected to lift from `5.9` to `≥ 7.5`.
- **Deliberately skipped checks** (signal-to-effort ratio is poor for a templates repo): `CII-Best-Practices` (binary check requires multi-page questionnaire on `bestpractices.coreinfrastructure.org`; not pursued), `Fuzzing` and `Packaging` (both inherent to the repo type — templates repo, not a shipped library). `Signed-Releases` is deferred to the first artifact-shipping release (likely v3.1+ if a consumer ships a built artifact through `templates/.github/workflows/release-please.yml`'s opt-in npm/PyPI/GHCR jobs). `Contributors` and `Maintained` clear naturally over time.

## [3.0.4] — 2026-05-09

Cleanup release. Closes the Node 20 deprecation deadline (every action with a Node-20 build has been bumped to its Node-24 successor via the dependabot run that fired on first activation of `dependabot.yml`), resolves the long-standing CoC-inlining decision (Issue #4) by shipping an opt-in full-text variant alongside the existing stub, and documents the GitHub Rulesets vs. legacy Branch-protection-rule gap in `security-scan.yml`. No semantic change to any rule, prompt file, governance doc, or checklist item — `prompt/00-version-check.md` still expects major `3`, consumers pinned to the `v3` major-tag pick up everything in this release on their next workflow run.

### Added

- `templates/.github/CODE_OF_CONDUCT-full.md` — opt-in Code-of-Conduct variant that vendors the full Contributor Covenant 2.1 text inline (CC BY 4.0, attribution preserved). Drop-in replacement for the existing minimal-stub `templates/.github/CODE_OF_CONDUCT.md`; the two are equivalent in normative force. Trades ~120 lines of size for self-containment + discoverability + survival of the canonical URL ever moving. Closes #4 (option A from the issue's three resolution paths).
- `-v` / `--verbose` flag on `scripts/dogfood-audit.py` (`argparse`-driven). When set, each `assert_file` and `assert_grep` call emits a `[verbose] is_file(/repo/path/...)` or `[verbose] grep r"<pattern>" against /repo/path/...` line before its PASS/FAIL line. Default output unchanged. `.github/workflows/dogfood-audit.yml` now passes `-v` so CI runs always emit verbose output for trivially-diffable `$GITHUB_STEP_SUMMARY` blobs.
- README "What's in here" row pointing at `templates/.github/CODE_OF_CONDUCT-full.md`.

### Changed

- `templates/.github/CODE_OF_CONDUCT.md` (the stub) — trailing HTML-comment hint at "future option C inline-fetcher script" replaced with a one-line pointer at the now-shipped `CODE_OF_CONDUCT-full.md` alternative. Stub itself unchanged so existing v3.x consumers don't see a surprise diff on next sync.
- `.github/workflows/security-scan.yml` (live root) and `templates/.github/workflows/security-scan.yml` — header comment block above the `branch_protection_rule:` trigger now explicitly notes that GitHub Actions does **not** currently expose a workflow trigger for the new Rulesets feature (`repository_ruleset:` exists as a webhook event but not as an Actions trigger; actionlint flags it as unknown). Comment includes a forward-compatibility hook so the next maintainer can drop the trigger in if/when GitHub adds it.
- `PROMPT.md` master prompt banner bumped from `repo-standards v3.0.1` → `repo-standards v3.0.4` (line 27, inside the pasteable fence). Surface only — the audit's [6] regex matches any `v3.x.y` so functional checks pass either way.
- 6 GitHub-Actions dependency bumps via dependabot (PRs #21, #22, #23, #24, #25, #26 — all merged before this release PR). Cumulative diff:
  - `actions/checkout` 4.3.1 → 6.0.2 (live + every template that uses it; closes Node 20 deprecation).
  - `actions/github-script` 7.0.1 → 9.0.0 (`workflow-summary.yml` live + template; closes Node 20 deprecation).
  - `github/codeql-action` 3.35.4 → 4.35.4 — all three sub-actions (`init`, `analyze`, `upload-sarif`) re-pinned in `security-scan.yml` live + template (closes Node 20 deprecation; the v3.0.3 imposter-SHA fix lands cleanly on the new v4 SHA `68bde559dea0fdcac2102bfdf6230c5f70eb485e`).
  - `actions/dependency-review-action` 4.7.1 → 5.0.0 (live `dependency-review.yml` + template; the `fail-on-severity` and `comment-summary-in-pr` inputs survive the major bump, no breaking-change for our usage).
  - `gitleaks/gitleaks-action` SHA bump within `v2` (live `security-scan.yml` + template; minor/patch).
  - `ossf/scorecard-action` 2.4.0 → 2.4.3 (live `security-scan.yml` + template; bundles upstream Scorecard v5.3.0).
- `VERSION` bumped from `3.0.3` to `3.0.4`.
- `.standards-version` bumped from `3.0.3` to `3.0.4` (kept aligned with `VERSION`).
- Root `README.md` standards badge bumped from `v3.0.3` to `v3.0.4`.
- Root `README.md` "Upgrade any repo to vX" headline + body bumped from `v3.0.1` to `v3.0.4` (had been left at v3.0.1 through the v3.0.2 + v3.0.3 hotfixes; brought current here).

### Migration notes

- **Node 20 deprecation deadline (2026-06-02):** GitHub is forcing all Node-20-built actions to Node-24 by this date. Every Node-20 action shipped in v3.0.x is now bumped to its Node-24 successor. **No consumer action required** — repos pinned to `v3` (the moving major-tag) automatically pick up the new SHAs on their next workflow run. Repos pinned to a specific patch version (`v3.0.0`–`v3.0.3`) continue working but will emit Node-20 deprecation warnings; bumping the pin to `v3` (or `v3.0.4`) clears them.
- **Major-version map** (for consumers maintaining their own pinned forks): `actions/checkout` v4 → v6, `actions/github-script` v7 → v9, `github/codeql-action` v3 → v4, `actions/dependency-review-action` v4 → v5. The `actions/setup-node` and `actions/setup-python` template references in `templates/.github/workflows/release-please.yml` were already on Node-24-compatible majors and do not need updating.
- **GitHub Rulesets users:** Note that `security-scan.yml` only auto-rescores OpenSSF Scorecard on `branch_protection_rule:` events (the legacy Branch-protection-rule feature). GitHub Actions does not currently expose a workflow trigger for the newer Rulesets feature — the `repository_ruleset` webhook event exists but is not in the Actions trigger list (actionlint correctly flags it as unknown). For repos using Rulesets (Settings → Rules → Rulesets) instead of legacy Branch protection, Scorecard re-scoring relies on the weekly schedule (Mondays 06:00 UTC) + manual `workflow_dispatch` after ruleset edits. The header comment in both `security-scan.yml` files documents this gap with a forward-compatibility hook for if/when GitHub adds the trigger.
- **No breaking changes** for downstream consumers in v3.0.4. The CoC-stub default behavior is unchanged; the full-text variant is purely additive. The audit script's verbose flag is opt-in and default output is identical to v3.0.3. The `security-scan.yml` `on:` block is unchanged from v3.0.3 (the documentation comment grew, the trigger list did not).

## [3.0.3] — 2026-05-09

Hotfix on top of v3.0.2. The `github/codeql-action/{init,analyze,upload-sarif}` SHA pinned in `security-scan.yml` (live root + template) — `52485aec7be33610227643b0fe83936b8b5f061a` — does not exist on `github/codeql-action`. The Scorecard signing server's [imposter-commit check](https://github.com/ossf/scorecard-action#workflow-restrictions) (`api.securityscorecards.dev`) returns HTTP 400 with `"workflow verification failed: imposter commit: 52485aec... does not belong to github/codeql-action/upload-sarif"`, so even with v3.0.2's permission scoping fix, Scorecard still refuses to publish results. Re-pin all three usages to the current `v3` major-tag commit (`7fd177fa680c9881b53cdab4d346d32574c9f7f4` = `github/codeql-action@v3.35.4`, May 8 2026). No other change.

### Fixed

- `.github/workflows/security-scan.yml` (live root) and `templates/.github/workflows/security-scan.yml` (downstream-facing) — three `github/codeql-action/{init,analyze,upload-sarif}` `uses:` lines re-pinned from the bogus `52485aec7be33610227643b0fe83936b8b5f061a` (404 on `github.com/github/codeql-action/commit/...`) to `7fd177fa680c9881b53cdab4d346d32574c9f7f4` (= `v3` / `v3.35.4` HEAD as of 2026-05-08, validated against `https://github.com/github/codeql-action/tags`). Six replacements total (3 per file × 2 files). The bogus SHA almost certainly entered when the templates were authored — possibly a copy-paste error or a stale SHA from a draft. Fix verified by re-running the live `security-scan.yml` against the v3.0.3 tree on push to `main` after this PR merges (Scorecard sub-job's webapp publish must succeed without HTTP 400).

### Changed

- `VERSION` bumped from `3.0.2` to `3.0.3`.
- `.standards-version` bumped from `3.0.2` to `3.0.3` (kept aligned with `VERSION`).
- Root `README.md` standards badge bumped from `v3.0.2` to `v3.0.3`.

## [3.0.2] — 2026-05-09

Hotfix release. Fixes one bug in v3.0.1's shipped `security-scan.yml` (live and template) that caused the OpenSSF Scorecard sub-job to fail with `"workflow verification failed: global perm is set to write"` on first activation. Without this fix, `api.securityscorecards.dev` refuses to publish results, the README OpenSSF Scorecard badge never resolves to a numeric score, and downstream consumers adopting the template hit the same failure. No semantic change to any rule, prompt file, governance doc, or checklist item — `prompt/00-version-check.md` still expects major `3` and consumer repos pinned to the `v3` major-tag pick up this fix on their next workflow run.

### Fixed

- `.github/workflows/security-scan.yml` (live root) and `templates/.github/workflows/security-scan.yml` (downstream-facing) — workflow-scope `permissions:` block trimmed from `{contents: read, security-events: write}` to `{contents: read}` only. The `security-events: write` permission previously declared at workflow scope is now declared at the **CodeQL job scope**, where it's actually needed for the SARIF upload step. The OpenSSF Scorecard signing server (`api.securityscorecards.dev`) verifies the workflow against `ossf/scorecard-action`'s [workflow-restrictions policy](https://github.com/ossf/scorecard-action#workflow-restrictions) and returns HTTP 400 for any workflow holding `*: write` permissions at workflow scope (treats them as "global" and refuses to sign the results bundle). Both files now satisfy the policy: only `contents: read` at workflow scope; all `*: write` scopes are job-scoped (CodeQL job: `security-events: write`; Scorecard job: `security-events: write` + `id-token: write`). Verified against the policy via `python -c "import yaml; ..."` plus a re-run of the live workflow on the v3.0.2 push to `main`.
- Added a multi-line comment under both files' workflow-scope `permissions:` block citing the Scorecard verification rule and the upstream policy URL, so future edits don't reintroduce the regression.

### Changed

- `VERSION` bumped from `3.0.1` to `3.0.2`.
- `.standards-version` bumped from `3.0.1` to `3.0.2` (kept aligned with `VERSION`).
- Root `README.md` standards badge bumped from `v3.0.1` to `v3.0.2`.

## [3.0.1] — 2026-05-08

Polish + full dogfood completion + self-audit. Started as a
surface-only patch refining the canonical "copy this" pasteable block
in `PROMPT.md` and adding a README quick-start section, then expanded
to close every remaining v3.0.0 dogfood gap surfaced post-merge: the
standards repo now ships its own live `LICENSE`, `.github/dependabot.yml`,
and the four supply-chain / observability / audit workflows
(`security-scan.yml`, `dependency-review.yml`, `workflow-summary.yml`,
`dogfood-audit.yml`). New `scripts/dogfood-audit.sh` asserts the repo
passes 31 of its own UPGRADE_CHECKLIST invariants on every PR + push
to main + weekly schedule. No semantic change to any template, rule,
governance doc, or checklist item — `prompt/00-version-check.md` still
expects major `3` and consumer repos pinned to the `v3` major-tag keep
working unchanged. Detailed walkthrough for the post-merge maintainer
sequence lives in `README.md` under "Post-merge finalization".

### Added

- Root `README.md` "Upgrade any repo to v3.0.1 — the one-step instruction" section, anchored between the badge block and the project tagline. Names the master-prompt-copy-paste flow as the entire setup story for the GitHub Action / direct Claude Code session, and points at `PROMPT.md`. Surfaces v3.0.1 above the fold.
- Root `LICENSE` (MIT, `Copyright (c) 2026 Ranzlappen`) — closes the v3.0.0 dogfood gap on `UPGRADE_CHECKLIST.md` Section 1's "LICENSE exists" audit. The downstream-facing boilerplate at `templates/LICENSE` keeps `<YEAR>` / `<COPYRIGHT_HOLDER>` placeholders for consumers to fill in. README's License badge link bumped from `./templates/LICENSE` to `./LICENSE`. New "What's in here" row + expanded `## License` section pointing at both copies.
- Root `.github/dependabot.yml` — dogfooded dependabot config covering only the `github-actions` ecosystem (the standards repo has no `package.json` / `pyproject.toml` / `Gemfile` / `build.gradle`). Settings carried verbatim from `templates/.github/dependabot.yml` lines 14–34: weekly schedule, `open-pull-requests-limit: 10`, labels `[dependencies, github-actions]`, conventional-commit `prefix: "chore(deps)"` with `include: "scope"`, `groups` rolling minor + patch into one PR per week. New "What's in here" row.
- Root `.github/workflows/security-scan.yml` — adapted from `templates/.github/workflows/security-scan.yml` with one tweak: CodeQL `matrix.language` set to `['actions']` (instead of the template default `['javascript-typescript']`) since this repo's "code" is its workflow templates — CodeQL's GitHub Actions analysis (GA since 2024) is the meaningful dogfood. Triggers Scorecard publishing to `https://api.securityscorecards.dev/projects/github.com/Ranzlappen/repo-standards` on the first push to `main`, resolving the OpenSSF Scorecard badge URL referenced in `README.md` since v3.0.0. No sidecar (live root workflows aren't enforced by self-validate's properties-pairing check).
- Root `.github/workflows/dependency-review.yml` — verbatim copy of `templates/.github/workflows/dependency-review.yml`. Per-PR supply-chain gate; triggers on `pull_request` to `main`; runs `actions/dependency-review-action` with `fail-on-severity: high` and `comment-summary-in-pr: on-failure`. No-op today (no dependency manifests in this repo) but self-activates the moment any are added. Pairs with `security-scan.yml` (deeper weekly sweep — complementary, not redundant).
- Root `.github/workflows/workflow-summary.yml` — verbatim copy of `templates/.github/workflows/workflow-summary.yml`. `workflow_call`-shaped reusable workflow that pulls jobs + annotations + timings via the GitHub REST API, writes a structured AI-parsable Markdown summary to `$GITHUB_STEP_SUMMARY`, and (when `post-pr-comment: true`) posts a sticky PR comment keyed by an HTML-comment marker. Wired into `self-validate.yml` via a new `summarize:` job — every self-validate PR run now produces a sticky comment with status, total duration, per-job table, sorted warnings + errors. Markdown shape is committed-to so AI agents can parse it reliably.
- Root `.github/workflows/dogfood-audit.yml` + `scripts/dogfood-audit.py` — new self-compliance audit layer (genuinely new functionality; no template counterpart for downstream consumers). The Python script runs **eight assertion groups**: (1) root `LICENSE` exists with MIT first line and no `<PLACEHOLDER>`s, (2) `VERSION` + `.standards-version` exist with aligned majors and `VERSION` parses as semver, (3) all 7 root community files present, (4) all 7 live workflows present, (5) README badges resolve (Standards / License / OpenSSF Scorecard URL formats correct), (6) all 6 modular `prompt/*.md` files present + `PROMPT.md` master prompt names a v3.x version, (7) placeholder hygiene — no `<PROJECT_NAME>` / `<OWNER>` / `<REPO>` / `<TODO>` leakage in tracked files outside `templates/` (rule 11 mechanical verification), (8) workflow-sidecar pairing — every `templates/.github/workflows/*.yml` has a matching `.properties.json` sidecar with no orphans (mirrors `self-validate.yml`'s existing check at the audit layer). Prints PASS/FAIL per assertion + summary; exits 1 on any FAIL. Workflow runs on PR + push to main + weekly schedule + manual dispatch; tee'd output uploaded to `$GITHUB_STEP_SUMMARY`. Local run on this commit's tree: **33 PASS / 0 FAIL**.
- Root `README.md` "Post-merge finalization (maintainer only)" section — five-step walkthrough the maintainer follows once PRs #16 and #17 land (auto-tag verification, security-scan / dogfood-audit / dependency-review / workflow-summary verification, ~10-min wait for OpenSSF Scorecard badge to resolve, one-time GitHub Settings polish for branch protection + Dependency Graph + Secret scanning + Discussions, optional follow-ups).
- README "What's in here" rows for `LICENSE`, `.github/dependabot.yml`, and `scripts/dogfood-audit.sh`; live-workflows row description rewritten to enumerate all 7 live workflows.

### Changed

- `PROMPT.md` "Prompt to paste" block — full rewrite into the official v3.0.1 master prompt: opens with the v3.0.1 banner naming the standards repo URL; preserves the 11-file fetch-list at the top so Claude knows where the modular files live; collapses the ground-rules section to seven headlines that defer to `prompt/01-ground-rules.md` (no rule duplication, eliminating drift risk); separates Phase 0 (`prompt/migration-planning.md`) from Step 0 (`prompt/00-version-check.md`) explicitly; references Steps 1–4 by file path; closes with "Begin now with Phase 0". Same intent as the v3.0.0 block, hardened against the v3 modular structure.
- `VERSION` bumped from `3.0.0` to `3.0.1`.
- `.standards-version` bumped from `3.0.0` to `3.0.1` (kept aligned with `VERSION`).
- Root `README.md` standards badge bumped from `v3.0.0` to `v3.0.1`.
- Root `README.md` License badge link bumped from `./templates/LICENSE` to `./LICENSE` so the badge resolves to the live root file.
- Root `README.md` `## License` section expanded from the bare `MIT.` to a sentence pointing at both `./LICENSE` (live) and `./templates/LICENSE` (boilerplate).
- `.github/workflows/self-validate.yml` — new `summarize:` job appended at the bottom that depends on the existing five validation jobs (with `if: ${{ always() }}` so it runs even when validation fails) and calls `./.github/workflows/workflow-summary.yml`. Permissions scoped to `contents: read`, `actions: read`, `pull-requests: write`, `checks: read`. Real dogfood — every self-validate PR run posts a structured sticky workflow-summary comment.
- Root `README.md` "What's in here" `.github/workflows/` row description rewritten to enumerate all 7 live workflows now present (`auto-tag`, `self-validate`, `tag-release`, `security-scan`, `dependency-review`, `workflow-summary`, `dogfood-audit`).

## [3.0.0] — 2026-05-08

The polished-rocket elevation. Six commits on top of v2.1.1 — five feature
batches plus the versioning + ship batch. Theme: dogfood the standards (live
community files at the standards repo's own root + sponsors page), modularize
the prompt, harden the supply chain, expand the quality baseline, and add a
strategic Phase 0 migration-planning layer that runs *before* the canonical
8-PR sequence to produce a tailored, resumable, AI-budget-aware roadmap per
target repo.

### Added — Batch 1: dogfood community files at repo root

- `.standards-version` at root containing `3.0.0` — dogfooded major-version declaration the standards repo follows itself. Read by `prompt/00-version-check.md` Step 0.
- `.github/CODE_OF_CONDUCT.md`, `.github/CONTRIBUTING.md`, `.github/SECURITY.md`, `.github/FUNDING.yml`, `.github/CODEOWNERS` — live community files for the standards repo itself, distinct from the unconsumed downstream-facing boilerplate at `templates/.github/`. The standards repo proves its own checklist before asking consumers to.
- `SPONSORS.md` at root — thank-you page documenting what sponsorship funds and explicitly what it does *not* buy. Surfaced from a new "Sponsor" badge in the README.
- Root `README.md` "Sponsor" badge linking to `SPONSORS.md`.
- Root `README.md` "What's in here" rows for the new root-level community files.
- Root `README.md` "Community standards (this repo)" subsection naming the dogfooded copies and the three layered standards (GitHub Community Guidelines + Acceptable Use Policies + Contributor Covenant 2.1).

### Added — Batch 2: modular PROMPT.md

- `prompt/00-version-check.md` — Step 0 (refuse on major mismatch).
- `prompt/01-ground-rules.md` — the 15 non-negotiable rules.
- `prompt/02-canonical-pr-sequence.md` — Steps 1 + 2 (read & audit + canonical 8-PR sequence with hard ordering and practical execution).
- `prompt/03-pr-description.md` — Step 3 (PR description structure: Summary / Checklist coverage / Refactoring opportunities / Test plan).
- `prompt/04-wiki-seeding.md` — Step 4 (optional, opt-in Wiki seeding via the GitHub web UI).

### Changed — Batch 2

- `PROMPT.md` reduced from ~350 lines to a thin entry-point index over the modular `prompt/` files. Every cross-reference in `README.md`, `UPGRADE_CHECKLIST.md`, `REFACTORING_GUIDE.md`, and `templates/CLAUDE.md.tmpl` cites "`PROMPT.md` rule N" or "`PROMPT.md` Step N" and clicks through to the modular file. No semantic change to any rule; rule numbering preserved (1–15).
- `REFACTORING_GUIDE.md` rule-2 anchor parenthetical updated to point at `prompt/01-ground-rules.md` instead of the old monolithic `PROMPT.md`.

### Added — Batch 3: supply-chain baseline + workflow-summary system

- `templates/.github/workflows/dependency-review.yml` — per-PR supply-chain gate. Fails the PR on `high`-severity (or above) CVEs in dependency changes; comments the diff summary on the PR. Pairs with `security-scan.yml` (deeper weekly sweep — the two are complementary, not redundant). Required as a status check on `main` per `templates/.github/GOVERNANCE.md`.
- `templates/.github/workflows/workflow-summary.yml` — reusable workflow producing a structured, AI-parsable Markdown summary (status, jobs table, warnings, errors, timings) emitted to `$GITHUB_STEP_SUMMARY` and optionally posted as a sticky PR comment keyed by an HTML-comment marker. Comment shape (headings, table columns, sort order) is committed-to so AI agents can parse it reliably.
- `templates/.github/workflows/dependency-review.properties.json` and `workflow-summary.properties.json` — companion sidecars (same schema as github/starter-workflows). Pairing enforced by the existing `validate-workflow-properties` job in `self-validate.yml`.
- Root `README.md` OpenSSF Scorecard badge alongside the existing CI / License / Standards / Sponsor badges.
- `templates/.github/SECURITY.md` "Supply-chain commitments" status table covering CodeQL, Gitleaks, dependency-review, OpenSSF Scorecard (floor `≥ 7.0`), and signed releases (cosign + Rekor).
- `templates/.github/GOVERNANCE.md` "Supply-chain governance" subsection — signed-release rotation, Scorecard score floor, dependency-review as a required status check on `main`, regression-below-floor flagged as a `security` PR.
- `UPGRADE_CHECKLIST.md` Section 3 — workflow-summary system bullet.
- `UPGRADE_CHECKLIST.md` Section 10 — `dependency-review.yml` bullet (per-PR supply-chain gating, complementary to `security-scan.yml`) and signed-releases-with-sigstore bullet (tagged release artifacts carry a `.sig` and verify in the Rekor transparency log; OIDC trust setup per `release-please.yml` header comments).

### Added — Batch 4: expanded quality baseline

- `UPGRADE_CHECKLIST.md` Section 11 — Lighthouse CI baseline (automated run on every PR + push to `main`, blocks on regression below the Section 11 thresholds, results uploaded as a workflow artifact, wired into `workflow-summary.yml` so failures surface in the PR comment) and Performance budgets versioned in the repo (`lighthouserc.json` declaring resource-size + timing + assertion thresholds — budgets live in source so they're reviewed in PRs like any other config; CI thresholds alone drift silently when tuned via the UI).
- `UPGRADE_CHECKLIST.md` Section 12 — Branch-protection rules enforced on `main`. Every recommended rule from `templates/.github/GOVERNANCE.md` "Recommended branch-protection rules" must be configured: required PR approvals (≥ 1) with stale-approval dismissal, required Code Owners review, required status checks (actionlint, lychee, VERSION-is-semver, uses-line SHA-pinning lint, dependency-review, project lint/test, CodeQL, Gitleaks), required conversation resolution, signed commits, linear history, no force-push, no deletions, **admin no-bypass**. Without admin no-bypass the rules are advisory.
- `UPGRADE_CHECKLIST.md` Section 13 — GitHub Discussions enabled if the repo collects long-form Q&A. Use Discussions for open-ended Q&A, ideas, and show-and-tell; reserve Issues for tracked work. Graduate recurring Discussion threads to `README.md` / `CLAUDE.md` / `docs/` rather than letting them live forever in Discussions. Skippable for repos that don't need long-form Q&A.
- `templates/.github/GOVERNANCE.md` "Automated triage" section — stale-bot tuning recap, label scheme alignment with Dependabot ecosystem labels, recommended auto-merge rules (Dependabot patch + minor after CI green; majors always human-reviewed).
- Root `README.md` "GitHub Discussions" subsection explaining when to use Discussions vs. Issues.
- `docs/README.md` (new root-level long-form documentation index for the standards repo itself — distinct from `templates/docs/`, which remains the boilerplate downstream consumers copy).
- Root `README.md` "What's in here" rows for `prompt/` and `docs/`.

### Added — Batch 5: Phase 0 migration planning + Dependabot PR-spam handling

- `prompt/migration-planning.md` — strategic-planning layer that runs **before** Step 0 (version check). Phase 0 produces a tailored, prioritized migration roadmap reflecting the target repo's actual size, complexity, and stack. Six sub-sections: (1) repo profiling (tech stack, project type, size bucket, complexity signals, owner profile), (2) score every checklist item by effort × value × risk and bucket as must / should / could / skip, (3) tailored migration roadmap with inter-batch hard ordering mirrored from the canonical 8-PR sequence, (4) AI / token / session / fair-use guardrails (each response under ~30% context window, ~4-hour session cap, fair-use awareness, tiny resumable batches every batch ending with a clean commit + push so a session crash never loses work), (5) Dependabot PR-spam mitigation audit (reference-only — points at `templates/.github/dependabot.yml`'s v2-era rules: grouping, weekly schedule, `open-pull-requests-limit`, labels, conventional-commit prefixes, dev/prod split — plus auto-merge via repo-setting + branch-protection or labeled-auto-merge workflow, plus `CODEOWNERS *` for routing), (6) the output artifact (profile + scoring table + roadmap + guardrails ack + dependabot status, posted as the first comment / response and gated on user confirmation before Step 0 runs).
- `UPGRADE_CHECKLIST.md` Section 0 (Migration Planning, Phase 0) at the top of the checklist with a single audit bullet asserting the Phase 0 artifact was produced before any other batch landed.
- `templates/CLAUDE.md.tmpl` "Migration planning" subsection right after AI readiness, pointing consumers at Phase 0.

### Changed — Batch 5

- `PROMPT.md` modular-structure table grew to six rows (Phase 0 added at the top alongside the five numbered Steps); pasteable block now fetches `prompt/migration-planning.md` and instructs Claude to run Phase 0 *before* Step 0; closing line points at Phase 0 instead of Step 0.
- `templates/README.md.tmpl` Operating modes subsection now states both rhythms (canonical 8-PR sequence and single-PR alternative) are preceded by Phase 0.
- `UPGRADE_CHECKLIST.md` "How to score a repo" — Section 0 added as the first gate; numbering now 0–10.

### Added — Batch 6: versioning + ship

- `templates/wiki/Migration-v2-to-v3.md` — per-repo migration log template for v2 → v3 upgrades. Mirrors the structure of `Migration-v1-to-v2.md`. Referenced from `prompt/00-version-check.md`.
- Root `README.md` "Next-level features (v3)" mini-section with six bullets, one per batch (dogfooded community files; modular prompt; supply-chain baseline + workflow-summary system; expanded quality baseline; Phase 0 migration planning + Dependabot PR-spam mitigation; sponsors page).

### Changed — Batch 6

- `VERSION` bumped from `2.1.1` to `3.0.0`.
- Root `README.md` standards badge bumped from `v2.1.1` to `v3.0.0`.
- `templates/README.md.tmpl` standards-version badge bumped from `repo--standards-v2` to `repo--standards-v3`.
- `UPGRADE_CHECKLIST.md` Section 13 — badge example bumped from `v2` to `v3`; pinned-dependency reference bumped from "`v2` (or a specific `v2.0.0`) so a future v3 doesn't silently break docs" to "`v3` (or a specific `v3.0.0`) so a future v4 doesn't silently break docs".
- `prompt/00-version-check.md` — expected major bumped from `2` to `3`; example `.standards-version` value bumped from `2` to `3` (or `3.0.0`); `Standards: v2` badge example bumped to `Standards: v3`; refusal-condition example bumped from "target says v1, prompt says v2" to "target says v2, prompt says v3"; migration-guide reference bumped from `Migration-v1-to-v2.md` to `Migration-v2-to-v3.md`; closing forward-looking note bumped from "v2 → v3" to "v3 → v4".

## [2.1.1] — 2026-05-08

Documentation-only patch closing three loose ends from the v2.1.0
release wave. No template, workflow, or rule semantics changed.

### Fixed

- Root `README.md` standards badge URL bumped from `standards-v2.0.0`
  to `standards-v2.1.1` so the front-door badge matches `VERSION`. The
  badge had been missed during the v2.1.0 cut; `self-validate.yml`'s
  `validate-version` job only checks that `VERSION` parses as semver,
  not that downstream references stay in sync.
- Root `README.md` "v2.1 — Complete Final Polish" bullet list extended
  with a Phase-L entry (Plan Management & Clean State Rule) so the
  README enumerates the same set of phases as the `[2.1.0]` body in
  this changelog. The opening paragraph of the `[2.1.0]` entry was
  also corrected from "Phases A–K" to "Phases A–L" for the same
  reason.
- `templates/CLAUDE.md.tmpl` "Plan Management & Clean State Rule"
  section — dropped the redundant first sentence that repeated the
  section heading verbatim; tightened lead to `**Critical safety
  net.**`. No change to the bullets or to the closing rationale.

## [2.1.0] — 2026-05-08

The complete v2.1 polish cut. Two waves: the original "rule-2 evidence
chain + rule-11 split" pass that landed first (now grouped inside this
entry) and the v2.1 complete final polish that added nine new feature
areas (Phases A–L). Consumer repos pin to `v2.1` (or a specific
`v2.1.0`) by referencing the matching git tag.

### Added

- `templates/.github/GOVERNANCE.md` — sustainable solo-or-small-team OSS governance template covering descriptive (not hierarchical) roles, lazy-consensus decision-making with a 72h window + 7-day tiebreaker, contribution lifecycle, and **recommended branch-protection rules** with the exact GitHub UI checkboxes that match v2.0's required status checks. Cross-linked from `templates/.github/CONTRIBUTING.md` and root `README.md`. (Phase C)
- `templates/.cursorrules` — Cursor IDE pointer file that defers to `CLAUDE.md` as architecture source of truth, surfaces the rule-2 non-negotiable triple, codifies Conventional Commits + tiny-commit rhythm, and forward-references the AI Team Playbook. (Phase D)
- `templates/ai/AI_TEAM_PLAYBOOK.md` — multi-AI coordination doc (Claude Code / Cursor / GitHub Copilot / Codex) with source-of-truth hierarchy, per-tool scope table, universal conventions, conflict-resolution defaults, and per-tool ignore-file mechanisms. (Phase D)
- `templates/.github/workflows/release-please.yml` — three opt-in post-release publish jobs gated on per-target repo variables: `PUBLISH_NPM_ENABLED` (npm OIDC trusted publishing with `--provenance`), `PUBLISH_PYPI_ENABLED` (PyPI OIDC trusted publishing), `PUBLISH_GHCR_ENABLED` (multi-arch container push to ghcr.io with provenance + SBOM). Each job conditional on (a) its own enable variable AND (b) release-please actually creating a release this run. Existing `RELEASE_PLEASE_ENABLED` gate kept on the upstream job. (Phase B)
- `templates/.github/workflows/security-scan.yml` — new `scorecard` job using `ossf/scorecard-action`. Triggers on weekly schedule, push-to-main, `branch_protection_rule` events, and manual dispatch (skipped on PRs to avoid noise). Publishes results to securityscorecards.dev and uploads SARIF to the Security tab. Workflow-scope event also gains `branch_protection_rule:` so the score reflects the live config. (Phase F)
- `templates/.github/workflows/stale.yml` — opt-in housekeeping workflow (gated on `STALE_ENABLED=true`). Defaults: issues 60d → 7d, PRs 90d → 14d. Exempts pinned, security, keep-open, dependencies (PRs only), milestoned, and assigned items. 100 ops/run cap, oldest-first. (Phase H)
- `templates/.github/workflows/*.properties.json` — companion metadata sidecar for **every** workflow template (9 files: ci-android, ci-node, ci-python, ci-static-html, lint-and-test, pages-deploy, release-please, security-scan, stale). Each carries `name`, `description`, `iconName`, `categories`, `filePatterns` — same schema as github/starter-workflows so internal catalogs and AI agents pick them up. (Phase E)
- `.github/workflows/self-validate.yml` — new `validate-workflow-properties` job hard-fails if any workflow lacks its `*.properties.json` sidecar (or vice versa, or if the sidecar is malformed JSON). Both directions enforced with `::error` annotations. (Phase E)
- `templates/.github/PULL_REQUEST_TEMPLATE.md` "Behavior-preservation evidence" sub-block — five tickable buckets (UI / URLs / Storage / Deployment shape / External dependencies) for refactoring PRs to record before/after evidence per `PROMPT.md` rule 2. Section is opt-out via the HTML comment for non-refactor PRs. (Original v2.1 wave)
- `UPGRADE_CHECKLIST.md` Section 4 — new bullet auditing that any refactor PR opened during an upgrade pass enumerates rule-2 evidence in its Test plan. PWA repos satisfy the Storage and External buckets via Section 6. (Original v2.1 wave)
- `UPGRADE_CHECKLIST.md` Section 4 — new bullet auditing the "Repo-specific risks / edge-cases" subsection introduced by rule 2's non-negotiable repo-tailoring clause. (Phase A)
- `UPGRADE_CHECKLIST.md` Section 10 — new bullet auditing the OpenSSF Scorecard job and badge URL pattern. (Phase F)
- `UPGRADE_CHECKLIST.md` Section 13 — new bullets auditing (a) the GitHub Template repository feature, (b) operating-mode duality (canonical 8-PR sequence vs. single-PR alternative), and (c) the `DISABLE_OUT_OF_SCOPE_ISSUES=true` opt-out. (Phases G, K)
- `README.md` (root) — "Release & publish automation matrix" subsection (4-row table mapping triggers × repo variables × actions); "Use as a GitHub Template repository" subsection (when to use it, when to keep `PROMPT.md`, 6-step consumer onboarding); "Community standards" subsection naming the GitHub Community Guidelines + Acceptable Use Policies + Contributor Covenant 2.1 as binding on contributions. (Phases B, G, I)
- `templates/docs/README.md` — "Release & publish automation" subsection mirroring the root README matrix; "OpenSSF Scorecard badge" subsection with copy-pasteable markdown snippet. (Phases B, F)
- `templates/CLAUDE.md.tmpl` — new top-level sections "Behavior preservation (non-negotiable)", "AI readiness", "Out-of-scope / Unrelated Findings (opt-out)", and "Alternative Operating Mode: Single Feature Branch / Single PR". Existing Conventional Commits + Testing blocks tightened to keep template within the ~200-line target. (Phases A, D, K)
- `templates/README.md.tmpl` — new subsections "Operating modes", "AI tooling", "Behavior preservation (non-negotiable)", "Template-repo origin (if applicable)", "Community standards". (Phases A, D, G, I, K)
- `templates/.github/CONTRIBUTING.md` — "Governance" link in Quick links; "Community standards" section naming the three layered standards + reporting routes. (Phases C, I)
- `PROMPT.md` rule 15 + `templates/CLAUDE.md.tmpl` "Plan Management & Clean State Rule" section + `UPGRADE_CHECKLIST.md` Section 13 audit bullet — critical safety net requiring AI-driven upgrade passes to start a fresh plan file or actively prune completed sections, never appending new phases to a plan that already contains shipped work. (Phase L)

### Changed

- `PROMPT.md` rule 2 — strengthened the "behavior preservation" rule from a one-line statement into five enumerated observable-behavior buckets (UI, URLs, Storage, Deployment shape, External dependencies) with burden-of-proof on the refactor and an explicit fallback to "Refactoring opportunities" when proof isn't possible. Cross-links the **PWA Refactor Addendum** in `REFACTORING_GUIDE.md` as the PWA evidence path. (Original v2.1 wave) **Then v2.1 complete polish:** prepended the **non-negotiable** triple — keep 100% of original functionality, analyze the target repo *before* editing, and flag a "Repo-specific risks / edge-cases" subsection in every PR description and post-task self-check. (Phase A)
- `REFACTORING_GUIDE.md` — opening note in the PWA Refactor Addendum names `pwa-inventory.md` (Step 1) as the rule-2 evidence artifact for PWA refactors and tells non-PWA refactors to enumerate touched buckets directly in PR 4's Test plan. (Original v2.1 wave) Then a top-of-file "Rule-2 anchor" cross-reference surfaces the non-negotiable triple inline. (Phase A)
- `PROMPT.md` rule 11 — split into (a) drift-detection (the existing CLAUDE.md.tmpl block) and (b) mechanical verification with five enumerated checks: files exist, YAML/JSON parses, links resolve, line-count delta matches the plan, no template placeholders remain in tracked files outside `templates/`. Output destination specified. Resolves the prior incoherence between rule 9's parenthetical, rule 11's hand-wave, and the template's drift block. (Original v2.1 wave)
- `PROMPT.md` — added rules 13 (out-of-scope auto-issue, opt-out via `DISABLE_OUT_OF_SCOPE_ISSUES=true`) and 14 (single-PR alternative operating mode for focused work that would otherwise produce ≤3 PRs). (Phase K)
- `PROMPT.md` Step 2 hard-vs-practical ordering — unpacked the dense one-liner (`1 → (2, 3, 7 in parallel; 4 needs 2) → 5 → 6 → 8`) into a bulleted dependency list and a single-row practical-execution sequence. (Original v2.1 wave)
- `README.md` "Repo upgrade order (recommended)" — opened with a reference to PROMPT.md Step 2's canonical 8-PR sequence; trailing sentence now says "first downstream upgrade" to acknowledge the standards repo itself was the first v2 application. (Original v2.1 wave)
- `templates/CLAUDE.md.tmpl` Post-task self-check — extended to mandate the "Repo-specific risks / edge-cases" subsection and tightened the auto-implement vs prompt-first decision block. (Phases A, K)

### Fixed

- `PROMPT.md` rule 1 — replaced the legacy `chore/upgrade-standards` single-branch instruction with a reference to Step 2's canonical 8-PR sequence, resolving the internal contradiction with rule 3 and Step 2. (Original v2.1 wave)
- `PROMPT.md` rule 3 — replaced the v1-era 4-PR list (Docs / Hygiene / CI / Refactor) with a reference to Step 2's canonical 8-PR sequence, so phased-PR guidance lives in exactly one place. (Original v2.1 wave)

## [2.0.0] — 2026-05-08

The v2 cut. Eight phased PRs landed across the standards repo's docs, templates, CI, and PROMPT — see the breakdown below for traceability. Consumer repos pin to `v2` (or a specific `v2.0.0`) by referencing the matching git tag.

### Added — PR 6: checklist expansion

- `UPGRADE_CHECKLIST.md` Section 10 — Security (CodeQL, secret scanning + push protection, Dependabot security alerts, SECURITY.md present, public-client-side-keys documented, .env hygiene, gitleaks-verified no-secrets-in-tracked-files).
- `UPGRADE_CHECKLIST.md` Section 11 — Accessibility / Performance / SEO (Lighthouse defaults Perf 80 / A11y 95 / BP 95 / SEO 90, accessible names, focus order, contrast, meta tags incl. Open Graph, sitemap.xml, robots.txt, manifest icons resolve). Skippable for non-web projects with a one-line reason.
- `UPGRADE_CHECKLIST.md` Section 12 — Testing & Quality (smoke tests, test command in CLAUDE.md, coverage thresholds matching pytest/vitest defaults, lint blocking in CI, Conventional Commits enforced via commit-msg hook, pre-commit installed by contributors, branch protection requires green CI, flaky tests get a label or issue rather than a TODO).
- `UPGRADE_CHECKLIST.md` Section 13 — Standards Versioning (.standards-version file, README badge, Upgrade-History wiki entry, CHANGELOG entry for standards-version-relevant changes, consumer-side references pinned to a tag, no mixed-version state).

### Changed

- `UPGRADE_CHECKLIST.md` "How to score a repo" — extended scoring to include sections 9 (Wiki) and 10–13 (Security, A11y, Testing, Versioning). Wiki and A11y skippable for non-applicable repos; Security and Standards Versioning non-negotiable for v2 compliance.

### Added — PR 5: PROMPT.md hardening

- `PROMPT.md` Step 0 — Standards version check preamble. Fetches the standards `VERSION` and the consumer repo's declared version (`.standards-version` file, README badge, or CLAUDE.md note); refuses on major mismatch, asks the user in offline-fallback mode, and proceeds otherwise.
- `PROMPT.md` ground rules 9–12 — Tiny commits (one file per response), Conventional Commits required, mandatory post-task self-check on every code-change commit, no PR opens without explicit user confirmation. These were the implicit rules followed throughout this v2 upgrade; codifying them so every downstream upgrade follows the same rhythm.
- `PROMPT.md` Step 2 — Canonical 8-PR sequence (`chore/v2-versioning-meta` through `chore/v2-readme-and-tag`) with branch names, per-PR scope, hard-ordering and practical-execution rules. Replaces the previous loose "1, 2, 3, optionally 4" guidance.

### Changed — PR 7: dependabot tightening

- `templates/.github/dependabot.yml` now applies the v2 expectations across every ecosystem entry: explicit `open-pull-requests-limit: 10`, `labels: ["dependencies", "<ecosystem>"]` for triage, conventional `commit-message` prefixes (`chore(deps)` / `chore(deps-dev)` plus `include: "scope"`), and dev-vs-prod group split for npm and pip (dev bumps no longer block prod review). The previously-bare `bundler` entry now matches the rest. Sub-app npm entry mirror-updated in the commented-out block so consumers uncomment a complete row.
- `UPGRADE_CHECKLIST.md` Section 2 (Repo hygiene) — the single dependabot bullet is now a sub-checklist mirroring the v2 dependabot.yml shape.

### Added — PR 4: CI hardening

- `templates/.github/workflows/lint-and-test.yml` — reusable `workflow_call` workflow with `language` input (node | python | static-html | mixed). Single entry point for lint+test across stacks.
- `templates/.github/workflows/security-scan.yml` — CodeQL static analysis (matrix on language, security-extended query suite) + Gitleaks full-history secret scan. Triggers on PR, push to main, and weekly Monday 06:00 UTC schedule.
- `templates/.github/workflows/release-please.yml` — Conventional-Commits-driven release-please integration. Disabled by default (`if: false`); maintainer enables explicitly.

### Changed — PR 4: existing workflows hardened

Every existing workflow now declares a least-privilege `permissions:` block, has every `uses:` line pinned to a 40-char commit SHA (with major-version trailing comment), and sets `timeout-minutes` on each job. Hardened workflows:

- `templates/.github/workflows/ci-node.yml` (timeout 15).
- `templates/.github/workflows/ci-python.yml` (timeout 15; lint/test tools now cached via `requirements-dev.txt`, no more inline `pip install`).
- `templates/.github/workflows/ci-static-html.yml` (timeout 10).
- `templates/.github/workflows/ci-android.yml` (timeout 30).
- `templates/.github/workflows/pages-deploy.yml` (timeout 15; permissions already correct, only SHA-pinning + timeout added).
- `.github/workflows/self-validate.yml` — SHA-pinned all `uses:` lines, **flipped the SHA-pinning lint job from soft warn to hard fail** (any non-SHA pin is now an `::error` and the job exits 1).
- `.github/workflows/tag-release.yml` — SHA-pinned `actions/checkout`.
- `.github/workflows/auto-tag.yml` — SHA-pinned `actions/checkout`.

### Changed — PR 4: checklist

- `UPGRADE_CHECKLIST.md` Section 3 (CI / GitHub Actions) tightened with the v2 requirements: workflow-scope `permissions:`, 40-char SHA-pin + trailing major-version comment, `timeout-minutes` per job (with default-by-stack values), pinned+cached lint/test tools, mandatory `security-scan.yml`, and reusable-workflow availability.

### Added — PR 3: wiki templates and Wiki seeding phase

- `templates/wiki/Home.md` — landing page with task-oriented "where to look" table.
- `templates/wiki/Architecture.md` — long-form architecture companion that defers to `CLAUDE.md` on disagreement.
- `templates/wiki/Upgrade-History.md` — append-only ledger of repo-standards upgrades.
- `templates/wiki/FAQ.md` — categorised FAQ skeleton (Using, Contributing, Operations, Standards).
- `templates/wiki/PWA-Safety.md` — links to `REFACTORING_GUIDE.md`'s PWA Refactor Addendum (single source of truth, no duplication).
- `templates/wiki/Migration-v1-to-v2.md` — per-repo migration log with v1 → v2 breaking-change summary.
- `templates/wiki/_Sidebar.md` — wiki sidebar grouped into Getting started / Architecture / Operations / Standards.
- `templates/wiki/_Footer.md` — single-line footer linking back to README, CLAUDE.md, Issues, and the standards version.
- `PROMPT.md` Step 4 (optional): Wiki seeding phase. Skipped by default; user-opt-in only. Manual paste via the GitHub web UI; no automated `.wiki.git` push.
- `UPGRADE_CHECKLIST.md` Section 9: Wiki (optional). Page-existence and structural invariants (append-only Upgrade-History, link-not-duplicate PWA-Safety, CLAUDE.md-wins Architecture).

### Added — PR 2: community files and tooling templates

- `templates/.github/PULL_REQUEST_TEMPLATE.md` — mirrors the PR description structure required by `PROMPT.md` Step 3, with optional PWA-specific verification block.
- `templates/.github/ISSUE_TEMPLATE/` — `config.yml` (no blank issues) plus YAML forms for bug, feature, question, and a Markdown `upgrade_request.md` that pre-fills the `@claude` upgrade flow.
- `templates/.github/CODE_OF_CONDUCT.md` — short stub linking to Contributor Covenant 2.1 (issue [#4](https://github.com/Ranzlappen/repo-standards/issues/4) tracks optional inlining).
- `templates/.github/CONTRIBUTING.md` — short contributor guide with inline conventional-commits cheat sheet.
- `templates/.github/SECURITY.md` — disclosure policy with private-reporting channel, response SLAs, supported-versions table.
- `templates/.github/FUNDING.yml` — sponsor-button skeleton, all platforms commented.
- `templates/.github/CODEOWNERS` — ownership-map skeleton with security-sensitive-paths section.
- `templates/.editorconfig` — cross-editor whitespace + encoding rules.
- `templates/.prettierrc` and `templates/.prettierignore` — Prettier formatting config.
- `templates/eslint.config.mjs` — ESLint 9 flat config starter.
- `templates/ruff.toml` — Ruff lint + format config.
- `templates/pyproject.toml.example` — Python project skeleton with pytest config.
- `templates/vitest.config.ts` — JS/TS testing starter.
- `templates/android-lint.xml` — Android Lint config.
- `templates/.pre-commit-config.yaml` — pre-commit hooks (hygiene, ruff, prettier, markdownlint, gitleaks, conventional-commit-msg).
- `templates/.markdownlint.json` — markdownlint config.
- `templates/.env.example` — documented environment-variable skeleton.
- `templates/docs/README.md` — starter folder explaining publishing options (plain Markdown / GitHub Pages + Jekyll / VitePress / MkDocs).

### Changed

- `templates/.gitignore.example` — expanded into seven well-commented sections (Secrets first, then Node/Vite, Python, JVM/Android, Static sites, Firebase/cloud, IDEs, OS noise, Misc) with explanatory comments per section.
- `templates/README.md.tmpl` — added a badge block (CI / License / Standards-version) and surfaced the LICENSE file with a one-sentence MIT summary instead of placeholder text.
- `templates/CLAUDE.md.tmpl` — added Conventional Commits, Testing, and Security & Secrets sections (template now 184 lines, still under the 200-line target).

### Added — PR 1: versioning + meta-CI scaffold

- `VERSION` file at repo root declaring the current standards version.
- `CHANGELOG.md` at repo root.
- `templates/CHANGELOG.md.tmpl` — Keep-a-Changelog skeleton for downstream repos.
- `.github/workflows/self-validate.yml` — actionlint + lychee `--offline` + semver assertion + uses-line SHA-pinning lint.
- `.github/workflows/tag-release.yml` — manual `workflow_dispatch` helper that creates and pushes annotated tags from a GitHub runner.
- `.github/workflows/auto-tag.yml` — push-to-main + VERSION-changed automated tagger (creates `vX.Y.Z` and force-updates `vMAJOR` for non-prereleases).

[Unreleased]: https://github.com/Ranzlappen/repo-standards/compare/v3.0.5...HEAD
[3.0.5]: https://github.com/Ranzlappen/repo-standards/releases/tag/v3.0.5
[3.0.4]: https://github.com/Ranzlappen/repo-standards/releases/tag/v3.0.4
[3.0.3]: https://github.com/Ranzlappen/repo-standards/releases/tag/v3.0.3
[3.0.2]: https://github.com/Ranzlappen/repo-standards/releases/tag/v3.0.2
[3.0.1]: https://github.com/Ranzlappen/repo-standards/releases/tag/v3.0.1
[3.0.0]: https://github.com/Ranzlappen/repo-standards/releases/tag/v3.0.0
[2.1.1]: https://github.com/Ranzlappen/repo-standards/releases/tag/v2.1.1
[2.1.0]: https://github.com/Ranzlappen/repo-standards/releases/tag/v2.1.0
[2.0.0]: https://github.com/Ranzlappen/repo-standards/releases/tag/v2.0.0
[1.0.0]: https://github.com/Ranzlappen/repo-standards/releases/tag/v1.0.0
