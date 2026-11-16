# EIS-KKA-FORMAL-001 — Lean 4 / Physlib mathematical contract

**Owner:** Earth ICT, SPC  
**Status:** Study-group review draft v0.2  
**Parent:** EIS-KKA-REF-001 and EIS-KKA-SOI-001B  
**Lean toolchain:** Lean 4.35.0  
**Physlib dependency:** `leanprover-community/physlib`, pinned to immutable commit `be0a9eef7dac78da524bfbde91c812340b194610`

## Purpose and boundary

This package makes device-independent mathematical conventions of the EIS KKA reference machine-checkable. It uses Physlib (the successor to the PhysLean and Lean-QuantumInfo repositories) for its unitary-group abstraction and builds a two-mode phase-shift specialization using the same diagonal phase-matrix pattern as Physlib's existing phase-shift formalization.

It does **not** prove that a fabricated device has a particular transfer curve, that a material has a particular Kramers–Kronig response, or that a simulation matches hardware. Those remain questions for measurement, calibrated simulation and evidence review.

## Normative conventions in v0.2

### 1. Phasor convention

EIS adopts the positive-time convention:

\[
E(t)=\operatorname{Re}\{\widetilde E e^{+i\omega t}\}.
\]

This is a frozen EIS convention, not a claim that all optics literature uses the same sign. Propagation, phase, conjugation, detector polarity and reported coupling signs must be derived consistently from it.

### 2. Field-amplitude coupling

Let (x=\ln A), where (A>0) is the **field-amplitude transmission** of the selected response, and let (\phi(x)) be its continuously unwrapped phase in radians.

\[
\boxed{\kappa_A(x)=\frac{d\phi}{dx}
=\frac{d\phi}{d\ln A}}
\]

The intensity coordinate is (y=\ln I=2x). The phase expressed in that coordinate is (\phi_I(y)=\phi(y/2)), so:

\[
\boxed{\kappa_I(x)=\frac{d\phi_I}{dy}\bigg|_{y=2x}
=\frac12\kappa_A(x)}
\]

The Lean theorem `kappaI_eq_half_kappaA` proves this under an explicit differentiability hypothesis. It avoids the incorrect shorthand `deriv φ (Real.log A)`, which evaluates the derivative at a point rather than differentiating with respect to the log-amplitude coordinate.

### 3. Modulator, cell and cascade coupling are distinct

The formal interface now provides two separately typed response records:

- `ModulatorPhaseResponse` and `kappaA_modulator`: the modulator transfer response at its declared output port and phase reference.
- `CellPhaseResponse` and `kappaA_cell`: the complete computational-cell response at its declared output port and phase reference.

Both use the same mathematical definition of `κ_A`, but their transfer functions and reference planes are not interchangeable. The cell response includes whatever modulator, interferometer and other optical elements are inside the declared cell boundary.

A cascade-level `κ_A` is **not** defined as the sum of per-cell values. A future cascade contract must first define the composite multiport transfer, selected input and output ports, control state, operating range and phase-reference propagation. Scalar serial products may admit additive log-derivative rules under explicit hypotheses; a general interferometric multiport network does not inherit that rule automatically.

### 4. Operating range and admissibility

`OperatingRange` is a closed interval in log-amplitude coordinates. `KappaAAdmissibleOnRange` requires both membership in that interval and existence of the phase derivative.

A physical profile must additionally provide calibrated amplitude range, wavelength, temperature, optical power, drive state, control-port state and measurement-validity conditions. The mathematical interval alone does not certify a device operating range.

### 5. Phase reference

`PhaseReference` records a reference-plane identifier and calibrated phase origin. The common-rotation theorem proves that rotating both interfering field envelopes by the same phase leaves their real cross term unchanged.

That invariance does not authorize silently resetting a reference at a cascade boundary. Future composition records must preserve or explicitly transform the reference metadata.

### 6. Balanced detector sign and normalization

The electrical output polarity is frozen as (I_+-I_-). Reversing it to (I_--I_+) reverses the reported sign. Swapping the two optical operands does not reverse the real cross term.

For an ideal 50:50 coupler with field outputs:

\[
E_+=\frac{A+B}{\sqrt 2},\qquad
E_-=\frac{A-B}{\sqrt 2},
\]

the intensity difference is:

\[
|E_+|^2-|E_-|^2=2\operatorname{Re}(AB^*).
\]

With detector responsivity (R) in A/W:

\[
\boxed{Y_{+-}=I_+-I_-=2R\operatorname{Re}(AB^*)}.
\]

The formal `DetectorNormalization` record carries both responsivity and `fieldScaleSq`, the squared field coefficient applied at each sum/difference output port. For the stated 50:50 convention, `fieldScaleSq = 1/2`; theorem `detector_50_50_plusMinus` proves the normalized output reduces to the expression above. Other splitter conventions must supply their own normalization rather than inheriting the factor by assumption.

The current scalar detector model is ideal. Gain imbalance, offsets, noise, bandwidth, saturation, responsivity uncertainty and calibration corrections remain future extensions.

## Physlib reuse

- `QuantumInfo.ForMathlib.HermitianMat.Unitary` supplies Physlib's `𝐔[n]` notation for `Matrix.unitaryGroup n ℂ`.
- `Physlib.Particles.FlavorPhysics.CKMMatrix.Basic` contains a diagonal three-mode phase-shift matrix, its identity, adjoint and phase-addition lemmas.
- `EISKKA.PhysLeanBridge` specializes that algebraic pattern to two optical ports and packages the two-mode phase shifter as a Physlib unitary-group element.

The CKM three-mode object is **not** treated as an optical MZI. Only its reusable unitary and diagonal phase-shift algebraic structure is borrowed. The MZI coupler and complete device cascade remain separate EIS models.

## Modules

| Module | Responsibility |
|---|---|
| `EISKKA.Conventions` | Phasor, phase reference, operating interval, `κ_A/κ_I`, distinct modulator and cell responses |
| `EISKKA.Detector` | Common phase invariance, optical-arm symmetry, electrical polarity and detector normalization |
| `EISKKA.PhysLeanBridge` | Physlib unitary group and two-mode phase-shift matrix |
| `EISKKA.Provenance` | Evidence quality and confidentiality as separate dimensions |
| `EISKKA.Scalar` | Exact Cartesian field and interference contract |

## Python relationship

Python remains an independently implemented binary64 executable reference. It is **not** generated wholesale from Lean. Lean is the normative mathematical source; generated JSON schemas and known-answer vectors may be added as derived artifacts. Python is checked against those artifacts and independent analytical tests. This preserves an independent implementation while preventing convention drift.

Any future generated artifact must be reproducibly derived from the pinned Lean specification, carry the source commit and schema version, and be checked into CI. The numerical Python implementation remains independently authored and tested.

## Evidence classes and release controls

The formal model separates evidence quality (`assumed`, `simulated`, `fitted`, `measured`) from confidentiality (`public`, `foundryConfidential`). A measured value may still be foundry-confidential. Public repository CI and human release review must reject confidential values before publication; the Lean type alone is not a repository secret-scanning or legal authorization system.

## Build and review

From the repository root:

```sh
lake build --wfail
```

CI also rejects unfinished proof placeholders in the formal source tree.

## Deliberately deferred

- A general multiport modulator–interferometer–detector cascade and its phase-reference composition theorem.
- A generic cascade `κ_A` composition rule; no sum-of-cells rule is assumed.
- Non-ideal arm-loss and absorption-dependent phase-shifter models.
- Full derivation of KKA activation operating-range conditions.
- Gain imbalance, offsets, detector noise, bandwidth, saturation and calibration uncertainty.
- Machine-generated Python source or bindings.
- Any claim of measured SOI behaviour, foundry qualification, physical performance, energy benefit or scalability.

These are subsequent study-group decisions, not silently assumed facts in v0.2.
