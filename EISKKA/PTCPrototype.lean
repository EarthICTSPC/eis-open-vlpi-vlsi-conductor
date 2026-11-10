module

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

/-- Three independently controlled phase shifters in one Tian-style MZI. -/
structure MZIControls where
  external : ℝ
  internalA : ℝ
  internalB : ℝ
  deriving Repr

/--
Signed field-amplitude transfer for the MZI, from SI-1 Eq. (S2)/(S3).
The signed cosine is retained; it is not replaced by an absolute value.
-/
def mziFieldAmplitude (inputAmplitude : ℝ) (c : MZIControls) : ℝ :=
  inputAmplitude / Real.sqrt 2 *
    Real.cos ((c.internalB - c.internalA) / 2 + Real.pi / 4)

/-- Output phase of the MZI, from SI-1 Eq. (S2)/(S3). -/
def mziFieldPhase (c : MZIControls) : ℝ :=
  c.external + (c.internalA + c.internalB) / 2 + Real.pi / 4

/-- Complex-envelope representation of the ideal MZI output field. -/
noncomputable def mziField (inputAmplitude : ℝ) (c : MZIControls) : Field :=
  Field.polar (mziFieldAmplitude inputAmplitude c) (mziFieldPhase c)

/--
Ideal balanced-detection observable for the paired input/weight MZIs,
transcribed from SI-1 Eq. (S4). Inputs are the real incident field amplitudes
before their respective MZI transfer functions.
-/
def bpdOutput
    (inputAmplitudeA inputAmplitudeB : ℝ)
    (a b : MZIControls) : ℝ :=
  2 * mziFieldAmplitude inputAmplitudeA a *
      mziFieldAmplitude inputAmplitudeB b *
      Real.sin
        (a.external - b.external
          + (a.internalA + a.internalB) / 2
          - (b.internalA + b.internalB) / 2)

/-- The published 10×1 prototype has ten A-side MZIs. -/
def outputChannelCount : ℕ := 10

/-- One shared B-side MZI is broadcast to all ten output channels. -/
def sharedWeightMziCount : ℕ := 1

/-- One A-side MZI is associated with each output channel. -/
def inputMziCount : ℕ := outputChannelCount

/-- Total MZI count in the published prototype. -/
def totalMziCount : ℕ := inputMziCount + sharedWeightMziCount

/-- Each MZI has one external and two internal phase shifters. -/
def phaseShiftersPerMzi : ℕ := 3

/-- Total thermal phase-shifter count. -/
def totalPhaseShifterCount : ℕ := totalMziCount * phaseShiftersPerMzi

theorem output_channel_count_is_ten : outputChannelCount = 10 := by decide

theorem input_mzi_count_is_ten : inputMziCount = 10 := by decide

theorem total_mzi_count_is_eleven : totalMziCount = 11 := by decide

theorem phase_shifters_per_mzi_is_three : phaseShiftersPerMzi = 3 := by decide

theorem total_phase_shifter_count_is_thirty_three :
    totalPhaseShifterCount = 33 := by decide

end EISKKA.PTC
