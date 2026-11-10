"""Ideal source-equation reference for the Tian et al. PTC 10x1 prototype.

This is an independent binary64 software implementation of the SI-1 MZI
transfer equations. It is not a device model or measured calibration.
"""
from __future__ import annotations

from dataclasses import dataclass
import cmath
import math


@dataclass(frozen=True)
class MZIControls:
    external: float
    internal_a: float
    internal_b: float


def mzi_field_amplitude(input_amplitude: float, controls: MZIControls) -> float:
    """Signed output amplitude from SI-1 Eq. (S2)/(S3)."""
    return (
        input_amplitude
        / math.sqrt(2.0)
        * math.cos((controls.internal_b - controls.internal_a) / 2.0 + math.pi / 4.0)
    )


def mzi_field_phase(controls: MZIControls) -> float:
    """Output phase from SI-1 Eq. (S2)/(S3)."""
    return (
        controls.external
        + (controls.internal_a + controls.internal_b) / 2.0
        + math.pi / 4.0
    )


def mzi_field(input_amplitude: float, controls: MZIControls) -> complex:
    """Ideal complex envelope; the signed amplitude is deliberately preserved."""
    return mzi_field_amplitude(input_amplitude, controls) * cmath.exp(
        1j * mzi_field_phase(controls)
    )


def bpd_output(
    input_amplitude_a: float,
    input_amplitude_b: float,
    a: MZIControls,
    b: MZIControls,
) -> float:
    """Ideal signed balanced-detection output from SI-1 Eq. (S4)."""
    phase_difference = (
        a.external
        - b.external
        + (a.internal_a + a.internal_b) / 2.0
        - (b.internal_a + b.internal_b) / 2.0
    )
    return (
        2.0
        * mzi_field_amplitude(input_amplitude_a, a)
        * mzi_field_amplitude(input_amplitude_b, b)
        * math.sin(phase_difference)
    )
