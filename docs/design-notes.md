# Design Notes

OpenAI's public Parameter Golf repository framed a compact language-model challenge around a 16 MB artifact, a time-bounded 8xH100 training setup, and tokenizer-agnostic bits-per-byte evaluation on FineWeb validation data. Limes Parameter Golf borrows the broad research shape with attribution, but defines an independent challenge aimed at accessible European participation.

Source: [openai/parameter-golf](https://github.com/openai/parameter-golf)

## Lessons Worth Carrying Forward

### Compression Is a First-Class Modeling Tool

The artifact limit makes compression part of the model design rather than a final packaging step. Useful directions include low-bit weights, entropy coding, sparse tables, shared embeddings, and compact tokenizer metadata.

### Quantization Should Be Trained, Not Just Applied

Post-training quantization is useful, but quantization-aware training, calibration, and mixed precision can change the reachable frontier under small artifacts.

### Parameter Tying Can Buy Capability

Reused layers, recurrent blocks, shared projections, and low-rank factors can trade test-time compute for a smaller stored model. The rules should decide which compute tradeoffs belong in each track.

### Tokenizer Choices Matter

Tokenizer-agnostic BPB avoids rewarding a tokenizer merely for producing fewer tokens. Entrants still need to count every byte of tokenizer state and any side information required to reconstruct the original stream.

### Test-Time Compute Needs Clear Boundaries

Some methods adapt during evaluation. Official rules should specify when adaptation is legal, whether the model may update state after seeing validation prefixes, and how score-first or document-specific tuning is handled.

### Small Data Pipelines Need Hashes

Even tiny corpora should have source URLs, preprocessing code, byte counts, and hashes. That discipline keeps local tracks reproducible without bundling large datasets.

### Agent-Assisted Research Is Plausible

The search space is full of small engineering ideas: compression formats, fused kernels, tokenizer variants, recurrence schedules, and calibration recipes. Agent-assisted experimentation can help document these ideas, but leaderboard submissions still need deterministic commands and human-readable explanations.

## Limes-Specific Direction

The Limes version should emphasize:

- public tooling over prize-scale infrastructure
- local/MPS/single-GPU participation
- European language and domain extensions after the first English-only scaffold
- transparent non-affiliation with OpenAI
- modest smoke tests that run before anyone downloads a large dataset
