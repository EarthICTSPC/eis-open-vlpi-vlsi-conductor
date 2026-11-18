"""EIS-KKA-BENCH-001 reference harness.

Pure-Python scaffold. KKA semantics are injected and versioned by the caller;
there is intentionally no guessed/default KKA activation or SoftMax fallback.
"""
from __future__ import annotations
from dataclasses import dataclass
from math import exp, sqrt
from typing import Callable, Sequence

Vector = Sequence[float]
Matrix = Sequence[Vector]
ComplexMatrix = Sequence[Sequence[complex]]
WeightOperator = Callable[[ComplexMatrix, ComplexMatrix, int | None], Matrix]


def _validate_qkv(q: Matrix, k: Matrix, v: Matrix) -> tuple[int, int, int]:
    if not q or not k or not v:
        raise ValueError("Q, K and V must be non-empty")
    d = len(q[0])
    dv = len(v[0])
    if d == 0 or any(len(row) != d for row in q) or any(len(row) != d for row in k):
        raise ValueError("Q and K must have one common non-zero head dimension")
    if dv == 0 or any(len(row) != dv for row in v):
        raise ValueError("V rows must have a common non-zero value dimension")
    if len(k) != len(v):
        raise ValueError("K and V sequence lengths must match")
    if len(q) > len(k):
        raise ValueError("query sequence cannot exceed key sequence in this scaffold")
    return len(q), len(k), d


def _stable_softmax_row(row: Sequence[float]) -> list[float]:
    if not row:
        raise ValueError("softmax row cannot be empty")
    m = max(row)
    exps = [exp(x - m) for x in row]
    denom = sum(exps)
    return [x / denom for x in exps]


def _apply_weights(weights: Matrix, v: Matrix) -> list[list[float]]:
    if not weights or not v or len(weights[0]) != len(v):
        raise ValueError("weight matrix key dimension must equal V sequence length")
    if any(len(row) != len(v) for row in weights):
        raise ValueError("weight matrix must be rectangular")
    d_v = len(v[0])
    if d_v == 0 or any(len(row) != d_v for row in v):
        raise ValueError("V rows must have a common non-zero dimension")
    return [[sum(weights[i][j] * v[j][c] for j in range(len(v)))
             for c in range(d_v)] for i in range(len(weights))]


def electronic_attention(q: Matrix, k: Matrix, v: Matrix,
                         causal: bool = False) -> list[list[float]]:
    """Conventional scaled dot-product attention with stable SoftMax."""
    sq, sk, d = _validate_qkv(q, k, v)
    scores = [[sum(qi * kj for qi, kj in zip(qrow, krow)) / sqrt(d)
               for krow in k] for qrow in q]
    weights = []
    for i, row in enumerate(scores):
        visible = i + (sk - sq) + 1 if causal else sk
        visible = min(visible, sk)
        if visible <= 0:
            raise ValueError("causal mask produced an empty attention row")
        probs = _stable_softmax_row(row[:visible])
        weights.append(probs + [0.0] * (sk - visible))
    return _apply_weights(weights, v)


def electronic_kka_reference(q_fields: ComplexMatrix, k_fields: ComplexMatrix,
                             v: Matrix, operator: WeightOperator,
                             causal_length_offset: int | None = None
                             ) -> list[list[float]]:
    """Apply caller-supplied KKA weights, then value aggregation.

    operator must implement the frozen KKA encoding/transfer/interference
    convention and return query-by-key weights. No SoftMax is inserted here.
    """
    if operator is None:
        raise ValueError("a pinned KKA operator is required; no SoftMax fallback")
    if not q_fields or not k_fields:
        raise ValueError("complex Q and K fields must be non-empty")
    if len(k_fields) != len(v):
        raise ValueError("K field and V sequence lengths must match")
    weights = operator(q_fields, k_fields, causal_length_offset)
    if len(weights) != len(q_fields) or any(len(row) != len(v) for row in weights):
        raise ValueError("KKA operator returned an invalid query-by-key weight matrix")
    if any(not all(_is_finite(x) for x in row) for row in weights):
        raise ValueError("KKA weights must be finite")
    return _apply_weights(weights, v)


def _is_finite(x: float) -> bool:
    return x == x and abs(x) != float("inf")


@dataclass(frozen=True)
class OutputMetrics:
    max_abs_error: float
    rms_error: float
    cosine_similarity: float


def compare_outputs(reference: Matrix, candidate: Matrix) -> OutputMetrics:
    if len(reference) != len(candidate) or not reference:
        raise ValueError("outputs must have matching non-empty row counts")
    if any(len(x) != len(y) for x, y in zip(reference, candidate)):
        raise ValueError("outputs must have matching row dimensions")
    a = [x for row in reference for x in row]
    b = [x for row in candidate for x in row]
    if not a:
        raise ValueError("outputs must have non-empty dimensions")
    diffs = [x - y for x, y in zip(a, b)]
    na, nb = sqrt(sum(x*x for x in a)), sqrt(sum(x*x for x in b))
    cosine = sum(x*y for x, y in zip(a, b)) / (na*nb) if na and nb else (1.0 if na == nb else 0.0)
    return OutputMetrics(max(abs(x) for x in diffs),
                         sqrt(sum(x*x for x in diffs) / len(diffs)), cosine)


def integrate_power_trace(samples: Sequence[tuple[float, float]]) -> float:
    """Trapezoidal joule integration from (seconds, watts) samples."""
    if len(samples) < 2:
        raise ValueError("at least two timestamped power samples are required")
    energy = 0.0
    previous_t, previous_p = samples[0]
    if previous_t < 0 or previous_p < 0:
        raise ValueError("timestamps and power must be non-negative")
    for t, p in samples[1:]:
        if t <= previous_t or p < 0:
            raise ValueError("timestamps must increase and power must be non-negative")
        energy += (t - previous_t) * (previous_p + p) / 2.0
        previous_t, previous_p = t, p
    return energy


@dataclass(frozen=True)
class PhysicalSOIRecord:
    detector_output: Matrix
    component_energy_j: dict[str, float]
    total_energy_j: float
    latency_s: float


def physical_soi_record(detector_output: Matrix,
                        component_power_traces: dict[str, Sequence[tuple[float, float]]],
                        latency_s: float) -> PhysicalSOIRecord:
    """Build a physical record only from supplied measured detector/power traces.

    Component traces must be synchronized to the same run window. This function
    integrates them; it does not establish instrument calibration or provenance.
    """
    if not detector_output or not component_power_traces:
        raise ValueError("measured detector output and component power traces are required")
    if latency_s <= 0:
        raise ValueError("measured latency must be positive")
    energies = {name: integrate_power_trace(trace)
                for name, trace in component_power_traces.items()}
    return PhysicalSOIRecord(detector_output, energies, sum(energies.values()), latency_s)


def softmax_operation_ledger(sequence_length: int, heads: int) -> dict[str, int]:
    """Operation classes, not a blended FLOP count.

    Excludes stable-softmax max-reduction comparisons and counts row-sum
    additions as S-1 per row. Score scaling is reported separately.
    """
    if sequence_length < 1 or heads < 1:
        raise ValueError("sequence_length and heads must be positive")
    rows = heads * sequence_length
    scores = heads * sequence_length * sequence_length
    return {
        "score_scale_multiplications": scores,
        "softmax_score_subtractions": scores,
        "softmax_exponentials": scores,
        "softmax_row_sum_additions": rows * (sequence_length - 1),
        "softmax_normalization_divisions": scores,
        "softmax_row_max_comparisons_lower_bound": rows * (sequence_length - 1),
    }
