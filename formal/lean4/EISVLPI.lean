/-!
# EIS VLPI formal foundation

This is the Lean 4 entry point for machine-checkable definitions and proofs
supporting Earth ICT, SPC's open VLPI contracts. Keep formal claims distinct
from simulation or measurement evidence.
-/

namespace EISVLPI

/-- Semantic meaning is distinct from the physical representation domain. -/
inductive Domain where
  | electronicDigital
  | electronicAnalog
  | photonicOpticalField
  | photonicOpticalPower
  deriving DecidableEq, Repr

/-- An in-flight optical field may carry semantically digital information.
This does not imply an electronic representation or an O/E/O crossing. -/
def inFlightRepresentation : Domain := .photonicOpticalField

/-- Latency values in this initial formal foundation are integer picoseconds. -/
abbrev Picoseconds := Nat

/-- Serial-additive latency acceptance predicate. The serial model is explicit. -/
def pipelineWithinBudget (stageLatencies : List Picoseconds)
    (budget : Picoseconds) : Bool :=
  stageLatencies.sum <= budget

/-- Shared-fixture arithmetic: 10 + 5 + 40 + 30 + 120 + 15 + 8 = 228 ps. -/
def budget001StageLatencies : List Picoseconds := [10, 5, 40, 30, 120, 15, 8]

def budget001Limit : Picoseconds := 200

theorem budget001_total_is_228 : budget001StageLatencies.sum = 228 := by
  decide

theorem budget001_exceeds_budget : budget001StageLatencies.sum > budget001Limit := by
  decide

theorem budget001_rejected :
    pipelineWithinBudget budget001StageLatencies budget001Limit = false := by
  decide

theorem in_flight_representation_is_optical_field :
    inFlightRepresentation = .photonicOpticalField := by
  rfl

end EISVLPI
