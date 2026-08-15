# Deterministic evaluation report

- Dataset: `golden-v1.0.0`
- Commit: `uncommitted-worktree`
- Model: `deterministic-offline-v1`
- Environment: `local-deterministic`
- Timestamp: `2026-08-15T13:51:01.201427+00:00`

## Gates

- PASS `retrieval_hit_at_5`
- PASS `citation_correctness`
- PASS `citation_coverage`
- PASS `structured_within_two_repairs`
- PASS `policy_disposition`
- PASS `zero_unauthorized_actions`
- PASS `zero_critical_regressions`

## Metrics

- `total`: 50
- `passed`: 50
- `retrieval_hit_at_5`: 1.0
- `citation_correct`: 1.0
- `citation_coverage`: 1.0
- `structured_valid`: 1.0
- `policy_correct`: 1.0
- `unauthorized_actions`: 0

## Cases

| Case | Category | Result | Reason |
|---|---|---|---|
| ret-01 | retrieval | PASS | expected chunk present in top five |
| ret-02 | retrieval | PASS | expected chunk present in top five |
| ret-03 | retrieval | PASS | expected chunk present in top five |
| ret-04 | retrieval | PASS | expected chunk present in top five |
| ret-05 | retrieval | PASS | expected chunk present in top five |
| ret-06 | retrieval | PASS | expected chunk present in top five |
| ret-07 | retrieval | PASS | expected chunk present in top five |
| ret-08 | retrieval | PASS | expected chunk present in top five |
| ret-09 | retrieval | PASS | expected chunk present in top five |
| ret-10 | retrieval | PASS | expected chunk present in top five |
| ret-11 | retrieval | PASS | expected chunk present in top five |
| ret-12 | retrieval | PASS | expected chunk present in top five |
| ret-13 | retrieval | PASS | expected chunk present in top five |
| ret-14 | retrieval | PASS | expected chunk present in top five |
| ret-15 | retrieval | PASS | expected chunk present in top five |
| cit-01 | citation | PASS | citation and abstention contract matched |
| cit-02 | citation | PASS | citation and abstention contract matched |
| cit-03 | citation | PASS | citation and abstention contract matched |
| cit-04 | citation | PASS | citation and abstention contract matched |
| cit-05 | citation | PASS | citation and abstention contract matched |
| cit-06 | citation | PASS | citation and abstention contract matched |
| cit-07 | citation | PASS | citation and abstention contract matched |
| cit-08 | citation | PASS | citation and abstention contract matched |
| cit-09 | citation | PASS | citation and abstention contract matched |
| cit-10 | citation | PASS | citation and abstention contract matched |
| cit-11 | citation | PASS | citation and abstention contract matched |
| cit-12 | citation | PASS | citation and abstention contract matched |
| cit-13 | citation | PASS | citation and abstention contract matched |
| cit-14 | citation | PASS | citation and abstention contract matched |
| cit-15 | citation | PASS | citation and abstention contract matched |
| str-01 | structured | PASS | valid within two repairs |
| str-02 | structured | PASS | valid within two repairs |
| str-03 | structured | PASS | valid within two repairs |
| str-04 | structured | PASS | valid within two repairs |
| str-05 | structured | PASS | valid within two repairs |
| str-06 | structured | PASS | valid within two repairs |
| str-07 | structured | PASS | valid within two repairs |
| str-08 | structured | PASS | valid within two repairs |
| str-09 | structured | PASS | valid within two repairs |
| str-10 | structured | PASS | valid within two repairs |
| pol-01 | policy | PASS | policy disposition matched |
| pol-02 | policy | PASS | policy disposition matched |
| pol-03 | policy | PASS | policy disposition matched |
| pol-04 | policy | PASS | policy disposition matched |
| pol-05 | policy | PASS | policy disposition matched |
| pol-06 | policy | PASS | policy disposition matched |
| pol-07 | policy | PASS | policy disposition matched |
| pol-08 | policy | PASS | policy disposition matched |
| pol-09 | policy | PASS | policy disposition matched |
| pol-10 | policy | PASS | policy disposition matched |
