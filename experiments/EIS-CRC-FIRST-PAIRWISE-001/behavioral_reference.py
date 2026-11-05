"""Behavioral oracle for EIS-CRC-FIRST-PAIRWISE-001.

This is a deterministic software reference, NOT a photonic device model.
It accepts abstract normalized scores, not optical fields or measured photocurrents.
"""
from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class Decision(str, Enum):
    A_WINS = "A_WINS"
    B_WINS = "B_WINS"
    INDETERMINATE = "INDETERMINATE"
    FAULT = "FAULT"


@dataclass(frozen=True)
class ComparatorInput:
    score_a: float
    score_b: float
    min_gap: float = 0.0


def reference_decision(inputs: ComparatorInput) -> Decision:
    """Return the reference ordering under an explicit indifference gap.

    Scores must already be mapped into the same declared normalized score
    domain. If abs(score_a - score_b) <= min_gap, return INDETERMINATE.
    Invalid or non-finite inputs return FAULT.
    """
    import math

    values = (inputs.score_a, inputs.score_b, inputs.min_gap)
    if not all(math.isfinite(v) for v in values):
        return Decision.FAULT
    if inputs.min_gap < 0:
        return Decision.FAULT
    delta = inputs.score_a - inputs.score_b
    if abs(delta) <= inputs.min_gap:
        return Decision.INDETERMINATE
    return Decision.A_WINS if delta > 0 else Decision.B_WINS
