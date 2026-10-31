import Mathlib

/-!
# EIS-MZI-EO-001 — MZI electro-optic drive and return-path contract

A ground/reference connection is distinguished from a regenerative energy-return
path. A common ground conductor closes a current loop and establishes a voltage
reference; by itself it does not demonstrate that a driver or supply can accept
returned charge/energy.

Tian et al. (PhotoniX 6, 45 (2025)) report TiN resistive thermo-optic heaters,
individual heater drive traces, and shared ground connections for phase shifters
in a column. This maps to thermoOpticResistive plus sharedGroundReturn below. The
reported ground pad is not evidence of a regenerative supply rail.

The RC ramp-loss expression is an idealized lumped-capacitor/series-resistance
model, not a foundry characterization.
-/

namespace EIS.MZI_EO

inductive PhaseShifterKind where
  | lumpedCapacitiveEO
  | terminatedTravelingWaveEO
  | thermoOpticResistive
  deriving DecidableEq, Repr

inductive ReturnTopology where
  | groundReferenceOnly
  | sharedGroundReturn
  | dissipativeTermination
  | regenerativeSupplyRail
  | resonantRecoveryReservoir
  deriving DecidableEq, Repr

/-- A shared ground may be part of a regenerative loop if the other facts are proven. -/
def ReturnTopology.maySupportRecovery : ReturnTopology → Prop
  | .groundReferenceOnly => False
  | .sharedGroundReturn => True
  | .dissipativeTermination => False
  | .regenerativeSupplyRail => True
  | .resonantRecoveryReservoir => True

inductive RecoveryEvidenceGrade where
  | analyticModel
  | circuitSimulation
  | measuredHardware
  deriving DecidableEq, Repr

/-
A ground pad is recorded independently from the properties needed to claim
energy recovery. Option Bool preserves UNKNOWN rather than treating missing
schematic/measurement evidence as PASS or FAIL.
-/
structure ReturnPathEvidence where
  groundReferencePresent : Bool
  closedLoopToSupply : Option Bool
  driverBidirectional : Option Bool
  supplyCanAbsorbEnergy : Option Bool
  energyBalanceVerified : Option Bool
  energyBalanceGrade : Option RecoveryEvidenceGrade
  deriving Repr

def ReturnPathEvidence.recoveryPathProven (r : ReturnPathEvidence) : Prop :=
  r.closedLoopToSupply = some true ∧
  r.driverBidirectional = some true ∧
  r.supplyCanAbsorbEnergy = some true ∧
  r.energyBalanceVerified = some true ∧
  r.energyBalanceGrade = some .measuredHardware

/-- A measured return is eligible only for a lumped capacitive EO load. -/
def recoveryEligible (kind : PhaseShifterKind) (topology : ReturnTopology)
    (returnEvidence : ReturnPathEvidence) : Prop :=
  kind = .lumpedCapacitiveEO ∧ topology.maySupportRecovery ∧
    returnEvidence.recoveryPathProven

theorem ground_reference_alone_does_not_establish_recovery
    (r : ReturnPathEvidence)
    (_hGround : r.groundReferencePresent = true)
    (hUnknownLoop : r.closedLoopToSupply = none) :
    ¬ r.recoveryPathProven := by
  simp [ReturnPathEvidence.recoveryPathProven, hUnknownLoop]

theorem shared_ground_without_supply_loop_cannot_earn_recovery_credit
    (r : ReturnPathEvidence)
    (_hGround : r.groundReferencePresent = true)
    (hUnknownLoop : r.closedLoopToSupply = none) :
    ¬ (r.recoveryPathProven ∧ ReturnTopology.maySupportRecovery .sharedGroundReturn) := by
  simp [ReturnPathEvidence.recoveryPathProven, ReturnTopology.maySupportRecovery,
    hUnknownLoop]

/-- Tian et al. report a shared ground pad; regenerative properties are unreported. -/
def tianSharedGroundEvidence : ReturnPathEvidence :=
  { groundReferencePresent := true
    closedLoopToSupply := none
    driverBidirectional := none
    supplyCanAbsorbEnergy := none
    energyBalanceVerified := none
    energyBalanceGrade := none }

theorem tian_shared_ground_heater_not_recovery_eligible :
    ¬ recoveryEligible .thermoOpticResistive .sharedGroundReturn tianSharedGroundEvidence := by
  simp [recoveryEligible, tianSharedGroundEvidence,
    ReturnTopology.maySupportRecovery, ReturnPathEvidence.recoveryPathProven]

/-- First-order resistive loss for one linear ramp of an ideal lumped capacitor. -/
def linearRampDissipationJ (R C V T : ℝ) : ℝ :=
  R * C ^ 2 * V ^ 2 / T

/-- Ideal electrostatic energy stored by capacitance C at voltage swing V. -/
def capacitorStoredEnergyJ (C V : ℝ) : ℝ :=
  C * V ^ 2 / 2

theorem linearRampDissipation_nonneg
    {R C V T : ℝ} (hR : 0 ≤ R) (hC : 0 ≤ C) (hV : 0 ≤ V) (hT : 0 < T) :
    0 ≤ linearRampDissipationJ R C V T := by
  unfold linearRampDissipationJ
  positivity

/--
If ramp duration is at least 2RC, this simple model dissipates no more than the
ideal stored capacitor energy during that one ramp.
-/
theorem ramp_loss_le_stored_energy
    {R C V T : ℝ}
    (hR : 0 ≤ R) (hC : 0 ≤ C) (hV : 0 ≤ V) (hT : 0 < T)
    (hSlow : 2 * R * C ≤ T) :
    linearRampDissipationJ R C V T ≤ capacitorStoredEnergyJ C V := by
  unfold linearRampDissipationJ capacitorStoredEnergyJ
  have hmul := mul_le_mul_of_nonneg_right hSlow (mul_nonneg hC (sq_nonneg V))
  rw [div_le_iff₀ hT]
  nlinarith [hmul]

/--
Operating-point parameters. The RC expression applies only when this effective
lumped capacitance and series resistance are a valid equivalent circuit.
-/
structure PhaseShifterProfile where
  kind : PhaseShifterKind
  returnTopology : ReturnTopology
  returnEvidence : ReturnPathEvidence
  effectiveCapacitanceF : ℝ
  seriesResistanceOhm : ℝ
  voltageSwingV : ℝ
  riseTimeS : ℝ
  fallTimeS : ℝ
  holdTimeS : ℝ
  leakagePowerW : ℝ
  bandwidthHz : ℝ
  settlingTimeS : ℝ
  phaseShiftRad : ℝ
  insertionLossDb : ℝ
  capacitance_nonneg : 0 ≤ effectiveCapacitanceF
  resistance_nonneg : 0 ≤ seriesResistanceOhm
  swing_nonneg : 0 ≤ voltageSwingV
  rise_pos : 0 < riseTimeS
  fall_pos : 0 < fallTimeS
  hold_nonneg : 0 ≤ holdTimeS
  leakage_nonneg : 0 ≤ leakagePowerW
  bandwidth_nonneg : 0 ≤ bandwidthHz
  settle_nonneg : 0 ≤ settlingTimeS
  insertion_loss_nonneg : 0 ≤ insertionLossDb

def riseLossJ (m : PhaseShifterProfile) : ℝ :=
  linearRampDissipationJ m.seriesResistanceOhm m.effectiveCapacitanceF
    m.voltageSwingV m.riseTimeS

def fallLossJ (m : PhaseShifterProfile) : ℝ :=
  linearRampDissipationJ m.seriesResistanceOhm m.effectiveCapacitanceF
    m.voltageSwingV m.fallTimeS

def idealStoredEnergyJ (m : PhaseShifterProfile) : ℝ :=
  capacitorStoredEnergyJ m.effectiveCapacitanceF m.voltageSwingV

def leakageEnergyJ (m : PhaseShifterProfile) : ℝ :=
  m.leakagePowerW * m.holdTimeS

def modeledTwoRampResistiveLossJ (m : PhaseShifterProfile) : ℝ :=
  riseLossJ m + fallLossJ m

/-- Per-cycle energy flow; the balance prevents unearned recovery credits. -/
structure ElectricalEnergyFlow where
  grossDrawFromSupplyJ : ℝ
  returnedToSupplyJ : ℝ
  dissipatedJ : ℝ
  retainedAtCycleEndJ : ℝ
  gross_nonneg : 0 ≤ grossDrawFromSupplyJ
  returned_nonneg : 0 ≤ returnedToSupplyJ
  dissipated_nonneg : 0 ≤ dissipatedJ
  retained_nonneg : 0 ≤ retainedAtCycleEndJ
  returned_le_gross : returnedToSupplyJ ≤ grossDrawFromSupplyJ
  energy_balance : grossDrawFromSupplyJ =
    returnedToSupplyJ + dissipatedJ + retainedAtCycleEndJ

def netSupplyEnergyJ (f : ElectricalEnergyFlow) : ℝ :=
  f.grossDrawFromSupplyJ - f.returnedToSupplyJ

theorem net_supply_energy_equals_loss_plus_retained (f : ElectricalEnergyFlow) :
    netSupplyEnergyJ f = f.dissipatedJ + f.retainedAtCycleEndJ := by
  unfold netSupplyEnergyJ
  linarith [f.energy_balance]

theorem net_supply_energy_nonneg (f : ElectricalEnergyFlow) :
    0 ≤ netSupplyEnergyJ f := by
  rw [net_supply_energy_equals_loss_plus_retained]
  positivity

/-- A recovery credit requires an eligible device/return path and positive returned energy. -/
structure EnergyRecoveryEvidence where
  device : PhaseShifterProfile
  flow : ElectricalEnergyFlow
  eligible : recoveryEligible device.kind device.returnTopology device.returnEvidence
  returned_positive : 0 < flow.returnedToSupplyJ

/-- Optical energy is tracked separately from electrical driver energy. -/
structure OpticalPathBudget where
  inputOpticalEnergyJ : ℝ
  pathTransmission : ℝ
  detectorEfficiency : ℝ
  input_nonneg : 0 ≤ inputOpticalEnergyJ
  transmission_nonneg : 0 ≤ pathTransmission
  transmission_le_one : pathTransmission ≤ 1
  detector_nonneg : 0 ≤ detectorEfficiency
  detector_le_one : detectorEfficiency ≤ 1

def opticalOutputEnergyJ (p : OpticalPathBudget) : ℝ :=
  p.inputOpticalEnergyJ * p.pathTransmission

def opticalPathLossJ (p : OpticalPathBudget) : ℝ :=
  p.inputOpticalEnergyJ * (1 - p.pathTransmission)

def opticalDetectedEnergyJ (p : OpticalPathBudget) : ℝ :=
  opticalOutputEnergyJ p * p.detectorEfficiency

theorem optical_energy_balance (p : OpticalPathBudget) :
    opticalOutputEnergyJ p + opticalPathLossJ p = p.inputOpticalEnergyJ := by
  unfold opticalOutputEnergyJ opticalPathLossJ
  ring

theorem optical_path_loss_nonneg (p : OpticalPathBudget) :
    0 ≤ opticalPathLossJ p := by
  unfold opticalPathLossJ
  apply mul_nonneg p.input_nonneg
  linarith [p.transmission_le_one]

theorem optical_detected_energy_nonneg (p : OpticalPathBudget) :
    0 ≤ opticalDetectedEnergyJ p := by
  unfold opticalDetectedEnergyJ opticalOutputEnergyJ
  exact mul_nonneg (mul_nonneg p.input_nonneg p.transmission_nonneg) p.detector_nonneg

end EIS.MZI_EO
