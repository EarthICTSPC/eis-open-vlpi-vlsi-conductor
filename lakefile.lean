import Lake
open Lake DSL

package eisKka where
  version := v!"0.1.0"

-- Mathlib v4.35.0, pinned to its immutable resolved commit.
require mathlib from git
  "https://github.com/leanprover-community/mathlib4" @ "56a005855ea17e0b0958f73ec801ae140b0a1679"

-- Physlib (formerly PhysLean / Lean-QuantumInfo), pinned to an immutable commit.
require Physlib from git
  "https://github.com/leanprover-community/physlib" @ "be0a9eef7dac78da524bfbde91c812340b194610"

@[default_target]
lean_lib EISKKA

lean_exe eis_tidy3d_spec where
  root := `EISKKA.Tidy3D.Emit
