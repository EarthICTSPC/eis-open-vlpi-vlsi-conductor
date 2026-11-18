import Lake
open Lake DSL

package eisKka where
  version := v!"0.1.0"

require mathlib from git
  "https://github.com/leanprover-community/mathlib4" @ "56a005855ea17e0b0958f73ec801ae140b0a1679"

lean_lib EISKKA

lean_exe eis_kka_bench_001a where
  root := `EISKKA.Bench001A
