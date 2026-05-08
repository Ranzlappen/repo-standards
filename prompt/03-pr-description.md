# Step 3 — Execute, one PR at a time

**Step 3** of the canonical Claude Code upgrade flow indexed by [`PROMPT.md`](../PROMPT.md). The PR description structure required for every PR opened during a v2 upgrade pass.

Step 3 runs after Step 2's plan has been confirmed by the user (per rule 12 in [`prompt/01-ground-rules.md`](./01-ground-rules.md): no PR opens without explicit user confirmation). Per-change ritual from rules 9 (tiny commits) and 11 (post-task self-check) applies to every commit made under each PR.

---

For each approved PR:
  - Create the branch
  - Make the changes
  - Open the PR
  - Use this PR description structure:

    ~~~
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
    ~~~

  - WAIT for review/merge before starting the next PR.
