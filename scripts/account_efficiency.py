#!/usr/bin/env python3
"""Account for hard-limit efficiency experiments.

The accounting model charges the submitted artifact plus training, optimizer,
selection, memory, update, and scoring costs. It is intentionally small enough
to run in local smoke tests and explicit enough to expose hidden overhead.
"""

from __future__ import annotations

import argparse
from dataclasses import asdict, dataclass
import json
from pathlib import Path
from typing import Any


def _reject_negative_fields(name: str, fields: dict[str, float | int]) -> None:
    for field_name, value in fields.items():
        if value < 0:
            raise ValueError(f"{name}.{field_name} must not be negative")


@dataclass(frozen=True)
class ExperimentCosts:
    artifact_size_bytes: int
    training_time_seconds: float
    update_steps: int
    optimizer_state_bytes: int
    peak_memory_bytes: int
    scoring_time_seconds: float
    selection_trials: int = 1
    selection_time_seconds: float = 0.0

    def __post_init__(self) -> None:
        _reject_negative_fields(
            "costs",
            {
                "artifact_size_bytes": self.artifact_size_bytes,
                "training_time_seconds": self.training_time_seconds,
                "update_steps": self.update_steps,
                "optimizer_state_bytes": self.optimizer_state_bytes,
                "peak_memory_bytes": self.peak_memory_bytes,
                "scoring_time_seconds": self.scoring_time_seconds,
                "selection_time_seconds": self.selection_time_seconds,
            },
        )
        if self.selection_trials < 1:
            raise ValueError("costs.selection_trials must be at least 1")

    @property
    def total_time_seconds(self) -> float:
        return self.training_time_seconds + self.scoring_time_seconds + self.selection_time_seconds

    @property
    def total_overhead_bytes(self) -> int:
        return self.optimizer_state_bytes + self.peak_memory_bytes


@dataclass(frozen=True)
class BudgetLimits:
    artifact_size_bytes: int
    training_time_seconds: float
    update_steps: int
    peak_memory_bytes: int
    scoring_time_seconds: float

    def __post_init__(self) -> None:
        fields = {
            "artifact_size_bytes": self.artifact_size_bytes,
            "training_time_seconds": self.training_time_seconds,
            "update_steps": self.update_steps,
            "peak_memory_bytes": self.peak_memory_bytes,
            "scoring_time_seconds": self.scoring_time_seconds,
        }
        for field_name, value in fields.items():
            if value <= 0:
                raise ValueError(f"limits.{field_name} must be positive")

    def evaluate(self, costs: ExperimentCosts) -> dict[str, dict[str, float | int | bool]]:
        fields: tuple[tuple[str, float | int, float | int], ...] = (
            ("artifact_size_bytes", costs.artifact_size_bytes, self.artifact_size_bytes),
            ("training_time_seconds", costs.training_time_seconds, self.training_time_seconds),
            ("update_steps", costs.update_steps, self.update_steps),
            ("peak_memory_bytes", costs.peak_memory_bytes, self.peak_memory_bytes),
            ("scoring_time_seconds", costs.scoring_time_seconds, self.scoring_time_seconds),
        )
        return {
            name: {"used": used, "limit": limit, "ok": used <= limit}
            for name, used, limit in fields
        }


def _load_dataclass(path: Path, key: str, cls: type[BudgetLimits] | type[ExperimentCosts]) -> Any:
    payload = json.loads(path.read_text(encoding="utf-8"))
    values = payload.get(key, payload)
    if not isinstance(values, dict):
        raise ValueError(f"{path} must contain a JSON object for {key}")
    return cls(**values)


def build_report(costs: ExperimentCosts, limits: BudgetLimits | None = None) -> dict[str, Any]:
    report: dict[str, Any] = {
        "costs": asdict(costs),
        "derived": {
            "total_time_seconds": costs.total_time_seconds,
            "total_overhead_bytes": costs.total_overhead_bytes,
        },
    }
    if limits is not None:
        status = limits.evaluate(costs)
        report["limits"] = asdict(limits)
        report["budget_status"] = status
        report["within_budget"] = all(field["ok"] for field in status.values())
    return report


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--costs", type=Path, required=True, help="JSON file with experiment costs")
    parser.add_argument("--limits", type=Path, help="Optional JSON file with hard budget limits")
    parser.add_argument(
        "--enforce",
        action="store_true",
        help="Exit with code 2 when any declared hard limit is exceeded",
    )
    args = parser.parse_args()

    costs = _load_dataclass(args.costs, "costs", ExperimentCosts)
    limits = _load_dataclass(args.limits, "limits", BudgetLimits) if args.limits else None
    if args.enforce and limits is None:
        parser.error("--enforce requires --limits")

    report = build_report(costs, limits)
    print(json.dumps(report, indent=2, sort_keys=True))
    if args.enforce and not report["within_budget"]:
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
