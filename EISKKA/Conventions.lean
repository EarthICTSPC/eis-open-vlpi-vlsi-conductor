module

import Mathlib.Analysis.Calculus.Deriv.Comp

/-!
# EIS-KKA-FORMAL-001 — Normative scalar conventions

The independent variable of the canonical phase response is log field amplitude
x = ln A. Thus κ_A is the derivative of unwrapped phase with respect to x.
The log-intensity coordinate is y = ln I = 2x, which fixes the factor-of-two
conversion without conflating field amplitude and intensity.

This module formalizes conventions and differentiability conditions only.
It does not assert that a physical device realizes a particular response.
-/

namespace EISKKA

/-- The phasor sign convention used by EIS: Re(Ẽ exp(+i ω t)). -/
inductive PhasorConvention where
  | positiveTimeExponential
  deriving DecidableEq, Repr

/-- The normative EIS phasor convention. -/
def eisPhasorConvention : PhasorConvention :=
  .positiveTimeExponential

/-- An optical phase reference plane and its calibrated phase origin. -/
structure PhaseReference where
  planeId : Nat
  phaseOriginRad : ℝ
  deriving Repr

/-- A closed interval in log field-amplitude coordinates. -/
structure OperatingRange where
  logAmplitudeMin : ℝ
  logAmplitudeMax : ℝ
  nonempty : logAmplitudeMin < logAmplitudeMax

/-- Membership in an EIS operating range. -/
def OperatingRange.Contains (r : OperatingRange) (x : ℝ) : Prop :=
  r.logAmplitudeMin ≤ x ∧ x ≤ r.logAmplitudeMax

/-- Phase response parameterized by x = ln(A), with A the field amplitude. -/
abbrev LogAmplitudePhase := ℝ → ℝ

/-- Canonical EIS field-amplitude coupling κ_A = dφ/d(ln A). -/
noncomputable def kappaA (phaseLogA : LogAmplitudePhase) (x : ℝ) : ℝ :=
  deriv phaseLogA x

/-- Express the same phase response in the log-intensity coordinate y = ln(I). -/
def phaseLogIntensity (phaseLogA : LogAmplitudePhase) : ℝ → ℝ :=
  fun y => phaseLogA (y / 2)

/-- Intensity-coordinate coupling, evaluated at y = 2 ln(A). -/
noncomputable def kappaI (phaseLogA : LogAmplitudePhase) (x : ℝ) : ℝ :=
  deriv (phaseLogIntensity phaseLogA) (2 * x)

/--
The factor-of-two conversion follows from the chain rule.
The hypothesis supplies differentiability of the phase response in log-amplitude
coordinates; no numerical approximation or finite-difference convention is used.
-/
theorem kappaI_eq_half_kappaA
    (phaseLogA : LogAmplitudePhase) (x k : ℝ)
    (hphase : HasDerivAt phaseLogA k x) :
    kappaI phaseLogA x = kappaA phaseLogA x / 2 := by
  have hlin : HasDerivAt (fun y : ℝ => y / 2) (1 / 2) (2 * x) := by
    simpa using (hasDerivAt_id' (2 * x)).div_const (2 : ℝ)
  have hcomp := deriv_comp_of_eq (2 * x) hphase.differentiableAt
    hlin.differentiableAt (by ring)
  calc
    kappaI phaseLogA x =
        deriv phaseLogA x * deriv (fun y : ℝ => y / 2) (2 * x) := by
          simpa [kappaI, phaseLogIntensity] using hcomp
    _ = kappaA phaseLogA x / 2 := by
      rw [hlin.deriv]
      simp [kappaA]
      ring

/-- A point is mathematically admissible for κ_A when the phase derivative exists. -/
def KappaAAdmissible (phaseLogA : LogAmplitudePhase) (x : ℝ) : Prop :=
  ∃ k, HasDerivAt phaseLogA k x

theorem kappaA_admissible_has_derivative
    (phaseLogA : LogAmplitudePhase) (x : ℝ)
    (h : KappaAAdmissible phaseLogA x) :
    DifferentiableAt ℝ phaseLogA x := by
  rcases h with ⟨k, hk⟩
  exact hk.differentiableAt

/-- κ_A is admissible only at points inside the declared operating interval. -/
def KappaAAdmissibleOnRange
    (phaseLogA : LogAmplitudePhase) (r : OperatingRange) (x : ℝ) : Prop :=
  r.Contains x ∧ KappaAAdmissible phaseLogA x

theorem kappaA_admissible_on_range_mem
    (phaseLogA : LogAmplitudePhase) (r : OperatingRange) (x : ℝ)
    (h : KappaAAdmissibleOnRange phaseLogA r x) :
    r.Contains x :=
  h.1

end EISKKA
