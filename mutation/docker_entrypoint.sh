#!/usr/bin/env bash
set -euo pipefail

# Optional seed for deterministic tests
export PYTHONHASHSEED=1337

echo "[mutation] Setting PYTHONPATH for baseline and mutation phases..."
export PYTHONPATH="/workspace:${PYTHONPATH:-}"

echo "[mutation] Running baseline test suite..."
if ! pytest -q; then
  echo "[mutation] Baseline tests failed. Aborting mutation run." >&2
  exit 1
fi

echo "[mutation] Baseline tests passed. Starting mutation testing with mutmut..."
# Ensure schemas (and potentially other resource dirs) are visible from mutants working directory
# Use config from setup.cfg (paths_to_mutate)
echo "[mutation] Using mutation targets from setup.cfg (paths_to_mutate + do_not_mutate exclusions)."

# Clean previous mutants directory to avoid stale symlinks/resources causing copy conflicts
if [ -d mutants ]; then
  echo "[mutation] Cleaning existing mutants directory to avoid stale symlinks..."
  rm -rf mutants || { echo "[mutation] Failed to clean mutants directory" >&2; exit 1; }
fi

# Run mutmut (full run). Capture exit code for infra failure detection.
set +e
mutmut run
MUTMUT_EXIT=$?
set -e

if [ $MUTMUT_EXIT -ne 0 ]; then
  # We'll still attempt to show partial results but treat as infrastructure failure unless only survivors.
  echo "[mutation] mutmut exited with code $MUTMUT_EXIT (potential infrastructure failure)." >&2
fi

echo "[mutation] Mutation testing finished. Results summary:" 
mutmut results || true

# Produce machine-readable summary file
mutmut results > mutation/mutmut_results.txt || true

# Exit non-zero if surviving mutants exist (enforce quality gate)
SURVIVED=$(mutmut results | grep -c ": survived" || echo 0)
if [ "${SURVIVED}" -gt 0 ]; then
  echo "[mutation] There are ${SURVIVED} surviving mutants. Please improve tests." >&2
  exit 2
fi

if [ $MUTMUT_EXIT -ne 0 ]; then
  echo "[mutation] Infrastructure issue detected during mutation run (no surviving mutants reported)." >&2
  exit 3
fi

echo "[mutation] All mutants killed. Success."