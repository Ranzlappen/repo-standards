#!/usr/bin/env python3
"""dogfood-audit.py — assert this repo passes its own UPGRADE_CHECKLIST.

Run from repo root. Prints PASS / FAIL per assertion; exits 1 on any FAIL
with a summary count. Called from .github/workflows/dogfood-audit.yml on
every PR + push to main + weekly schedule, and runnable locally for fast
feedback.

Eight assertion groups covering the mechanically-verifiable invariants
in UPGRADE_CHECKLIST.md:

  [1] Root LICENSE — file exists, MIT first line, no <PLACEHOLDER>s.
  [2] Versioning — VERSION + .standards-version exist, majors aligned,
      VERSION parses as semver.
  [3] Root community files — all 7 dogfooded files present.
  [4] Live workflows — all 7 workflows present at .github/workflows/.
  [5] README badges — Standards / License / OpenSSF Scorecard URLs valid.
  [6] Modular prompt files — all 7 prompt/*.md present + master prompt.
  [7] Placeholder hygiene — no <PROJECT_NAME>, <OWNER>, <REPO>, <TODO>
      leakage in tracked files outside templates/ (per ground rule 11
      mechanical verification).
  [8] Workflow-sidecar pairing — every templates/.github/workflows/*.yml
      has a matching .properties.json sidecar; no orphans.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

_argparser = argparse.ArgumentParser(
    description="Assert this repo passes its own UPGRADE_CHECKLIST. Exits 1 on any FAIL.",
)
_argparser.add_argument(
    "-v",
    "--verbose",
    action="store_true",
    help="emit the underlying check (file path / regex pattern) before each PASS/FAIL line",
)
ARGS = _argparser.parse_args()
VERBOSE = ARGS.verbose

passes = 0
fails = 0


def trace(msg: str) -> None:
    if VERBOSE:
        print(f"  [verbose] {msg}")


def ok(msg: str) -> None:
    global passes
    passes += 1
    print(f"  PASS  {msg}")


def ng(msg: str) -> None:
    global fails
    fails += 1
    print(f"  FAIL  {msg}")


def assert_file(path: str, label: str | None = None) -> bool:
    p = ROOT / path
    label = label or path
    trace(f"is_file({p})")
    if p.is_file():
        ok(f"{label} exists")
        return True
    ng(f"{label} MISSING ({path})")
    return False


def assert_grep(pattern: str, path: str, label: str) -> bool:
    p = ROOT / path
    trace(f"grep r{pattern!r} against {p}")
    if not p.is_file():
        ng(f"{label} (file missing: {path})")
        return False
    if re.search(pattern, p.read_text()):
        ok(label)
        return True
    ng(f"{label} (pattern not found in {path})")
    return False


def section(name: str) -> None:
    print()
    print(name)


# ───────────────────────────────────────────────────────────────────────────
print("── dogfood-audit ──")
print(f"Repo: {ROOT}")

section("[1/8] Root LICENSE")
if assert_file("LICENSE"):
    text = (ROOT / "LICENSE").read_text()
    if text.splitlines()[0].strip() == "MIT License":
        ok("LICENSE first line is 'MIT License'")
    else:
        ng("LICENSE first line is not 'MIT License'")
    if re.search(r"<[A-Z_]+>", text):
        ng("LICENSE has unfilled <PLACEHOLDER>s")
    else:
        ok("LICENSE has no unfilled placeholders")

section("[2/8] Versioning files")
v_ok = assert_file("VERSION")
sv_ok = assert_file(".standards-version")
if v_ok and sv_ok:
    v = (ROOT / "VERSION").read_text().strip()
    sv = (ROOT / ".standards-version").read_text().strip()
    v_major = v.split(".", 1)[0]
    sv_major = sv.split(".", 1)[0]
    if v_major == sv_major:
        ok(f"VERSION ({v_major}.x) and .standards-version ({sv_major}.x) majors aligned")
    else:
        ng(f"VERSION major ({v_major}) != .standards-version major ({sv_major})")
    if re.match(r"^\d+\.\d+\.\d+(-[A-Za-z0-9.-]+)?(\+[A-Za-z0-9.-]+)?$", v):
        ok(f"VERSION is semver ({v})")
    else:
        ng(f"VERSION is not semver ({v!r})")

section("[3/8] Root community files")
for f in [
    "SPONSORS.md",
    ".github/CODE_OF_CONDUCT.md",
    ".github/CONTRIBUTING.md",
    ".github/SECURITY.md",
    ".github/FUNDING.yml",
    ".github/CODEOWNERS",
    ".github/dependabot.yml",
]:
    assert_file(f)

section("[4/8] Live workflows at .github/workflows/")
for wf in [
    "auto-tag",
    "self-validate",
    "tag-release",
    "security-scan",
    "dependency-review",
    "workflow-summary",
    "dogfood-audit",
]:
    assert_file(f".github/workflows/{wf}.yml")

section("[5/8] README badges")
assert_grep(r"shields\.io/badge/standards-v\d+\.\d+\.\d+", "README.md", "Standards badge cites a semver")
assert_grep(r"shields\.io/badge/License-MIT.*\]\(\./LICENSE\)", "README.md", "License badge points at ./LICENSE")
assert_grep(
    r"securityscorecards\.dev/projects/github\.com/Ranzlappen/repo-standards",
    "README.md",
    "OpenSSF Scorecard badge cites Ranzlappen/repo-standards",
)

section("[6/8] Modular prompt files")
for p in [
    "migration-planning",
    "00-version-check",
    "01-ground-rules",
    "02-canonical-pr-sequence",
    "03-pr-description",
    "04-wiki-seeding",
    "05-migration-debrief",
]:
    assert_file(f"prompt/{p}.md")
assert_grep(r"repo-standards v\d+\.\d+\.\d+", "PROMPT.md", "PROMPT.md master prompt names a v3.x version")

section("[7/8] Placeholder hygiene (rule 11 mechanical verification)")
# Patterns explicitly enumerated in prompt/01-ground-rules.md rule 11.
PLACEHOLDER_PATTERNS = [r"<PROJECT_NAME>", r"<OWNER>", r"<REPO>", r"<TODO>"]
# Files where these patterns appear in *normative* contexts (rule definitions,
# substitution instructions, release notes that quote the rule by name) and
# are intentional, not leakage.
ALLOWED_NORMATIVE_FILES = {
    "prompt/01-ground-rules.md",  # rule 11 enumerates these patterns by name
    "prompt/04-wiki-seeding.md",  # Step 4 substitution instruction
    "CHANGELOG.md",  # release notes quote the rule-11 patterns by name
}
EXCLUDED_DIRS = {"templates", ".git", "node_modules"}
leaks: list[str] = []
for path in ROOT.rglob("*.md"):
    rel = path.relative_to(ROOT).as_posix()
    if rel.split("/", 1)[0] in EXCLUDED_DIRS:
        continue
    if rel in ALLOWED_NORMATIVE_FILES:
        continue
    text = path.read_text(errors="ignore")
    for pat in PLACEHOLDER_PATTERNS:
        for m in re.finditer(pat, text):
            line_no = text[: m.start()].count("\n") + 1
            leaks.append(f"{rel}:{line_no} {pat}")
if leaks:
    ng(f"Placeholder leakage outside templates/ ({len(leaks)} hit(s)):")
    for leak in leaks[:10]:
        print(f"        {leak}")
else:
    ok("No <PROJECT_NAME>/<OWNER>/<REPO>/<TODO> leakage outside templates/")

section("[8/8] Workflow-sidecar pairing (templates/.github/workflows/)")
tmpl_dir = ROOT / "templates/.github/workflows"
unpaired: list[str] = []
orphans: list[str] = []
template_yml_count = 0
for wf in tmpl_dir.glob("*.yml"):
    template_yml_count += 1
    sidecar = wf.parent / f"{wf.stem}.properties.json"
    if not sidecar.is_file():
        unpaired.append(wf.name)
for sc in tmpl_dir.glob("*.properties.json"):
    base = sc.name[: -len(".properties.json")]
    wf = tmpl_dir / f"{base}.yml"
    if not wf.is_file():
        orphans.append(sc.name)
if unpaired:
    ng(f"Workflow templates missing sidecars: {', '.join(unpaired)}")
elif orphans:
    ng(f"Orphan sidecars (no matching .yml): {', '.join(orphans)}")
else:
    ok(f"All {template_yml_count} workflow templates have valid .properties.json sidecars")

# ───────────────────────────────────────────────────────────────────────────
print()
print("── summary ──")
print(f"  PASS: {passes}")
print(f"  FAIL: {fails}")

sys.exit(1 if fails > 0 else 0)
