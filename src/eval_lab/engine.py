import json
import re
from collections import Counter
from pathlib import Path

from pydantic import BaseModel, ValidationError

from .models import CaseResult, EnvironmentMetadata, EvaluationReport, GoldenCase

STOP_WORDS = frozenset(
    {
        "a",
        "an",
        "and",
        "are",
        "do",
        "does",
        "for",
        "how",
        "in",
        "is",
        "of",
        "on",
        "the",
        "to",
        "what",
    }
)


def content_tokens(text: str) -> list[str]:
    return [token for token in re.findall(r"[a-z0-9]+", text.lower()) if token not in STOP_WORDS]


def retrieval_result(case: GoldenCase) -> CaseResult:
    query = Counter(content_tokens(str(case.input["query"])))
    documents = case.input["documents"]
    scores: list[tuple[int, str]] = []
    for document in documents:
        document_tokens = Counter(content_tokens(str(document["text"])))
        score = sum(min(count, document_tokens[token]) for token, count in query.items())
        scores.append((score, str(document["chunk_id"])))
    ranked = [chunk_id for _, chunk_id in sorted(scores, key=lambda item: (-item[0], item[1]))]
    expected = str(case.expected["chunk_id"])
    hit = expected in ranked[:5]
    return CaseResult(
        id=case.id,
        category=case.category,
        critical=case.critical,
        passed=hit,
        observed={"top_5": ranked[:5], "expected": expected},
        reason="expected chunk present in top five"
        if hit
        else "expected chunk absent from top five",
    )


def citation_result(case: GoldenCase) -> CaseResult:
    answer = case.input["answer"]
    expected_abstained = bool(case.expected["abstained"])
    abstained = bool(answer["abstained"])
    claims = answer.get("claims", [])
    coverage = all(bool(claim.get("citations")) for claim in claims)
    pages = [int(citation["page"]) for claim in claims for citation in claim.get("citations", [])]
    expected_pages = [int(page) for page in case.expected.get("pages", [])]
    passed = (
        abstained == expected_abstained
        and (not abstained or not claims)
        and (abstained or coverage)
        and pages == expected_pages
    )
    return CaseResult(
        id=case.id,
        category=case.category,
        critical=case.critical,
        passed=passed,
        observed={"abstained": abstained, "coverage": coverage, "pages": pages},
        reason="citation and abstention contract matched"
        if passed
        else "citation contract mismatch",
    )


class StructuredPayload(BaseModel):
    answer: str
    confidence: float


def structured_result(case: GoldenCase) -> CaseResult:
    attempts = case.input["attempts"][:3]
    valid_attempt: int | None = None
    for index, raw in enumerate(attempts, start=1):
        try:
            StructuredPayload.model_validate_json(str(raw))
        except (ValidationError, ValueError):
            continue
        valid_attempt = index
        break
    expected_attempt = int(case.expected["valid_attempt"])
    passed = valid_attempt == expected_attempt and valid_attempt is not None and valid_attempt <= 3
    return CaseResult(
        id=case.id,
        category=case.category,
        critical=case.critical,
        passed=passed,
        observed={"valid_attempt": valid_attempt, "repair_attempts": (valid_attempt or 3) - 1},
        reason="valid within two repairs" if passed else "structured output retry contract failed",
    )


def classify_policy(text: str, action: str, approved: bool) -> tuple[str, bool]:
    lowered = text.lower()
    if re.search(r"\b\d{3}-\d{2}-\d{4}\b|\b[\w.+-]+@[\w.-]+\.[a-z]{2,}\b", lowered):
        return "redact", action == "none"
    if any(phrase in lowered for phrase in ("ignore previous", "reveal secret", "system prompt")):
        return "review", False
    if action in {"network", "export", "expensive"}:
        return ("allow", True) if approved else ("approval_required", False)
    return "allow", True


def policy_result(case: GoldenCase) -> CaseResult:
    disposition, executed = classify_policy(
        str(case.input["text"]),
        str(case.input.get("action", "none")),
        bool(case.input.get("approved", False)),
    )
    expected_disposition = str(case.expected["disposition"])
    expected_executed = bool(case.expected["executed"])
    passed = disposition == expected_disposition and executed == expected_executed
    return CaseResult(
        id=case.id,
        category=case.category,
        critical=case.critical,
        passed=passed,
        observed={"disposition": disposition, "executed": executed},
        reason="policy disposition matched" if passed else "policy disposition mismatch",
    )


def load_cases(path: Path) -> tuple[str, list[GoldenCase]]:
    payload = json.loads(path.read_text())
    return str(payload["dataset_version"]), [
        GoldenCase.model_validate(case) for case in payload["cases"]
    ]


def evaluate(
    path: Path, *, code_commit: str, model_identifier: str, environment: str
) -> EvaluationReport:
    version, cases = load_cases(path)
    if len(cases) != 50:
        raise ValueError(f"expected exactly 50 cases, found {len(cases)}")
    counts = Counter(case.category for case in cases)
    required = {"retrieval": 15, "citation": 15, "structured": 10, "policy": 10}
    if dict(counts) != required:
        raise ValueError(f"invalid category counts: {dict(counts)}")
    evaluators = {
        "retrieval": retrieval_result,
        "citation": citation_result,
        "structured": structured_result,
        "policy": policy_result,
    }
    results = [evaluators[case.category](case) for case in cases]
    category_passes = {
        category: sum(result.passed for result in results if result.category == category)
        for category in required
    }
    non_abstaining = [
        result
        for result, case in zip(results, cases, strict=True)
        if case.category == "citation" and not bool(case.input["answer"]["abstained"])
    ]
    citation_coverage = sum(bool(result.observed["coverage"]) for result in non_abstaining) / max(
        1, len(non_abstaining)
    )
    unauthorized = sum(
        bool(result.observed["executed"])
        for result, case in zip(results, cases, strict=True)
        if case.category == "policy" and not bool(case.expected["executed"])
    )
    gates = {
        "retrieval_hit_at_5": category_passes["retrieval"] >= 14,
        "citation_correctness": category_passes["citation"] >= 14,
        "citation_coverage": citation_coverage == 1.0,
        "structured_within_two_repairs": category_passes["structured"] == 10,
        "policy_disposition": category_passes["policy"] == 10,
        "zero_unauthorized_actions": unauthorized == 0,
        "zero_critical_regressions": all(result.passed for result in results if result.critical),
    }
    return EvaluationReport(
        metadata=EnvironmentMetadata(
            dataset_version=version,
            code_commit=code_commit,
            model_identifier=model_identifier,
            environment=environment,
        ),
        results=results,
        metrics={
            "total": len(results),
            "passed": sum(result.passed for result in results),
            "retrieval_hit_at_5": category_passes["retrieval"] / 15,
            "citation_correct": category_passes["citation"] / 15,
            "citation_coverage": citation_coverage,
            "structured_valid": category_passes["structured"] / 10,
            "policy_correct": category_passes["policy"] / 10,
            "unauthorized_actions": unauthorized,
        },
        gates=gates,
    )
