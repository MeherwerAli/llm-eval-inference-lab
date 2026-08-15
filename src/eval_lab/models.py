from datetime import UTC, datetime
from typing import Any, Literal

from pydantic import BaseModel, Field, model_validator

Category = Literal["retrieval", "citation", "structured", "policy"]


class GoldenCase(BaseModel):
    id: str
    category: Category
    critical: bool = True
    input: dict[str, Any]
    expected: dict[str, Any]


class CaseResult(BaseModel):
    id: str
    category: Category
    critical: bool
    passed: bool
    observed: dict[str, Any]
    reason: str


class EnvironmentMetadata(BaseModel):
    dataset_version: str
    code_commit: str
    model_identifier: str
    environment: str
    timestamp: datetime = Field(default_factory=lambda: datetime.now(UTC))


class EvaluationReport(BaseModel):
    metadata: EnvironmentMetadata
    results: list[CaseResult]
    metrics: dict[str, float | int]
    gates: dict[str, bool]

    @model_validator(mode="after")
    def require_exact_dataset(self) -> "EvaluationReport":
        if len(self.results) != 50:
            raise ValueError("the versioned evaluation suite must contain exactly 50 cases")
        return self
