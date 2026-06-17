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

python3 -m unittest discover -s "$ROOT_DIR/tests"
