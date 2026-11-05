import Lake
open Lake DSL

package «eis-kka» where
  version := v!"0.1.0"

-- Mathlib release v4.35.0, pinned to the immutable commit resolved from the tag.
require mathlib from git
  "https://github.com/leanprover-community/mathlib4" @ "56a005855ea17e0b0958f73ec801ae140b0a1679"

lean_lib EISKKA
