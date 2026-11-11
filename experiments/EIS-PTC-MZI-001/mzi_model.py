"""Parameterized, technology-independent EIS three-heater MZI model.

The ideal transfer equations follow EISKKA.PTC.PTCPrototype and Tian et al.
(2025), SI-1. All non-ideal numerical parameters are caller-supplied. The
module contains no foundry-specific geometry, layer map, or proprietary model.

Model equations are deliberately transparent:
- coupler visibility = product of 2*sqrt(k*(1-k)) for the two couplers;
- amplitude attenuation = 10**(-loss_dB/20);
- heater power = V**2/R(T);
- phase target = phase_efficiency[i] * sum_j(C[i,j] * P[j]);
- thermal state follows a first-order exponential response.

These are a configurable engineering abstraction, not a claim that Tian's
device follows this exact fitted response. Replace it with measured data and
a justified compact model when available.
"""
from __future__ import annotations

from dataclasses import dataclass
import cmath
import math
from typing import Sequence

Evidence = str


@dataclass(frozen=True)
class MZIControls:
    external: float
    internal_a: float
    internal_b: float


@dataclass(frozen=True)
class MZIParameters:
    wavelength_m: float
    effective_index: float
    propagation_loss_db_per_m: float
    interaction_length_m: float
    coupler1_split_ratio: float
    coupler2_split_ratio: float
    coupler1_excess_loss_db: float
    coupler2_excess_loss_db: float
    heater_resistance_ohm: tuple[float, float, float]
    heater_tempco_per_K: tuple[float, float, float]
    phase_efficiency_rad_per_W: tuple[float, float, float]
    thermal_coupling: tuple[tuple[float, float, float], ...]
    thermal_time_constant_s: tuple[float, float, float]
    parameter_evidence: Evidence = "ASSUMED"
    model_version: str = "0.1.0"

    def validate(self) -> None:
        if self.wavelength_m <= 0 or self.effective_index <= 0:
            raise ValueError("wavelength and effective index must be positive")
        if self.propagation_loss_db_per_m < 0 or self.interaction_length_m < 0:
            raise ValueError("loss and interaction length must be non-negative")
        for ratio in (self.coupler1_split_ratio, self.coupler2_split_ratio):
            if not 0.0 < ratio < 1.0:
                raise ValueError("coupler split ratios must be strictly between 0 and 1")
        if min(self.heater_resistance_ohm) <= 0:
            raise ValueError("heater resistances must be positive")
        if min(self.thermal_time_constant_s) <= 0:
            raise ValueError("thermal time constants must be positive")
        if len(self.thermal_coupling) != 3 or any(len(row) != 3 for row in self.thermal_coupling):
            raise ValueError("thermal_coupling must be a 3x3 matrix")


@dataclass(frozen=True)
class ThermalState:
    phase_rad: tuple[float, float, float] = (0.0, 0.0, 0.0)


@dataclass(frozen=True)
class MZIResult:
    signed_amplitude: float
    phase_rad: float
    field: complex
    output_power_relative: float
    heater_power_w: tuple[float, float, float]
    model_evidence: Evidence


def _coupler_visibility(split_ratio: float) -> float:
    return 2.0 * math.sqrt(split_ratio * (1.0 - split_ratio))


def heater_resistance_at_temperature(
    resistance_ohm: float, tempco_per_K: float, delta_temperature_K: float
) -> float:
    resistance = resistance_ohm * (1.0 + tempco_per_K * delta_temperature_K)
    if resistance <= 0:
        raise ValueError("temperature-adjusted heater resistance must be positive")
    return resistance


def heater_power(
    voltage_v: float,
    resistance_ohm: float,
    tempco_per_K: float = 0.0,
    delta_temperature_K: float = 0.0,
) -> float:
    resistance = heater_resistance_at_temperature(
        resistance_ohm, tempco_per_K, delta_temperature_K
    )
    return voltage_v * voltage_v / resistance


def target_heater_phases(
    powers_w: Sequence[float], params: MZIParameters
) -> tuple[float, float, float]:
    if len(powers_w) != 3:
        raise ValueError("exactly three heater powers are required")
    phases = []
    for i in range(3):
        coupled_power = sum(params.thermal_coupling[i][j] * powers_w[j] for j in range(3))
        phases.append(params.phase_efficiency_rad_per_W[i] * coupled_power)
    return tuple(phases)  # type: ignore[return-value]


def advance_thermal_state(
    state: ThermalState,
    target_phase_rad: Sequence[float],
    dt_s: float,
    params: MZIParameters,
) -> ThermalState:
    if dt_s < 0:
        raise ValueError("dt_s must be non-negative")
    if dt_s == 0:
        return state
    if len(target_phase_rad) != 3:
        raise ValueError("exactly three target phases are required")
    updated = tuple(
        target + (current - target) * math.exp(-dt_s / tau)
        for current, target, tau in zip(
            state.phase_rad, target_phase_rad, params.thermal_time_constant_s
        )
    )
    return ThermalState(updated)  # type: ignore[arg-type]


def ideal_field_amplitude(input_amplitude: float, controls: MZIControls) -> float:
    """Signed Tian SI-1 field-amplitude transfer; do not take abs(cos)."""
    return (
        input_amplitude
        / math.sqrt(2.0)
        * math.cos((controls.internal_b - controls.internal_a) / 2.0 + math.pi / 4.0)
    )


def ideal_field_phase(controls: MZIControls) -> float:
    return (
        controls.external
        + (controls.internal_a + controls.internal_b) / 2.0
        + math.pi / 4.0
    )


def evaluate_mzi(
    input_amplitude: float,
    controls: MZIControls,
    params: MZIParameters,
    heater_voltages_v: tuple[float, float, float] = (0.0, 0.0, 0.0),
    heater_delta_temperature_K: tuple[float, float, float] = (0.0, 0.0, 0.0),
    thermal_state: ThermalState | None = None,
) -> MZIResult:
    params.validate()
    powers = tuple(
        heater_power(v, r, tc, dtemp)
        for v, r, tc, dtemp in zip(
            heater_voltages_v,
            params.heater_resistance_ohm,
            params.heater_tempco_per_K,
            heater_delta_temperature_K,
        )
    )
    thermal = thermal_state or ThermalState()
    heater_phase = target_heater_phases(powers, params)
    controls_eff = MZIControls(
        external=controls.external + thermal.phase_rad[0] + heater_phase[0],
        internal_a=controls.internal_a + thermal.phase_rad[1] + heater_phase[1],
        internal_b=controls.internal_b + thermal.phase_rad[2] + heater_phase[2],
    )

    visibility = (
        _coupler_visibility(params.coupler1_split_ratio)
        * _coupler_visibility(params.coupler2_split_ratio)
    )
    total_loss_db = (
        params.propagation_loss_db_per_m * params.interaction_length_m
        + params.coupler1_excess_loss_db
        + params.coupler2_excess_loss_db
    )
    amplitude_transmission = 10.0 ** (-total_loss_db / 20.0)
    amplitude = (
        amplitude_transmission * visibility
        * ideal_field_amplitude(input_amplitude, controls_eff)
    )
    phase = ideal_field_phase(controls_eff)
    field = amplitude * cmath.exp(1j * phase)
    return MZIResult(
        signed_amplitude=amplitude,
        phase_rad=phase,
        field=field,
        output_power_relative=abs(field) ** 2,
        heater_power_w=powers,
        model_evidence=params.parameter_evidence,
    )
