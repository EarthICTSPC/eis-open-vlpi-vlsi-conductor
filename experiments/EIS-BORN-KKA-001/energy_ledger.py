"""Explicit wall-plug energy accounting for EIS-BORN-KKA-001.

Values are supplied by a future matched measurement or a clearly labelled
simulation. This module contains no default device or energy values.
"""
from __future__ import annotations

from dataclasses import dataclass
import math
from collections.abc import Mapping


ENERGY_COMPONENTS = frozenset(
    {
        "laser_wall_plug_j",
        "modulator_and_driver_j",
        "detector_readout_and_conversion_j",
        "electronic_feedback_normalization_control_j",
        "phase_setting_and_calibration_j",
        "memory_j",
        "data_movement_and_interconnect_j",
        "other_compute_and_control_j",
        "cooling_j",
        "power_delivery_overhead_j",
    }
)


@dataclass(frozen=True)
class EnergyLedger:
    """One run's energy and accepted-output record.

    optical_loss_fraction is metadata, not an additive energy component:
    the electrical cost of replacing lost optical power is already reflected
    in measured laser_wall_plug_j. This prevents double counting.
    """

    workload_id: str
    acceptance_contract_id: str
    accepted_useful_transformations: int
    components_j: Mapping[str, float]
    optical_loss_fraction: float | None = None

    def __post_init__(self) -> None:
        if not self.workload_id.strip() or not self.acceptance_contract_id.strip():
            raise ValueError("workload and acceptance contract identifiers are required")
        if self.accepted_useful_transformations <= 0:
            raise ValueError("accepted useful transformations must be positive")
        keys = set(self.components_j)
        missing = ENERGY_COMPONENTS - keys
        extra = keys - ENERGY_COMPONENTS
        if missing or extra:
            raise ValueError(f"energy ledger terms mismatch; missing={sorted(missing)}, extra={sorted(extra)}")
        for name, value in self.components_j.items():
            if not math.isfinite(value) or value < 0.0:
                raise ValueError(f"{name} must be finite and nonnegative")
        if self.optical_loss_fraction is not None:
            if not math.isfinite(self.optical_loss_fraction) or not 0.0 <= self.optical_loss_fraction <= 1.0:
                raise ValueError("optical_loss_fraction must be in [0, 1]")

    @property
    def total_wall_plug_j(self) -> float:
        return math.fsum(self.components_j.values())

    @property
    def joules_per_accepted_transformation(self) -> float:
        return self.total_wall_plug_j / self.accepted_useful_transformations


@dataclass(frozen=True)
class MatchedComparison:
    baseline_j_per_accepted: float
    candidate_j_per_accepted: float

    @property
    def fractional_energy_savings(self) -> float:
        return 1.0 - self.candidate_j_per_accepted / self.baseline_j_per_accepted


def compare_matched_runs(
    baseline: EnergyLedger, candidate: EnergyLedger
) -> MatchedComparison:
    """Compare only runs with identical workload and acceptance contracts."""
    if baseline.workload_id != candidate.workload_id:
        raise ValueError("baseline and candidate workload_id must match")
    if baseline.acceptance_contract_id != candidate.acceptance_contract_id:
        raise ValueError("baseline and candidate acceptance_contract_id must match")
    baseline_energy = baseline.joules_per_accepted_transformation
    candidate_energy = candidate.joules_per_accepted_transformation
    if baseline_energy <= 0.0:
        raise ValueError("baseline energy per accepted transformation must be positive")
    return MatchedComparison(baseline_energy, candidate_energy)
