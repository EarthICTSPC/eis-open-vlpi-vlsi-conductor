module

import QuantumInfo.ForMathlib.HermitianMat.Unitary
import Physlib.Particles.FlavorPhysics.CKMMatrix.Basic

/-!
# EIS-KKA-FORMAL-001 — PhysLean / Physlib bridge

Physlib (the successor to the PhysLean repository) supplies the unitary-group
abstraction used here. Its CKM phase-shift module provides a reviewed diagonal
phase-matrix construction and composition lemmas. The 3-mode CKM object is
not reused as an optical MZI; EIS defines the corresponding 2-mode specialization
below, preserving the same algebraic structure.

The imported Physlib code is a mathematical library dependency, not a claim
that its particle-physics model describes a photonic device.
-/

open Matrix Complex

namespace EISKKA

/-- Two-port unitary transformations, using Physlib's unitary-group notation. -/
abbrev TwoPortUnitary := 𝐔[Fin 2]

/-- Two-mode diagonal phase-shift matrix, specialized from the Physlib pattern. -/
def phaseShiftMatrix2 (a b : ℝ) : Matrix (Fin 2) (Fin 2) ℂ :=
  ![![cexp (I * a), 0], ![0, cexp (I * b)]]

/-- The two-mode zero phase-shift matrix is the identity. -/
lemma phaseShiftMatrix2_one : phaseShiftMatrix2 0 0 = 1 := by
  ext i j
  fin_cases i <;> fin_cases j <;> simp [phaseShiftMatrix2, one_apply]

/-- Conjugate transpose negates the two phase shifts. -/
lemma phaseShiftMatrix2_star (a b : ℝ) :
    (phaseShiftMatrix2 a b)ᴴ = phaseShiftMatrix2 (-a) (-b) := by
  funext i j
  fin_cases i <;> fin_cases j <;>
    simp [phaseShiftMatrix2, conjTranspose_apply, ← exp_conj, conj_I, conj_ofReal]

/-- Multiplication of phase-shift matrices adds the phase coordinates. -/
lemma phaseShiftMatrix2_mul (a b c d : ℝ) :
    phaseShiftMatrix2 a b * phaseShiftMatrix2 c d =
      phaseShiftMatrix2 (a + c) (b + d) := by
  ext i j
  fin_cases i <;> fin_cases j <;>
    simp [phaseShiftMatrix2, mul_apply, Fin.sum_univ_two, ← exp_add, mul_add]

/-- The two-mode phase-shift matrix packaged as a Physlib unitary-group element. -/
def phaseShift2 (a b : ℝ) : TwoPortUnitary :=
  ⟨phaseShiftMatrix2 a b, by
    rw [Matrix.mem_unitaryGroup_iff]
    change _ * (phaseShiftMatrix2 a b)ᴴ = 1
    rw [phaseShiftMatrix2_star, phaseShiftMatrix2_mul, ← phaseShiftMatrix2_one]
    simp only [phaseShiftMatrix2, add_neg_cancel, ofReal_zero, mul_zero, exp_zero]⟩

/-- Coercion from the unitary-group element returns its phase-shift matrix. -/
@[simp] lemma phaseShift2_coe (a b : ℝ) :
    (phaseShift2 a b : Matrix (Fin 2) (Fin 2) ℂ) = phaseShiftMatrix2 a b := rfl

/-- Physlib's existing three-mode phase-shift composition theorem, re-exported for traceability. -/
theorem physlib_threeMode_phaseShift_mul (a b c d e f : ℝ) :
    phaseShiftMatrix a b c * phaseShiftMatrix d e f =
      phaseShiftMatrix (a + d) (b + e) (c + f) :=
  phaseShiftMatrix_mul a b c d e f

end EISKKA
