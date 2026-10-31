import Mathlib

/-!
# EIS-ADIA-IO-001 — Adiabatic electrical I/O control contract

Abstract contract for a reversible controller and its power-clock. This does not
assert that an ordinary RISC-V RTL core becomes adiabatic by changing its clock.
A concrete implementation must use a reversible/adiabatic logic family, represent
its complete state, and validate switch and power-clock waveforms.

The external I/O commit is an explicit boundary outside the reversible internal
transition. It carries an audit record; it is not declared thermodynamically
reversible.
-/

namespace EIS.AdiaIO

inductive PowerClockSegment where
  | rampUp
  | evaluate
  | highHold
  | rampDown
  | lowHold
  deriving DecidableEq, Repr

/-- A parameterized trapezoidal envelope and a number of staggered power-clock rails. -/
structure TrapezoidalPowerClock where
  vLowV : ℝ
  vHighV : ℝ
  rampUpS : ℝ
  evaluateHoldS : ℝ
  rampDownS : ℝ
  lowHoldS : ℝ
  phaseRailCount : ℕ
  low_nonneg : 0 ≤ vLowV
  low_lt_high : vLowV < vHighV
  ramp_up_pos : 0 < rampUpS
  evaluate_hold_pos : 0 < evaluateHoldS
  ramp_down_pos : 0 < rampDownS
  low_hold_pos : 0 < lowHoldS
  enough_phase_rails : 4 ≤ phaseRailCount

def periodS (p : TrapezoidalPowerClock) : ℝ :=
  p.rampUpS + p.evaluateHoldS + p.rampDownS + p.lowHoldS

theorem periodS_pos (p : TrapezoidalPowerClock) : 0 < periodS p := by
  unfold periodS
  positivity

inductive SwitchAction where
  | turnOn
  | turnOff
  deriving DecidableEq, Repr

structure SwitchEvent where
  action : SwitchAction
  voltageAcrossSwitchV : ℝ
  currentThroughSwitchA : ℝ
  deriving Repr

structure SwitchSafetyTolerance where
  turnOnVoltageToleranceV : ℝ
  turnOffCurrentToleranceA : ℝ
  voltage_tolerance_nonneg : 0 ≤ turnOnVoltageToleranceV
  current_tolerance_nonneg : 0 ≤ turnOffCurrentToleranceA

/-- Close near zero voltage; open near zero current. -/
def SwitchSafetyTolerance.eventSafe
    (p : SwitchSafetyTolerance) (e : SwitchEvent) : Prop :=
  match e.action with
  | .turnOn => |e.voltageAcrossSwitchV| ≤ p.turnOnVoltageToleranceV
  | .turnOff => |e.currentThroughSwitchA| ≤ p.turnOffCurrentToleranceA

def allEventsSafe (p : SwitchSafetyTolerance) (events : List SwitchEvent) : Prop :=
  ∀ e, e ∈ events → p.eventSafe e

/-- The complete represented controller state includes queues and transaction history. -/
structure TransactionRecord where
  sequenceId : Nat
  requestCode : Nat
  priorProgramCounter : Nat
  priorRegisterImage : List Nat
  responseCode : Option Nat
  externalCommitId : Option Nat
  deriving DecidableEq, Repr

structure ControllerState where
  programCounter : Nat
  registers : List Nat
  requestQueue : List Nat
  responseQueue : List Nat
  transactionHistory : List TransactionRecord
  deriving DecidableEq, Repr

/-- A reversible state transition over the complete represented state. -/
structure ReversibleTransition (State : Type) where
  forward : State → State
  backward : State → State
  backward_after_forward : ∀ s, backward (forward s) = s
  forward_after_backward : ∀ s, forward (backward s) = s

/-- Forward microsteps may append records but cannot discard prior transaction history. -/
structure ReversibleController where
  transition : ReversibleTransition ControllerState
  forward_preserves_history : ∀ s r, r ∈ s.transactionHistory →
    r ∈ (transition.forward s).transactionHistory

/-- Ordered request/response handshake timestamps for one transaction. -/
structure BusHandshake where
  requestValidS : ℝ
  requestAcceptedS : ℝ
  responseValidS : ℝ
  responseAcceptedS : ℝ
  externalCommitS : ℝ
  request_valid_nonneg : 0 ≤ requestValidS
  request_accept_nonneg : 0 ≤ requestAcceptedS
  response_valid_nonneg : 0 ≤ responseValidS
  response_accept_nonneg : 0 ≤ responseAcceptedS
  commit_nonneg : 0 ≤ externalCommitS
  request_before_accept : requestValidS ≤ requestAcceptedS
  accept_before_response : requestAcceptedS ≤ responseValidS
  response_before_accept : responseValidS ≤ responseAcceptedS
  accept_before_commit : responseAcceptedS ≤ externalCommitS

/--
External irreversible boundary. The audit record binds request and pre-commit
architectural image. It is deliberately outside the reversible transition theorem.
-/
structure ExternalIOCommitBoundary where
  requestCode : Nat
  preCommitState : ControllerState
  externalEffectCode : Nat
  auditRecord : TransactionRecord
  audit_binds_request : auditRecord.requestCode = requestCode
  audit_binds_pc : auditRecord.priorProgramCounter = preCommitState.programCounter
  audit_binds_registers : auditRecord.priorRegisterImage = preCommitState.registers
  audit_marks_commit : auditRecord.externalCommitId.isSome = true

/-- Complete obligations for a proposed adiabatic I/O controller implementation. -/
structure AdiabaticIOContract where
  powerClock : TrapezoidalPowerClock
  switchTolerance : SwitchSafetyTolerance
  switchTrace : List SwitchEvent
  controller : ReversibleController
  bus : BusHandshake
  switch_trace_safe : allEventsSafe switchTolerance switchTrace

end EIS.AdiaIO
