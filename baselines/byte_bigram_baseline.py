#!/usr/bin/env python3
"""A byte-bigram baseline with unigram backoff for local research runs."""

from __future__ import annotations

import argparse
from dataclasses import dataclass
import json
import math
from pathlib import Path


@dataclass(frozen=True)
class ByteBigramModel:
    unigram_counts: list[int]
    bigram_counts: list[list[int]]
    alpha: float = 0.01


def train_bigram_counts(data: bytes, alpha: float = 0.01) -> ByteBigramModel:
    unigram_counts = [0] * 256
    bigram_counts = [[0] * 256 for _ in range(256)]
    previous: int | None = None
    for byte in data:
        unigram_counts[byte] += 1
        if previous is not None:
            bigram_counts[previous][byte] += 1
        previous = byte
    return ByteBigramModel(unigram_counts=unigram_counts, bigram_counts=bigram_counts, alpha=alpha)


def _unigram_log_prob(byte: int, model: ByteBigramModel) -> float:
    total = sum(model.unigram_counts)
    probability = (model.unigram_counts[byte] + model.alpha) / (total + model.alpha * 256)
    return math.log(probability)


def byte_bigram_log_prob(byte: int, previous: int | None, model: ByteBigramModel) -> float:
    if previous is None:
        return _unigram_log_prob(byte, model)

    context_counts = model.bigram_counts[previous]
    context_total = sum(context_counts)
    if context_total == 0:
        return _unigram_log_prob(byte, model)

    probability = (context_counts[byte] + model.alpha) / (context_total + model.alpha * 256)
    return math.log(probability)


def evaluate_bytes(data: bytes, model: ByteBigramModel) -> dict[str, float | int]:
    if not data:
        raise ValueError("validation data must not be empty")

    total_log_prob = 0.0
    previous: int | None = None
    for byte in data:
        total_log_prob += byte_bigram_log_prob(byte, previous, model)
        previous = byte
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
    parser.add_argument("--alpha", type=float, default=0.01)
    args = parser.parse_args()

    model = train_bigram_counts(args.train.read_bytes(), alpha=args.alpha)
    metrics = evaluate_bytes(args.valid.read_bytes(), model)

    args.artifact.parent.mkdir(parents=True, exist_ok=True)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.artifact.write_text(
        json.dumps(
            {
                "model": "byte_bigram_backoff",
                "alpha": model.alpha,
                "unigram_counts": model.unigram_counts,
                "bigram_counts": model.bigram_counts,
            },
            indent=2,
        ),
        encoding="utf-8",
    )
    args.output.write_text(json.dumps(metrics, indent=2, sort_keys=True), encoding="utf-8")
    print(json.dumps(metrics, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
