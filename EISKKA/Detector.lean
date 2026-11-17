module

import Mathlib
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

/-- Apply a common optical phase-reference rotation to a Cartesian field. -/
def rotateField (θ : ℝ) (a : _root_.EISKKA.Field) : _root_.EISKKA.Field :=
  ⟨a.re * Real.cos θ - a.im * Real.sin θ,
   a.re * Real.sin θ + a.im * Real.cos θ⟩

/-- Difference of two complex field envelopes. -/
def subtractField (a b : _root_.EISKKA.Field) : _root_.EISKKA.Field :=
  ⟨a.re - b.re, a.im - b.im⟩

/-- A common phase-reference rotation preserves the signed interference cross term. -/
theorem crossTerm_common_rotation (θ : ℝ) (a b : _root_.EISKKA.Field) :
    _root_.EISKKA.Field.crossTerm (rotateField θ a) (rotateField θ b) =
      _root_.EISKKA.Field.crossTerm a b := by
  cases a with
  | mk ar ai =>
    cases b with
    | mk br bi =>
      simp [rotateField, _root_.EISKKA.Field.crossTerm]
      nlinarith [Real.sin_sq_add_cos_sq θ]

/-- Interchanging the two optical arms does not reverse the real cross term. -/
theorem crossTerm_optical_arm_swap (a b : _root_.EISKKA.Field) :
    _root_.EISKKA.Field.crossTerm b a =
      _root_.EISKKA.Field.crossTerm a b :=
  _root_.EISKKA.Field.crossTerm_symm b a

/--
The difference between the unscaled output intensities of the sum and
difference ports is twice the signed cross term.
-/
theorem sum_difference_intensity (a b : _root_.EISKKA.Field) :
    _root_.EISKKA.Field.normSq (_root_.EISKKA.Field.add a b) -
      _root_.EISKKA.Field.normSq (subtractField a b) =
        2 * _root_.EISKKA.Field.crossTerm a b := by
  cases a with
  | mk ar ai =>
    cases b with
    | mk br bi =>
      simp [_root_.EISKKA.Field.normSq, _root_.EISKKA.Field.add,
        subtractField, _root_.EISKKA.Field.crossTerm]
      ring

/-- Electrical polarity convention for the differential detector output. -/
inductive DetectorPolarity where
  | plusMinus
  | minusPlus
  deriving DecidableEq, Repr

/-- Signed ideal balanced-detector cross term under the selected polarity. -/
def detectorOutput
    (polarity : DetectorPolarity) (a b : _root_.EISKKA.Field) : ℝ :=
  match polarity with
  | .plusMinus => _root_.EISKKA.Field.crossTerm a b
  | .minusPlus => - _root_.EISKKA.Field.crossTerm a b

/-- Reversing the electrical subtraction order reverses the detector sign. -/
theorem detector_polarity_reversal (a b : _root_.EISKKA.Field) :
    detectorOutput .minusPlus a b = - detectorOutput .plusMinus a b :=
  rfl

/-- The plus-minus convention is exactly the factor-two real cross term. -/
theorem detector_plusMinus_contract (a b : _root_.EISKKA.Field) :
    detectorOutput .plusMinus a b =
      2 * (_root_.EISKKA.Field.mul a (_root_.EISKKA.Field.conj b)).re :=
  _root_.EISKKA.Field.crossTerm_eq_two_mul_conj_re a b

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
    (normalization : DetectorNormalization) (a b : _root_.EISKKA.Field) : ℝ :=
  normalization.fieldScaleSq *
    (_root_.EISKKA.Field.normSq (_root_.EISKKA.Field.add a b) -
      _root_.EISKKA.Field.normSq (subtractField a b))

/-- The normalized optical difference is the declared scale times the cross term. -/
theorem normalizedOpticalDifference_contract
    (normalization : DetectorNormalization) (a b : _root_.EISKKA.Field) :
    normalizedOpticalDifference normalization a b =
      (2 * normalization.fieldScaleSq) * _root_.EISKKA.Field.crossTerm a b := by
  rw [normalizedOpticalDifference, sum_difference_intensity]
  ring

/-- Electrical output including responsivity, optical normalization and polarity. -/
def normalizedDetectorOutput
    (normalization : DetectorNormalization) (polarity : DetectorPolarity)
    (a b : _root_.EISKKA.Field) : ℝ :=
  normalization.responsivity *
    (2 * normalization.fieldScaleSq) * detectorOutput polarity a b

/--
For the 50:50 field normalization (A±B)/sqrt(2), the plus-minus detector
output is R times 2 Re(A conjugate(B)).
-/
theorem detector_50_50_plusMinus
    (normalization : DetectorNormalization) (a b : _root_.EISKKA.Field)
    (hscale : normalization.fieldScaleSq = 1 / 2) :
    normalizedDetectorOutput normalization .plusMinus a b =
      normalization.responsivity *
        (2 * (_root_.EISKKA.Field.mul a (_root_.EISKKA.Field.conj b)).re) := by
  simp [normalizedDetectorOutput, detectorOutput, hscale,
    _root_.EISKKA.Field.crossTerm_eq_two_mul_conj_re]
  ring

/-- Reversing polarity negates the normalized detector output. -/
theorem normalized_detector_polarity_reversal
    (normalization : DetectorNormalization) (a b : _root_.EISKKA.Field) :
    normalizedDetectorOutput normalization .minusPlus a b =
      - normalizedDetectorOutput normalization .plusMinus a b := by
  simp [normalizedDetectorOutput, detectorOutput]

end EISKKA
