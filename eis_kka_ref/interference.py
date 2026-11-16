"""Ideal scalar interference operators with explicit output conventions."""
from __future__ import annotations
import math

def _field(value: complex, name: str) -> complex:
    z = complex(value)
    if not (math.isfinite(z.real) and math.isfinite(z.imag)):
        raise ValueError(f"{name} must be finite")
    return z

def total_intensity(a: complex, b: complex) -> float:
    """Return |a+b|^2, including both self-intensity terms."""
    a, b = _field(a, "a"), _field(b, "b")
    return abs(a + b) ** 2

def balanced_cross_term(a: complex, b: complex) -> float:
    """Return the signed balanced cross term 2 Re(a conjugate(b))."""
    a, b = _field(a, "a"), _field(b, "b")
    return 2.0 * (a * b.conjugate()).real
