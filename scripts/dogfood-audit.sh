#!/usr/bin/env bash
# dogfood-audit.sh — assert this repo passes its own UPGRADE_CHECKLIST.
#
# Run from repo root. Prints PASS / FAIL per assertion; exits 1 on any
# FAIL with a summary count. Called from .github/workflows/dogfood-audit.yml
# on every PR + push to main + weekly schedule, and runnable locally for
# fast feedback during development.
#
# Scope: mechanically-verifiable invariants only (file existence, version
# alignment, badge URL format, prompt-file presence). Comprehensive
# UPGRADE_CHECKLIST.md line-item parsing is deferred to a future release.

set -u

PASS=0
FAIL=0

ok() { echo "  PASS  $1"; PASS=$((PASS+1)); }
ng() { echo "  FAIL  $1"; FAIL=$((FAIL+1)); }

assert_file() {
  local path="$1"; local label="${2:-$1}"
  if [ -f "$path" ]; then ok "$label exists"; else ng "$label MISSING ($path)"; fi
}

assert_grep() {
  local pattern="$1"; local path="$2"; local label="$3"
  if grep -qE "$pattern" "$path" 2>/dev/null; then ok "$label"; else ng "$label (pattern not found in $path)"; fi
}

echo "── dogfood-audit ──"
echo "Repo: $(pwd)"
echo

echo "[1/6] Root LICENSE"
assert_file "LICENSE"
if [ -f LICENSE ]; then
  if [ "$(head -n 1 LICENSE)" = "MIT License" ]; then ok "LICENSE first line is 'MIT License'"; else ng "LICENSE first line is not 'MIT License'"; fi
  if grep -qE '<[A-Z_]+>' LICENSE; then ng "LICENSE has unfilled <PLACEHOLDER>s"; else ok "LICENSE has no unfilled placeholders"; fi
fi
echo

echo "[2/6] Versioning files"
assert_file "VERSION"
assert_file ".standards-version"
if [ -f VERSION ] && [ -f .standards-version ]; then
  V_MAJOR="$(cut -d. -f1 < VERSION | tr -d '[:space:]')"
  S_MAJOR="$(cut -d. -f1 < .standards-version | tr -d '[:space:]')"
  if [ "$V_MAJOR" = "$S_MAJOR" ]; then ok "VERSION ($V_MAJOR.x) and .standards-version ($S_MAJOR.x) majors aligned"; else ng "VERSION major ($V_MAJOR) != .standards-version major ($S_MAJOR)"; fi
  if echo "$(cat VERSION)" | grep -qE '^[0-9]+\.[0-9]+\.[0-9]+(-[A-Za-z0-9.-]+)?(\+[A-Za-z0-9.-]+)?$'; then ok "VERSION is semver"; else ng "VERSION is not semver"; fi
fi
echo

echo "[3/6] Root community files"
for f in SPONSORS.md \
         .github/CODE_OF_CONDUCT.md \
         .github/CONTRIBUTING.md \
         .github/SECURITY.md \
         .github/FUNDING.yml \
         .github/CODEOWNERS \
         .github/dependabot.yml; do
  assert_file "$f"
done
echo

echo "[4/6] Live workflows at .github/workflows/"
for wf in auto-tag self-validate tag-release security-scan dependency-review workflow-summary dogfood-audit; do
  assert_file ".github/workflows/${wf}.yml" ".github/workflows/${wf}.yml"
done
echo

echo "[5/6] README badges"
if [ -f README.md ]; then
  assert_grep 'shields\.io/badge/standards-v[0-9]+\.[0-9]+\.[0-9]+' README.md "Standards badge cites a semver"
  assert_grep 'shields\.io/badge/License-MIT.*\]\(\./LICENSE\)' README.md "License badge points at ./LICENSE"
  assert_grep 'securityscorecards\.dev/projects/github\.com/Ranzlappen/repo-standards' README.md "OpenSSF Scorecard badge cites Ranzlappen/repo-standards"
fi
echo

echo "[6/6] Modular prompt files"
for p in migration-planning 00-version-check 01-ground-rules 02-canonical-pr-sequence 03-pr-description 04-wiki-seeding; do
  assert_file "prompt/${p}.md"
done
if [ -f PROMPT.md ]; then
  assert_grep 'repo-standards v[0-9]+\.[0-9]+\.[0-9]+' PROMPT.md "PROMPT.md master prompt names a v3.x version"
fi
echo

echo "── summary ──"
echo "  PASS: $PASS"
echo "  FAIL: $FAIL"

if [ "$FAIL" -gt 0 ]; then
  exit 1
fi
exit 0
