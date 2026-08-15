import html
import json
from pathlib import Path

from .models import EvaluationReport


def write_reports(report: EvaluationReport, output: Path) -> None:
    output.mkdir(parents=True, exist_ok=True)
    (output / "evaluation.json").write_text(
        json.dumps(report.model_dump(mode="json"), indent=2) + "\n"
    )
    rows = "\n".join(
        "| "
        f"{result.id} | {result.category} | {'PASS' if result.passed else 'FAIL'} | "
        f"{result.reason} |"
        for result in report.results
    )
    gates = "\n".join(
        f"- {'PASS' if passed else 'FAIL'} `{name}`" for name, passed in report.gates.items()
    )
    metrics = "\n".join(f"- `{name}`: {value}" for name, value in report.metrics.items())
    markdown = f"""# Deterministic evaluation report

- Dataset: `{report.metadata.dataset_version}`
- Commit: `{report.metadata.code_commit}`
- Model: `{report.metadata.model_identifier}`
- Environment: `{report.metadata.environment}`
- Timestamp: `{report.metadata.timestamp.isoformat()}`

## Gates

{gates}

## Metrics

{metrics}

## Cases

| Case | Category | Result | Reason |
|---|---|---|---|
{rows}
"""
    (output / "evaluation.md").write_text(markdown)
    category_metrics = [
        ("Retrieval", float(report.metrics["retrieval_hit_at_5"])),
        ("Citations", float(report.metrics["citation_correct"])),
        ("Structured", float(report.metrics["structured_valid"])),
        ("Policy", float(report.metrics["policy_correct"])),
    ]
    bars = []
    for index, (label, value) in enumerate(category_metrics):
        y = 35 + index * 55
        width = round(value * 420, 2)
        bars.append(
            f'<text x="10" y="{y + 18}" fill="#d9e1e8">{html.escape(label)}</text>'
            f'<rect x="115" y="{y}" width="420" height="24" rx="4" fill="#27313a"/>'
            f'<rect x="115" y="{y}" width="{width}" height="24" rx="4" fill="#6ee7b7"/>'
            f'<text x="545" y="{y + 18}" fill="#d9e1e8">{value:.0%}</text>'
        )
    svg = (
        '<svg xmlns="http://www.w3.org/2000/svg" width="620" height="280" role="img" '
        'aria-label="Evaluation category pass rates">'
        '<rect width="100%" height="100%" fill="#11171d"/>'
        '<text x="10" y="22" fill="#ffffff" font-size="16">Evaluation category pass rates</text>'
        + "".join(bars)
        + "</svg>\n"
    )
    (output / "evaluation.svg").write_text(svg)
