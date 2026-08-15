# NVIDIA L4 benchmark protocol

This repository provides a bounded, auditable protocol; it does not include fabricated GPU numbers. Apple Silicon is suitable only for smoke testing and does not establish representative vLLM GPU performance.

## Matrix

- Models: `Qwen/Qwen2.5-7B-Instruct` FP16 and `Qwen/Qwen2.5-7B-Instruct-AWQ`
- Prefix caching: disabled and enabled
- Concurrency: 1, 4, and 8
- Input: 512 and 2,048 tokens
- Output: 128 tokens
- Repetitions: 3
- Total matrix cells: 24; total measured repetitions: 72

Generate the machine-readable plan without requiring a GPU:

```bash
uv run vllm-benchmark --plan > benchmark-plan.json
```

## Controlled L4 run

1. Record the cloud instance type, NVIDIA driver, CUDA, Python, vLLM, model revision, command line, and wall-clock time.
2. Verify `nvidia-smi --query-gpu=name --format=csv,noheader` identifies an NVIDIA L4.
3. Start one model/server configuration at a time. For prefix caching, pass `--enable-prefix-caching`; omit it for the disabled condition.
4. Warm the server with one excluded request.
5. Run each matrix cell three times through `vllm bench serve`, retaining its raw JSON output and `nvidia-smi` peak-memory sampling.
6. Store immutable raw results in `benchmarks/results/` before deriving the JSON, Markdown, and SVG report.
7. Stop the instance immediately after artifact checks. The USD 25 cap and explicit approval requirement remain controlling gates.

Required measurements are time-to-first-token, p50/p95 end-to-end latency, output tokens per second, failure rate, and peak GPU memory. Report the model revisions and any failed repetitions. Do not average away failures.

The cost claim is deliberately bounded: **no per-token provider fee during local inference**. Hardware and electricity remain costs.
