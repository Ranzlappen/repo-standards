# Ground rules — non-negotiable

The **18 non-negotiable ground rules** of the canonical Claude Code upgrade flow indexed by [`PROMPT.md`](../PROMPT.md). They apply to every commit, every PR, and every Step (0–5) of the flow.

- Rules **1–8** cover branching, behavior preservation, phased PRs, templates as starting points, length discipline, single-file projects, PWA detection, and default-to-autonomy.
- Rules **9–12** codify the tiny-commit / Conventional Commits / mandatory-self-check / no-PR-without-confirmation rhythm — the same rhythm this repo's own v2 and v3 upgrade passes followed end to end.
- Rules **13–15** cover out-of-scope auto-issuing (with opt-out), the single-feature-branch / single-PR alternative operating mode, and plan-file hygiene (the Plan Management & Clean State Rule).
- Rule **16** is the **Conflict / Assumption Failure Protocol** — the critical-safety rule that overrides every other rule when an assumption fails or an unexpected problem hits mid-execution.
- Rules **17–18** are the **branch-lifecycle rules** — the merged-PR branch guard (never keep committing to a branch whose PR already merged) and the rebase-when-behind rule (bring a working branch current against `main` before continuing).

Every cross-reference elsewhere in the repo (`UPGRADE_CHECKLIST.md`, `REFACTORING_GUIDE.md`, `templates/CLAUDE.md.tmpl`, `templates/README.md.tmpl`) cites "`PROMPT.md` rule N" — those numbers map to the rules below.

---

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
   into one mega-PR. Use the canonical 8-PR sequence in
   [`prompt/02-canonical-pr-sequence.md`](./02-canonical-pr-sequence.md) — open
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
    its CLI equivalent). Clicking the **"Approve plan mode"** button — or
    replying with "yes", "approved", "proceed", "confirmed", "go ahead",
    or similar — counts as explicit confirmation. Drafts are okay if the
    user explicitly asks. PR sequencing is sequential: PR N must merge
    before PR N+1 opens.

13. **Out-of-scope findings auto-file an issue (opt-out).** When the
    upgrade pass surfaces something unrelated to the current task or PR,
    auto-file a GitHub issue with
    `gh issue create --title "<summary>" --body "<context>"
    --label "out-of-scope,from-claude"` and link it from the PR's
    "Refactoring opportunities" subsection. **Opt out** by setting the
    repo variable `DISABLE_OUT_OF_SCOPE_ISSUES=true` — under opt-out,
    surface the finding only in the PR description and skip the issue.

14. **Alternative Operating Mode: Single Feature Branch / Single PR.**
    The default is the canonical 8-PR sequence above. For focused work
    that would otherwise produce three or fewer PRs (small repos, polish
    passes, single-module refactors), the user may approve a one-branch /
    one-PR mode. In that mode: open the PR draft after the first commit,
    subscribe to PR activity (`gh pr subscribe <PR#>` or the MCP
    equivalent) so CI failures and review comments arrive in the
    session, push every subsequent commit to the same branch (each one
    re-triggers integrity workflows), and mark ready-for-review only at
    completion. Per-change ritual (rules 9 and 11) still applies to
    every commit.

15. **Plan Management & Clean State Rule.** When the user asks for a
    new plan, or when plan mode reopens during a long session, start a
    fresh plan file or actively prune completed sections. Never append
    to an old plan that already contains shipped work — that's how plan
    bloat happens. Keep plan files concise and focused on the remaining
    scope.

16. **Conflict / Assumption Failure Protocol (critical safety rule).**
    If at any point during execution you discover that an assumption
    in the Phase 0 plan or any later step was wrong, or you encounter
    an unexpected problem, **do not make any self-decided compromises
    or adjustments**. Immediately stop, clearly state the exact issue
    and the assumption that failed, propose 2–3 concrete options with
    trade-offs, and wait for my explicit confirmation before proceeding.
    Never silently alter the plan, skip steps, or decide on a
    workaround yourself.

    This rule **overrides every other rule in this file** when they
    conflict. Examples of triggers: a file the plan assumed exists
    doesn't; a CI check the plan didn't anticipate gates the merge;
    a `git push` is rejected and the workaround changes the PR
    boundary; a refactor uncovers behavior the Phase 0 audit missed;
    a tool returns a permissions error the plan didn't budget for.
    In all such cases: stop, surface the failure, propose options,
    wait. Clicking the **"Approve plan mode"** button — or replying
    with "yes", "approved", "proceed", "confirmed", "go ahead", or
    similar (per rule 12) — counts as explicit confirmation.

17. **Merged-PR branch guard — never keep committing to a branch
    whose PR already merged.** A long or resumed session can drift
    into adding commits to the branch it was *last* on — but if that
    branch's PR has already merged, the new commits land on a dead
    branch. They will never be reviewed or merged through that closed
    PR, and the **"View PR"** button in the Claude Code chat keeps
    pointing at the already-merged PR (a known Claude Code failure
    mode). Guard against it:
      - **Check before you commit or push** in any continuing or
        resumed session — and always before starting the next PR in
        the canonical sequence — whether the current branch's PR is
        still open. Use `gh pr view <branch> --json state,mergedAt`
        (or the MCP `pull_request_read` equivalent). The branch is
        also effectively dead if it is already contained in
        `origin/main` (`git branch --merged origin/main` lists it).
      - **If the PR is merged** (or the branch is already in
        `origin/main`), do **not** add commits to it. Instead:
        `git fetch origin main`, cut a **new** branch from
        `origin/main` (the next canonical branch name, or a fresh
        `<type>/<scope>` per rule 1), move the pending work there, and
        open a **new** PR — subject to rule 12 confirmation.
      - **GitHub cannot reopen a *merged* PR.** `gh pr reopen` only
        works on PRs that were closed **without** merging (and whose
        head branch still exists). So: closed-unmerged → reopening is
        an option; merged → always a fresh branch and a new PR.
      - This is the guard that makes the rule 1 (branch per PR) /
        rule 12 (PR N merges before N+1 opens) transition safe — the
        moment a PR merges, its branch is retired.

18. **Keep the working branch current — rebase onto `main` when
    behind.** When the working branch falls behind `origin/main` —
    `main` moved while a PR was open, or you're about to start the
    next PR in the sequence — bring it up to date by **rebasing, not
    merging**:
      - `git fetch origin main` then `git rebase origin/main`.
      - Rebase (not a merge commit) keeps history linear, matching the
        governance template's **Require linear history** and
        **Require branches to be up to date before merging**
        branch-protection rules (`templates/.github/GOVERNANCE.md`).
        Squash-merge is the default merge style, so a linear working
        branch is the expected input.
      - New branches in the canonical 8-PR sequence are always cut
        from freshly-fetched `origin/main`, so each one starts current
        (this pairs with rule 17's "fetch main, cut a new branch").
      - If the rebase hits conflicts the plan didn't anticipate, that
        is a **rule 16** trigger: stop, state the conflict, propose
        2–3 options, and wait for explicit confirmation before
        resolving — do not silently force-resolve.
