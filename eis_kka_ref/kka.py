"""Independent numerical reference for EIS KKA trajectory conventions.

Lean4 owns the formal definition. This module independently evaluates a
finite-difference estimate from caller-supplied amplitude and unwrapped phase
functions; it is not a formal proof or a physical device model.
"""
from __future__ import annotations

import math
from collections.abc import Callable

PHASOR_CONVENTION = "physical_field = Re(E_phasor * exp(+i*omega*t))"
AMPLITUDE_CONVENTION = "A is field-amplitude transmission, not intensity"
BALANCED_DETECTOR_CONVENTION = (
    "E_plus=(a+b)/sqrt(2); E_minus=(a-b)/sqrt(2); "
    "I_plus-I_minus=2*R*Re(a*conj(b)) for matched ideal branches"
)


def _finite(value: float, name: str) -> float:
    result = float(value)
    if not math.isfinite(result):
        raise ValueError(f"{name} must be finite")
    return result


def _central_derivative(
    function: Callable[[float], float], point: float, step: float, name: str
) -> float:
    plus = _finite(function(point + step), f"{name}(u+h)")
    minus = _finite(function(point - step), f"{name}(u-h)")
    return (plus - minus) / (2.0 * step)


def kappa_a_from_drive(
    amplitude: Callable[[float], float],
    phase_rad_unwrapped: Callable[[float], float],
    drive: float,
    *,
    step: float = 1e-5,
    denominator_tolerance: float = 1e-12,
) -> float:
    r"""Estimate kappa_A = d(phi)/d(ln A) from a drive parameter u.

    Uses central finite differences:
        kappa_A(u) ~= (d phi/du) / ((d A/du) / A).

    A must be positive at u. The phase function must be continuous and
    unwrapped over [u-step, u+step]. The result is undefined when dA/du
    is zero (within denominator_tolerance). A is field-amplitude transmission,
    not intensity transmission.
    """
    u = _finite(drive, "drive")
    h = _finite(step, "step")
    tol = _finite(denominator_tolerance, "denominator_tolerance")
    if h <= 0.0:
        raise ValueError("step must be positive")
    if tol <= 0.0:
        raise ValueError("denominator_tolerance must be positive")

    a0 = _finite(amplitude(u), "amplitude(u)")
    if a0 <= 0.0:
        raise ValueError("amplitude(u) must be positive for ln(A)")

    da_du = _central_derivative(amplitude, u, h, "amplitude")
    dphi_du = _central_derivative(phase_rad_unwrapped, u, h, "phase")
    dln_a_du = da_du / a0
    if abs(dln_a_du) <= tol:
        raise ValueError("d(ln A)/du is zero or numerically singular")
    return dphi_du / dln_a_du


def kappa_i_from_drive(
    amplitude: Callable[[float], float],
    phase_rad_unwrapped: Callable[[float], float],
    drive: float,
    *,
    step: float = 1e-5,
    denominator_tolerance: float = 1e-12,
) -> float:
    r"""Return kappa_I = d(phi)/d(ln I) = kappa_A/2 for I proportional to A²."""
    return 0.5 * kappa_a_from_drive(
        amplitude,
        phase_rad_unwrapped,
        drive,
        step=step,
        denominator_tolerance=denominator_tolerance,
    )
