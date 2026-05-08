# Sponsors

Thank you to everyone who has, does, or might support **Ranzlappen Repo Standards**. The repo is a permanent work-in-progress — every downstream upgrade pass surfaces another rule worth codifying — and time spent on it is largely time funded by sponsors.

## What sponsorship funds

- **Standards research.** Reading through GitHub's starter-workflows, OpenSSF best practices, SLSA / sigstore primitives, and the policy fine-print that turns into rule changes here.
- **Downstream upgrade passes.** Running the full canonical 8-PR sequence on the next consumer repo, fixing whatever the audit shakes loose, and folding learnings back into `templates/` and `UPGRADE_CHECKLIST.md`.
- **CI maintenance.** Keeping the SHA pins, sidecar metadata, and self-validate gates current as upstream actions release new versions.
- **Mobile-first DX.** Shrinking the friction of the GitHub-mobile + `@claude` flow, since the repo is built for phone-driven repo upkeep.

## How to sponsor

The Sponsor button on the repo page surfaces every active route. The wiring lives in [`.github/FUNDING.yml`](./.github/FUNDING.yml). All routes are private payments to the repo owner; no entity, foundation, or LLC sits between you and the work.

If a sponsorship route you'd prefer isn't listed, open an issue or DM and we'll add it.

## What sponsorship does **not** buy

- **No endorsements.** Sponsors are not credited inside the standards themselves, in template files, or in `CHANGELOG.md` entries. The standards must read as if they were unsponsored. Public thank-yous (in this file, on the Sponsor page) are fine; embedded recommendations are not.
- **No priority on rule changes.** Issues are triaged on technical merit, not sponsor status. A sponsor-filed issue and a non-sponsor-filed issue follow the same lifecycle in [`.github/CONTRIBUTING.md`](./.github/CONTRIBUTING.md).
- **No private forks of the standards.** The standards are MIT — sponsors are welcome to fork, but a sponsorship doesn't create a private branch of the rules.

## Recognition

This file is the recognition surface. Once the first GitHub-Sponsors-tier route is live and a sponsor has explicitly opted into being listed, names land here in alphabetical order under a `## Current sponsors` heading. Anonymous sponsorship is the default.

## Tiers

There are no formal tiers. The Sponsor button surfaces whichever platforms are active in `FUNDING.yml`; whatever each platform exposes is what's available. Sponsorship-as-philanthropy rather than sponsorship-as-perks-bundle.

---

*Last updated: 2026-05-08 (v3.0.0 cut). For the boilerplate template that downstream repos adopt, see [`templates/.github/FUNDING.yml`](./templates/.github/FUNDING.yml).*
