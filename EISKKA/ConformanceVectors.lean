module

import EISKKA.Scalar

/-!
Exact rational/integer examples for the scalar operator. These named
theorems are formal anchors for the JSON/Python conformance vectors.
The Python side uses binary64 approximations with its separately declared
1e-12 software tolerance.
-/

namespace EISKKA.ConformanceVectors

open EISKKA.Field

def constructiveA : Field := ⟨1, 0⟩
def constructiveB : Field := ⟨2, 0⟩
def destructiveB : Field := ⟨-2, 0⟩
def quadratureB : Field := ⟨0, 1⟩
def unequalA : Field := ⟨2, 1⟩
def unequalB : Field := ⟨1, 2⟩
def zeroA : Field := ⟨0, 0⟩
def zeroB : Field := ⟨3, -4⟩
def zeroRightA : Field := ⟨-3, 4⟩
def zeroRightB : Field := ⟨0, 0⟩
def complexQuadratureA : Field := ⟨1, 1⟩
def complexQuadratureB : Field := ⟨-1, 1⟩
def generalA : Field := ⟨(1 : ℝ) / 4, -(3 : ℝ) / 4⟩
def generalB : Field := ⟨-(1 : ℝ) / 2, (1 : ℝ) / 8⟩

def identityTransfer : Field := ⟨1, 0⟩
def phaseLossTransfer : Field := ⟨0, (1 : ℝ) / 2⟩
def zeroTransfer : Field := ⟨0, 0⟩
def inputField12 : Field := ⟨1, 2⟩
def inputField10 : Field := ⟨1, 0⟩
def inputField2m1 : Field := ⟨2, -1⟩

theorem constructive_cross :
    crossTerm constructiveA constructiveB = 4 := by
  norm_num [constructiveA, constructiveB, crossTerm]

theorem constructive_total :
    totalIntensity constructiveA constructiveB = 9 := by
  norm_num [constructiveA, constructiveB, totalIntensity, normSq, add]

theorem destructive_cross :
    crossTerm constructiveA destructiveB = -4 := by
  norm_num [constructiveA, destructiveB, crossTerm]

theorem quadrature_cross :
    crossTerm constructiveA quadratureB = 0 := by
  norm_num [constructiveA, quadratureB, crossTerm]

theorem unequal_complex_cross :
    crossTerm unequalA unequalB = 8 := by
  norm_num [unequalA, unequalB, crossTerm]

theorem zero_operand_cross :
    crossTerm zeroA zeroB = 0 := by
  norm_num [zeroA, zeroB, crossTerm]

theorem zero_right_operand_cross :
    crossTerm zeroRightA zeroRightB = 0 := by
  norm_num [zeroRightA, zeroRightB, crossTerm]

theorem complex_quadrature_cross :
    crossTerm complexQuadratureA complexQuadratureB = 0 := by
  norm_num [complexQuadratureA, complexQuadratureB, crossTerm]

theorem general_complex_cross :
    crossTerm generalA generalB = -(7 : ℝ) / 16 := by
  norm_num [generalA, generalB, crossTerm]

theorem general_complex_total :
    totalIntensity generalA generalB = (29 : ℝ) / 64 := by
  norm_num [generalA, generalB, totalIntensity, normSq, add]

theorem transfer_identity :
    (transfer identityTransfer inputField12).re = 1 ∧
    (transfer identityTransfer inputField12).im = 2 := by
  constructor <;> norm_num [identityTransfer, inputField12, transfer, mul]

theorem transfer_phase_loss :
    (transfer phaseLossTransfer inputField10).re = 0 ∧
    (transfer phaseLossTransfer inputField10).im = (1 : ℝ) / 2 := by
  constructor <;> norm_num [phaseLossTransfer, inputField10, transfer, mul]

theorem transfer_zero :
    (transfer zeroTransfer inputField2m1).re = 0 ∧
    (transfer zeroTransfer inputField2m1).im = 0 := by
  constructor <;> norm_num [zeroTransfer, inputField2m1, transfer, mul]

end EISKKA.ConformanceVectors
