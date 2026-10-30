import EIS.OptInterference

/-!
# Typed ideal two-input, two-output interferometer

The netlist denotes the unnormalised sum/difference transform. Its two output
intensities are combined as half their difference. This convention makes that
balanced observable equal the EIS interference contract. This is a mathematical
reference model, not a foundry PDK model or a claim of physical conformance.
-/

namespace EIS.OptInterference

/-- Port direction is part of the port's type. -/
inductive Direction where
  | input
  | output
  deriving DecidableEq, Repr

/-- The four named ports, indexed by direction so input/output ports cannot be
accidentally interchanged at the type level. -/
inductive Port : Direction → Type where
  | inputA : Port .input
  | inputB : Port .input
  | outputSum : Port .output
  | outputDifference : Port .output

/-- A typed 2×2 interferometer netlist with two explicitly named input ports. -/
structure InterferometerNetlist where
  inputA : Port .input := .inputA
  inputB : Port .input := .inputB

/-- Semantic values observed at the two output ports. -/
structure OutputBundle where
  sum : Field
  difference : Field
  deriving Repr, DecidableEq

/-- The denotation of the netlist: constructive sum and difference outputs. -/
def denote (_netlist : InterferometerNetlist) (a b : Field) : OutputBundle :=
  { sum := ⟨a.re + b.re, a.im + b.im⟩
    difference := ⟨a.re - b.re, a.im - b.im⟩ }

/-- Balanced output observable: half the difference of output intensities. -/
def balancedObservable (outputs : OutputBundle) : ℝ :=
  (intensity outputs.sum - intensity outputs.difference) / 2

/-- The netlist semantics satisfy the EIS interference contract.

This theorem explicitly composes the netlist denotation with the balanced output
observable and equates the result to the independently defined contract. -/
theorem netlist_semantics_satisfy_contract
    (netlist : InterferometerNetlist) (a b : Field) :
    balancedObservable (denote netlist a b) = contract a b := by
  simp [balancedObservable, denote, intensity, contract]
  ring

end EIS.OptInterference
