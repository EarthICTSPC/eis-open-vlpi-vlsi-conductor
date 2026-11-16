# EIS-KKA-FORMAL-001 — Lean 4 / Physlib mathematical contract

**Owner:** Earth ICT, SPC  
**Status:** Study-group review draft v0.1  
**Parent:** EIS-KKA-REF-001 and EIS-KKA-SOI-001B  
**Lean toolchain:** Lean 4.35.0  
**Physlib dependency:** `leanprover-community/physlib` commit `be0a9eef7dac78da524bfbde91c812340b194610`

## Purpose and boundary

This package makes the device-independent mathematical conventions of the EIS KKA reference machine-checkable. It uses Physlib (the successor to the PhysLean and Lean-QuantumInfo repositories) for its unitary-group abstraction and builds a two-mode phase-shift specialization using the same diagonal phase-matrix pattern as Physlib's existing phase-shift formalization.

It does **not** prove that a fabricated device has a particular transfer curve, that a material has a particular Kramers–Kronig response, or that a simulation matches hardware. Those remain questions for measurement, calibrated simulation and evidence review.

## Normative conventions in v0.1

### 1. Field-amplitude coupling

Let (x=\ln A), where (A\) is the **field-amplitude transmission** of the selected response, and let (\phi(x)\) be its continuously unwrapped phase in radians.

\[
\boxed{\kappa_A(x)=\frac{d\phi}{dx}
=\frac{d\phi}{d\ln A}}
\]

The intensity coordinate is (y=\ln I=2x\). The phase expressed in that coordinate is (\phi_I(y)=\phi(y/2)\), so the chain rule gives:

\[
\boxed{\kappa_I(x)=\frac{d\phi_I}{dy}\bigg|_{y=2x}
=\frac12\kappa_A(x)}
\]

The Lean theorem `kappaI_eq_half_kappaA` proves this under an explicit differentiability hypothesis. It avoids the incorrect shorthand `deriv φ (Real.log A)`, which differentiates with respect to the argument of `φ` rather than differentiating with respect to log-amplitude.

**Scope:** v0.1 defines the phase response in log-amplitude coordinates. The modulator's intrinsic response and the complete modulator–interferometer–detector cell response must be represented by distinct phase-response functions in subsequent device modules.

### 2. Operating range

`OperatingRange` is a closed interval in log-amplitude coordinates. A coupling value is admissible only where the phase response has a derivative. A physical profile must additionally supply the calibrated amplitude range, wavelength, temperature, optical power, drive state and measurement-validity conditions.

### 3. Phasor convention and phase reference

The normative EIS time dependence is:

\[
E(t)=\operatorname{Re}\{\widetilde E e^{+i\omega t}\}.
\]

`PhaseReference` records a reference-plane identifier and calibrated phase origin. Later cascade modules must carry this reference metadata rather than silently resetting phase at cell boundaries.

### 4. Balanced detector

For Cartesian field envelopes (a,b\), the existing scalar contract defines:

\[
Y_{+-}=2\operatorname{Re}(ab^*).
\]

The new detector module proves that a common phase-reference rotation applied to both arms preserves the cross term. It also distinguishes optical-arm exchange (which preserves the real cross term) from electrical detector polarity reversal (which changes the reported sign).

## Physlib reuse

- `QuantumInfo.ForMathlib.HermitianMat.Unitary` supplies Physlib's `𝐔[n]` notation for `Matrix.unitaryGroup n ℂ`.
- `Physlib.Particles.FlavorPhysics.CKMMatrix.Basic` contains a diagonal three-mode phase-shift matrix, its identity, adjoint and phase-addition lemmas.
- `EISKKA.PhysLeanBridge` specializes that algebraic pattern to two optical ports and packages the two-mode phase shifter as a Physlib unitary-group element.

The CKM three-mode object is **not** treated as an optical MZI. Only its reusable unitary and diagonal phase-shift algebraic structure is borrowed. The MZI coupler and complete device cascade remain separate EIS models.

## Modules

| Module | Responsibility |
|---|---|
| `EISKKA.Conventions` | Phasor, phase reference, log-amplitude domain and `κ_A/κ_I` |
| `EISKKA.Detector` | Common phase invariance and electrical polarity |
| `EISKKA.PhysLeanBridge` | Physlib unitary group and two-mode phase shifter |
| `EISKKA.Provenance` | Evidence quality and confidentiality as separate dimensions |
| `EISKKA.Scalar` | Existing exact Cartesian field and interference contract |

## Python relationship

Python remains an independently implemented binary64 executable reference. It is **not** generated wholesale from Lean. Lean is the normative mathematical source; generated JSON schemas and known-answer vectors may be added as derived artifacts. Python is checked against those artifacts and independent analytical tests. This preserves a useful independent implementation while preventing convention drift.

## Evidence classes and release controls

The formal model separates evidence quality (`assumed`, `simulated`, `fitted`, `measured`) from confidentiality (`public`, `foundryConfidential`). This is intentional: a measured value may still be foundry-confidential. Public repository CI and human release review must reject confidential values before publication; the Lean type alone is not a repository secret-scanning or legal authorization system.

## Build and review

From the repository root:

```sh
lake build --wfail
```

CI also rejects unfinished proof placeholders in the formal source tree.

## Deliberately deferred

- Full derivation of the KKA activation operating-range conditions.
- Proof of the ideal MZI matrix's unitary property and single-input port phase behaviour using the final frozen coupler convention.
- Non-ideal arm-loss and absorption-dependent phase-shifter models.
- Full modulator–interferometer–detector cascade and phase-reference composition theorem.
- Machine-generated Python bindings or Python source.
- Any claim of measured SOI behaviour, foundry qualification, physical performance, energy benefit or scalability.

These are subsequent study-group decisions, not silently assumed facts in v0.1.
