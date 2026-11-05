import Mathlib

namespace EIS.Softmax001

inductive EvidenceClass where
  | specification
  | proofChecked
  | numericalSimulation
  | physicalMeasurement
  deriving DecidableEq, Repr

inductive AttentionMethod where
  | conventionalSoftmax
  | sigmoidAttention
  | interferenceNativeKKA
  deriving DecidableEq, Repr

inductive PrecisionProfile where
  | bf16Training
  | fp16Training
  | w4a16Inference
  | w4a8Inference
  deriving DecidableEq, Repr

inductive GateStatus where
  | blocked
  | admissibleForDigitalExperiment
  | admissibleForSimulationRequest
  | simulationDispatched
  | resultReceived
  | evidenceReviewed
  deriving DecidableEq, Repr

structure Candidate where
  method : AttentionMethod
  precision : PrecisionProfile
  taskId : String
  modelConfigHash : String
  datasetHash : String
  seed : Nat
  deriving Repr

structure AcceptanceEvidence where
  baselineQualityRecorded : Bool
  candidateQualityRecorded : Bool
  qualityToleranceDefined : Bool
  latencyRecorded : Bool
  totalSystemEnergyRecorded : Bool
  thermalBehaviorRecorded : Bool
  evidenceClass : EvidenceClass
  deriving Repr

def evidenceComplete (e : AcceptanceEvidence) : Bool :=
  e.baselineQualityRecorded &&
  e.candidateQualityRecorded &&
  e.qualityToleranceDefined &&
  e.latencyRecorded &&
  e.totalSystemEnergyRecorded &&
  e.thermalBehaviorRecorded

def requiredMethods : List AttentionMethod :=
  [.conventionalSoftmax, .interferenceNativeKKA, .sigmoidAttention]

def isDigitalTraining (p : PrecisionProfile) : Bool :=
  match p with
  | .bf16Training => true
  | .fp16Training => true
  | _ => false

def isDigitalInference (p : PrecisionProfile) : Bool :=
  match p with
  | .w4a16Inference => true
  | .w4a8Inference => true
  | _ => false

structure SimulationRequest where
  candidate : Candidate
  sourceRevision : String
  adapterVersion : String
  simulator : String
  budgetUnits : Nat
  explicitAuthorization : Bool
  deriving Repr

def requestWellFormed (r : SimulationRequest) : Bool :=
  !r.sourceRevision.isEmpty &&
  !r.adapterVersion.isEmpty &&
  !r.simulator.isEmpty &&
  r.budgetUnits > 0 &&
  r.explicitAuthorization

def lowerToSimulationRequest (r : SimulationRequest) : Option SimulationRequest :=
  if requestWellFormed r then some r else none

def mayClaimSimulationDispatched (status : GateStatus) : Bool :=
  status == .simulationDispatched ||
  status == .resultReceived ||
  status == .evidenceReviewed

def mayClaimUsefulAdvantage (e : AcceptanceEvidence) : Bool :=
  evidenceComplete e &&
  (e.evidenceClass == .numericalSimulation ||
   e.evidenceClass == .physicalMeasurement)

theorem malformed_request_not_lowered
    (r : SimulationRequest) (h : requestWellFormed r = false) :
    lowerToSimulationRequest r = none := by
  simp [lowerToSimulationRequest, h]

theorem specification_or_proof_alone_not_advantage
    (e : AcceptanceEvidence)
    (h : e.evidenceClass = .specification ∨
         e.evidenceClass = .proofChecked) :
    mayClaimUsefulAdvantage e = false := by
  cases h with
  | inl hs =>
      simp [mayClaimUsefulAdvantage, hs]
  | inr hp =>
      simp [mayClaimUsefulAdvantage, hp]

end EIS.Softmax001
