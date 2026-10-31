import EIS.AdiaIO
import EIS.MZI_EO
import EIS.ResPwr


/-!
# EIS-COPOWER-001 — Integrated electrical/optical power-domain contract

Composes the adiabatic electrical controller, EO driver, optical path, and
measurement/readout domains. Electrical and optical energies are not added as if
they were the same boundary: laser wall-plug energy belongs in the electrical
ledger, while optical launch/transmission/detection are tracked separately.
-/

namespace EIS.CoPower

open EIS.AdiaIO
open EIS.MZI_EO

structure CoDesignTimingWindow where
  commandReadyS : ℝ
  modulatorSettleS : ℝ
  opticalSampleS : ℝ
  controllerHoldEndsS : ℝ
  command_nonneg : 0 ≤ commandReadyS
  settle_nonneg : 0 ≤ modulatorSettleS
  sample_nonneg : 0 ≤ opticalSampleS
  hold_nonneg : 0 ≤ controllerHoldEndsS
  modulator_settles_before_sample : commandReadyS + modulatorSettleS ≤ opticalSampleS
  sample_inside_controller_hold : opticalSampleS ≤ controllerHoldEndsS

/-- Electrical wall-plug ledger; the EO return credit is counted exactly once. -/
structure SystemElectricalEnergyLedger where
  controllerLogicJ : ℝ
  controllerPowerClockGenerationJ : ℝ
  controllerPowerClockDistributionJ : ℝ
  modulatorGrossDrawJ : ℝ
  modulatorReturnedToSupplyJ : ℝ
  resonantReservoirReplenishmentWallPlugJ : ℝ
  resonantReservoirCoolingWallPlugJ : ℝ
  opticalSourceWallPlugJ : ℝ
  detectorAndReadoutJ : ℝ
  conversionAndDataMovementJ : ℝ
  controller_nonneg : 0 ≤ controllerLogicJ
  power_clock_gen_nonneg : 0 ≤ controllerPowerClockGenerationJ
  power_clock_dist_nonneg : 0 ≤ controllerPowerClockDistributionJ
  modulator_gross_nonneg : 0 ≤ modulatorGrossDrawJ
  modulator_return_nonneg : 0 ≤ modulatorReturnedToSupplyJ
  modulator_return_le_gross : modulatorReturnedToSupplyJ ≤ modulatorGrossDrawJ
  reservoir_replenishment_nonneg : 0 ≤ resonantReservoirReplenishmentWallPlugJ
  reservoir_cooling_nonneg : 0 ≤ resonantReservoirCoolingWallPlugJ
  source_nonneg : 0 ≤ opticalSourceWallPlugJ
  detector_nonneg : 0 ≤ detectorAndReadoutJ
  conversion_nonneg : 0 ≤ conversionAndDataMovementJ

def netModulatorEnergyJ (e : SystemElectricalEnergyLedger) : ℝ :=
  e.modulatorGrossDrawJ - e.modulatorReturnedToSupplyJ

def totalSystemElectricalEnergyJ (e : SystemElectricalEnergyLedger) : ℝ :=
  e.controllerLogicJ + e.controllerPowerClockGenerationJ +
  e.controllerPowerClockDistributionJ + netModulatorEnergyJ e +
  e.resonantReservoirReplenishmentWallPlugJ +
  e.resonantReservoirCoolingWallPlugJ + e.opticalSourceWallPlugJ + e.detectorAndReadoutJ +
  e.conversionAndDataMovementJ

theorem net_modulator_energy_nonneg (e : SystemElectricalEnergyLedger) :
    0 ≤ netModulatorEnergyJ e := by
  unfold netModulatorEnergyJ
  linarith [e.modulator_return_le_gross]

theorem total_system_electrical_energy_nonneg (e : SystemElectricalEnergyLedger) :
    0 ≤ totalSystemElectricalEnergyJ e := by
  unfold totalSystemElectricalEnergyJ
  nlinarith [e.controller_nonneg, e.power_clock_gen_nonneg,
    e.power_clock_dist_nonneg, net_modulator_energy_nonneg e,
    e.reservoir_replenishment_nonneg, e.reservoir_cooling_nonneg,
    e.source_nonneg, e.detector_nonneg, e.conversion_nonneg]

/-- Cross-domain contract with linked driver flow and system energy ledger. -/
structure CoPowerContract where
  controller : AdiabaticIOContract
  modulator : PhaseShifterProfile
  opticalPath : OpticalPathBudget
  timing : CoDesignTimingWindow
  modulatorFlow : ElectricalEnergyFlow
  electricalLedger : SystemElectricalEnergyLedger
  ledger_matches_gross : electricalLedger.modulatorGrossDrawJ =
    modulatorFlow.grossDrawFromSupplyJ
  ledger_matches_return : electricalLedger.modulatorReturnedToSupplyJ =
    modulatorFlow.returnedToSupplyJ
  no_unproven_recovery_credit :
    ¬ recoveryEligible modulator.kind modulator.returnTopology modulator.returnEvidence →
      modulatorFlow.returnedToSupplyJ = 0
  resonantDomain : Option EIS.ResPwr.ResonantPowerDomainContract
  resonant_modulator_matches_system :
    match resonantDomain with
    | none => True
    | some d => d.modulator = modulator
  resonant_replenishment_bound_to_ledger :
    match resonantDomain with
    | none => electricalLedger.resonantReservoirReplenishmentWallPlugJ = 0
    | some d => electricalLedger.resonantReservoirReplenishmentWallPlugJ =
        EIS.ResPwr.resonantDomainWallPlugEnergyJ d
  resonant_cooling_bound_to_ledger :
    match resonantDomain with
    | none => electricalLedger.resonantReservoirCoolingWallPlugJ = 0
    | some d => electricalLedger.resonantReservoirCoolingWallPlugJ =
        EIS.ResPwr.resonantDomainCoolingEnergyJ d

theorem coPower_net_energy_nonneg (c : CoPowerContract) :
    0 ≤ totalSystemElectricalEnergyJ c.electricalLedger :=
  total_system_electrical_energy_nonneg c.electricalLedger

theorem modulator_return_credit_bounded (c : CoPowerContract) :
    c.electricalLedger.modulatorReturnedToSupplyJ ≤
      c.electricalLedger.modulatorGrossDrawJ :=
  c.electricalLedger.modulator_return_le_gross

end EIS.CoPower
