import argparse
import itertools
import json
import shutil
import subprocess
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

MODELS = {
    "fp16": "Qwen/Qwen2.5-7B-Instruct",
    "awq": "Qwen/Qwen2.5-7B-Instruct-AWQ",
}


def matrix() -> list[dict[str, Any]]:
    return [
        {
            "model_variant": variant,
            "model_identifier": model,
            "prefix_caching": cache,
            "concurrency": concurrency,
            "input_tokens": prompt,
            "output_tokens": 128,
            "repetitions": 3,
        }
        for (variant, model), cache, concurrency, prompt in itertools.product(
            MODELS.items(), [False, True], [1, 4, 8], [512, 2048]
        )
    ]


def require_nvidia_l4() -> str:
    executable = shutil.which("nvidia-smi")
    if not executable:
        raise RuntimeError("nvidia-smi is unavailable; benchmark results cannot be produced here")
    result = subprocess.run(
        [executable, "--query-gpu=name", "--format=csv,noheader"],
        check=True,
        capture_output=True,
        text=True,
    )
    gpu = result.stdout.strip()
    if "L4" not in gpu:
        raise RuntimeError(f"expected an NVIDIA L4, observed {gpu!r}")
    return gpu


def main() -> None:
    parser = argparse.ArgumentParser(description="Emit or execute the bounded L4 benchmark matrix")
    parser.add_argument(
        "--plan", action="store_true", help="print the matrix without claiming results"
    )
    parser.add_argument("--output", type=Path, default=Path("benchmarks/results/raw.json"))
    args = parser.parse_args()
    plan = {
        "created_at": datetime.now(UTC).isoformat(),
        "required_gpu": "NVIDIA L4",
        "runs": matrix(),
        "metrics": [
            "time_to_first_token_ms",
            "latency_p50_ms",
            "latency_p95_ms",
            "output_tokens_per_second",
            "failure_rate",
            "peak_gpu_memory_mib",
        ],
        "cost_language": (
            "No per-token provider fee during local inference; "
            "hardware and electricity remain costs."
        ),
    }
    if args.plan:
        print(json.dumps(plan, indent=2))
        return
    gpu = require_nvidia_l4()
    raise RuntimeError(
        f"L4 detected ({gpu}), but execution remains explicit: "
        "follow benchmarks/README.md and capture raw vLLM output"
    )


if __name__ == "__main__":
    main()
