module

import Mathlib
import EISKKA.Scalar

/-!
# Tian et al. PTC 10×1 prototype — source-faithful ideal transfer contract

This module formalizes the published six-phase-shifter equations for a pair
of Tian-style MZIs feeding one balanced-interference output. It also records
the prototype's published 10+1 MZI and 33-phase-shifter counts.

The equations are ideal analytical transfer equations transcribed from
Supporting Information SI-1, Eqs. (S2)–(S4), of Tian et al. (2025).
They are not a foundry device model, fitted response, layout, DRC result,
or physical measurement. Device-specific calibration and thermal coupling
remain separate evidence obligations.
-/

namespace EISKKA.PTC

open EISKKA

/-- Three independently controlled phase shifters in one Tian-style MZI. -/
structure MZIControls where
  external : ℝ
  internalA : ℝ
  internalB : ℝ

/--
Signed field-amplitude transfer for the MZI, from SI-1 Eq. (S2)/(S3).
The signed cosine is retained; it is not replaced by an absolute value.
-/
noncomputable def mziFieldAmplitude (inputAmplitude : ℝ) (c : MZIControls) : ℝ :=
  inputAmplitude / Real.sqrt 2 *
    Real.cos ((c.internalB - c.internalA) / 2 + Real.pi / 4)

/-- Output phase of the MZI, from SI-1 Eq. (S2)/(S3). -/
noncomputable def mziFieldPhase (c : MZIControls) : ℝ :=
  c.external + (c.internalA + c.internalB) / 2 + Real.pi / 4

/-- Complex-envelope representation of the ideal MZI output field. -/
noncomputable def mziField (inputAmplitude : ℝ) (c : MZIControls) : EISKKA.Field :=
  EISKKA.Field.polar (mziFieldAmplitude inputAmplitude c) (mziFieldPhase c)

/--
Ideal balanced-detection observable for the paired input/weight MZIs,
transcribed from SI-1 Eq. (S4). Inputs are the real incident field amplitudes
before their respective MZI transfer functions.
-/
noncomputable def bpdOutput
    (inputAmplitudeA inputAmplitudeB : ℝ)
    (a b : MZIControls) : ℝ :=
  2 * mziFieldAmplitude inputAmplitudeA a *
      mziFieldAmplitude inputAmplitudeB b *
      Real.sin
        (a.external - b.external
          + (a.internalA + a.internalB) / 2
          - (b.internalA + b.internalB) / 2)

/-- The published 10×1 prototype has ten A-side MZIs. -/
def outputChannelCount : Nat := 10

/-- One shared B-side MZI is broadcast to all ten output channels. -/
def sharedWeightMziCount : Nat := 1

/-- One A-side MZI is associated with each output channel. -/
def inputMziCount : Nat := outputChannelCount

/-- Total MZI count in the published prototype. -/
def totalMziCount : Nat := inputMziCount + sharedWeightMziCount

/-- Each MZI has one external and two internal phase shifters. -/
def phaseShiftersPerMzi : Nat := 3

/-- Total thermal phase-shifter count. -/
def totalPhaseShifterCount : Nat := totalMziCount * phaseShiftersPerMzi

theorem output_channel_count_is_ten : outputChannelCount = 10 := by decide

theorem input_mzi_count_is_ten : inputMziCount = 10 := by decide

theorem total_mzi_count_is_eleven : totalMziCount = 11 := by decide

theorem phase_shifters_per_mzi_is_three : phaseShiftersPerMzi = 3 := by decide

theorem total_phase_shifter_count_is_thirty_three :
    totalPhaseShifterCount = 33 := by decide


/-- Zero incident amplitude produces a zero ideal MZI output amplitude. -/
theorem mziFieldAmplitude_zero (c : MZIControls) :
    mziFieldAmplitude 0 c = 0 := by
  simp [mziFieldAmplitude]

/-- The ideal MZI field-amplitude transfer is linear in incident amplitude. -/
theorem mziFieldAmplitude_scale (r inputAmplitude : ℝ) (c : MZIControls) :
    mziFieldAmplitude (r * inputAmplitude) c =
      r * mziFieldAmplitude inputAmplitude c := by
  simp [mziFieldAmplitude]
  ring

/-- Adding a phase increment to the external shifter adds that increment to output phase. -/
theorem mziFieldPhase_external_shift (c : MZIControls) (delta : ℝ) :
    mziFieldPhase { c with external := c.external + delta } =
      mziFieldPhase c + delta := by
  simp [mziFieldPhase]
  ring

/-- Balanced output is zero when the incident A-side field is zero. -/
theorem bpdOutput_zero_A (inputB : ℝ) (a b : MZIControls) :
    bpdOutput 0 inputB a b = 0 := by
  simp [bpdOutput, mziFieldAmplitude]

/-- Balanced output is zero when the incident B-side field is zero. -/
theorem bpdOutput_zero_B (inputA : ℝ) (a b : MZIControls) :
    bpdOutput inputA 0 a b = 0 := by
  simp [bpdOutput, mziFieldAmplitude]

/-- Swapping the two coherent operands reverses the signed BPD output. -/
theorem bpdOutput_swap_neg (inputA inputB : ℝ) (a b : MZIControls) :
    bpdOutput inputA inputB a b =
      - bpdOutput inputB inputA b a := by
  simp only [bpdOutput]
  have hdelta :
      b.external - a.external
        + (b.internalA + b.internalB) / 2
        - (a.internalA + a.internalB) / 2 =
      -(a.external - b.external
        + (a.internalA + a.internalB) / 2
        - (b.internalA + b.internalB) / 2) := by
    ring
  rw [hdelta, Real.sin_neg]
  ring

end EISKKA.PTC
