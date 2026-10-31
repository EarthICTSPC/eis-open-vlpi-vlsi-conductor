import Mathlib
import EIS.MZI_EO

/-!
# EIS-4LC-COUPLED-001 — DeBenedictis four-node resonant ring

Source topology: DeBenedictis, ZF013 (2025), Fig. 4a:
four inductors form a closed ring P0-P1-P2-P3-P0, with one capacitor
from each phase node to ground. Fig. 4b tiles these quad resonators in a
checkerboard and changes the boundary inductors.

This is an ideal lumped ring model plus explicit load ports. It does not
silently treat the paper's simulated HKI implementation as room-temperature
hardware, nor does it assume a measured SiN/TFLN EO equivalent circuit.
-/

namespace EIS.FourLC

noncomputable section

open EIS.MZI_EO

/-- Four node/edge quantities in cyclic order 0,1,2,3. -/
structure Four where
  x0 : ℝ
  x1 : ℝ
  x2 : ℝ
  x3 : ℝ

def fourZero : Four := ⟨0, 0, 0, 0⟩

def fourScale (k : ℝ) (x : Four) : Four :=
  ⟨k * x.x0, k * x.x1, k * x.x2, k * x.x3⟩

/--
The graph Laplacian of the four-node ring. Its four edges are
L0:P0-P1, L1:P1-P2, L2:P2-P3, L3:P3-P0.
-/
def ringLaplacian (x : Four) : Four :=
  ⟨2 * x.x0 - x.x1 - x.x3,
   2 * x.x1 - x.x2 - x.x0,
   2 * x.x2 - x.x3 - x.x1,
   2 * x.x3 - x.x0 - x.x2⟩

/-- Uniform common-mode vector; its ideal ring eigenvalue is zero. -/
def commonMode : Four := ⟨1, 1, 1, 1⟩

/-- Cosine member of the degenerate quadrature-mode pair. -/
def quadratureCosMode : Four := ⟨1, 0, -1, 0⟩

/-- Sine member of the degenerate quadrature-mode pair. -/
def quadratureSinMode : Four := ⟨0, 1, 0, -1⟩

/-- Alternating mode P0,-P1,P2,-P3. -/
def alternatingMode : Four := ⟨1, -1, 1, -1⟩

theorem common_mode_eigenvalue_zero :
    ringLaplacian commonMode = fourScale 0 commonMode := by
  ext <;> norm_num [ringLaplacian, commonMode, fourScale]

theorem quadrature_cos_mode_eigenvalue_two :
    ringLaplacian quadratureCosMode = fourScale 2 quadratureCosMode := by
  ext <;> norm_num [ringLaplacian, quadratureCosMode, fourScale]

theorem quadrature_sin_mode_eigenvalue_two :
    ringLaplacian quadratureSinMode = fourScale 2 quadratureSinMode := by
  ext <;> norm_num [ringLaplacian, quadratureSinMode, fourScale]

theorem alternating_mode_eigenvalue_four :
    ringLaplacian alternatingMode = fourScale 4 alternatingMode := by
  ext <;> norm_num [ringLaplacian, alternatingMode, fourScale]

/-- Four ideal ring modes and their graph-Laplacian eigenvalues. -/
inductive RingMode where
  | common
  | quadratureCos
  | quadratureSin
  | alternating
  deriving DecidableEq, Repr

def modeEigenvalue : RingMode → ℝ
  | .common => 0
  | .quadratureCos => 2
  | .quadratureSin => 2
  | .alternating => 4

/--
For an equal-L, equal-C, lossless ring, a mode with graph eigenvalue λ has
ω²=λ/(LC). The quadrature pair is degenerate; its two spatial basis vectors
can be combined with temporal sine/cosine to produce four phase-shifted nodes.
-/
def idealModeAngularFrequencyRadPerS
    (inductanceH capacitanceF eigenvalue : ℝ) : ℝ :=
  Real.sqrt (eigenvalue / (inductanceH * capacitanceF))

def quadratureAngularFrequencyRadPerS (inductanceH capacitanceF : ℝ) : ℝ :=
  idealModeAngularFrequencyRadPerS inductanceH capacitanceF 2

def alternatingAngularFrequencyRadPerS (inductanceH capacitanceF : ℝ) : ℝ :=
  idealModeAngularFrequencyRadPerS inductanceH capacitanceF 4

theorem quadrature_frequency_positive
    {L C : ℝ} (hL : 0 < L) (hC : 0 < C) :
    0 < quadratureAngularFrequencyRadPerS L C := by
  unfold quadratureAngularFrequencyRadPerS idealModeAngularFrequencyRadPerS
  apply Real.sqrt_pos.2
  exact div_pos (by norm_num) (mul_pos hL hC)

theorem alternating_frequency_positive
    {L C : ℝ} (hL : 0 < L) (hC : 0 < C) :
    0 < alternatingAngularFrequencyRadPerS L C := by
  unfold alternatingAngularFrequencyRadPerS idealModeAngularFrequencyRadPerS
  apply Real.sqrt_pos.2
  exact div_pos (by norm_num) (mul_pos hL hC)

/-- Differential channel between opposite phase nodes P0 and P2. -/
def differentialP0P2 (v : Four) : ℝ := v.x0 - v.x2

/-- Differential channel between opposite phase nodes P1 and P3. -/
def differentialP1P3 (v : Four) : ℝ := v.x1 - v.x3

theorem quadrature_cos_has_P0P2_differential :
    differentialP0P2 quadratureCosMode = 2 := by
  rfl

theorem quadrature_cos_has_zero_P1P3_differential :
    differentialP1P3 quadratureCosMode = 0 := by
  rfl

theorem quadrature_sin_has_zero_P0P2_differential :
    differentialP0P2 quadratureSinMode = 0 := by
  rfl

theorem quadrature_sin_has_P1P3_differential :
    differentialP1P3 quadratureSinMode = 2 := by
  rfl

/-- Whether the EO port is a DC phase setting or a periodic data waveform. -/
inductive EOControlRegime where
  | staticPhaseHold
  | periodicDataModulation
  deriving DecidableEq, Repr

/--
A direct quadrature sinusoid is a periodic drive, not a DC hold voltage.
Static phase settings require an isolation/sample-hold or another explicit
bias-retention interface; it is not silently inferred from resonance.
-/
inductive EOOutputInterface where
  | directDifferentialP0P2
  | directDifferentialP1P3
  | bufferedSampleHold
  | customCharacterizedInterface
  deriving DecidableEq, Repr

def eoInterfaceCompatible
    (regime : EOControlRegime) (interface : EOOutputInterface) : Prop :=
  match regime, interface with
  | .periodicDataModulation, _ => True
  | .staticPhaseHold, .bufferedSampleHold => True
  | .staticPhaseHold, .customCharacterizedInterface => True
  | .staticPhaseHold, .directDifferentialP0P2 => False
  | .staticPhaseHold, .directDifferentialP1P3 => False

theorem directQuadratureIsNotAStaticHold :
    ¬ eoInterfaceCompatible .staticPhaseHold .directDifferentialP0P2 := by
  simp [eoInterfaceCompatible]

/-- Four branch inductances L0..L3, each joining adjacent ring nodes. -/
structure FourLCParameters where
  inductanceH : Four
  branchResistanceOhm : Four
  shuntCapacitanceF : Four
  inductance_positive :
    0 < inductanceH.x0 ∧ 0 < inductanceH.x1 ∧
    0 < inductanceH.x2 ∧ 0 < inductanceH.x3
  resistance_nonnegative :
    0 ≤ branchResistanceOhm.x0 ∧ 0 ≤ branchResistanceOhm.x1 ∧
    0 ≤ branchResistanceOhm.x2 ∧ 0 ≤ branchResistanceOhm.x3
  capacitance_positive :
    0 < shuntCapacitanceF.x0 ∧ 0 < shuntCapacitanceF.x1 ∧
    0 < shuntCapacitanceF.x2 ∧ 0 < shuntCapacitanceF.x3

/--
Equivalent EO load at each phase node for the first single-ended-to-ground
model. Differential/push-pull electrode loads require an extracted multiport
capacitance/conductance matrix before claiming this approximation is valid.
-/
structure EOPhasePortLoad where
  shuntCapacitanceF : Four
  shuntConductanceS : Four
  targetPhaseShiftRad : ℝ
  requiredVoltageSwingV : ℝ
  targetBandwidthHz : ℝ
  maximumSettlingTimeS : ℝ
  load_cap_nonnegative :
    0 ≤ shuntCapacitanceF.x0 ∧ 0 ≤ shuntCapacitanceF.x1 ∧
    0 ≤ shuntCapacitanceF.x2 ∧ 0 ≤ shuntCapacitanceF.x3
  load_conductance_nonnegative :
    0 ≤ shuntConductanceS.x0 ∧ 0 ≤ shuntConductanceS.x1 ∧
    0 ≤ shuntConductanceS.x2 ∧ 0 ≤ shuntConductanceS.x3
  voltage_swing_nonnegative : 0 ≤ requiredVoltageSwingV
  target_bandwidth_nonnegative : 0 ≤ targetBandwidthHz
  maximum_settling_time_positive : 0 < maximumSettlingTimeS

/-- Node-voltage and branch-current state for the coupled ring. -/
structure FourLCState where
  nodeVoltageV : Four
  branchCurrentA : Four

/-- Four current-source inputs from the phase-selective AC/top-off network. -/
abbrev FourLCDriveCurrentA := Four

/-- KCL at P0: C0*dV0/dt = u0 - (i0-i3) - G0*V0. -/
def nodeVoltageSlope0
    (p : FourLCParameters) (load : EOPhasePortLoad)
    (s : FourLCState) (u : FourLCDriveCurrentA) : ℝ :=
  (u.x0 - (s.branchCurrentA.x0 - s.branchCurrentA.x3) -
    load.shuntConductanceS.x0 * s.nodeVoltageV.x0) /
    (p.shuntCapacitanceF.x0 + load.shuntCapacitanceF.x0)

/-- KCL at P1. -/
def nodeVoltageSlope1
    (p : FourLCParameters) (load : EOPhasePortLoad)
    (s : FourLCState) (u : FourLCDriveCurrentA) : ℝ :=
  (u.x1 - (s.branchCurrentA.x1 - s.branchCurrentA.x0) -
    load.shuntConductanceS.x1 * s.nodeVoltageV.x1) /
    (p.shuntCapacitanceF.x1 + load.shuntCapacitanceF.x1)

/-- KCL at P2. -/
def nodeVoltageSlope2
    (p : FourLCParameters) (load : EOPhasePortLoad)
    (s : FourLCState) (u : FourLCDriveCurrentA) : ℝ :=
  (u.x2 - (s.branchCurrentA.x2 - s.branchCurrentA.x1) -
    load.shuntConductanceS.x2 * s.nodeVoltageV.x2) /
    (p.shuntCapacitanceF.x2 + load.shuntCapacitanceF.x2)

/-- KCL at P3. -/
def nodeVoltageSlope3
    (p : FourLCParameters) (load : EOPhasePortLoad)
    (s : FourLCState) (u : FourLCDriveCurrentA) : ℝ :=
  (u.x3 - (s.branchCurrentA.x3 - s.branchCurrentA.x2) -
    load.shuntConductanceS.x3 * s.nodeVoltageV.x3) /
    (p.shuntCapacitanceF.x3 + load.shuntCapacitanceF.x3)

/-- KVL across L0, oriented P0 to P1. -/
def branchCurrentSlope0
    (p : FourLCParameters) (s : FourLCState) : ℝ :=
  (s.nodeVoltageV.x0 - s.nodeVoltageV.x1 -
    p.branchResistanceOhm.x0 * s.branchCurrentA.x0) / p.inductanceH.x0

/-- KVL across L1, oriented P1 to P2. -/
def branchCurrentSlope1
    (p : FourLCParameters) (s : FourLCState) : ℝ :=
  (s.nodeVoltageV.x1 - s.nodeVoltageV.x2 -
    p.branchResistanceOhm.x1 * s.branchCurrentA.x1) / p.inductanceH.x1

/-- KVL across L2, oriented P2 to P3. -/
def branchCurrentSlope2
    (p : FourLCParameters) (s : FourLCState) : ℝ :=
  (s.nodeVoltageV.x2 - s.nodeVoltageV.x3 -
    p.branchResistanceOhm.x2 * s.branchCurrentA.x2) / p.inductanceH.x2

/-- KVL across L3, oriented P3 to P0. -/
def branchCurrentSlope3
    (p : FourLCParameters) (s : FourLCState) : ℝ :=
  (s.nodeVoltageV.x3 - s.nodeVoltageV.x0 -
    p.branchResistanceOhm.x3 * s.branchCurrentA.x3) / p.inductanceH.x3

/-- Complete eight-state coupled-resonator differential model. -/
structure FourLCRightHandSide where
  nodeVoltageSlopeVPerS : Four
  branchCurrentSlopeAPerS : Four

def fourLCRightHandSide
    (p : FourLCParameters) (load : EOPhasePortLoad)
    (s : FourLCState) (drive : FourLCDriveCurrentA) : FourLCRightHandSide :=
  { nodeVoltageSlopeVPerS :=
      ⟨nodeVoltageSlope0 p load s drive,
       nodeVoltageSlope1 p load s drive,
       nodeVoltageSlope2 p load s drive,
       nodeVoltageSlope3 p load s drive⟩
    branchCurrentSlopeAPerS :=
      ⟨branchCurrentSlope0 p s,
       branchCurrentSlope1 p s,
       branchCurrentSlope2 p s,
       branchCurrentSlope3 p s⟩ }

/-- Ideal LC stored energy in the four shunt capacitors and four ring inductors. -/
def fourLCStoredEnergyJ
    (p : FourLCParameters) (load : EOPhasePortLoad) (s : FourLCState) : ℝ :=
  (p.shuntCapacitanceF.x0 + load.shuntCapacitanceF.x0) *
      s.nodeVoltageV.x0 ^ 2 / 2 +
  (p.shuntCapacitanceF.x1 + load.shuntCapacitanceF.x1) *
      s.nodeVoltageV.x1 ^ 2 / 2 +
  (p.shuntCapacitanceF.x2 + load.shuntCapacitanceF.x2) *
      s.nodeVoltageV.x2 ^ 2 / 2 +
  (p.shuntCapacitanceF.x3 + load.shuntCapacitanceF.x3) *
      s.nodeVoltageV.x3 ^ 2 / 2 +
  p.inductanceH.x0 * s.branchCurrentA.x0 ^ 2 / 2 +
  p.inductanceH.x1 * s.branchCurrentA.x1 ^ 2 / 2 +
  p.inductanceH.x2 * s.branchCurrentA.x2 ^ 2 / 2 +
  p.inductanceH.x3 * s.branchCurrentA.x3 ^ 2 / 2

theorem fourLC_stored_energy_nonnegative
    (p : FourLCParameters) (load : EOPhasePortLoad) (s : FourLCState) :
    0 ≤ fourLCStoredEnergyJ p load s := by
  rcases p.inductance_positive with ⟨hL0, hL1, hL2, hL3⟩
  rcases p.capacitance_positive with ⟨hC0, hC1, hC2, hC3⟩
  rcases load.load_cap_nonnegative with ⟨hCL0, hCL1, hCL2, hCL3⟩
  unfold fourLCStoredEnergyJ
  have hT0 : 0 ≤ p.shuntCapacitanceF.x0 + load.shuntCapacitanceF.x0 :=
    add_nonneg (le_of_lt hC0) hCL0
  have hT1 : 0 ≤ p.shuntCapacitanceF.x1 + load.shuntCapacitanceF.x1 :=
    add_nonneg (le_of_lt hC1) hCL1
  have hT2 : 0 ≤ p.shuntCapacitanceF.x2 + load.shuntCapacitanceF.x2 :=
    add_nonneg (le_of_lt hC2) hCL2
  have hT3 : 0 ≤ p.shuntCapacitanceF.x3 + load.shuntCapacitanceF.x3 :=
    add_nonneg (le_of_lt hC3) hCL3
  positivity

/-- The four modal energy buckets used to track the intended and parasitic modes. -/
structure ModalEnergyContent where
  commonModeJ : ℝ
  quadratureCosModeJ : ℝ
  quadratureSinModeJ : ℝ
  alternatingModeJ : ℝ
  all_nonnegative :
    0 ≤ commonModeJ ∧ 0 ≤ quadratureCosModeJ ∧
    0 ≤ quadratureSinModeJ ∧ 0 ≤ alternatingModeJ

def desiredQuadratureModeEnergyJ (m : ModalEnergyContent) : ℝ :=
  m.quadratureCosModeJ + m.quadratureSinModeJ

def undesiredModeEnergyJ (m : ModalEnergyContent) : ℝ :=
  m.commonModeJ + m.alternatingModeJ

def totalModalEnergyJ (m : ModalEnergyContent) : ℝ :=
  desiredQuadratureModeEnergyJ m + undesiredModeEnergyJ m

theorem undesired_modal_energy_nonnegative (m : ModalEnergyContent) :
    0 ≤ undesiredModeEnergyJ m := by
  rcases m.all_nonnegative with ⟨h0, _, _, h3⟩
  exact add_nonneg h0 h3

theorem desired_modal_energy_nonnegative (m : ModalEnergyContent) :
    0 ≤ desiredQuadratureModeEnergyJ m := by
  rcases m.all_nonnegative with ⟨_, h1, h2, _⟩
  exact add_nonneg h1 h2

/-- Fraction of represented resonator mode energy in the desired quadrature pair. -/
def quadratureModePurity (m : ModalEnergyContent) : ℝ :=
  if totalModalEnergyJ m = 0 then 0
  else desiredQuadratureModeEnergyJ m / totalModalEnergyJ m

/--
One cycle of mode-selective operation. Drain from undesired modes is accounted
separately from energy delivered to the EO load. The sink may be dissipative or
an external source that accepts energy; the evidence field distinguishes them.
-/
inductive ModeDrainDestination where
  | dissipatedInConditioner
  | returnedToExternalDrive
  deriving DecidableEq, Repr

structure ModeConditioningCycle where
  start : ModalEnergyContent
  finish : ModalEnergyContent
  desiredModeTopoffJ : ℝ
  energyReturnedFromEOLoadJ : ℝ
  energyDeliveredToEOLoadJ : ℝ
  resonatorAndDriverLossJ : ℝ
  undesiredModeDrainJ : ℝ
  drainDestination : ModeDrainDestination
  all_nonnegative :
    0 ≤ desiredModeTopoffJ ∧ 0 ≤ energyReturnedFromEOLoadJ ∧
    0 ≤ energyDeliveredToEOLoadJ ∧ 0 ≤ resonatorAndDriverLossJ ∧
    0 ≤ undesiredModeDrainJ
  energy_balance :
    totalModalEnergyJ start + energyReturnedFromEOLoadJ +
      desiredModeTopoffJ =
    totalModalEnergyJ finish + energyDeliveredToEOLoadJ +
      resonatorAndDriverLossJ + undesiredModeDrainJ

/-- Room-temperature geometric/passive LC versus cryogenic HKI implementation. -/
inductive FourLCImplementation where
  | roomTemperatureGeometricLC
  | cryogenicHKI
  deriving DecidableEq, Repr

inductive ParameterEvidence where
  | assumedModel
  | extractedCircuit
  | circuitSimulation
  | measuredHardware
  deriving DecidableEq, Repr

/-- Technology-specific reservoir and packaging inputs; none are defaulted. -/
structure FourLCBuildProfile where
  implementation : FourLCImplementation
  parameters : FourLCParameters
  operatingTemperatureK : ℝ
  inductorFootprintAreaM2 : ℝ
  maximumBranchCurrentA : ℝ
  loadedQualityFactor : ℝ
  measuredOrExtractedResonanceHz : ℝ
  driverWallPlugEnergyPerCycleJ : ℝ
  coolingWallPlugPowerW : ℝ
  evidence : ParameterEvidence
  artifactIdentity : String
  temperature_positive : 0 < operatingTemperatureK
  area_positive : 0 < inductorFootprintAreaM2
  current_positive : 0 < maximumBranchCurrentA
  loaded_q_positive : 0 < loadedQualityFactor
  resonance_positive : 0 < measuredOrExtractedResonanceHz
  driver_energy_nonnegative : 0 ≤ driverWallPlugEnergyPerCycleJ
  cooling_power_nonnegative : 0 ≤ coolingWallPlugPowerW

/-- Shared workload/load boundary for a fair two-technology comparison. -/
structure MatchedFourLCComparison where
  eoLoad : EOPhasePortLoad
  controlRegime : EOControlRegime
  outputInterface : EOOutputInterface
  targetResonanceHz : ℝ
  allowedFrequencyErrorHz : ℝ
  minimumLoadedQ : ℝ
  maximumPhaseErrorRad : ℝ
  roomTemperature : FourLCBuildProfile
  hkiCryogenic : FourLCBuildProfile
  room_temperature_technology :
    roomTemperature.implementation = .roomTemperatureGeometricLC
  hki_technology : hkiCryogenic.implementation = .cryogenicHKI
  frequency_target_positive : 0 < targetResonanceHz
  frequency_error_nonnegative : 0 ≤ allowedFrequencyErrorHz
  minimum_q_positive : 0 < minimumLoadedQ
  phase_error_nonnegative : 0 ≤ maximumPhaseErrorRad
  same_eo_load_used_for_both_candidates : True

/-- Frequency tolerance acceptance for one candidate. -/
def frequencyAccepted (targetHz toleranceHz measuredHz : ℝ) : Prop :=
  |measuredHz - targetHz| ≤ toleranceHz

def candidateFrequencyAccepted (c : MatchedFourLCComparison)
    (build : FourLCBuildProfile) : Prop :=
  frequencyAccepted c.targetResonanceHz c.allowedFrequencyErrorHz
    build.measuredOrExtractedResonanceHz

def candidateQAccepted (c : MatchedFourLCComparison)
    (build : FourLCBuildProfile) : Prop :=
  c.minimumLoadedQ ≤ build.loadedQualityFactor

/-- Wall-plug energy includes resonator driver and cooling over one cycle. -/
def buildWallPlugEnergyPerCycleJ (build : FourLCBuildProfile)
    (cycleDurationS : ℝ) : ℝ :=
  build.driverWallPlugEnergyPerCycleJ +
    build.coolingWallPlugPowerW * cycleDurationS

theorem build_wallplug_energy_nonnegative
    (build : FourLCBuildProfile) (durationS : ℝ) (hDuration : 0 ≤ durationS) :
    0 ≤ buildWallPlugEnergyPerCycleJ build durationS := by
  unfold buildWallPlugEnergyPerCycleJ
  exact add_nonneg build.driver_energy_nonnegative
    (mul_nonneg build.cooling_power_nonnegative hDuration)

end
end EIS.FourLC
