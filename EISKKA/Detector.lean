module

import EISKKA.Scalar

/-!
# EIS-KKA-FORMAL-001 — Detector sign, phase-reference and normalization contract

The optical field convention is the EIS positive-time phasor convention
Re(Ẽ exp(+i ω t)). For an ideal 50:50 coupler with output fields
(A+B)/sqrt(2) and (A-B)/sqrt(2), the optical intensity difference is
2 Re(A conjugate(B)). Detector responsivity multiplies this optical difference.
The electrical output polarity is I_plus - I_minus.
-/

namespace EISKKA

namespace Field

/-- Apply a common optical phase-reference rotation to a Cartesian field. -/
def rotate (θ : ℝ) (a : Field) : Field :=
  ⟨a.re * Real.cos θ - a.im * Real.sin θ,
   a.re * Real.sin θ + a.im * Real.cos θ⟩

/-- Difference of two complex field envelopes. -/
def sub (a b : Field) : Field :=
  ⟨a.re - b.re, a.im - b.im⟩

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

/--
The difference between the unscaled output intensities of the sum and
difference ports is twice the signed cross term.
-/
theorem sum_difference_intensity (a b : Field) :
    normSq (add a b) - normSq (sub a b) = 2 * crossTerm a b := by
  cases a with
  | mk ar ai =>
    cases b with
    | mk br bi =>
      simp [normSq, add, sub, crossTerm]
      ring

end Field

/-- Electrical polarity convention for the differential detector output. -/
inductive DetectorPolarity where
  | plusMinus
  | minusPlus
  deriving DecidableEq, Repr

/-- Signed ideal balanced-detector cross term under the selected polarity. -/
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

/--
Detector normalization metadata. fieldScaleSq is the squared field
coefficient applied to each ideal sum/difference output port. For a 50:50
coupler using (A±B)/sqrt(2), it is exactly 1/2. Responsivity is in A/W
when the optical intensities are in W.
-/
structure DetectorNormalization where
  responsivity : ℝ
  fieldScaleSq : ℝ

/-- The optical intensity difference after the declared coupler normalization. -/
def normalizedOpticalDifference
    (normalization : DetectorNormalization) (a b : Field) : ℝ :=
  normalization.fieldScaleSq *
    (Field.normSq (Field.add a b) - Field.normSq (Field.sub a b))

/-- The normalized optical difference is the declared scale times the cross term. -/
theorem normalizedOpticalDifference_contract
    (normalization : DetectorNormalization) (a b : Field) :
    normalizedOpticalDifference normalization a b =
      (2 * normalization.fieldScaleSq) * Field.crossTerm a b := by
  rw [normalizedOpticalDifference, Field.sum_difference_intensity]
  ring

/-- Electrical output including responsivity, optical normalization and polarity. -/
def normalizedDetectorOutput
    (normalization : DetectorNormalization) (polarity : DetectorPolarity)
    (a b : Field) : ℝ :=
  normalization.responsivity *
    (2 * normalization.fieldScaleSq) * detectorOutput polarity a b

/--
For the 50:50 field normalization (A±B)/sqrt(2), the plus-minus detector
output is R times 2 Re(A conjugate(B)).
-/
theorem detector_50_50_plusMinus
    (normalization : DetectorNormalization) (a b : Field)
    (hscale : normalization.fieldScaleSq = 1 / 2) :
    normalizedDetectorOutput normalization .plusMinus a b =
      normalization.responsivity *
        (2 * (Field.mul a (Field.conj b)).re) := by
  simp [normalizedDetectorOutput, detectorOutput, hscale,
    Field.crossTerm_eq_two_mul_conj_re]

/-- Reversing polarity negates the normalized detector output. -/
theorem normalized_detector_polarity_reversal
    (normalization : DetectorNormalization) (a b : Field) :
    normalizedDetectorOutput normalization .minusPlus a b =
      - normalizedDetectorOutput normalization .plusMinus a b := by
  simp [normalizedDetectorOutput, detectorOutput]

end EISKKA
