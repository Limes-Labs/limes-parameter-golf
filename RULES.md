# Rules

These rules are a starting point for a reproducible small-model efficiency challenge. They are designed to support ambitious research submissions and accessible local participation.

## Non-Affiliation

Limes Parameter Golf is an independent Limes Labs project. It is inspired by OpenAI's Parameter Golf challenge but is not affiliated with, endorsed by, sponsored by, or administered by OpenAI.

## Tracks

### Classic 16 MiB Artifact Track

- Artifact limit: 16 MiB, measured as the total submitted model artifact bytes.
- Scoring: lowest bits per byte on the canonical validation split wins.
- Training budget: to be finalized before official leaderboard launch.
- Runtime budget: submissions must include enough detail for evaluators to reproduce training and validation on the declared hardware.
- Allowed methods: architecture changes, compression, quantization, parameter sharing, tokenizer choices, and deterministic test-time compute that follows the evaluation rules.

This track is intentionally reminiscent of the OpenAI Parameter Golf constraint, with attribution, while Limes Labs defines its own datasets, budgets, and governance.

### Local Student Track

- Artifact limit: 16 MiB.
- Hardware target: a laptop CPU, Apple Silicon MPS device, or a single consumer GPU.
- Training target: should run from scratch in a reasonable local session, with the exact wall-clock budget to be finalized.
- Dataset footprint: small public training samples or user-provided local corpora only; no bundled large datasets.
- Purpose: make the challenge approachable for European students, independent researchers, and open-source contributors.

### Open Exploration Track

- Artifact limit: declared by the submitter.
- Hardware: declared by the submitter.
- Leaderboard status: non-record unless it also satisfies a record track.
- Purpose: document interesting ideas without forcing every experiment into the strict official limits.

## Artifact Definition

The artifact includes everything needed at inference time: weights, tokenizer files, lookup tables, generated code, compressed archives, metadata used by the model, and any calibration data. Evaluation harness code supplied by this repository is not counted.

Artifacts must not download weights, validation labels, hidden data, or external services during scoring.

## Reproducibility

Submissions must include:

- exact commit hash or source archive
- artifact hash
- training command
- evaluation command
- hardware used
- random seeds
- dependency versions
- a short method summary

## Prohibited Behavior

- Fitting to the validation split or public leaderboard outcomes.
- Bundling or fetching hidden validation data.
- Using non-deterministic external APIs during scoring.
- Omitting files needed to reproduce the artifact.
- Misrepresenting affiliation with OpenAI or Limes Labs.

## Governance Notes

The maintainers may rerun submissions, request simpler reproduction steps, move entries between tracks, or reject entries that are not reproducible. Final official rules should be versioned before the first public leaderboard.
