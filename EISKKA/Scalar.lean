module

import Mathlib

/-!
# EIS-KKA-SOI-001 — scalar field and interference contract

This module formalizes the device-independent scalar contract.  A field is
represented by its Cartesian coordinates over the mathematical reals.  This
is an exact mathematical model of a complex envelope, not an IEEE-754 value
and not a physical device model.

The transfer coefficients are supplied inputs.  No SOI, TPA, Kerr, thermal,
or Kramers–Kronig mechanism is postulated here.
-/

namespace EISKKA

/-- Exact Cartesian representation of a dimensionless complex field envelope. -/
structure Field where
  re : ℝ
  im : ℝ

namespace Field

/-- Addition of coherent field envelopes. -/
def add (a b : Field) : Field :=
  ⟨a.re + b.re, a.im + b.im⟩

/-- Complex conjugation. -/
def conj (a : Field) : Field :=
  ⟨a.re, -a.im⟩

/-- Complex multiplication, used for independently supplied path transfers. -/
def mul (a b : Field) : Field :=
  ⟨a.re * b.re - a.im * b.im, a.re * b.im + a.im * b.re⟩

/-- Squared field magnitude |a|². -/
def normSq (a : Field) : ℝ :=
  a.re ^ 2 + a.im ^ 2

/-- Ideal coherent total intensity |a+b|². -/
def totalIntensity (a b : Field) : ℝ :=
  normSq (add a b)

/-- Signed balanced interference cross term: 2 Re(a * conjugate(b)). -/
def crossTerm (a b : Field) : ℝ :=
  2 * (a.re * b.re + a.im * b.im)

/-- The scalar cross term is exactly twice the real part of a * conjugate(b). -/
theorem crossTerm_eq_two_mul_conj_re (a b : Field) :
    crossTerm a b = 2 * (mul a (conj b)).re := by
  cases a with
  | mk ar ai =>
    cases b with
    | mk br bi =>
      simp [crossTerm, mul, conj]

/-- Polar representation of a field with real amplitude and phase. -/
noncomputable def polar (amplitude phase : ℝ) : Field :=
  ⟨amplitude * Real.cos phase, amplitude * Real.sin phase⟩

/-- The cross term in polar coordinates is 2AB cos(phase difference). -/
theorem crossTerm_polar (amplitudeA amplitudeB phaseA phaseB : ℝ) :
    crossTerm (polar amplitudeA phaseA) (polar amplitudeB phaseB) =
      2 * amplitudeA * amplitudeB * Real.cos (phaseA - phaseB) := by
  simp [crossTerm, polar]
  rw [Real.cos_sub]
  ring

/-- Apply an independently supplied complex transfer to a field. -/
def transfer (t a : Field) : Field :=
  mul t a

/-- Interference after independently transferring the two operand paths. -/
def transferredCrossTerm (ta a tb b : Field) : ℝ :=
  crossTerm (transfer ta a) (transfer tb b)

@[simp] theorem crossTerm_symm (a b : Field) :
    crossTerm a b = crossTerm b a := by
  cases a
  cases b
  simp [crossTerm]
  ring

@[simp] theorem crossTerm_conj_invariant (a b : Field) :
    crossTerm (conj a) (conj b) = crossTerm a b := by
  cases a
  cases b
  simp [crossTerm, conj]

@[simp] theorem crossTerm_zero_left (b : Field) :
    crossTerm ⟨0, 0⟩ b = 0 := by
  simp [crossTerm]

@[simp] theorem crossTerm_zero_right (a : Field) :
    crossTerm a ⟨0, 0⟩ = 0 := by
  simp [crossTerm]

/-- The intensity expansion fixes the factor-of-two convention. -/
theorem totalIntensity_eq_norms_add_cross (a b : Field) :
    totalIntensity a b = normSq a + normSq b + crossTerm a b := by
  cases a
  cases b
  simp [totalIntensity, normSq, add, crossTerm]
  ring

/--
Cauchy-Schwarz bound in squared form.  This avoids importing an analytic
square-root convention into the core operator contract.
-/
theorem crossTerm_sq_le (a b : Field) :
    crossTerm a b ^ 2 ≤ 4 * normSq a * normSq b := by
  cases a with
  | mk ar ai =>
    cases b with
    | mk br bi =>
      simp [crossTerm, normSq]
      nlinarith [sq_nonneg (ar * bi - ai * br)]

/-- Absolute-value Cauchy-Schwarz bound for the signed interference cross term. -/
theorem crossTerm_abs_le (a b : Field) :
    |crossTerm a b| ≤ 2 * Real.sqrt (normSq a) * Real.sqrt (normSq b) := by
  have ha : 0 ≤ normSq a := by
    cases a with
    | mk ar ai =>
      change 0 ≤ ar ^ 2 + ai ^ 2
      positivity
  have hb : 0 ≤ normSq b := by
    cases b with
    | mk br bi =>
      change 0 ≤ br ^ 2 + bi ^ 2
      positivity
  have hsa : Real.sqrt (normSq a) ^ 2 = normSq a := Real.sq_sqrt ha
  have hsb : Real.sqrt (normSq b) ^ 2 = normSq b := Real.sq_sqrt hb
  have hsq := crossTerm_sq_le a b
  have hbound_nonneg :
      0 ≤ 2 * Real.sqrt (normSq a) * Real.sqrt (normSq b) := by
    positivity
  have hbound_sq :
      (2 * Real.sqrt (normSq a) * Real.sqrt (normSq b)) ^ 2 =
        4 * normSq a * normSq b := by
    calc
      _ = 4 * (Real.sqrt (normSq a)) ^ 2 *
          (Real.sqrt (normSq b)) ^ 2 := by ring
      _ = _ := by rw [hsa, hsb]
  nlinarith [sq_abs (crossTerm a b)]

/-- Complex transfer distributes over no assumed device model: it is simply multiplication. -/
theorem transfer_coordinates (t a : Field) :
    (transfer t a).re = t.re * a.re - t.im * a.im ∧
    (transfer t a).im = t.re * a.im + t.im * a.re := by
  constructor <;> rfl

end Field

end EISKKA

#print axioms EISKKA.Field.crossTerm_symm
#print axioms EISKKA.Field.crossTerm_conj_invariant
#print axioms EISKKA.Field.crossTerm_zero_left
#print axioms EISKKA.Field.crossTerm_zero_right
#print axioms EISKKA.Field.totalIntensity_eq_norms_add_cross
#print axioms EISKKA.Field.crossTerm_sq_le
#print axioms EISKKA.Field.crossTerm_abs_le
#print axioms EISKKA.Field.crossTerm_eq_two_mul_conj_re
#print axioms EISKKA.Field.crossTerm_polar
#print axioms EISKKA.Field.transfer_coordinates
