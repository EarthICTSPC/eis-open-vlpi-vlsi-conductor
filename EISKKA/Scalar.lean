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
#print axioms EISKKA.Field.transfer_coordinates
