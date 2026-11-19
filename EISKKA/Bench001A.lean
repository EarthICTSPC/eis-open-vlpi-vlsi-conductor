module

public import Mathlib

open Lean

/-!
EIS-KKA-BENCH-001A
Formal boundary for Tian et al. PTC Eq. (1) and the attention comparison in Eq. (2).

This module proves the ideal two-field interference/BPD identities and exact
integer operation-count formulae. It deliberately does NOT prove that the
approximation in Tian Eq. (2) holds for arbitrary Q/K/V, nor that a physical
device realizes the ideal field model.
-/

namespace EISKKA.Bench001A

/-- A complex optical field represented by its real and imaginary components. -/
structure Field where
  re : ℝ
  im : ℝ

def add (a b : Field) : Field := ⟨a.re + b.re, a.im + b.im⟩
def sub (a b : Field) : Field := ⟨a.re - b.re, a.im - b.im⟩

/-- Squared field magnitude, |a|². -/
def intensity (a : Field) : ℝ := a.re ^ 2 + a.im ^ 2

/-- Re(a * conj(b)), expanded in real coordinates. -/
def crossTerm (a b : Field) : ℝ := a.re * b.re + a.im * b.im

/-- Tian PTC Eq. (1): total two-field interference intensity. -/
def interference (a b : Field) : ℝ :=
  intensity a + intensity b + 2 * crossTerm a b

/--
Exact expansion of the two-field interference identity:
|a+b|² = |a|² + |b|² + 2 Re(a conj(b)).
-/
theorem interference_identity (a b : Field) :
    intensity (add a b) = interference a b := by
  simp [intensity, add, interference, crossTerm]
  ring

/--
Ideal balanced photodetection with fields (a+b)/sqrt(2) and (a-b)/sqrt(2).
The factor 1/2 inside the difference is the 50:50 field-normalization factor.
-/
noncomputable def balancedDifference (responsivity : ℝ) (a b : Field) : ℝ :=
  responsivity * ((intensity (add a b) - intensity (sub a b)) / 2)

/-- The self-intensity terms cancel in ideal balanced detection. -/
theorem balanced_difference_identity (r : ℝ) (a b : Field) :
    balancedDifference r a b = 2 * r * crossTerm a b := by
  simp [balancedDifference, intensity, add, sub, crossTerm]
  ring

/-- Tensor dimensions used by the operation ledger for one attention invocation. -/
structure Shape where
  heads : Nat
  sequenceLength : Nat
  headDimension : Nat
  valueDimension : Nat
deriving Repr, DecidableEq

def scoreCount (s : Shape) : Nat :=
  s.heads * s.sequenceLength * s.sequenceLength

/-- Conventional QK multiply count, with one product per feature per score. -/
def qkMultiplications (s : Shape) : Nat :=
  scoreCount s * s.headDimension

/-- Conventional QK additions, using d-1 additions per dot product. -/
def qkAdditions (s : Shape) : Nat :=
  scoreCount s * (s.headDimension - 1)

/-- Conventional score scaling by 1/sqrt(d), one multiply per score. -/
def scoreScalingMultiplications (s : Shape) : Nat := scoreCount s

/-- Stable SoftMax row-maximum comparisons, using S-1 comparisons per row. -/
def softmaxRowMaxComparisons (s : Shape) : Nat :=
  s.heads * s.sequenceLength * (s.sequenceLength - 1)

/-- Stable SoftMax score subtractions, one per score. -/
def softmaxSubtractions (s : Shape) : Nat := scoreCount s

/-- Stable SoftMax exponentials, one per score. -/
def softmaxExponentials (s : Shape) : Nat := scoreCount s

/-- Stable SoftMax row-sum additions, using S-1 additions per row. -/
def softmaxRowSumAdditions (s : Shape) : Nat :=
  s.heads * s.sequenceLength * (s.sequenceLength - 1)

/-- Stable SoftMax normalization divisions, one per score. -/
def softmaxDivisions (s : Shape) : Nat := scoreCount s

/-- Conventional AV products, one per score and value channel. -/
def avMultiplications (s : Shape) : Nat :=
  scoreCount s * s.valueDimension

/-- Conventional AV additions, using S-1 additions per output channel. -/
def avAdditions (s : Shape) : Nat :=
  s.heads * s.sequenceLength * s.valueDimension * (s.sequenceLength - 1)

/--
Logical pairwise field-interference samples in the KKA QK stage.
This is an event count, not a FLOP count or a hardware-cycle count.
-/
def kkaQkInterferenceSamples (s : Shape) : Nat := qkMultiplications s

/--
Logical pairwise field-interference samples in the KKA value-aggregation stage.
This is an event count, not a FLOP count or a hardware-cycle count.
-/
def kkaAvInterferenceSamples (s : Shape) : Nat := avMultiplications s

def kkaAttentionInterferenceSamples (s : Shape) : Nat :=
  kkaQkInterferenceSamples s + kkaAvInterferenceSamples s

/-- The three elementwise SoftMax classes share the same score cardinality. -/
theorem softmax_elementwise_triad (s : Shape) :
    softmaxSubtractions s + softmaxExponentials s + softmaxDivisions s
      = 3 * scoreCount s := by
  simp [softmaxSubtractions, softmaxExponentials, softmaxDivisions]
  omega

/-- QK interference samples have the same logical pair cardinality as QK products. -/
theorem kka_qk_pair_count (s : Shape) :
    kkaQkInterferenceSamples s = qkMultiplications s := by
  rfl

/-- AV interference samples have the same logical pair cardinality as AV products. -/
theorem kka_av_pair_count (s : Shape) :
    kkaAvInterferenceSamples s = avMultiplications s := by
  rfl

/--
The following status is intentional: Tian Eq. (2) is an approximation claim
supported in the paper by RFF analysis and model/device experiments. It is not
a universal equality theorem for arbitrary tensors or physical devices.
-/
def tianEq2Status : String :=
  "approximation_claim_not_universal_identity"

def exampleShape : Shape :=
  ⟨2, 10, 5, 5⟩

def shapeJson (s : Shape) : Json :=
  Json.mkObj
    [ ("heads", toJson s.heads)
    , ("sequence_length", toJson s.sequenceLength)
    , ("head_dimension", toJson s.headDimension)
    , ("value_dimension", toJson s.valueDimension)
    ]

def ledgerJson (s : Shape) : Json :=
  Json.mkObj
    [ ("score_count", toJson (scoreCount s))
    , ("qk_multiplications", toJson (qkMultiplications s))
    , ("qk_additions", toJson (qkAdditions s))
    , ("score_scaling_multiplications", toJson (scoreScalingMultiplications s))
    , ("softmax_row_max_comparisons", toJson (softmaxRowMaxComparisons s))
    , ("softmax_score_subtractions", toJson (softmaxSubtractions s))
    , ("softmax_exponentials", toJson (softmaxExponentials s))
    , ("softmax_row_sum_additions", toJson (softmaxRowSumAdditions s))
    , ("softmax_normalization_divisions", toJson (softmaxDivisions s))
    , ("av_multiplications", toJson (avMultiplications s))
    , ("av_additions", toJson (avAdditions s))
    , ("kka_qk_interference_samples", toJson (kkaQkInterferenceSamples s))
    , ("kka_av_interference_samples", toJson (kkaAvInterferenceSamples s))
    , ("kka_total_interference_samples", toJson (kkaAttentionInterferenceSamples s))
    ]

def specJson (s : Shape) : Json :=
  Json.mkObj
    [ ("spec_id", toJson "EIS-KKA-BENCH-001A")
    , ("spec_version", toJson "0.1.0")
    , ("source_equation", toJson "Tian et al., PTC (2025), Eq. 1 and Eq. 2")
    , ("interference_equation", toJson "|a+b|^2 = |a|^2 + |b|^2 + 2 Re(a conj(b))")
    , ("balanced_detector_equation", toJson "Y = 2 R Re(a conj(b))")
    , ("tian_eq2_status", toJson tianEq2Status)
    , ("shape", shapeJson s)
    , ("operation_ledger", ledgerJson s)
    , ("counting_note", toJson "Interference samples are logical field-pair events, not FLOPs, cycles, or measured device operations.")
    , ("scope_note", toJson "Q/K/V projections are upstream and excluded from this attention-core ledger; report them separately when comparing a complete transformer block.")
    ]

end EISKKA.Bench001A

def main : IO Unit := do
  IO.println (EISKKA.Bench001A.specJson EISKKA.Bench001A.exampleShape).compress
