# ADR 0001: Separate deterministic evaluations from GPU benchmarks

- Status: accepted
- Date: 2026-08-15

## Decision

Run the 50 contract cases offline and deterministically in every CI build. Run vLLM performance measurements only on a verified NVIDIA L4, recording raw results and environment metadata.

## Consequences

CI can block functional regressions cheaply. Performance results cost time and money and therefore remain an explicitly approved, bounded activity. Neither evidence class is substituted for the other.
