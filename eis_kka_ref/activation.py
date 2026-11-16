"""Analytical KKA activation; physical phase response is caller-supplied."""
from __future__ import annotations
import math
from collections.abc import Callable

def kka_activation(amplitude: float, phase_response: Callable[[float], float],
                   theta_n_rad: float = 0.0, *, denominator_tolerance: float = 1e-12) -> float:
    r"""Evaluate f_NL(A)=A cos(phi(A)+theta_n)/cos(theta_n).

    phase_response(A) returns radians. No platform-specific phi(A) is assumed.
    """
    if not all(math.isfinite(float(v)) for v in (amplitude, theta_n_rad, denominator_tolerance)):
        raise ValueError("amplitude, theta_n_rad, and tolerance must be finite")
    if amplitude < 0.0:
        raise ValueError("amplitude must be non-negative")
    if denominator_tolerance <= 0.0:
        raise ValueError("denominator_tolerance must be positive")
    denominator = math.cos(theta_n_rad)
    if abs(denominator) <= denominator_tolerance:
        raise ValueError("cos(theta_n_rad) is too close to zero")
    phase = float(phase_response(amplitude))
    if not math.isfinite(phase):
        raise ValueError("phase_response must return a finite phase")
    return amplitude * math.cos(phase + theta_n_rad) / denominator
