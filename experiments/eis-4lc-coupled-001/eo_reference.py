"""Published hybrid SiN/TFLN differential EO load reference.

Source: W.-B. Lee et al., Optics Express 32(6), 9171-9183 (2024),
DOI 10.1364/OE.518961. This is a measured external device reference,
not EIS PDK data and not a measured room-temperature 4LC implementation.

The ideal 4LC sizing relation assumes equal ring inductors, equal node
shunt capacitances, and two matched differential EO capacitors across
opposite node pairs P0-P2 and P1-P3. It is a modal sizing equation, not
a circuit/EM simulation.
"""
from __future__ import annotations

from dataclasses import dataclass
import math


@dataclass(frozen=True)
class PublishedEOReference:
    name: str
    source_doi: str
    interaction_length_m: float
    differential_capacitance_f: float
    half_wave_voltage_v: float
    reported_energy_per_pi_j: float
    estimated_bandwidth_hz: float
    measured_test_bandwidth_hz: float
    measured_test_length_m: float
    electrode_configuration: str

    def validate(self) -> None:
        positive = {
            "interaction_length_m": self.interaction_length_m,
            "differential_capacitance_f": self.differential_capacitance_f,
            "half_wave_voltage_v": self.half_wave_voltage_v,
            "reported_energy_per_pi_j": self.reported_energy_per_pi_j,
            "estimated_bandwidth_hz": self.estimated_bandwidth_hz,
            "measured_test_bandwidth_hz": self.measured_test_bandwidth_hz,
            "measured_test_length_m": self.measured_test_length_m,
        }
        for name, value in positive.items():
            if not math.isfinite(value) or value <= 0:
                raise ValueError(f"{name} must be finite and positive")


LEE_2024_TFLN_SIN = PublishedEOReference(
    name="Lee et al. 2024 hybrid TFLN-SiN push-pull EO phase shifter",
    source_doi="10.1364/OE.518961",
    interaction_length_m=15.6e-3,
    differential_capacitance_f=0.98e-12,
    half_wave_voltage_v=3.64,
    reported_energy_per_pi_j=3.2e-12,
    estimated_bandwidth_hz=1.2e9,
    measured_test_bandwidth_hz=2.9e9,
    measured_test_length_m=9.4e-3,
    electrode_configuration="push-pull MZI; differential two-terminal EO load",
)


def reported_style_sinusoidal_energy_j(capacitance_f: float,
                                        peak_half_wave_voltage_v: float) -> float:
    """Mean electric energy of a sinusoidal capacitor voltage: C*Vpk^2/4."""
    if capacitance_f < 0 or peak_half_wave_voltage_v < 0:
        raise ValueError("capacitance and voltage must be nonnegative")
    return capacitance_f * peak_half_wave_voltage_v**2 / 4.0


def ideal_quadrature_frequency_hz(inductance_h: float,
                                  node_shunt_capacitance_f: float,
                                  differential_eo_capacitance_f: float) -> float:
    """Ideal 4LC quadrature frequency with two matched diagonal EO capacitors.

    f_q = (1/2π) sqrt(2 / (L * (C_g + 2*C_EO)))

    L is each equal ring branch inductance. C_g is each node's equal
    ground-referenced capacitance. C_EO is the differential capacitance
    across each of P0-P2 and P1-P3.
    """
    if not math.isfinite(inductance_h) or inductance_h <= 0:
        raise ValueError("inductance_h must be finite and positive")
    if (not math.isfinite(node_shunt_capacitance_f)
            or node_shunt_capacitance_f < 0):
        raise ValueError("node_shunt_capacitance_f must be finite and nonnegative")
    if (not math.isfinite(differential_eo_capacitance_f)
            or differential_eo_capacitance_f <= 0):
        raise ValueError("differential_eo_capacitance_f must be finite and positive")
    c_mode = node_shunt_capacitance_f + 2*differential_eo_capacitance_f
    return math.sqrt(2/(inductance_h*c_mode))/(2*math.pi)


def required_ring_inductance_h(target_frequency_hz: float,
                               node_shunt_capacitance_f: float,
                               differential_eo_capacitance_f: float) -> float:
    """Ideal equal branch L required for the requested quadrature frequency."""
    if not math.isfinite(target_frequency_hz) or target_frequency_hz <= 0:
        raise ValueError("target_frequency_hz must be finite and positive")
    if (not math.isfinite(node_shunt_capacitance_f)
            or node_shunt_capacitance_f < 0):
        raise ValueError("node_shunt_capacitance_f must be finite and nonnegative")
    if (not math.isfinite(differential_eo_capacitance_f)
            or differential_eo_capacitance_f <= 0):
        raise ValueError("differential_eo_capacitance_f must be finite and positive")
    omega = 2*math.pi*target_frequency_hz
    c_mode = node_shunt_capacitance_f + 2*differential_eo_capacitance_f
    return 2/(omega**2*c_mode)


def matched_pair_mean_eo_energy_j(case: PublishedEOReference) -> float:
    """Average electric energy in two identical diagonal EO loads at Vπ peak."""
    case.validate()
    return 2*reported_style_sinusoidal_energy_j(
        case.differential_capacitance_f, case.half_wave_voltage_v
    )
