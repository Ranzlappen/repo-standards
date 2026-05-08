# Security policy

## Reporting a vulnerability

Please **do not** open a public issue for vulnerabilities in this repository.

Use one of the private channels below:

1. **GitHub private vulnerability reporting** (preferred): [open a draft advisory](../../security/advisories/new).
2. **Direct message** to the repo owner ([`@Ranzlappen`](https://github.com/Ranzlappen)) with a description, reproduction steps, and any relevant logs.

Include in the report:

- A summary of the issue.
- Steps to reproduce.
- The version / commit SHA you tested against.
- Your assessment of impact.
- Optional: a proposed fix.

You can expect:

- An acknowledgement within **3 business days**.
- A triage decision (accepted / needs more info / not a vulnerability) within **10 business days**.
- A coordinated disclosure window once a fix is identified — typically 30–90 days, longer for complex issues.

## Supported versions

| Version | Supported |
| --- | --- |
| Latest `main` | ✅ |
| Latest tagged release (`v3.x`) | ✅ |
| `v2.x` tagged releases | ⚠️ Best-effort backports until `v3` reaches one downstream upgrade |
| `v1.x` and older | ❌ Out of scope |
| Forks | ❌ Out of scope |

## Threat model

This repository ships **documentation, prompts, and template files** — no executable code beyond the meta-CI workflows in `.github/workflows/`. The realistic threat surface is:

1. **Workflow tampering** — a malicious PR that changes a `uses:` line to an unpinned ref or a tampered SHA. Mitigated by `validate-sha-pinning` (hard-fails any `uses:` not pinned to a 40-char SHA) in [`.github/workflows/self-validate.yml`](./workflows/self-validate.yml).
2. **Template poisoning** — a change to a `templates/` file that ships a backdoor downstream. Mitigated by branch protection (required review on `main`) plus the standards-versioning check in `PROMPT.md` Step 0 (downstream consumers pin a major; a malicious commit on `main` doesn't propagate until a consumer re-tags).
3. **Secret leakage** — accidental commit of a token, key, or credential. Mitigated by `gitleaks` in [`templates/.github/workflows/security-scan.yml`](../templates/.github/workflows/security-scan.yml) (runs on every PR + push to main + weekly schedule once that workflow is also installed at the root level).

## Supply-chain commitments

This repo tracks against the following supply-chain primitives. Status legend: **live** = enforced by CI on `main`; **in flight** = wired but waiting on an external trust setup or a future major; **aspirational** = on the long-term roadmap.

| Primitive | Status | Mechanism |
| --- | --- | --- |
| **SHA-pinning of every `uses:` line** | live | Hard-failed by [`validate-sha-pinning`](./workflows/self-validate.yml) — any 40-char-SHA mismatch exits 1 with `::error`. Major-version pins (`@v6`) and floating refs (`@main`) are rejected. |
| **OpenSSF Scorecard score floor ≥ 7.0** | live | [Scorecard badge](https://securityscorecards.dev/viewer/?uri=github.com/Ranzlappen/repo-standards) on the README; `scorecard` job in `templates/.github/workflows/security-scan.yml` runs weekly + on `branch_protection_rule` changes + on push-to-main. SARIF lands in the Security tab. |
| **Dependency review on every PR to `main`** | live | `templates/.github/workflows/dependency-review.yml` — fails on `high`-severity CVEs, comments diff summary on the PR. (Best-effort for this repo, which has no runtime deps; binding on every consumer.) |
| **Workflow-property sidecar pairing** | live | Hard-failed by `validate-workflow-properties` — every workflow template ships a `*.properties.json` sidecar with `name` / `description` / `iconName` / `categories` / `filePatterns`; orphans are rejected in either direction. |
| **CodeQL on every language present** | live (downstream) | `templates/.github/workflows/security-scan.yml` runs CodeQL on the matching language matrix on PR + push + weekly. |
| **Gitleaks full-history secret scan** | live (downstream) | Same workflow, same triggers, separate job. |
| **Signed releases via [sigstore](https://www.sigstore.dev/) / cosign** | in flight | Release-please artifacts will carry `.sig` files + transparency-log entries once the publishing OIDC trust is configured per registry. See `templates/.github/workflows/release-please.yml` header comments for the npm / PyPI / GHCR setup pages. |
| **SLSA build provenance — target Level 3** | in flight | The `release-please.yml` GHCR publish path already emits provenance + SBOM; npm and PyPI publish paths use OIDC trusted publishing with `--provenance` where the registry supports it. Level-3 attestation lands when sigstore signing above is live. |
| **Reproducible builds** | aspirational | N/A for a docs/templates repo; downstream consumers' build pipelines are responsible for reproducibility. |

The Scorecard score is the single rolled-up health metric — a regression below 7.0 is a separate `security` PR, not folded into routine work. See [`templates/.github/GOVERNANCE.md`](../templates/.github/GOVERNANCE.md) "Supply-chain governance" for the score-floor and required-checks policy.

## Out of scope

- Vulnerabilities in third-party actions used by templates that have not yet been patched upstream — please report those to the upstream project first. Once an upstream fix exists, a report here is welcome to track our adoption (we'll bump the SHA pin).
- Social engineering, phishing, or physical attacks against contributors.
- Issues that require an attacker to already control the user's device or network at a level that bypasses normal browser/OS sandboxing.
- "The template recommends X but I want Y" — that's a feature request, not a security report; open a normal issue.
