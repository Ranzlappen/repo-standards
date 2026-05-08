# Step 0 — Standards version check (before anything else)

This is **Step 0** of the canonical Claude Code upgrade flow indexed by [`PROMPT.md`](../PROMPT.md). It runs after Phase 0 (migration planning) but before reading or planning the actual upgrade work in Steps 1–4. The major-version-mismatch refusal is the gate that prevents v4 rules from silently being applied to a v3 repo, or vice versa, on every future major bump.

If this step refuses, stop. Don't continue to Steps 1–4.

---

This prompt is for **repo-standards v3**. Before reading or planning anything,
verify the version compatibility:

1. Fetch the current standards version:
   `https://raw.githubusercontent.com/Ranzlappen/repo-standards/main/VERSION`
   Expected major version: **3** (i.e. the file starts with `3.`).

2. Check this repo's declared standards version. Look for:
   - `.standards-version` at the repo root (one line, e.g. `3` or `3.0.0`), OR
   - A `Standards: v3` badge in `README.md`, OR
   - A note in `CLAUDE.md` declaring the version followed.

3. Decide:
   - **Match** (both are major v3): proceed to Step 1.
   - **No declared version** in the target repo: assume the user wants the
     latest major; surface a one-line confirmation in the plan and proceed.
   - **Major mismatch** (target says v2, prompt says v3): **refuse** to
     proceed. Tell the user to either upgrade the target repo to v3 first
     (using the v2 → v3 migration guide in `templates/wiki/Migration-v2-to-v3.md`)
     or paste the v2 prompt instead.
   - **Network unavailable** (can't fetch the standards `VERSION`): proceed
     in offline-fallback mode — ask the user for the version they're
     targeting and trust their answer.

This check exists so any future major-version bump (v3 → v4) doesn't
silently apply v4 rules to a v3 repo or vice versa.
