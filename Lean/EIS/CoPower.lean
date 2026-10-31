import EIS.AdiaIO
import EIS.MZI_EO

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
  opticalSourceWallPlugJ : ℝ
  detectorAndReadoutJ : ℝ
  conversionAndDataMovementJ : ℝ
  controller_nonneg : 0 ≤ controllerLogicJ
  power_clock_gen_nonneg : 0 ≤ controllerPowerClockGenerationJ
  power_clock_dist_nonneg : 0 ≤ controllerPowerClockDistributionJ
  modulator_gross_nonneg : 0 ≤ modulatorGrossDrawJ
  modulator_return_nonneg : 0 ≤ modulatorReturnedToSupplyJ
  modulator_return_le_gross : modulatorReturnedToSupplyJ ≤ modulatorGrossDrawJ
  source_nonneg : 0 ≤ opticalSourceWallPlugJ
  detector_nonneg : 0 ≤ detectorAndReadoutJ
  conversion_nonneg : 0 ≤ conversionAndDataMovementJ

def netModulatorEnergyJ (e : SystemElectricalEnergyLedger) : ℝ :=
  e.modulatorGrossDrawJ - e.modulatorReturnedToSupplyJ

def totalSystemElectricalEnergyJ (e : SystemElectricalEnergyLedger) : ℝ :=
  e.controllerLogicJ + e.controllerPowerClockGenerationJ +
  e.controllerPowerClockDistributionJ + netModulatorEnergyJ e +
  e.opticalSourceWallPlugJ + e.detectorAndReadoutJ +
  e.conversionAndDataMovementJ

theorem net_modulator_energy_nonneg (e : SystemElectricalEnergyLedger) :
    0 ≤ netModulatorEnergyJ e := by
  unfold netModulatorEnergyJ
  linarith [e.modulator_return_le_gross]

theorem total_system_electrical_energy_nonneg (e : SystemElectricalEnergyLedger) :
    0 ≤ totalSystemElectricalEnergyJ e := by
  unfold totalSystemElectricalEnergyJ
  positivity

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
  modulator_energy_balance : modulatorFlow.energy_balance
  no_unproven_recovery_credit :
    ¬ recoveryEligible modulator.kind modulator.returnEvidence →
      modulatorFlow.returnedToSupplyJ = 0

theorem coPower_net_energy_nonneg (c : CoPowerContract) :
    0 ≤ totalSystemElectricalEnergyJ c.electricalLedger :=
  total_system_electrical_energy_nonneg c.electricalLedger

theorem modulator_return_credit_bounded (c : CoPowerContract) :
    c.electricalLedger.modulatorReturnedToSupplyJ ≤
      c.electricalLedger.modulatorGrossDrawJ :=
  c.electricalLedger.modulator_return_le_gross

end EIS.CoPower
