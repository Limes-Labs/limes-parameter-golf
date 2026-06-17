#!/usr/bin/env python3
"""Check that a submission artifact fits within a track size limit."""

from __future__ import annotations

import argparse
from pathlib import Path


def artifact_size_bytes(path: Path) -> int:
    """Return the total byte size of a file or all files inside a directory."""
    if not path.exists():
        raise FileNotFoundError(path)
    if path.is_file():
        return path.stat().st_size
    if not path.is_dir():
        raise ValueError(f"Unsupported artifact path: {path}")

    total = 0
    for child in path.rglob("*"):
        if child.is_file():
            total += child.stat().st_size
    return total


def check_artifact_size(path: Path, limit_mib: float) -> bool:
    """Return True when the artifact is no larger than limit_mib."""
    limit_bytes = int(limit_mib * 1024 * 1024)
    return artifact_size_bytes(path) <= limit_bytes


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("artifact", type=Path)
    parser.add_argument("--limit-mib", type=float, default=16.0)
    args = parser.parse_args()

    size = artifact_size_bytes(args.artifact)
    limit = int(args.limit_mib * 1024 * 1024)
    status = "ok" if size <= limit else "too_large"
    print(f"{status}: {size} bytes / {limit} bytes")
    return 0 if size <= limit else 1


if __name__ == "__main__":
    raise SystemExit(main())
