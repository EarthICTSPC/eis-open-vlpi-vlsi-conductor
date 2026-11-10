module

import Mathlib
import EISKKA.PTCPrototype

/-!
# EIS PTC MZI cell contract — technology-independent v0.1

The ideal field transfer is inherited from the source-transcribed Tian SI-1
equations in PTCPrototype.lean. This module adds typed cell interfaces and a
parameterized, explicitly non-physical placeholder model boundary.

No foundry stack, layer map, compact model, or measured device parameter is
asserted here. Numeric device characterization remains outside this Lean
contract until evidence-backed data are available.
-/

namespace EISKKA.PTCMZI

open EISKKA.PTC

/-- Optical port roles at the single-MZI cell boundary. -/
inductive OpticalPortRole
  | input
  | outputBar
  | outputCross
  | monitor
  deriving DecidableEq, Repr

/-- Electrical roles are heater terminals, not optical detector pins. -/
inductive ElectricalPortRole
  | heaterExternalPositive
  | heaterExternalNegative
  | heaterInternalAPositive
  | heaterInternalANegative
  | heaterInternalBPositive
  | heaterInternalBNegative
  deriving DecidableEq, Repr

/-- Port direction is explicit and machine-checkable. -/
inductive PortDirection
  | input
  | output
  | inout
  deriving DecidableEq, Repr

/-- Typed logical optical port. Geometry and layer identifiers are backend data. -/
structure OpticalPort where
  name : String
  role : OpticalPortRole
  direction : PortDirection
  wavelengthNm : ℝ
  modeIndex : Nat
  deriving Repr

/-- Typed logical electrical port. Units and limits are carried by the adapter. -/
structure ElectricalPort where
  name : String
  role : ElectricalPortRole
  direction : PortDirection
  deriving Repr

/-- Three independent heater commands, matching the Tian MZI control count. -/
structure HeaterCommands where
  externalVoltageV : ℝ
  internalAVoltageV : ℝ
  internalBVoltageV : ℝ

/-- Non-ideal model parameters; values must be supplied with evidence externally. -/
structure DeviceModelParameters where
  amplitudeTransmission : ℝ
  couplerVisibility : ℝ
  externalPhaseErrorRad : ℝ
  internalAPhaseErrorRad : ℝ
  internalBPhaseErrorRad : ℝ
  deriving Repr

/-- Apply explicit model corrections to the three ideal phase controls. -/
def correctedControls (c : MZIControls) (p : DeviceModelParameters) : MZIControls :=
  { external := c.external + p.externalPhaseErrorRad
    internalA := c.internalA + p.internalAPhaseErrorRad
    internalB := c.internalB + p.internalBPhaseErrorRad }

/-- Model-qualified amplitude after explicit transmission and visibility factors. -/
noncomputable def modeledFieldAmplitude
    (inputAmplitude : ℝ) (c : MZIControls) (p : DeviceModelParameters) : ℝ :=
  p.amplitudeTransmission * p.couplerVisibility *
    mziFieldAmplitude inputAmplitude (correctedControls c p)

/-- Complex-envelope field under the corrected phase and amplitude model. -/
noncomputable def modeledField
    (inputAmplitude : ℝ) (c : MZIControls) (p : DeviceModelParameters) : Field :=
  Field.polar
    (modeledFieldAmplitude inputAmplitude c p)
    (mziFieldPhase (correctedControls c p))

/-- Zero input remains zero for any finite model correction factors. -/
theorem modeledFieldAmplitude_zero
    (c : MZIControls) (p : DeviceModelParameters) :
    modeledFieldAmplitude 0 c p = 0 := by
  simp [modeledFieldAmplitude, mziFieldAmplitude]

/-- Ideal parameter boundary: unit transmission, unit visibility, zero phase errors. -/
def idealParameters : DeviceModelParameters :=
  { amplitudeTransmission := 1
    couplerVisibility := 1
    externalPhaseErrorRad := 0
    internalAPhaseErrorRad := 0
    internalBPhaseErrorRad := 0 }

theorem correctedControls_ideal (c : MZIControls) :
    correctedControls c idealParameters = c := by
  cases c
  rfl

theorem modeledFieldAmplitude_ideal (x : ℝ) (c : MZIControls) :
    modeledFieldAmplitude x c idealParameters = mziFieldAmplitude x c := by
  simp [modeledFieldAmplitude, idealParameters, correctedControls]

/-- This logical cell has three heater circuits; shared-return routing is backend-defined. -/
def heaterCircuitCount : Nat := 3

theorem heaterCircuitCount_is_three : heaterCircuitCount = 3 := by decide

end EISKKA.PTCMZI

#print axioms EISKKA.PTCMZI.modeledFieldAmplitude_zero
#print axioms EISKKA.PTCMZI.correctedControls_ideal
#print axioms EISKKA.PTCMZI.modeledFieldAmplitude_ideal
#print axioms EISKKA.PTCMZI.heaterCircuitCount_is_three
