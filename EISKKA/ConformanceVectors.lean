import EISKKA.Scalar

/-!
Exact rational/integer examples for the scalar operator.  These named
examples are the formal anchors for the JSON/Python conformance vectors.
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

theorem constructive_cross :
    crossTerm constructiveA constructiveB = 4 := by
  norm_num [constructiveA, constructiveB, crossTerm]

theorem constructive_total :
    totalIntensity constructiveA constructiveB = 9 := by
  norm_num [constructiveA, constructiveB, totalIntensity, normSq, add]

theorem destructive_cross :
    crossTerm constructiveA destructiveB = -4 := by
  norm_num [constructiveA, destructiveB, constructiveA, crossTerm]

theorem quadrature_cross :
    crossTerm constructiveA quadratureB = 0 := by
  norm_num [constructiveA, quadratureB, crossTerm]

theorem unequal_complex_cross :
    crossTerm unequalA unequalB = 8 := by
  norm_num [unequalA, unequalB, crossTerm]

theorem zero_operand_cross :
    crossTerm zeroA zeroB = 0 := by
  norm_num [zeroA, zeroB, crossTerm]

end EISKKA.ConformanceVectors
