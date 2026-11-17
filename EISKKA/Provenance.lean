module

@[expose] public section

/-!
# EIS-KKA-FORMAL-001 — Evidence provenance and release classification

Evidence quality and confidentiality are separate dimensions. In particular,
"foundry-confidential" is a release classification, not an evidence-quality
level: a measured parameter can still be confidential.
-/

namespace EISKKA

/-- Scientific evidence class for a model parameter. -/
inductive EvidenceClass where
  | assumed
  | simulated
  | fitted
  | measured
  deriving DecidableEq, Repr

/-- Release classification is independent of evidence quality. -/
inductive Confidentiality where
  | publicRelease
  | foundryConfidential
  deriving DecidableEq, Repr

/-- Provenance metadata attached to one physical or model parameter. -/
structure ParameterProvenance where
  evidence : EvidenceClass
  confidentiality : Confidentiality
  sourceRecord : String

/-- Public release is permitted only when the confidentiality tag is public. -/
def PubliclyReleasable (p : ParameterProvenance) : Prop :=
  p.confidentiality = .publicRelease

/-- Evidence rank, from weakest to strongest evidence. -/
def EvidenceClass.rank : EvidenceClass → Nat
  | .assumed => 0
  | .simulated => 1
  | .fitted => 2
  | .measured => 3

/-- Combining evidence uses the weaker of the two evidence classes. -/
def EvidenceClass.combine (a b : EvidenceClass) : EvidenceClass :=
  if a.rank ≤ b.rank then a else b

@[simp] theorem combine_rank_le_left (a b : EvidenceClass) :
    (EvidenceClass.combine a b).rank ≤ a.rank := by
  cases a <;> cases b <;> decide

@[simp] theorem combine_rank_le_right (a b : EvidenceClass) :
    (EvidenceClass.combine a b).rank ≤ b.rank := by
  cases a <;> cases b <;> decide

end EISKKA
