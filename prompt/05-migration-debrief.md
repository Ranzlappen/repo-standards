# Step 5 — Migration debrief

**Step 5** of the canonical Claude Code upgrade flow indexed by [`PROMPT.md`](../PROMPT.md). Mandatory by default. Produces a single Markdown debrief at the end of every migration pass — the rolled-up record of what shipped, what didn't, and why.

Skip this step only when the user explicitly says "skip the debrief" (or similar). Per-PR descriptions (Step 3) and per-commit self-checks (rule 11) cover *intra*-pass communication; the debrief covers *post*-pass communication. The debrief is the single artifact a returning reviewer reads to understand the session's outcome without re-walking every PR.

---

After the last PR of the migration pass merges (or the user signals "done"), produce a single Markdown debrief covering:

1. **Headline** — From standards version → To standards version, total PRs merged, session date (UTC, ISO).

2. **What landed** — Bulleted list of merged PRs. One bullet per PR: branch name + one-sentence scope summary + PR link + merged-commit SHA.

3. **What didn't land — and why** — For every item from the Phase 0 scoring table marked **must / should / could** that was NOT shipped: the item name, the **reason** (technical blocker / out-of-scope finding / user-deferred / dependency on unmerged upstream / time / scope drift), and the next-step (issue link, follow-up branch, or "documented for next pass"). Items marked **skip** in Phase 0 are out of scope for this section by definition — don't list them.

4. **Out-of-scope issues filed** — List of GitHub issues opened during the session per [rule 13](./01-ground-rules.md). One bullet per issue: title, URL, label.

5. **Follow-ups for the next pass** — Anything noted but not actioned that should feed Phase 0 of the next upgrade. One bullet per item; cross-reference rule-13 issues where applicable. "None" is acceptable.

6. **Repo-state delta** — `.standards-version` before → after; tag created (if any); workflows added/removed; templates touched.

## Delivery

- **GitHub Action flow:** post the debrief as a final comment on the originating "Upgrade to repo standards" issue, then close the issue.
- **Direct Claude Code session:** post as the final response in the session.
- **If [Step 4](./04-wiki-seeding.md) (wiki seeding) was taken:** the Headline + Scope (derived from the *What landed* + *Repo-state delta* sections) + Notes (derived from the *What didn't land* + *Follow-ups* sections) are exactly the structure of a new entry in `templates/wiki/Upgrade-History.md`. Substitute the placeholders and output the entry as the final additional artifact for the user to paste into the wiki.

## Boundary

The debrief must NOT introduce new findings — every item it lists must already exist as a per-PR description, an out-of-scope issue, a self-check finding, or a Phase 0 scoring-table row. **It is a roll-up, not a re-audit.** If the debrief would surface something genuinely new, that's a rule-13 out-of-scope issue first; it then enters the debrief by reference.
