module

public import QuantumInfo.ForMathlib.HermitianMat.Unitary

@[expose] public section

/-!
# EIS-KKA-FORMAL-001 — Physlib dependency boundary

This module records the available unitary-group abstraction and the pinned
Physlib/QuantumInfo dependencies. The CKM phase-shift definitions are
three-mode particle-physics objects; they are not reused or presented as an
optical MZI model.

No EIS two-mode phase-shifter specialization is asserted here. Such a
specialization must be introduced only with its own explicit optical
conventions and independently checked Lean proofs.
-/

namespace EISKKA

/-- Two-port unitary transformations over complex amplitudes. -/
abbrev TwoPortUnitary := 𝐔[Fin 2]

end EISKKA
