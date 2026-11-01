from __future__ import annotations

"""Independent mathematical reference for EIS KKA-001A.

PhotonForge-independent: validates ideal interference and detector sign/scale;
does not model the full KKA algorithm or a calibrated physical transfer law.
"""
import math
from typing import Sequence


def real_cross_term_current(a: complex, b: complex, responsivity_a_per_w: float, *, power_scale_w: float = 1.0) -> float:
    """Ideal balanced-detector current for E1=(A+B)/sqrt(2), E2=(A-B)/sqrt(2).

    A and B are dimensionless complex envelopes. power_scale_w converts
    squared envelope magnitude to watts. Output units are amperes.
    """
    if responsivity_a_per_w < 0:
        raise ValueError("responsivity must be non-negative")
    if power_scale_w < 0:
        raise ValueError("power_scale_w must be non-negative")
    root_two = math.sqrt(2.0)
    e1 = (a + b) / root_two
    e2 = (a - b) / root_two
    p_diff_w = power_scale_w * (abs(e1) ** 2 - abs(e2) ** 2)
    return float(responsivity_a_per_w * p_diff_w)


def real_cross_term_current_direct(a: complex, b: complex, responsivity_a_per_w: float, *, power_scale_w: float = 1.0) -> float:
    """Equivalent closed-form expression used as an independent oracle."""
    return float(2.0 * responsivity_a_per_w * power_scale_w * (a * b.conjugate()).real)


def integrate_current(time_s: Sequence[float], current_a: Sequence[float]) -> tuple[float, float]:
    """Return integrated charge in coulombs and average current in amperes."""
    t = [float(v) for v in time_s]
    i = [float(v) for v in current_a]
    if len(t) != len(i) or len(t) < 2:
        raise ValueError("time and current must be equal-length sequences of size >= 2")
    if not all(math.isfinite(v) for v in t + i):
        raise ValueError("time and current must be finite")
    if any(t[k + 1] <= t[k] for k in range(len(t) - 1)):
        raise ValueError("time samples must be strictly increasing")
    charge_c = sum((t[k + 1] - t[k]) * (i[k + 1] + i[k]) / 2.0 for k in range(len(t) - 1))
    average_current_a = charge_c / (t[-1] - t[0])
    return charge_c, average_current_a
