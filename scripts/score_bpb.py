#!/usr/bin/env python3
"""Compute bits per byte from model probabilities or baseline outputs."""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path
from typing import Iterable


def bits_per_byte_from_log_probs(log_probs: Iterable[float], byte_count: int) -> float:
    """Return BPB from natural-log probabilities and the evaluated byte count."""
    if byte_count <= 0:
        raise ValueError("byte_count must be positive")

    total_log_prob = sum(log_probs)
    return -total_log_prob / (math.log(2.0) * byte_count)


def _read_json_or_jsonl(path: Path) -> list[object]:
    text = path.read_text(encoding="utf-8").strip()
    if not text:
        return []
    if text[0] in "[{":
        parsed = json.loads(text)
        if isinstance(parsed, list):
            return parsed
        return [parsed]
    return [json.loads(line) for line in text.splitlines() if line.strip()]


def read_log_probs(path: Path) -> list[float]:
    """Read natural-log probabilities from JSON, JSONL, or a plain number list."""
    records = _read_json_or_jsonl(path)
    values: list[float] = []
    for record in records:
        if isinstance(record, (int, float)):
            values.append(float(record))
        elif isinstance(record, dict) and "log_prob" in record:
            values.append(float(record["log_prob"]))
        else:
            raise ValueError(f"Unsupported log-probability record in {path}: {record!r}")
    return values


def read_probabilities(path: Path) -> list[float]:
    """Read probabilities and convert them to natural-log probabilities."""
    records = _read_json_or_jsonl(path)
    values: list[float] = []
    for record in records:
        if isinstance(record, (int, float)):
            probability = float(record)
        elif isinstance(record, dict) and "probability" in record:
            probability = float(record["probability"])
        else:
            raise ValueError(f"Unsupported probability record in {path}: {record!r}")
        if probability <= 0.0:
            raise ValueError("probabilities must be positive")
        values.append(math.log(probability))
    return values


def score_baseline_output(path: Path) -> float:
    """Read a baseline JSON output with total_log_prob_nats and byte_count fields."""
    payload = json.loads(path.read_text(encoding="utf-8"))
    return bits_per_byte_from_log_probs(
        [float(payload["total_log_prob_nats"])],
        int(payload["byte_count"]),
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--log-probs", type=Path, help="JSON/JSONL natural log probabilities")
    group.add_argument("--probabilities", type=Path, help="JSON/JSONL probabilities")
    group.add_argument("--baseline-output", type=Path, help="JSON output from a baseline")
    parser.add_argument("--byte-count", type=int, help="Required with --log-probs or --probabilities")
    args = parser.parse_args()

    if args.baseline_output:
        bpb = score_baseline_output(args.baseline_output)
        byte_count = json.loads(args.baseline_output.read_text(encoding="utf-8"))["byte_count"]
    else:
        if args.byte_count is None:
            parser.error("--byte-count is required with probability inputs")
        if args.log_probs:
            log_probs = read_log_probs(args.log_probs)
        else:
            log_probs = read_probabilities(args.probabilities)
        bpb = bits_per_byte_from_log_probs(log_probs, args.byte_count)
        byte_count = args.byte_count

    print(json.dumps({"bpb": bpb, "byte_count": int(byte_count)}, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
