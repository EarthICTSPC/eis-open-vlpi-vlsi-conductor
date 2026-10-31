import Mathlib
import EIS.MZI_EO

/-!
# EIS-RES-PWR-001 — Resonant energy-recycling power domain

This contract models the resonant energy reservoir itself, not merely a return
conductor. It separates:
* energy circulating between the reservoir and EO load,
* energy replenished by the external electrical supply,
* energy dissipated in the resonator/driver/coupling network,
* thermal-management overhead,
* resonant phase rails versus proven logic-sequencing behavior.

The LC equations are ideal lumped-model definitions. The cycle ledger is an
abstract conservation contract. Neither establishes a fabricated resonator,
measured Q, driver efficiency, or physical energy recovery.
-/

namespace EIS.ResPwr

noncomputable section

open EIS.MZI_EO

inductive ReservoirTechnology where
  | passiveRoomTemperatureLC
  | superconductingKineticInductor
  | otherResonantImplementation
  deriving DecidableEq, Repr

/-- Instantaneous state variables for an ideal lumped LC energy store. -/
structure ReservoirState where
  inductorCurrentA : ℝ
  capacitorVoltageV : ℝ

/--
Effective lumped reservoir parameters. The loaded series resistance is intended
to include the resonator's effective loaded loss, not only bare inductor ESR.
-/
structure LCResonantReservoir where
  technology : ReservoirTechnology
  inductanceH : ℝ
  capacitanceF : ℝ
  loadedSeriesResistanceOhm : ℝ
  inductance_pos : 0 < inductanceH
  capacitance_pos : 0 < capacitanceF
  loaded_resistance_pos : 0 < loadedSeriesResistanceOhm

/-- Ideal undamped LC angular resonance frequency. -/
def resonantAngularFrequencyRadPerS (r : LCResonantReservoir) : ℝ :=
  Real.sqrt (1 / (r.inductanceH * r.capacitanceF))

/-- Ideal undamped LC resonant frequency in cycles per second. -/
def resonantFrequencyHz (r : LCResonantReservoir) : ℝ :=
  resonantAngularFrequencyRadPerS r / (2 * Real.pi)

/-- Series-model loaded Q using the effective loaded resistance. -/
def loadedQualityFactor (r : LCResonantReservoir) : ℝ :=
  resonantAngularFrequencyRadPerS r * r.inductanceH /
    r.loadedSeriesResistanceOhm

/-- Energy stored in the inductor. -/
def inductorStoredEnergyJ (r : LCResonantReservoir) (s : ReservoirState) : ℝ :=
  r.inductanceH * s.inductorCurrentA ^ 2 / 2

/-- Energy stored in the capacitor. -/
def capacitorStoredEnergyJ (r : LCResonantReservoir) (s : ReservoirState) : ℝ :=
  r.capacitanceF * s.capacitorVoltageV ^ 2 / 2

/-- Total ideal lumped LC stored energy. -/
def storedEnergyJ (r : LCResonantReservoir) (s : ReservoirState) : ℝ :=
  inductorStoredEnergyJ r s + capacitorStoredEnergyJ r s

theorem resonant_angular_frequency_positive (r : LCResonantReservoir) :
    0 < resonantAngularFrequencyRadPerS r := by
  unfold resonantAngularFrequencyRadPerS
  apply Real.sqrt_pos.2
  positivity

theorem resonant_frequency_positive (r : LCResonantReservoir) :
    0 < resonantFrequencyHz r := by
  unfold resonantFrequencyHz
  positivity

theorem loaded_quality_factor_positive (r : LCResonantReservoir) :
    0 < loadedQualityFactor r := by
  unfold loadedQualityFactor
  positivity

theorem stored_energy_nonnegative (r : LCResonantReservoir) (s : ReservoirState) :
    0 ≤ storedEnergyJ r s := by
  unfold storedEnergyJ inductorStoredEnergyJ capacitorStoredEnergyJ
  positivity

/-- Canonical four sinusoidal phase offsets in quadrature. -/
def quadratureFourPhaseOffsetsRad : List ℝ :=
  [0, Real.pi / 2, Real.pi, 3 * Real.pi / 2]

/-- Exact ideal 0°, 90°, 180°, 270° phase-offset predicate. -/
def isFourPhaseQuadrature (offsets : List ℝ) : Prop :=
  offsets = quadratureFourPhaseOffsetsRad

theorem quadrature_four_phase_count :
    quadratureFourPhaseOffsetsRad.length = 4 := by
  rfl

inductive ExcitationWaveform where
  | sinusoidal
  | trapezoidal
  | otherPeriodic
  deriving DecidableEq, Repr

/-- The AC excitation may supply energy only, or may also be assigned sequencing. -/
inductive ExcitationRole where
  | energyOnly
  | energyAndLogicSequence
  deriving DecidableEq, Repr

/--
A resonant excitation profile. Phase offsets are explicit; a waveform is not
assumed to be a logic clock merely because it is periodic.
-/
structure ResonantExcitationProfile where
  waveform : ExcitationWaveform
  role : ExcitationRole
  frequencyHz : ℝ
  peakVoltageV : ℝ
  peakCurrentA : ℝ
  phaseOffsetsRad : List ℝ
  phaseSequenceEvidence : Option Bool
  frequency_pos : 0 < frequencyHz
  voltage_nonneg : 0 ≤ peakVoltageV
  current_nonneg : 0 ≤ peakCurrentA
  at_least_one_phase_rail : 1 ≤ phaseOffsetsRad.length
  sequence_role_requires_evidence :
    role = .energyAndLogicSequence → phaseSequenceEvidence = some true

/-- True only when the excitation frequency is within the declared tolerance. -/
def frequencyWithinTolerance
    (r : LCResonantReservoir) (x : ResonantExcitationProfile)
    (toleranceHz : ℝ) : Prop :=
  |x.frequencyHz - resonantFrequencyHz r| ≤ toleranceHz

/-- Dissipation categories are kept separate for attribution. -/
structure ReservoirLossBreakdown where
  inductorCopperLossJ : ℝ
  capacitorDielectricLossJ : ℝ
  driverConductionLossJ : ℝ
  couplingAndDistributionLossJ : ℝ
  otherLossJ : ℝ
  inductor_nonneg : 0 ≤ inductorCopperLossJ
  capacitor_nonneg : 0 ≤ capacitorDielectricLossJ
  driver_nonneg : 0 ≤ driverConductionLossJ
  coupling_nonneg : 0 ≤ couplingAndDistributionLossJ
  other_nonneg : 0 ≤ otherLossJ

def totalDissipatedJ (l : ReservoirLossBreakdown) : ℝ :=
  l.inductorCopperLossJ + l.capacitorDielectricLossJ +
  l.driverConductionLossJ + l.couplingAndDistributionLossJ + l.otherLossJ

theorem total_dissipated_nonnegative (l : ReservoirLossBreakdown) :
    0 ≤ totalDissipatedJ l := by
  unfold totalDissipatedJ
  positivity

/-- External wall-plug energy is converted to replenishment energy at the reservoir. -/
structure ExternalReplenishment where
  wallPlugEnergyJ : ℝ
  energyAtReservoirJ : ℝ
  conversionEfficiency : ℝ
  wallplug_nonneg : 0 ≤ wallPlugEnergyJ
  reservoir_energy_nonneg : 0 ≤ energyAtReservoirJ
  efficiency_pos : 0 < conversionEfficiency
  efficiency_le_one : conversionEfficiency ≤ 1
  replenishment_conversion :
    energyAtReservoirJ = wallPlugEnergyJ * conversionEfficiency

theorem reservoir_replenishment_le_wallplug (p : ExternalReplenishment) :
    p.energyAtReservoirJ ≤ p.wallPlugEnergyJ := by
  have hOneMinusEfficiency : 0 ≤ 1 - p.conversionEfficiency := by
    linarith [p.efficiency_le_one]
  have hLostWallplug : 0 ≤
      p.wallPlugEnergyJ * (1 - p.conversionEfficiency) :=
    mul_nonneg p.wallplug_nonneg hOneMinusEfficiency
  rw [p.replenishment_conversion]
  nlinarith [hLostWallplug]

/--
One complete reservoir/load cycle. Energy returned from the load is returned
to the reservoir, not necessarily to the external utility supply.
-/
structure ReservoirCycle (r : LCResonantReservoir) where
  startState : ReservoirState
  endState : ReservoirState
  energyDeliveredToLoadJ : ℝ
  energyReturnedFromLoadJ : ℝ
  losses : ReservoirLossBreakdown
  replenishment : ExternalReplenishment
  delivered_nonneg : 0 ≤ energyDeliveredToLoadJ
  returned_nonneg : 0 ≤ energyReturnedFromLoadJ
  returned_le_delivered : energyReturnedFromLoadJ ≤ energyDeliveredToLoadJ
  reservoir_energy_balance :
    storedEnergyJ r startState + energyReturnedFromLoadJ +
      replenishment.energyAtReservoirJ =
    storedEnergyJ r endState + energyDeliveredToLoadJ + totalDissipatedJ losses

/-- A periodic steady-state cycle has the same stored energy at both boundaries. -/
def periodicSteadyState (r : LCResonantReservoir) (c : ReservoirCycle r) : Prop :=
  storedEnergyJ r c.startState = storedEnergyJ r c.endState

/--
At periodic steady state, external reservoir replenishment exactly replaces
net energy delivered to the load plus reservoir/driver losses.
-/
theorem steady_state_replenishment_balance
    (r : LCResonantReservoir) (c : ReservoirCycle r)
    (hPeriodic : periodicSteadyState r c) :
    c.replenishment.energyAtReservoirJ =
      (c.energyDeliveredToLoadJ - c.energyReturnedFromLoadJ) +
        totalDissipatedJ c.losses := by
  unfold periodicSteadyState at hPeriodic
  linarith [c.reservoir_energy_balance]

theorem steady_state_replenishment_nonnegative
    (r : LCResonantReservoir) (c : ReservoirCycle r)
    (hPeriodic : periodicSteadyState r c) :
    0 ≤ c.replenishment.energyAtReservoirJ := by
  rw [steady_state_replenishment_balance r c hPeriodic]
  have hNet : 0 ≤ c.energyDeliveredToLoadJ - c.energyReturnedFromLoadJ := by
    linarith [c.returned_le_delivered]
  exact add_nonneg hNet (total_dissipated_nonnegative c.losses)

/-- A thermal boundary records refrigeration overhead rather than hiding it. -/
structure ThermalOperatingDomain where
  operatingTemperatureK : ℝ
  heatSinkTemperatureK : ℝ
  coolingWallPlugPowerW : ℝ
  temperature_nonneg : 0 ≤ operatingTemperatureK
  heat_sink_nonneg : 0 ≤ heatSinkTemperatureK
  cooling_power_nonneg : 0 ≤ coolingWallPlugPowerW

def coolingWallPlugEnergyJ (t : ThermalOperatingDomain) (durationS : ℝ) : ℝ :=
  t.coolingWallPlugPowerW * durationS

theorem cooling_wallplug_energy_nonnegative
    (t : ThermalOperatingDomain) (durationS : ℝ) (hDuration : 0 ≤ durationS) :
    0 ≤ coolingWallPlugEnergyJ t durationS := by
  unfold coolingWallPlugEnergyJ
  exact mul_nonneg t.cooling_power_nonneg hDuration

/--
The integrated resonant EO domain. The measured return path is required by
EIS-MZI-EO-001; the reservoir cycle separately balances internal circulation
and external top-off. No claim is made that the circuit dynamics are validated.
-/
structure ResonantPowerDomainContract where
  reservoir : LCResonantReservoir
  modulator : PhaseShifterProfile
  excitation : ResonantExcitationProfile
  cycle : ReservoirCycle reservoir
  thermal : ThermalOperatingDomain
  cycleDurationS : ℝ
  frequencyToleranceHz : ℝ
  cycle_duration_pos : 0 < cycleDurationS
  frequency_tolerance_nonneg : 0 ≤ frequencyToleranceHz
  drive_near_resonance :
    frequencyWithinTolerance reservoir excitation frequencyToleranceHz
  recovery_path_measured :
    recoveryEligible modulator.kind modulator.returnTopology modulator.returnEvidence
  capacitive_modulator : modulator.kind = .lumpedCapacitiveEO
  sequencing_evidence_if_used :
    excitation.role = .energyOnly ∨ excitation.phaseSequenceEvidence = some true

/-- External wall-plug cost of keeping this resonator replenished for one cycle. -/
def resonantDomainWallPlugEnergyJ (p : ResonantPowerDomainContract) : ℝ :=
  p.cycle.replenishment.wallPlugEnergyJ

/-- Cooling wall-plug energy is a separate system cost, including cryogenic overhead. -/
def resonantDomainCoolingEnergyJ (p : ResonantPowerDomainContract) : ℝ :=
  coolingWallPlugEnergyJ p.thermal p.cycleDurationS

theorem resonant_domain_replenishment_is_at_least_reservoir_topoff
    (p : ResonantPowerDomainContract) :
    p.cycle.replenishment.energyAtReservoirJ ≤ resonantDomainWallPlugEnergyJ p :=
  reservoir_replenishment_le_wallplug p.cycle.replenishment

theorem resonant_domain_cooling_energy_nonnegative (p : ResonantPowerDomainContract) :
    0 ≤ resonantDomainCoolingEnergyJ p := by
  unfold resonantDomainCoolingEnergyJ
  exact cooling_wallplug_energy_nonnegative p.thermal p.cycleDurationS
    (le_of_lt p.cycle_duration_pos)

end
end EIS.ResPwr
