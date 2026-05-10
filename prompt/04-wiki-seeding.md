# Step 4 — Wiki seeding (optional, only if user opts in)

**Step 4** of the canonical Claude Code upgrade flow indexed by [`PROMPT.md`](../PROMPT.md). Skipped by default; runs only when the user explicitly says "seed the wiki" (or similar).

Manual paste via the GitHub web UI; no automated `.wiki.git` push from inside the upgrade session. Skipping this step never blocks the rest of the upgrade.

---

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
   from the start. The entry's Headline / Scope / Notes blocks come from
   the Step 5 debrief produced in [`prompt/05-migration-debrief.md`](./05-migration-debrief.md);
   Step 5 produces them whether or not Step 4 was taken, so when both
   apply, reuse them verbatim instead of re-deriving.

This phase is purely additive: skipping it never blocks the rest of the
upgrade.
