#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
WORK_DIR="$(mktemp -d)"
trap 'rm -rf "$WORK_DIR"' EXIT

python3 "$ROOT_DIR/baselines/char_unigram_baseline.py" \
  --train "$ROOT_DIR/data/smoke_train.txt" \
  --valid "$ROOT_DIR/data/smoke_valid.txt" \
  --artifact "$WORK_DIR/byte_unigram.json" \
  --output "$WORK_DIR/baseline_output.json"

python3 "$ROOT_DIR/scripts/score_bpb.py" \
  --baseline-output "$WORK_DIR/baseline_output.json"

python3 "$ROOT_DIR/scripts/check_artifact_size.py" \
  "$WORK_DIR/byte_unigram.json" \
  --limit-mib 16

python3 "$ROOT_DIR/baselines/byte_bigram_baseline.py" \
  --train "$ROOT_DIR/data/smoke_train.txt" \
  --valid "$ROOT_DIR/data/smoke_valid.txt" \
  --artifact "$WORK_DIR/byte_bigram.json" \
  --output "$WORK_DIR/byte_bigram_output.json"

cat > "$WORK_DIR/costs.json" <<'JSON'
{
  "costs": {
    "artifact_size_bytes": 4096,
    "training_time_seconds": 3.0,
    "update_steps": 20,
    "optimizer_state_bytes": 8192,
    "peak_memory_bytes": 65536,
    "scoring_time_seconds": 1.0,
    "selection_trials": 1,
    "selection_time_seconds": 0.0
  }
}
JSON

cat > "$WORK_DIR/limits.json" <<'JSON'
{
  "limits": {
    "artifact_size_bytes": 16777216,
    "training_time_seconds": 600.0,
    "update_steps": 1000,
    "peak_memory_bytes": 1073741824,
    "scoring_time_seconds": 60.0
  }
}
JSON

python3 "$ROOT_DIR/scripts/account_efficiency.py" \
  --costs "$WORK_DIR/costs.json" \
  --limits "$WORK_DIR/limits.json"

python3 -m unittest discover -s "$ROOT_DIR/tests"
