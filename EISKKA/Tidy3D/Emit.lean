module

public import Lean
public import EISKKA.Tidy3D.Spec

@[expose] public section

/-! Executable JSON emitter for EIS-TIDY3D-LEAN-001. -/

def main : IO Unit := do
  IO.println (EISKKA.Tidy3D.toJson EISKKA.Tidy3D.illustrativeSOI).compress
