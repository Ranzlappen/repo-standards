# Claude Code Upgrade Prompt

The standardized prompt for upgrading a Ranzlappen repo to the project's documentation, CI, and structural standards. Paste the entire **"Prompt to paste"** section below into a Claude Code session opened in the target repo, or into a GitHub issue tagged `@claude` if using the Claude Code GitHub Action.

The same prompt works in both flows.

---

## Prompt to paste

```
You are upgrading this repository to match the standards defined at:
  https://github.com/Ranzlappen/repo-standards

Before doing anything else, fetch and read these files from that repo:
  - README.md
  - UPGRADE_CHECKLIST.md
  - REFACTORING_GUIDE.md (includes the mandatory PWA Refactor Addendum)
  - templates/CLAUDE.md.tmpl
  - templates/README.md.tmpl

Then audit THIS repository against UPGRADE_CHECKLIST.md and produce one or more
pull requests that bring it into compliance.

## Ground rules (non-negotiable)

1. **Branch and PR.** Never commit directly to main. Each PR uses the branch
   it's assigned in Step 2's canonical 8-PR sequence (`chore/v2-versioning-meta`,
   `chore/v2-community-and-templates`, …). Every PR description carries the
   relevant slice of the checklist.

2. **Behavior preservation (non-negotiable).** Every change must keep
   **100% of the target repo's original functionality**. Before any edit:
     - **Analyze the target repo first.** Read the entrypoints, the build
       config, every workflow, every tracked config file, and the data
       layer. Form a mental model of what observable behavior exists *today*
       on `main` before proposing a single character of change.
     - **Flag repo-specific risks explicitly.** Every PR description and
       every post-task self-check (see rule 11) must include a
       **Repo-specific risks / edge-cases** subsection naming any quirks
       this particular repo has that interact with the change — non-obvious
       conventions, in-flight migrations, hand-rolled scripts that depend
       on file paths, undocumented env vars, browser/mobile quirks the
       project specifically handles, etc. "None observed" is an acceptable
       value, but the heading must appear.

   Refactoring may not change observable behavior. "Observable behavior"
   is everything a user, installed-PWA client, external integrator, or CI
   smoke check would notice:
     - **UI**: rendered output, layout, animations, focus order, accessibility tree.
     - **URLs**: deployed domain, route paths, query parameters, deep-link contracts.
     - **Storage**: `localStorage` / `sessionStorage` keys, IndexedDB schema
       versions, cache names, service-worker registration order.
     - **Deployment shape**: hosting target, asset URLs, build-output paths,
       redirect rules.
     - **External dependencies**: third-party endpoint shapes, webhook payloads,
       analytics identifiers, manifest `start_url` / `scope` / `id`,
       `assetlinks.json` fingerprints.
   Burden of proof is on the refactor: PR 4's Test plan must enumerate
   before/after evidence for each touched item, and PWA work additionally
   follows the **PWA Refactor Addendum** in `REFACTORING_GUIDE.md` (the
   `pwa-inventory.md` artifact is its evidence). If you cannot prove
   preservation, skip the refactor and add it to "Refactoring opportunities"
   in the PR description instead of doing it.

3. **Phased PRs.** Do NOT bundle docs, CI, structural changes, and refactoring
   into one mega-PR. Use the canonical 8-PR sequence in Step 2 below — open
   the PRs sequentially per the hard-ordering rule there, and don't start
   PR N+1 until PR N merges. Skip any PR whose scope is empty for this repo
   (with a one-line reason).

4. **Templates are starting points, not gospel.** Adapt the CLAUDE.md and
   README.md skeletons to this project's actual architecture. Don't paste
   placeholder text — fill it in with real content based on what you find in
   the repo.

5. **Length discipline for CLAUDE.md.** Target under 200 lines. If you find
   yourself writing more, you're including things Claude could infer from the
   code. Cut.

6. **Single-file projects get special handling.** If this repo is a single
   large HTML/JS or Python file (>800 lines), follow REFACTORING_GUIDE.md
   carefully. Refactoring is its own PR (PR 4). Do NOT refactor in PR 1–3.

7. **PWA detection is automatic and triggers extra protections.** During
   Step 1, check for any of: `sw.js` / `service-worker.js`, `manifest.json` /
   `manifest.webmanifest`, `<link rel="manifest">`, `.well-known/assetlinks.json`,
   calls to `navigator.serviceWorker.register`, `Notification.requestPermission`,
   `caches.open`, IndexedDB, or `localStorage`/`sessionStorage`. If ANY are
   present, the project is a PWA (or has installed users via storage) and
   the entire **PWA Refactor Addendum** in REFACTORING_GUIDE.md applies
   automatically. Produce the `pwa-inventory.md` artifact in PR 4's description
   without being asked. Apply every rule in that addendum without asking.

8. **Default to autonomy. Ask only when truly necessary.** The user has
   explicitly asked for minimal correspondence. Make decisions yourself for
   anything reversible or anything covered by the standards. The narrow list
   of cases that DO require stopping and asking the user:
     - A storage key, schema version, manifest `start_url`/`scope`/`id`, or
       `assetlinks.json` would have to change to complete the work.
     - The deployed URL would change.
     - A tracked file or major directory would have to be deleted (not moved).
     - You discover the project is broken on `main` (not just imperfect — actually
       broken) and fixing it is outside the upgrade scope.
     - The standards themselves don't fit the project and you need a judgment call
       on which rule to bend.
   Everything else: decide, do, document in the PR. Do not ask permission for
   bumping cache versions, updating manifest paths to match moved assets,
   adding `skipWaiting`/`clients.claim`, choosing module boundaries, naming
   modules, picking which CI workflow template to start from, or any other
   reversible call. The PR is the conversation — the user reviews there.

9. **Tiny commits — one file per response.** Make exactly one file change
   per commit unless the change is atomically inseparable across two files
   (rare). Each commit is preceded by a one-paragraph plain-English plan,
   followed by a post-task self-check (file exists / YAML/JSON parses /
   links resolve / line count consistent), and a one-line summary. This is
   the rhythm the user has chosen for *every* upgrade — do not bundle
   unrelated changes into a single commit even if they all belong in the
   same PR.

10. **Conventional Commits required.** Every commit message uses the
    Conventional Commits spec
    (https://www.conventionalcommits.org/en/v1.0.0/). Recommended scopes
    for repo upgrades: `version`, `meta`, `tmpl`, `wf` (workflow), `gh`
    (community files), `wiki`, `prompt`, `checklist`, `dependabot`,
    `release`. Breaking changes get `!` and a `BREAKING CHANGE:` footer.
    Non-conformant messages are blocked locally by the `commit-msg` hook
    in `templates/.pre-commit-config.yaml`.

11. **Post-task self-check is mandatory after every code change.** Run two
    self-checks per commit:

      a. **Drift-detection** (defined in `CLAUDE.md.tmpl`'s "Post-task
         self-check" block): does this change introduce something that
         should be codified in docs, workflows, or `dependabot.yml`?

      b. **Mechanical verification** — at minimum:
           - **Files exist** at every path the commit adds or modifies.
           - **YAML/JSON parses** for any touched workflow, manifest,
             lockfile, or config.
           - **Links resolve** in touched markdown — relative paths point
             to real files, anchors to real headings.
           - **Line-count delta matches the plan** stated before the
             commit (e.g. "+15 lines" predicted, +15 measured).
           - **No template placeholders remain** — `<PROJECT_NAME>`,
             `<OWNER>`, `<REPO>`, or unfilled `<TODO>` markers introduced
             by templates are absent from tracked files outside
             `templates/`.

    Output both results inline in the response that proposes the next
    change. Every commit that changes tracked files runs this — the
    template's "skip for pure Q&A turns" exception does NOT apply during
    a repo-upgrade pass. This is how doc drift and inconsistent state are
    caught before they accumulate.

12. **No PR opens without explicit user confirmation.** After the last
    commit of a category lands on the working branch, stop and ask the
    user to confirm before calling `mcp__github__create_pull_request` (or
    its CLI equivalent). Drafts are okay if the user explicitly asks. PR
    sequencing is sequential: PR N must merge before PR N+1 opens.

## Step 0 — Standards version check (before anything else)

This prompt is for **repo-standards v2**. Before reading or planning anything,
verify the version compatibility:

1. Fetch the current standards version:
   `https://raw.githubusercontent.com/Ranzlappen/repo-standards/main/VERSION`
   Expected major version: **2** (i.e. the file starts with `2.`).

2. Check this repo's declared standards version. Look for:
   - `.standards-version` at the repo root (one line, e.g. `2`), OR
   - A `Standards: v2` badge in `README.md`, OR
   - A note in `CLAUDE.md` declaring the version followed.

3. Decide:
   - **Match** (both are major v2): proceed to Step 1.
   - **No declared version** in the target repo: assume the user wants the
     latest major; surface a one-line confirmation in the plan and proceed.
   - **Major mismatch** (target says v1, prompt says v2): **refuse** to
     proceed. Tell the user to either upgrade the target repo to v2 first
     (using the v1 → v2 migration guide in `templates/wiki/Migration-v1-to-v2.md`)
     or paste the v1 prompt instead.
   - **Network unavailable** (can't fetch the standards `VERSION`): proceed
     in offline-fallback mode — ask the user for the version they're
     targeting and trust their answer.

This check exists so any future major-version bump (v2 → v3) doesn't
silently apply v3 rules to a v2 repo or vice versa.

## Step 1 — Read and audit

Read every top-level file in the repo. Read the entrypoints of every code
directory. Build a mental model of:
  - What this project does (one sentence)
  - How it's built and deployed
  - What languages, frameworks, and external services it uses
  - What conventions exist (naming, structure, error handling)
  - What's missing that the checklist requires

## Step 2 — Plan

Post a single comment (or your initial Claude Code response) containing:
  - One-sentence project summary
  - Detected stack and deployment shape
  - Checklist results: for each item, mark ✓ / — / ⚠️ with a short reason
  - Proposed PR sequence using the **canonical 8-PR template** below;
    omit any PR whose scope doesn't apply to this repo and say so explicitly
  - Refactoring opportunities found (whether or not you'll act on them)

### Canonical 8-PR sequence for v2 upgrades

Follow this order unless the audit shows a PR has nothing to do (in which
case skip with a one-line reason). PRs are sequential — PR N+1 only opens
after PR N merges.

| # | Branch | Scope |
|---|---|---|
| 1 | `chore/v2-versioning-meta` | `VERSION` + `CHANGELOG.md` + `self-validate.yml` + (if applicable) `tag-release.yml` and `auto-tag.yml`. |
| 2 | `chore/v2-community-and-templates` | `templates/.github/` community files + tooling configs + expanded `.gitignore.example` + `templates/docs/` + badge block + new CLAUDE.md.tmpl sections. |
| 3 | `chore/v2-wiki-templates` | `templates/wiki/*.md` + new optional Wiki phase in PROMPT + new section 9 in checklist. |
| 4 | `chore/v2-ci-hardening` | least-privilege `permissions:` blocks + 40-char SHA pinning + `timeout-minutes` + cached lint/test tools + reusable lint-and-test + security-scan + release-please. |
| 5 | `chore/v2-prompt-hardening` | PROMPT.md ground rules 9–12 + Step 0 version check + canonical 8-PR sequence. |
| 6 | `chore/v2-checklist-expansion` | `UPGRADE_CHECKLIST.md` new sections (Security, A11y/Perf/SEO, Testing & Quality, Standards Versioning). |
| 7 | `chore/v2-dependabot-tighten` | `dependabot.yml` v2 expectations: limits, conventional-commit prefixes, labels, npm/pip dev-vs-prod split. |
| 8 | `chore/v2-readme-and-tag` | Root README "Next-level features (v2)" + standards-version badge; bump VERSION to `2.0.0`; cut CHANGELOG; tag `v2.0.0` and `v2`. |

**Hard ordering** (what must come before what):
- PR 1 first.
- PRs 2, 3, and 7 can run in parallel after PR 1.
- PR 4 needs PR 2 done first.
- Then PR 5 → PR 6 → PR 8, strictly sequential.

**Practical execution** (one PR at a time): PR 1 → 2 → 3 → 4 → 7 → 5 → 6 → 8.

Skip any PR whose scope is empty for this repo (e.g. no PWA code → PR 4's
PWA-relevant subsections drop out; no Python code → ruff/pytest configs
in PR 2 are skipped).

WAIT for user confirmation before opening any PR. The plan is the
deliverable for this step.

## Step 3 — Execute, one PR at a time

For each approved PR:
  - Create the branch
  - Make the changes
  - Open the PR
  - Use this PR description structure:

    ```
    ## Summary
    One paragraph: what this PR does and why.

    ## Checklist coverage
    Pasted UPGRADE_CHECKLIST items addressed by this PR, marked ✓ / — / ⚠️.

    ## Refactoring opportunities (not in this PR)
    Bulleted list of things worth doing next.

    ## Test plan
    How to verify this PR doesn't break anything. For docs PRs: "N/A".
    For CI PRs: "Workflow file is valid YAML; will run on next push."
    For refactoring PRs: full behavior-verification checklist per
    REFACTORING_GUIDE.md.
    ```

  - WAIT for review/merge before starting the next PR.

## Step 4 — Wiki seeding (optional, only if user opts in)

Skip this step entirely unless the user explicitly says "seed the wiki" (or
similar). If they do:

1. Confirm the repo's GitHub Wiki is enabled. If it isn't, ask the user to
   enable it from the repo's Settings → Features → Wikis. The Wiki must be
   enabled before content can be pasted in.
2. For each file in `templates/wiki/` (Home.md, Architecture.md, FAQ.md,
   Upgrade-History.md, PWA-Safety.md, Migration-v1-to-v2.md, _Sidebar.md,
   _Footer.md), substitute `<PROJECT_NAME>`, `<OWNER>`, `<REPO>`, and any
   other placeholders to match this project. Fill in the architecture and
   FAQ specifics from what the audit in Step 1 surfaced.
3. Output the substituted Markdown for each page back to the user as a
   single response per page, in fenced code blocks they can copy. The user
   pastes each into the Wiki tab via the GitHub web UI.
4. Do NOT attempt to push to `<repo>.wiki.git` from inside this session.
   GitHub Wiki edits are user-driven in v2; automated pushes are out of
   scope.
5. Update the `Upgrade-History` page with the entry for this upgrade as
   the first content the user pastes, so the wiki has a real first entry
   from the start.

This phase is purely additive: skipping it never blocks the rest of the
upgrade.

## Final note on adaptation

If anything in the standards genuinely doesn't fit this project, say so in
the plan and propose how to handle it. The standards are meant to be lived
with, not enforced robotically. If your audit reveals something that should
be added to UPGRADE_CHECKLIST.md or the templates themselves, mention that
too — it's a separate PR against the standards repo.

Begin with Step 1.
```

---

## Notes on the two flows

**GitHub Action flow (recommended for phone):**
- Open a new issue in the target repo with the title "Upgrade to repo standards" and the prompt above as the body, with `@claude` at the very top.
- Claude posts a plan as a comment.
- Reply to confirm the plan or adjust scope.
- Claude opens PRs sequentially. Review and merge each from the GitHub mobile app.

**Direct Claude Code session:**
- `cd` into the repo (or open it in the Claude Code Android app via `claude remote-control`).
- Paste the prompt.
- Same flow — plan, then PRs.

If you want Claude to handle the standards repo itself (not the target repo), just say "this is the standards repo, audit it for self-consistency instead" — the audit still applies.
