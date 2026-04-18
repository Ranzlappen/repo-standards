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

1. **Branch and PR.** Never commit directly to main. Create a branch named
   `chore/upgrade-standards` and open a PR with the checklist in the description.

2. **Behavior preservation.** Refactoring may not change observable behavior.
   This includes UI, animations, storage keys, URLs, deployment shape, and
   external dependencies. If you cannot prove a refactor preserves behavior,
   skip it and add it to "Refactoring opportunities" in the PR description
   instead of doing it.

3. **Phased PRs.** Do NOT bundle docs, CI, structural changes, and refactoring
   into one mega-PR. Use this order:
     - PR 1: Docs only (README.md, CLAUDE.md, LICENSE if missing).
     - PR 2: Repo hygiene (.gitignore, dependabot.yml, repo description / topics
             noted in the PR body even if you can't set them yourself).
     - PR 3: CI / GitHub Actions workflows.
     - PR 4 (only if applicable): Refactoring per REFACTORING_GUIDE.md.
   Open them sequentially. Do not start PR N+1 until PR N is reviewed.
   If only PR 1–3 are needed, stop there.

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
  - Proposed PR sequence (1, 2, 3, optionally 4) with a 1–2 line scope per PR
  - Refactoring opportunities found (whether or not you'll act on them)

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
