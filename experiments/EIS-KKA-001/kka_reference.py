from __future__ import annotations

"""Independent mathematical reference for EIS KKA-001A.

PhotonForge-independent: validates ideal interference and detector sign/scale;
does not model the full KKA algorithm or a calibrated physical transfer law.
"""
import numpy as np


def real_cross_term_current(a: complex, b: complex, responsivity_a_per_w: float, *, power_scale_w: float = 1.0) -> float:
    """Ideal balanced-detector current for E1=(A+B)/sqrt(2), E2=(A-B)/sqrt(2).

    A and B are dimensionless complex envelopes. power_scale_w converts
    squared envelope magnitude to watts. Output units are amperes.
    """
    if responsivity_a_per_w < 0:
        raise ValueError("responsivity must be non-negative")
    if power_scale_w < 0:
        raise ValueError("power_scale_w must be non-negative")
    e1 = (a + b) / np.sqrt(2.0)
    e2 = (a - b) / np.sqrt(2.0)
    p_diff_w = power_scale_w * (abs(e1) ** 2 - abs(e2) ** 2)
    return float(responsivity_a_per_w * p_diff_w)


def real_cross_term_current_direct(a: complex, b: complex, responsivity_a_per_w: float, *, power_scale_w: float = 1.0) -> float:
    """Equivalent closed-form expression used as an independent oracle."""
    return float(2.0 * responsivity_a_per_w * power_scale_w * np.real(a * np.conjugate(b)))


def integrate_current(time_s: np.ndarray, current_a: np.ndarray) -> tuple[float, float]:
    """Return integrated charge in coulombs and average current in amperes."""
    t = np.asarray(time_s, dtype=float)
    i = np.asarray(current_a, dtype=float)
    if t.ndim != 1 or i.ndim != 1 or t.size != i.size or t.size < 2:
        raise ValueError("time and current must be 1-D arrays of equal length >= 2")
    if not np.all(np.isfinite(t)) or not np.all(np.isfinite(i)):
        raise ValueError("time and current must be finite")
    if np.any(np.diff(t) <= 0):
        raise ValueError("time samples must be strictly increasing")
    charge_c = float(np.trapezoid(i, x=t))
    average_current_a = charge_c / float(t[-1] - t[0])
    return charge_c, average_current_a
