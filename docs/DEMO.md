# Two-to-three-minute demo script

1. Run `uv run eval-lab --output reports/current` and show the exact 15/15/10/10 category split.
2. Open the JSON and Markdown evidence; point out dataset version, commit state, model identifier, environment, timestamp, per-case result, and gate status.
3. Introduce one intentional critical regression and show the process fail, then revert that local demonstration edit.
4. Run `uv run vllm-benchmark --plan` and show the 24 matrix cells and 72 measured repetitions.
5. Show the four GPU-only Compose profiles and the pinned model revisions.
6. Run the hardware preflight on the Mac and show that it refuses to produce an L4 result.
7. Close with the bounded claim: no per-token provider fee during local inference; hardware and electricity still cost money.

The recorded video and L4 measurements remain publication/spend gates.
