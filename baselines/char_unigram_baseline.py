#!/usr/bin/env python3
"""A tiny byte-unigram baseline for local smoke tests."""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path


def train_byte_counts(data: bytes) -> list[int]:
    counts = [0] * 256
    for byte in data:
        counts[byte] += 1
    return counts


def byte_unigram_log_prob(byte: int, counts: list[int], alpha: float = 0.5) -> float:
    total = sum(counts)
    probability = (counts[byte] + alpha) / (total + alpha * 256)
    return math.log(probability)


def evaluate_bytes(data: bytes, counts: list[int], alpha: float = 0.5) -> dict[str, float | int]:
    if not data:
        raise ValueError("validation data must not be empty")
    total_log_prob = sum(byte_unigram_log_prob(byte, counts, alpha) for byte in data)
    bpb = -total_log_prob / (math.log(2.0) * len(data))
    return {
        "byte_count": len(data),
        "total_log_prob_nats": total_log_prob,
        "bpb": bpb,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--train", type=Path, required=True)
    parser.add_argument("--valid", type=Path, required=True)
    parser.add_argument("--artifact", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--alpha", type=float, default=0.5)
    args = parser.parse_args()

    train_data = args.train.read_bytes()
    valid_data = args.valid.read_bytes()
    counts = train_byte_counts(train_data)
    metrics = evaluate_bytes(valid_data, counts, alpha=args.alpha)

    args.artifact.parent.mkdir(parents=True, exist_ok=True)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.artifact.write_text(
        json.dumps({"model": "byte_unigram", "alpha": args.alpha, "counts": counts}, indent=2),
        encoding="utf-8",
    )
    args.output.write_text(json.dumps(metrics, indent=2, sort_keys=True), encoding="utf-8")
    print(json.dumps(metrics, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
