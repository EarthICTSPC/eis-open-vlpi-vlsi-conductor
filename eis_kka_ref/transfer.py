"""Complex field-transfer reference model; no platform law is prescribed."""
from __future__ import annotations
from dataclasses import dataclass
import cmath
import math

def _finite(value: float, name: str) -> None:
    if not math.isfinite(value):
        raise ValueError(f"{name} must be finite")

@dataclass(frozen=True)
class ComplexTransfer:
    """H = amplitude * exp(1j * phase_rad); amplitude is field, not power."""
    amplitude: float
    phase_rad: float

    def __post_init__(self) -> None:
        _finite(self.amplitude, "amplitude")
        _finite(self.phase_rad, "phase_rad")
        if self.amplitude < 0.0:
            raise ValueError("amplitude must be non-negative")

    @property
    def coefficient(self) -> complex:
        return self.amplitude * cmath.exp(1j * self.phase_rad)

    @classmethod
    def from_complex(cls, value: complex) -> "ComplexTransfer":
        z = complex(value)
        if not (math.isfinite(z.real) and math.isfinite(z.imag)):
            raise ValueError("complex transfer must be finite")
        return cls(abs(z), cmath.phase(z))

def complex_transfer(amplitude: float, phase_rad: float) -> complex:
    """Return H = A exp(j phi), validating polar parameters."""
    return ComplexTransfer(amplitude, phase_rad).coefficient

def apply_complex_transfer(field: complex, transfer: ComplexTransfer | complex) -> complex:
    """Apply H to a finite complex input field."""
    e = complex(field)
    if not (math.isfinite(e.real) and math.isfinite(e.imag)):
        raise ValueError("input field must be finite")
    h = transfer.coefficient if isinstance(transfer, ComplexTransfer) else complex(transfer)
    if not (math.isfinite(h.real) and math.isfinite(h.imag)):
        raise ValueError("transfer coefficient must be finite")
    return h * e
