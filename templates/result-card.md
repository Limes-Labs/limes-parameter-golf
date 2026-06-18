# Result Card: <experiment-name>

## Summary

- status: candidate | diagnostic | mixed | negative | verified
- track: classic-16mib | local-student | research-efficiency | open-exploration
- commit: `<git-sha>`
- artifact hash: `<sha256>`
- validation split: `<name, version, byte count, hash>`

## Method

Describe the model, tokenizer or byte representation, optimizer, compression,
test-time compute, and any training-only teachers or selectors.

## Budget

| Field | Used | Limit | Notes |
| --- | ---: | ---: | --- |
| artifact size bytes |  |  | counted with `scripts/check_artifact_size.py` |
| training time seconds |  |  | wall clock |
| update steps |  |  | optimizer or equivalent update events |
| optimizer state bytes |  | n/a | charged as overhead |
| peak memory bytes |  |  | measured during training or scoring |
| scoring time seconds |  |  | validation wall clock |
| selection trials |  | n/a | sweeps, reruns, hand-tuned variants |
| selection time seconds |  | n/a | overhead before choosing artifact |

Attach the JSON output from `scripts/account_efficiency.py`.

## Results

| Metric | Value |
| --- | ---: |
| BPB |  |
| baseline BPB |  |
| delta BPB |  |

## Failure Modes

List known weaknesses, negative results, overfitting risks, and cases where the
method loses to a simpler baseline.

## Reproducibility

```bash
# training

# scoring

# accounting
python3 scripts/account_efficiency.py --costs <costs.json> --limits <limits.json> --enforce
```
