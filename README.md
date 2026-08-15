# LLM Eval & Inference Lab

A reproducible evaluation and performance lab for reliable AI systems. It versions exactly 50 synthetic/public contract cases, fails CI on critical regressions, and keeps deterministic quality gates separate from hardware benchmarking.

## Current evidence

The checked-in suite contains:

- 15 retrieval relevance cases;
- 15 citation correctness and abstention cases;
- 10 structured-output and bounded-retry cases;
- 10 policy, PII, prompt-injection, and approval cases.

Run it locally:

```bash
uv sync --extra dev
uv run ruff check .
uv run mypy src
uv run pytest
uv run eval-lab --output reports/current
```

Reports contain the dataset version, code commit state, model identifier, environment, timestamp, per-case results, gate outcomes, and JSON/Markdown/SVG outputs.

## Performance protocol

The benchmark plan compares `Qwen/Qwen2.5-7B-Instruct` FP16 with its AWQ variant, prefix caching on/off, concurrency 1/4/8, 512/2,048 input tokens, 128 output tokens, and three repetitions. See [the protocol](benchmarks/README.md).

Four GPU-gated Compose profiles pin vLLM v0.27.1 and immutable model revisions. `vllm/models.json` records the 2026-08-15 source check and Apache-2.0 licenses; `benchmarks/raw-result.schema.json` prevents derived reports from omitting failed repetitions or environment identity.

No L4 result is included until an explicitly approved session runs. This project says **no per-token provider fee during local inference**, not zero cost.

## Known limitations

- The deterministic provider verifies contracts and regressions, not general model intelligence.
- The lexical retrieval reference is intentionally small and does not replace the Qdrant workbench evaluation.
- Apple Silicon smoke tests do not establish representative vLLM GPU performance.
- No release, remote repository, demo video, or cloud benchmark has been created from this local worktree.
