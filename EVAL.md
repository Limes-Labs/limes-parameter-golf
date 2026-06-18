# Evaluation

The primary score is bits per byte (BPB). Lower is better.

## BPB Definition

For validation bytes `x_1 ... x_n`, the model assigns a probability to each next byte. BPB is:

```text
BPB = -sum(log2 p(x_i)) / n
```

The helper script accepts natural-log probabilities and converts them to bits:

```bash
python3 scripts/score_bpb.py --log-probs predictions.jsonl --byte-count 12345
```

It also accepts baseline outputs written by the included byte-unigram baseline:

```bash
python3 scripts/score_bpb.py --baseline-output result.json
```

The byte-bigram baseline writes the same output shape, so it can be scored with
the same command.

## Tokenizer-Agnostic Policy

Models may use any tokenizer or byte-level representation, but scoring is normalized by the number of original validation bytes. If a tokenizer transforms text, the submission must prove the transform is lossless for the evaluated byte stream or account for any side information inside the artifact.

## Validation Split

The initial repository includes only smoke data. Official validation splits should be:

- public enough for reproducibility, or hidden enough for a final held-out leaderboard
- immutable after publication
- identified by source, version, byte count, and cryptographic hashes
- separated from tuning data

No large dataset is bundled in this repository.

## Anti-Overfitting Notes

Parameter-limited contests can overfit through repeated leaderboard probing, validation-specific transforms, or hand-tuned post-processing. Before an official leaderboard, Limes Labs should define:

- a public development split
- a private final split
- submission frequency limits
- rerun policy across multiple seeds
- rules for test-time training and score-first adaptation

## Script Interfaces

`scripts/score_bpb.py` supports three inputs:

- `--log-probs`: JSON/JSONL numbers or objects containing `log_prob`
- `--probabilities`: JSON/JSONL numbers or objects containing `probability`
- `--baseline-output`: JSON with `total_log_prob_nats` and `byte_count`

`scripts/check_artifact_size.py` sums either a single file or every file inside a directory:

```bash
python3 scripts/check_artifact_size.py artifact.json --limit-mib 16
```

`scripts/account_efficiency.py` reports costs and hard-limit status for research-track experiments:

```bash
python3 scripts/account_efficiency.py \
  --costs templates/accounting-costs.example.json \
  --limits templates/accounting-limits.example.json
```
