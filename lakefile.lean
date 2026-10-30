import Lake
open Lake DSL

package eisOptInterference where
  version := v!"0.1.0"

require mathlib from git
  "https://github.com/leanprover-community/mathlib4" @ "v4.19.0"

@[default_target]
lean_lib EIS where
  srcDir := "Lean"
