# Changelog

All notable changes to **repo-standards** are recorded here. Format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/) and the project uses [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

Consumer repos pin a major version (`v1`, `v2`, …) by referencing the matching git tag.

## [Unreleased]

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

[Unreleased]: https://github.com/Ranzlappen/repo-standards/compare/v3.0.0...HEAD
[3.0.0]: https://github.com/Ranzlappen/repo-standards/releases/tag/v3.0.0
[2.1.1]: https://github.com/Ranzlappen/repo-standards/releases/tag/v2.1.1
[2.1.0]: https://github.com/Ranzlappen/repo-standards/releases/tag/v2.1.0
[2.0.0]: https://github.com/Ranzlappen/repo-standards/releases/tag/v2.0.0
[1.0.0]: https://github.com/Ranzlappen/repo-standards/releases/tag/v1.0.0
