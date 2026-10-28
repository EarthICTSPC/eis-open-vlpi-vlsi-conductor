import Mathlib

/-!
# EIS-OPT-INTERFERENCE-001 — ideal mathematical contract

This module formalizes an ideal real-coordinate field model. It does not model
loss, coupler imbalance, detector noise, phase error, calibration, or a fabricated
device. The observable convention is fixed here as
`I(a,b) = 2 * (a.re*b.re + a.im*b.im)`.
-/

namespace EIS.OptInterference

structure Field where
  re : ℝ
  im : ℝ
  deriving Repr, DecidableEq

/-- Ideal interference observable `2 Re(a * conjugate(b))`. -/
def contract (a b : Field) : ℝ :=
  2 * (a.re * b.re + a.im * b.im)

/-- Squared field magnitude / ideal intensity. -/
def intensity (z : Field) : ℝ := z.re ^ 2 + z.im ^ 2

/-- Coordinate identity for the chosen real-coordinate representation. -/
theorem contract_coordinate_identity (a b : Field) :
    contract a b = 2 * (a.re * b.re + a.im * b.im) := by
  rfl

/-- Interference is symmetric in its two field inputs. -/
theorem contract_symmetric (a b : Field) :
    contract a b = contract b a := by
  simp [contract]
  ring

/-- Self-interference equals twice the ideal intensity. -/
theorem contract_self (a : Field) :
    contract a a = 2 * intensity a := by
  simp [contract, intensity]

/-- A zero first input gives zero interference. -/
theorem contract_zero_left (b : Field) :
    contract ⟨0, 0⟩ b = 0 := by
  simp [contract]

/-- A zero second input gives zero interference. -/
theorem contract_zero_right (a : Field) :
    contract a ⟨0, 0⟩ = 0 := by
  simp [contract]

end EIS.OptInterference
