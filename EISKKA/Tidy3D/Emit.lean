import Lean
import EISKKA.Tidy3D.Spec

/-! Executable JSON emitter for EIS-TIDY3D-LEAN-001. -/

def main : IO Unit := do
  IO.println (EISKKA.Tidy3D.toJson EISKKA.Tidy3D.illustrativeSOI).compress
