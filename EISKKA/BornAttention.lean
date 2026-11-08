import EISKKA.Scalar

/-!
# EIS-BORN-KKA-001 — Born attention and KKA computational contract

This module formalizes the mathematical attention score and scalar bilinear
readout bridge. It does not model an optical mesh, detector, modulator,
normalization circuit, device transfer, or energy consumption.

A vector is a finite family of EISKKA.Field values. Its overlap is the
complex inner product sum q[r] * conjugate(k[r]). Born attention uses
the fourth power of the overlap magnitude and requires a strictly positive
row denominator.
-/

namespace EISKKA.Born

open Finset

/-- Complex overlap <q,k> = sum_r q[r] * conjugate(k[r]). -/
def overlap {d : ℕ} (q k : Fin d → EISKKA.Field.Field) : Field :=
  ⟨
    ∑ r : Fin d, (Field.mul (q r) (Field.conj (k r))).re,
    ∑ r : Fin d, (Field.mul (q r) (Field.conj (k r))).im
  ⟩

/-- Born score |<q,k>|^4 = (|<q,k>|^2)^2. -/
def bornScore {d : ℕ} (q k : Fin d → EISKKA.Field.Field) : ℝ :=
  (Field.normSq (overlap q k)) ^ 2

/-- Quadrature form of the fourth-power score. -/
def quadratureScore (re im : ℝ) : ℝ :=
  (re ^ 2 + im ^ 2) ^ 2

/-- The overlap score is exactly the squared intensity of its two quadratures. -/
theorem bornScore_eq_quadratureScore {d : ℕ} (q k : Fin d → EISKKA.Field.Field) :
    bornScore q k = quadratureScore (overlap q k).re (overlap q k).im := by
  rfl

/-- Born scores are nonnegative. -/
theorem bornScore_nonneg {d : ℕ} (q k : Fin d → EISKKA.Field.Field) :
    0 ≤ bornScore q k := by
  unfold bornScore
  exact sq_nonneg _

/-- Sum of Born scores across the keys for one query row. -/
def rowDenominator {d m : ℕ}
    (q : Fin d → EISKKA.Field.Field) (keys : Fin m → Fin d → EISKKA.Field.Field) : ℝ :=
  ∑ j : Fin m, bornScore q (keys j)

/-- A Born attention weight. Its denominator must be strictly positive. -/
def bornWeight {d m : ℕ}
    (q : Fin d → EISKKA.Field.Field) (keys : Fin m → Fin d → EISKKA.Field.Field) (j : Fin m) : ℝ :=
  bornScore q (keys j) / rowDenominator q keys

/-- Every row denominator is nonnegative. -/
theorem rowDenominator_nonneg {d m : ℕ}
    (q : Fin d → EISKKA.Field.Field) (keys : Fin m → Fin d → EISKKA.Field.Field) :
    0 ≤ rowDenominator q keys := by
  unfold rowDenominator
  apply Finset.sum_nonneg
  intro j hj
  exact bornScore_nonneg q (keys j)

/-- With a positive denominator, every Born attention weight is nonnegative. -/
theorem bornWeight_nonneg {d m : ℕ}
    (q : Fin d → EISKKA.Field.Field) (keys : Fin m → Fin d → EISKKA.Field.Field)
    (j : Fin m) (hden : 0 < rowDenominator q keys) :
    0 ≤ bornWeight q keys j := by
  unfold bornWeight
  exact div_nonneg (bornScore_nonneg q (keys j)) (le_of_lt hden)

/-- Positive-denominator Born attention weights sum exactly to one. -/
theorem rowWeights_sum_one {d m : ℕ}
    (q : Fin d → EISKKA.Field.Field) (keys : Fin m → Fin d → EISKKA.Field.Field)
    (hden : 0 < rowDenominator q keys) :
    (∑ j : Fin m, bornWeight q keys j) = 1 := by
  unfold bornWeight rowDenominator
  rw [Finset.sum_div]
  exact div_self (ne_of_gt hden)

/-- Each normalized Born attention weight is at most one. -/
theorem bornWeight_le_one {d m : ℕ}
    (q : Fin d → EISKKA.Field.Field) (keys : Fin m → Fin d → EISKKA.Field.Field)
    (j : Fin m) (hden : 0 < rowDenominator q keys) :
    bornWeight q keys j ≤ 1 := by
  have hscore : 0 ≤ bornScore q (keys j) :=
    bornScore_nonneg q (keys j)
  have hsingle : bornScore q (keys j) ≤ rowDenominator q keys := by
    unfold rowDenominator
    exact Finset.single_le_sum
      (fun k hk => bornScore_nonneg q (keys k))
      (Finset.mem_univ j)
  unfold bornWeight
  rw [div_le_iff₀ hden]
  simpa using hsingle

/-- Scalar measured bilinear feed-forward readout Re(x*y). -/
def bilinearReadout (x y : EISKKA.Field.Field) : ℝ :=
  (Field.mul x y).re

/--
The measured bilinear readout is half the EIS signed KKA cross-term when
the second operand is conjugated before the KKA primitive:
2*Re(x*y) = X(x, conjugate(y)).
This is an algebraic identity, not a physical conjugator or circuit claim.
-/
theorem bilinearReadout_eq_kka_crossTerm (x y : EISKKA.Field.Field) :
    2 * bilinearReadout x y = Field.crossTerm x (Field.conj y) := by
  unfold bilinearReadout
  rw [Field.crossTerm_eq_two_mul_conj_re]
  simp [Field.conj]

end EISKKA.Born
