"""Balanced two-port photodetector reference model."""
from __future__ import annotations
from dataclasses import dataclass
import math

@dataclass(frozen=True)
class DetectorOutput:
    current_plus_a: float
    current_minus_a: float
    differential_current_a: float

@dataclass(frozen=True)
class BalancedDetector:
    """Ideal +/- ports plus explicit branch gains and dark offsets.

    E+ = (a+b)/sqrt(2), E- = (a-b)/sqrt(2), so equal-gain,
    zero-offset differential current is R * 2 Re(a conjugate(b)).
    Fields are dimensionless envelopes under a caller-declared normalization.
    """
    responsivity_a_per_unit: float = 1.0
    gain_plus: float = 1.0
    gain_minus: float = 1.0
    offset_plus_a: float = 0.0
    offset_minus_a: float = 0.0

    def __post_init__(self) -> None:
        for name in ("responsivity_a_per_unit", "gain_plus", "gain_minus",
                     "offset_plus_a", "offset_minus_a"):
            if not math.isfinite(getattr(self, name)):
                raise ValueError(f"{name} must be finite")
        if self.responsivity_a_per_unit < 0 or self.gain_plus < 0 or self.gain_minus < 0:
            raise ValueError("responsivity and branch gains must be non-negative")

    def measure(self, a: complex, b: complex) -> DetectorOutput:
        a, b = complex(a), complex(b)
        for name, value in (("a", a), ("b", b)):
            if not (math.isfinite(value.real) and math.isfinite(value.imag)):
                raise ValueError(f"{name} must be finite")
        scale = math.sqrt(0.5)
        e_plus, e_minus = (a + b) * scale, (a - b) * scale
        p_plus, p_minus = abs(e_plus) ** 2, abs(e_minus) ** 2
        i_plus = self.responsivity_a_per_unit * self.gain_plus * p_plus + self.offset_plus_a
        i_minus = self.responsivity_a_per_unit * self.gain_minus * p_minus + self.offset_minus_a
        return DetectorOutput(i_plus, i_minus, i_plus - i_minus)
