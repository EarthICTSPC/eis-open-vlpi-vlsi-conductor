module

public import Mathlib
public import EISKKA.Bench001A

/-!
EIS-KKA-CONTRACT-001
Canonical conventions and evidence contract for EIS KKA primitive qualification.
This module is process-independent and does not assert that any foundry device
realizes the ideal definitions.
-/

namespace EISKKA.Contract001

open EISKKA.Bench001A

/-- Physical field convention: Re(E_phasor * exp(+i omega t)). -/
def phasorConvention : String :=
  "physical_field = Re(E_phasor * exp(+i*omega*t))"

/-- A denotes field-amplitude transmission, not intensity transmission. -/
def amplitudeConvention : String :=
  "A is field-amplitude transmission, not intensity transmission"

/-- Construct a complex-envelope field from amplitude and phase in radians. -/
def amplitudePhaseField (amplitude phaseRad : ℝ) : Field :=
  ⟨amplitude * Real.cos phaseRad, amplitude * Real.sin phaseRad⟩

/-- A transfer sample keeps field amplitude and phase as distinct quantities. -/
structure TransferSample where
  amplitude : ℝ
  phaseRad : ℝ
  amplitude_nonneg : 0 ≤ amplitude

def TransferSample.toField (sample : TransferSample) : Field :=
  amplitudePhaseField sample.amplitude sample.phaseRad

/-- κ_A = (dφ/du) / (d ln(A)/du) = (dφ/du) / ((dA/du)/A). -/
noncomputable def kappaAFromDrive
    (amplitude phaseRad : ℝ → ℝ) (u : ℝ) : ℝ :=
  deriv phaseRad u / (deriv amplitude u / amplitude u)

/-- Since intensity is proportional to A², κ_I = κ_A / 2. -/
noncomputable def kappaIFromDrive
    (amplitude phaseRad : ℝ → ℝ) (u : ℝ) : ℝ :=
  kappaAFromDrive amplitude phaseRad u / 2

/-- Conditions under which the drive-parameter KKA trajectory is meaningful. -/
def KKARegularPoint (amplitude phaseRad : ℝ → ℝ) (u : ℝ) : Prop :=
  0 < amplitude u ∧
  DifferentiableAt ℝ amplitude u ∧
  DifferentiableAt ℝ phaseRad u ∧
  deriv amplitude u ≠ 0

/-- Plus-port power for an ideal 50:50 balanced combiner. -/
def plusPortPower (a b : Field) : ℝ :=
  intensity (add a b) / 2

/-- Minus-port power for an ideal 50:50 balanced combiner. -/
def minusPortPower (a b : Field) : ℝ :=
  intensity (sub a b) / 2

/-- Ideal signed detector output; polarity is I_plus minus I_minus. -/
noncomputable def idealBalancedOutput (r : ℝ) (a b : Field) : ℝ :=
  balancedDifference r a b

/-- Difference of the normalized ideal output powers is the signed cross term. -/
lemma balanced_port_power_difference (a b : Field) :
    plusPortPower a b - minusPortPower a b = 2 * crossTerm a b := by
  simp [plusPortPower, minusPortPower, intensity, add, sub, crossTerm]
  ring

/-- Ideal balanced detection retains the signed cross term:
    Y = 2 r Re(a * conj(b)).
    Assumes a 50:50 combiner and matched detector branches. -/
lemma ideal_balanced_detector_identity (r : ℝ) (a b : Field) :
    idealBalancedOutput r a b = 2 * r * crossTerm a b := by
  exact balanced_difference_identity r a b

/-- Explicit branch calibration parameters for a nonideal detector. -/
structure DetectorCalibration where
  responsivity : ℝ
  responsivityUnit : String
  gainPlus : ℝ
  gainMinus : ℝ
  offsetPlus : ℝ
  offsetMinus : ℝ

def plusBranchCurrent (cal : DetectorCalibration) (a b : Field) : ℝ :=
  cal.responsivity * cal.gainPlus * plusPortPower a b + cal.offsetPlus

def minusBranchCurrent (cal : DetectorCalibration) (a b : Field) : ℝ :=
  cal.responsivity * cal.gainMinus * minusPortPower a b + cal.offsetMinus

def differentialCurrent (cal : DetectorCalibration) (a b : Field) : ℝ :=
  plusBranchCurrent cal a b - minusBranchCurrent cal a b

/-- Provenance class is explicit; it is never inferred from numerical values. -/
inductive EvidenceClass
  | formal
  | simulated
  | synthetic
  | physicallyMeasured
deriving Repr, DecidableEq

/-- Operating conditions and field normalization used to interpret measurements. -/
structure OperatingPoint where
  wavelengthNm : ℝ
  temperatureC : ℝ
  driveValue : ℝ
  driveUnit : String
  fieldPowerUnit : String
  phaseReferenceRad : ℝ
  biasValue : Option ℝ
  biasUnit : Option String

/-- Process-independent numerical limits; units are declared by the operating point. -/
structure AcceptanceLimits where
  maxAbsResidual : ℝ
  maxStandardUncertainty : ℝ
  minVisibility : ℝ
  maxInsertionLossDb : ℝ
  minKappaA : ℝ
  maxKappaA : ℝ
  maxNoiseRmsA : Option ℝ
  minBandwidthHz : Option ℝ

structure EvidenceRecord where
  evidenceClass : EvidenceClass
  deviceId : String
  processId : String
  layoutRevision : String
  instrumentId : String
  instrumentCalibrationId : String
  calibrationRecordId : String
  rawDataSha256 : String
  operatingPoint : OperatingPoint
  detectorCalibration : DetectorCalibration
  sampleCount : Nat
  absResidual : ℝ
  standardUncertainty : ℝ
  visibility : ℝ
  insertionLossDb : ℝ
  kappaA : ℝ
  noiseRmsA : Option ℝ
  bandwidthHz : Option ℝ

structure AcceptanceContract where
  contractId : String
  version : String
  limits : AcceptanceLimits

def AcceptanceLimits.WellFormed (limits : AcceptanceLimits) : Prop :=
  0 ≤ limits.maxAbsResidual ∧
  0 ≤ limits.maxStandardUncertainty ∧
  0 ≤ limits.minVisibility ∧ limits.minVisibility ≤ 1 ∧
  0 ≤ limits.maxInsertionLossDb ∧
  limits.minKappaA ≤ limits.maxKappaA ∧
  (limits.maxNoiseRmsA = none ∨ ∃ bound, limits.maxNoiseRmsA = some bound ∧ 0 ≤ bound) ∧
  (limits.minBandwidthHz = none ∨ ∃ bound, limits.minBandwidthHz = some bound ∧ 0 ≤ bound)

def optionalUpperBoundPasses (limit measurement : Option ℝ) : Prop :=
  match limit, measurement with
  | none, _ => True
  | some bound, some value => 0 ≤ value ∧ value ≤ bound
  | some _, none => False

def optionalLowerBoundPasses (limit measurement : Option ℝ) : Prop :=
  match limit, measurement with
  | none, _ => True
  | some bound, some value => 0 ≤ value ∧ bound ≤ value
  | some _, none => False

/-- A physical pass requires measured evidence, complete provenance, an
    operating point, KKA trajectory value, and every enabled numerical limit. -/
def passesPhysicalAcceptance
    (contract : AcceptanceContract) (evidence : EvidenceRecord) : Prop :=
  contract.limits.WellFormed ∧
  evidence.evidenceClass = EvidenceClass.physicallyMeasured ∧
  evidence.deviceId ≠ "" ∧
  evidence.processId ≠ "" ∧
  evidence.layoutRevision ≠ "" ∧
  evidence.instrumentId ≠ "" ∧
  evidence.instrumentCalibrationId ≠ "" ∧
  evidence.calibrationRecordId ≠ "" ∧
  evidence.rawDataSha256 ≠ "" ∧
  0 < evidence.operatingPoint.wavelengthNm ∧
  evidence.operatingPoint.driveUnit ≠ "" ∧
  evidence.operatingPoint.fieldPowerUnit ≠ "" ∧
  ((evidence.operatingPoint.biasValue = none ∧ evidence.operatingPoint.biasUnit = none) ∨
    (∃ value unitName, evidence.operatingPoint.biasValue = some value ∧
      evidence.operatingPoint.biasUnit = some unitName ∧ unitName ≠ "")) ∧
  0 ≤ evidence.detectorCalibration.responsivity ∧
  evidence.detectorCalibration.responsivityUnit ≠ "" ∧
  0 ≤ evidence.detectorCalibration.gainPlus ∧
  0 ≤ evidence.detectorCalibration.gainMinus ∧
  0 < evidence.sampleCount ∧
  0 ≤ evidence.absResidual ∧
  evidence.absResidual ≤ contract.limits.maxAbsResidual ∧
  0 ≤ evidence.standardUncertainty ∧
  evidence.standardUncertainty ≤ contract.limits.maxStandardUncertainty ∧
  0 ≤ evidence.visibility ∧ evidence.visibility ≤ 1 ∧
  contract.limits.minVisibility ≤ evidence.visibility ∧
  0 ≤ evidence.insertionLossDb ∧
  evidence.insertionLossDb ≤ contract.limits.maxInsertionLossDb ∧
  contract.limits.minKappaA ≤ evidence.kappaA ∧
  evidence.kappaA ≤ contract.limits.maxKappaA ∧
  optionalUpperBoundPasses contract.limits.maxNoiseRmsA evidence.noiseRmsA ∧
  optionalLowerBoundPasses contract.limits.minBandwidthHz evidence.bandwidthHz

/-- Simulated, synthetic or formal evidence alone cannot satisfy physical qualification. -/
lemma nonphysical_evidence_cannot_pass
    (contract : AcceptanceContract) (evidence : EvidenceRecord)
    (h : passesPhysicalAcceptance contract evidence) :
    evidence.evidenceClass = EvidenceClass.physicallyMeasured :=
  h.2.1

end EISKKA.Contract001
