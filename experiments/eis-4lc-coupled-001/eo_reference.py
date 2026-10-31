"""Published hybrid SiN/TFLN EO phase-modulator reference.

Source: W.-B. Lee et al., Optics Express 32(6), 9171-9183 (2024),
DOI 10.1364/OE.518961.

Important evidence boundary:
- The paper reports 0.98 pF capacitance per EO phase modulator, measured
  with a HIOKI IM3536 LCR meter.
- It describes a push-pull MZI characterization and GSG electrode probing,
  but does not specify the exact LCR terminal definition or measurement
  frequency for the 0.98 pF value.
- Therefore the published 0.98 pF is NOT silently typed as a differential
  two-terminal capacitance or as four node-to-ground shunts.

The ring-sizing function below is explicitly conditional: its C_EO argument
must come from a subsequently verified differential-port definition.
"""
from __future__ import annotations

from dataclasses import dataclass
import math


@dataclass(frozen=True)
class PublishedEOReference:
    name: str
    source_doi: str
    interaction_length_m: float
    capacitance_per_phase_modulator_f: float
    capacitance_measurement_method: str
    capacitance_terminal_definition: str
    capacitance_measurement_frequency_hz: float | None
    half_wave_voltage_v: float
    reported_energy_per_pi_j: float
    estimated_bandwidth_hz: float
    measured_test_bandwidth_hz: float
    measured_test_length_m: float
    electrode_configuration: str

    def validate(self) -> None:
        positive = {
            "interaction_length_m": self.interaction_length_m,
            "capacitance_per_phase_modulator_f": self.capacitance_per_phase_modulator_f,
            "half_wave_voltage_v": self.half_wave_voltage_v,
            "reported_energy_per_pi_j": self.reported_energy_per_pi_j,
            "estimated_bandwidth_hz": self.estimated_bandwidth_hz,
            "measured_test_bandwidth_hz": self.measured_test_bandwidth_hz,
            "measured_test_length_m": self.measured_test_length_m,
        }
        for name, value in positive.items():
            if not math.isfinite(value) or value <= 0:
                raise ValueError(f"{name} must be finite and positive")
        if (self.capacitance_measurement_frequency_hz is not None
                and (not math.isfinite(self.capacitance_measurement_frequency_hz)
                     or self.capacitance_measurement_frequency_hz <= 0)):
            raise ValueError("capacitance measurement frequency must be positive or None")


LEE_2024_TFLN_SIN = PublishedEOReference(
    name="Lee et al. 2024 hybrid TFLN-SiN EO phase modulator",
    source_doi="10.1364/OE.518961",
    interaction_length_m=15.6e-3,
    capacitance_per_phase_modulator_f=0.98e-12,
    capacitance_measurement_method="HIOKI IM3536 LCR meter",
    capacitance_terminal_definition="not specified in the paper",
    capacitance_measurement_frequency_hz=None,
    half_wave_voltage_v=3.64,
    reported_energy_per_pi_j=3.2e-12,
    estimated_bandwidth_hz=1.2e9,
    measured_test_bandwidth_hz=2.9e9,
    measured_test_length_m=9.4e-3,
    electrode_configuration="push-pull MZI characterization; GSG electrode probe",
)


def reported_style_sinusoidal_energy_j(capacitance_f: float,
                                        peak_half_wave_voltage_v: float) -> float:
    """Paper's mean capacitor-energy expression: C*Vpi^2/4."""
    if not math.isfinite(capacitance_f) or capacitance_f < 0:
        raise ValueError("capacitance must be finite and nonnegative")
    if not math.isfinite(peak_half_wave_voltage_v) or peak_half_wave_voltage_v < 0:
        raise ValueError("voltage must be finite and nonnegative")
    return capacitance_f * peak_half_wave_voltage_v**2 / 4.0


def conditional_ideal_quadrature_frequency_hz(
        inductance_h: float,
        node_shunt_capacitance_f: float,
        assumed_differential_eo_capacitance_f: float) -> float:
    """Ideal four-ring frequency, conditional on a verified differential C.

    f_q = (1/2π) sqrt(2 / (L * (C_g + 2*C_EO))).

    L is each equal ring branch inductance; C_g is equal node shunt
    capacitance per node. C_EO must be the actual measured/extracted
    two-terminal capacitance across each of P0-P2 and P1-P3. The
    published Lee et al. 0.98 pF value is NOT known to have this
    terminal definition and must not be passed without verification.
    """
    values = (inductance_h, node_shunt_capacitance_f,
              assumed_differential_eo_capacitance_f)
    if any(not math.isfinite(x) for x in values):
        raise ValueError("all inputs must be finite")
    if inductance_h <= 0:
        raise ValueError("inductance_h must be positive")
    if node_shunt_capacitance_f < 0:
        raise ValueError("node_shunt_capacitance_f must be nonnegative")
    if assumed_differential_eo_capacitance_f <= 0:
        raise ValueError("assumed differential EO capacitance must be positive")
    c_mode = node_shunt_capacitance_f + 2*assumed_differential_eo_capacitance_f
    return math.sqrt(2/(inductance_h*c_mode))/(2*math.pi)


def conditional_required_ring_inductance_h(
        target_frequency_hz: float,
        node_shunt_capacitance_f: float,
        assumed_differential_eo_capacitance_f: float) -> float:
    """Ideal L sizing, conditional on the true differential EO port C."""
    values = (target_frequency_hz, node_shunt_capacitance_f,
              assumed_differential_eo_capacitance_f)
    if any(not math.isfinite(x) for x in values):
        raise ValueError("all inputs must be finite")
    if target_frequency_hz <= 0:
        raise ValueError("target_frequency_hz must be positive")
    if node_shunt_capacitance_f < 0:
        raise ValueError("node_shunt_capacitance_f must be nonnegative")
    if assumed_differential_eo_capacitance_f <= 0:
        raise ValueError("assumed differential EO capacitance must be positive")
    omega = 2*math.pi*target_frequency_hz
    c_mode = node_shunt_capacitance_f + 2*assumed_differential_eo_capacitance_f
    return 2/(omega**2*c_mode)
