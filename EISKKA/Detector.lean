module

import EISKKA.Scalar

/-!
# EIS-KKA-FORMAL-001 — Detector sign and phase-reference contract

The ideal balanced output is the signed cross term 2 Re(A conjugate(B)).
A common rotation of both fields leaves this value unchanged. Swapping the
electrical detector polarity reverses the reported sign; swapping optical
arms does not.
-/

namespace EISKKA

namespace Field

/-- Apply a common optical phase-reference rotation to a Cartesian field. -/
def rotate (θ : ℝ) (a : Field) : Field :=
  ⟨a.re * Real.cos θ - a.im * Real.sin θ,
   a.re * Real.sin θ + a.im * Real.cos θ⟩

/-- A common phase-reference rotation preserves the signed interference cross term. -/
theorem crossTerm_common_rotation (θ : ℝ) (a b : Field) :
    crossTerm (rotate θ a) (rotate θ b) = crossTerm a b := by
  cases a with
  | mk ar ai =>
    cases b with
    | mk br bi =>
      simp [rotate, crossTerm]
      nlinarith [Real.sin_sq_add_cos_sq θ]

/-- Interchanging the two optical arms does not reverse the real cross term. -/
theorem crossTerm_optical_arm_swap (a b : Field) :
    crossTerm b a = crossTerm a b := by
  exact crossTerm_symm b a

end Field

/-- Electrical polarity convention for the differential detector output. -/
inductive DetectorPolarity where
  | plusMinus
  | minusPlus
  deriving DecidableEq, Repr

/-- Signed ideal balanced-detector output under the selected electrical polarity. -/
def detectorOutput (polarity : DetectorPolarity) (a b : Field) : ℝ :=
  match polarity with
  | .plusMinus => Field.crossTerm a b
  | .minusPlus => - Field.crossTerm a b

/-- Reversing the electrical subtraction order reverses the detector sign. -/
theorem detector_polarity_reversal (a b : Field) :
    detectorOutput .minusPlus a b = - detectorOutput .plusMinus a b := by
  rfl

/-- The plus-minus convention is exactly the factor-two real cross term. -/
theorem detector_plusMinus_contract (a b : Field) :
    detectorOutput .plusMinus a b =
      2 * (Field.mul a (Field.conj b)).re := by
  exact Field.crossTerm_eq_two_mul_conj_re a b

end EISKKA
