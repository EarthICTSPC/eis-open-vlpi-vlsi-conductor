"""Parameterized complex-field model for a two-coupler SOI MZI.

EIS-KKA-001B — analytical reference model, not a Tidy3D simulation.
No optimizer and no 001A calibration coefficients are imported.
All device parameters are explicit inputs; no SOI material constants or
dimensions are assumed.

Coupler convention:
    C(k) = [[sqrt(1-k), sqrt(k)],
            [sqrt(k),  -sqrt(1-k)]]
"""
from __future__ import annotations
from dataclasses import dataclass
import numpy as np
from numpy.typing import ArrayLike, NDArray

ComplexArray = NDArray[np.complex128]
FloatArray = NDArray[np.float64]


def directional_coupler(kappa: float) -> NDArray[np.float64]:
    """Ideal lossless 2x2 coupler; kappa is cross-coupled power fraction."""
    if not np.isfinite(kappa) or not 0.0 <= kappa <= 1.0:
        raise ValueError("kappa must be finite and in [0, 1]")
    t, c = np.sqrt(1.0 - kappa), np.sqrt(kappa)
    return np.array([[t, c], [c, -t]], dtype=float)


def _field_pair(value: ArrayLike, name: str) -> ComplexArray:
    arr = np.asarray(value, dtype=np.complex128)
    if arr.shape != (2,):
        raise ValueError(f"{name} must be a complex field pair with shape (2,)")
    if not np.isfinite(arr).all():
        raise ValueError(f"{name} must contain finite complex values")
    return arr


@dataclass(frozen=True)
class MZIResult:
    input_fields: ComplexArray
    after_input_coupler: ComplexArray
    arm_fields: ComplexArray
    output_fields: ComplexArray
    output_powers: FloatArray
    balanced_difference: float


def simulate_mzi(
    input_fields: ArrayLike,
    *,
    kappa_in: float = 0.5,
    kappa_out: float = 0.5,
    phase_rad: ArrayLike = (0.0, 0.0),
    arm_loss_db: ArrayLike = (0.0, 0.0),
) -> MZIResult:
    """Evaluate a static monochromatic two-coupler MZI.

    arm_loss_db is total POWER loss per arm in dB. Input field normalization
    and reference planes are caller responsibilities.
    """
    ein = _field_pair(input_fields, "input_fields")
    phase = np.asarray(phase_rad, dtype=float)
    loss = np.asarray(arm_loss_db, dtype=float)
    if phase.shape != (2,) or not np.isfinite(phase).all():
        raise ValueError("phase_rad must be two finite radians values")
    if loss.shape != (2,) or not np.isfinite(loss).all() or np.any(loss < 0):
        raise ValueError("arm_loss_db must be two finite nonnegative values")

    cin, cout = directional_coupler(kappa_in), directional_coupler(kappa_out)
    after_in = cin @ ein
    field_attenuation = 10.0 ** (-loss / 20.0)
    arm_fields = after_in * field_attenuation * np.exp(1j * phase)
    output_fields = cout @ arm_fields
    output_powers = np.abs(output_fields) ** 2
    return MZIResult(
        input_fields=ein.copy(),
        after_input_coupler=after_in,
        arm_fields=arm_fields,
        output_fields=output_fields,
        output_powers=np.asarray(output_powers, dtype=float),
        balanced_difference=float(output_powers[0] - output_powers[1]),
    )


def ideal_balanced_interference(field_a: complex, field_b: complex) -> float:
    """Ideal 50:50 output-port difference: 2 Re(A B*)."""
    return float(2.0 * np.real(complex(field_a) * np.conj(complex(field_b))))


def mzi_scattering_matrix(
    *,
    kappa_in: float = 0.5,
    kappa_out: float = 0.5,
    phase_rad: ArrayLike = (0.0, 0.0),
    arm_loss_db: ArrayLike = (0.0, 0.0),
) -> ComplexArray:
    """Return the idealized reciprocal 4-port MZI scattering matrix.

    Port ordering is [left_0, left_1, right_0, right_1]. The forward
    left-to-right transfer block is U = C_out @ D @ C_in; reciprocity
    sets the reverse block to U.T. Reflection blocks are zero by model
    definition. With zero arm loss, S is unitary. With positive arm loss,
    S is reciprocal but subunitary because dissipative channels are omitted.

    This is an analytical network representation, not a foundry compact
    model or a claim about a measured SOI device.
    """
    phase = np.asarray(phase_rad, dtype=float)
    loss = np.asarray(arm_loss_db, dtype=float)
    if phase.shape != (2,) or not np.isfinite(phase).all():
        raise ValueError("phase_rad must be two finite radians values")
    if loss.shape != (2,) or not np.isfinite(loss).all() or np.any(loss < 0):
        raise ValueError("arm_loss_db must be two finite nonnegative values")

    cin = directional_coupler(kappa_in)
    cout = directional_coupler(kappa_out)
    field_attenuation = 10.0 ** (-loss / 20.0)
    arm_transfer = np.diag(field_attenuation * np.exp(1j * phase))
    forward = cout @ arm_transfer @ cin

    scattering = np.zeros((4, 4), dtype=np.complex128)
    scattering[:2, 2:] = forward.T
    scattering[2:, :2] = forward
    return scattering
