import argparse
import os
import subprocess
from pathlib import Path

from .engine import evaluate
from .report import write_reports


def git_commit() -> str:
    override = os.getenv("EVAL_CODE_COMMIT")
    if override:
        return override
    result = subprocess.run(
        ["git", "rev-parse", "--verify", "HEAD"],
        check=False,
        capture_output=True,
        text=True,
    )
    return result.stdout.strip() if result.returncode == 0 else "uncommitted-worktree"


def main() -> None:
    parser = argparse.ArgumentParser(description="Run the 50-case deterministic evaluation suite")
    parser.add_argument("--dataset", type=Path, default=Path("datasets/golden-v1.json"))
    parser.add_argument("--output", type=Path, default=Path("reports/current"))
    parser.add_argument("--model", default="deterministic-offline-v1")
    parser.add_argument("--environment", default="local-deterministic")
    args = parser.parse_args()
    report = evaluate(
        args.dataset,
        code_commit=git_commit(),
        model_identifier=args.model,
        environment=args.environment,
    )
    write_reports(report, args.output)
    print(f"{report.metrics['passed']}/{report.metrics['total']} cases passed")
    for name, passed in report.gates.items():
        print(f"{'PASS' if passed else 'FAIL'} {name}")
    if not all(report.gates.values()):
        raise SystemExit(1)


if __name__ == "__main__":
    main()
