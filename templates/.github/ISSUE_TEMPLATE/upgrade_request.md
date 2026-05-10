---
name: Upgrade to repo-standards
about: Trigger a Claude Code upgrade to the latest Ranzlappen repo-standards.
title: 'Upgrade to repo-standards'
labels: 'standards-upgrade'
assignees: ''
---

@claude

You are upgrading this repository to match the standards defined at:
  https://github.com/Ranzlappen/repo-standards

Before doing anything else, fetch and read these files from that repo:
  - VERSION
  - README.md
  - UPGRADE_CHECKLIST.md
  - REFACTORING_GUIDE.md (includes the mandatory PWA Refactor Addendum)
  - PROMPT.md
  - templates/CLAUDE.md.tmpl
  - templates/README.md.tmpl

Then follow `PROMPT.md` end-to-end, treating that file as the
authoritative spec for what to do. The summary of expectations:

1. Verify the standards version. Refuse to proceed unless the
   standards-repo `VERSION` file matches the version this repo is
   targeting (declared in this repo's `.standards-version`, falling
   back to the latest major).
2. Audit this repo against `UPGRADE_CHECKLIST.md`. Post a single
   plan comment on this issue with: one-sentence project summary,
   detected stack, checklist results (✓ / — / ⚠️), proposed phased
   PR sequence.
3. WAIT for confirmation in this issue before opening any PR. Replying
   with "approved", "yes", "proceed", "confirmed", "go ahead", or a 👍
   reaction on Claude's plan comment counts as explicit confirmation.
4. Open PRs in the order PROMPT.md specifies. One small change per
   commit; conventional commits; tiny PRs; mandatory post-task
   self-check after every edit.
5. Do not bundle docs, CI, structural changes, and refactoring
   into one mega-PR.
6. PWA detection is automatic and triggers extra protections —
   apply the PWA Refactor Addendum without being asked.

Begin with Step 1.
