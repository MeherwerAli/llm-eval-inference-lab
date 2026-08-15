import json
from pathlib import Path

import pytest

from eval_lab.benchmark import matrix, require_nvidia_l4
from eval_lab.engine import evaluate, load_cases
from eval_lab.report import write_reports

DATASET = Path("datasets/golden-v1.json")


def test_dataset_has_exact_versioned_category_contract() -> None:
    version, cases = load_cases(DATASET)
    assert version == "golden-v1.0.0"
    assert len(cases) == 50
    assert len({case.id for case in cases}) == 50
    assert sum(case.category == "retrieval" for case in cases) == 15
    assert sum(case.category == "citation" for case in cases) == 15
    assert sum(case.category == "structured" for case in cases) == 10
    assert sum(case.category == "policy" for case in cases) == 10


def test_deterministic_suite_meets_all_acceptance_gates(tmp_path: Path) -> None:
    report = evaluate(
        DATASET,
        code_commit="test-commit",
        model_identifier="deterministic-offline-v1",
        environment="pytest",
    )
    assert report.metrics["passed"] == 50
    assert all(report.gates.values())
    assert report.metrics["unauthorized_actions"] == 0
    write_reports(report, tmp_path)
    assert json.loads((tmp_path / "evaluation.json").read_text())["metrics"]["total"] == 50
    assert "PASS `zero_critical_regressions`" in (tmp_path / "evaluation.md").read_text()
    assert "Evaluation category pass rates" in (tmp_path / "evaluation.svg").read_text()


def test_benchmark_matrix_is_bounded_and_complete() -> None:
    runs = matrix()
    assert len(runs) == 24
    assert {run["model_variant"] for run in runs} == {"fp16", "awq"}
    assert {run["concurrency"] for run in runs} == {1, 4, 8}
    assert {run["input_tokens"] for run in runs} == {512, 2048}
    assert {run["prefix_caching"] for run in runs} == {False, True}
    assert all(run["output_tokens"] == 128 and run["repetitions"] == 3 for run in runs)


def test_benchmark_refuses_to_claim_results_without_l4(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr("eval_lab.benchmark.shutil.which", lambda _: None)
    with pytest.raises(RuntimeError, match="cannot be produced"):
        require_nvidia_l4()
