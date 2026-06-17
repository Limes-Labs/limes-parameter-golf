# Limes Parameter Golf

Limes Parameter Golf is a small-model efficiency challenge from Limes Labs. The goal is to build language models that compress validation text well while staying inside strict artifact and reproducibility limits.

This repository is inspired by OpenAI's Model Craft Challenge: Parameter Golf, whose public repository describes a 16 MB artifact limit, a 10 minute training budget on 8xH100s, and tokenizer-agnostic FineWeb validation scoring in bits per byte. See the original OpenAI repository for the source context: [openai/parameter-golf](https://github.com/openai/parameter-golf).

Limes Parameter Golf is independent from OpenAI. It is not affiliated with, endorsed by, sponsored by, or a continuation of OpenAI's contest. We use the Parameter Golf idea as attributed inspiration for a European, open, and more locally accessible efficiency track.

## Why This Matters

Efficient language modeling is a practical research frontier for European students, labs, startups, and open-source contributors who may not have frontier-scale compute. Small artifacts, transparent scoring, and local smoke tests make it easier to compare ideas such as compression, quantization, parameter tying, recurrence, tokenizer choices, and test-time compute without requiring huge downloads.

## Quickstart

Requirements:

- Python 3.10 or newer
- Bash for the smoke script
- No external Python packages

Run the smoke test:

```bash
scripts/run_smoke.sh
```

Run the unit tests only:

```bash
python3 -m unittest discover -s tests
```

Run the included baseline manually:

```bash
python3 baselines/char_unigram_baseline.py \
  --train data/smoke_train.txt \
  --valid data/smoke_valid.txt \
  --artifact /tmp/limes-byte-unigram.json \
  --output /tmp/limes-byte-unigram-output.json

python3 scripts/score_bpb.py --baseline-output /tmp/limes-byte-unigram-output.json
python3 scripts/check_artifact_size.py /tmp/limes-byte-unigram.json --limit-mib 16
```

## Repository Map

- `RULES.md`: challenge tracks, limits, and conduct expectations
- `EVAL.md`: BPB scoring and validation policy
- `SUBMISSIONS.md`: artifact and reproducibility format
- `baselines/`: simple local baselines
- `scripts/`: scoring, artifact checks, and smoke test
- `tests/`: unit tests for scoring and size enforcement
- `docs/design-notes.md`: design lessons from Parameter Golf-style challenges

## Status

This is an initial scaffold. The public leaderboard, canonical validation split hashes, and submission review process still need to be finalized before accepting official entries.
