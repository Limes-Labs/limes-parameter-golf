# Efficiency Research Track

The research track turns Limes Parameter Golf into a public place for testing
small-model efficiency hypotheses under hard constraints. It is not only a
leaderboard. It is a record of what was tried, what it cost, what failed, and
what should be promoted to larger experiments.

## Research Question Format

Every research-track experiment should start with a short preregistration:

- hypothesis: the concrete efficiency claim being tested
- mechanism: why the method should improve BPB, cost, or robustness
- baseline: the exact baseline and commit used for comparison
- hard limits: artifact size, training time, update steps, peak memory, and
  scoring time
- selection rule: how many variants may be tried before reporting a result
- promotion gate: the condition required before the idea moves to a larger run
- failure modes: expected ways the method might lose or overfit

## Hard Limits

Record-like claims must report these limits and costs:

- artifact size: all inference-time files counted by `scripts/check_artifact_size.py`
- training time: wall-clock time to produce the artifact from declared inputs
- update budget: optimizer steps or equivalent parameter-update events
- optimizer state: bytes used for optimizer slots, schedules, teachers, or
  training-only learned state
- peak memory: maximum observed memory during training or scoring
- scoring cost: validation/evaluation wall-clock time
- selection overhead: trials, sweeps, reruns, and hand-tuned variants that were
  used to choose the submitted artifact

Use `scripts/account_efficiency.py` to produce a machine-readable budget report:

```bash
python3 scripts/account_efficiency.py \
  --costs templates/accounting-costs.example.json \
  --limits templates/accounting-limits.example.json \
  --enforce
```

`--enforce` exits with code 2 if any declared hard limit is exceeded. Use it in
CI or smoke scripts when an over-budget result should fail the run.

## No-Cheating Protocol

Research-track entries must not tune against hidden validation data, leaderboard
probes, or private evaluator feedback. Public development splits may be used for
iteration, but final claims should name the split, hash the data, and state the
number of attempted variants. Test-time adaptation is allowed only when the
track explicitly permits it and all state needed for adaptation is charged.

## Promotion Gates

An idea should move from diagnostic to public claim only when it:

- beats the named baseline under the same hard limits
- reports BPB and all accounting fields
- includes at least one failure mode or negative result
- can be rerun from a clean clone with pinned commands
- survives a simpler baseline comparison, such as byte unigram or byte bigram

Suggested statuses:

- `candidate`: plausible idea, not yet tested cleanly
- `diagnostic`: useful for understanding, not a performance claim
- `mixed`: improves one metric while worsening another
- `negative`: clear loss under the declared limits
- `verified`: reproducible improvement that passes the promotion gate

## Baseline Policy

The repository includes byte-unigram and byte-bigram baselines for smoke-scale
comparisons. Stronger baselines are encouraged, but every submitted claim should
preserve a cheap baseline path so reviewers can distinguish real efficiency
signal from harness breakage.
