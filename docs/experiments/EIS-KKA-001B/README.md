# EIS-KKA-001B — SOI MZI Optical-Field Model

**Status:** analytical model specification and reference implementation; not a physical simulation  
**Baseline dependency:** none at runtime on EIS-TIAN-KKA-LIFT-001A  
**Optimizer:** prohibited in this work package

## Purpose

Create a separately versioned, parameter-explicit complex-field model for a two-coupler Mach–Zehnder interferometer (MZI). It maps complex optical fields at declared reference planes to output-port fields and powers. It is not a reconstruction of Tian's complete physical device.

## Frozen mathematical convention

The ideal, reciprocal, lossless 2×2 coupler convention is:

\[
C(\kappa)=
\begin{bmatrix}
\sqrt{1-\kappa} & \sqrt{\kappa}\\
\sqrt{\kappa} & -\sqrt{1-\kappa}
\end{bmatrix}
\]

Here κ is the cross-coupled power fraction. This is a declared mathematical port/phase convention, not a claim that a particular Tian coupler has this exact scattering matrix.

For complex input field vector E_in:

\[
E_1=C(\kappa_{in})E_{in}
\]

\[
E_{arm}=\operatorname{diag}(10^{-L_j/20}e^{i\phi_j})E_1
\]

\[
E_{out}=C(\kappa_{out})E_{arm}
\]

L_j is total power loss in dB for arm j; φ_j is phase in radians. Output port power is |E_out,j|².

For the balanced 50:50 output coupler under this convention:

\[
P_0-P_1=2\operatorname{Re}(E_{arm,1}E_{arm,2}^{*})
\]

This is an ideal model identity, not an established identification of Tian's SI-4 measured scalar observable.

## KKA input boundary

The two complex input amplitudes are caller-supplied. No voltage-to-complex-field law is invented for the Kramers–Kronig amplitude–phase-coupled input.

- SI-4 Eq. (S13) remains the frozen scalar fitted response in 001A.
- No Table S1 coefficient is imported into this field model.
- No equation maps VA, VB to complex field amplitudes until the physical relationship and reference planes are source-supported.
- A future KKA field adapter must have a separate source/evidence contract.

## Evidence classifications

| Item | Classification |
|---|---|
| Two-coupler topology and complex-field algebra | EIS analytical model |
| Coupler fractions | Explicit inputs; device values unknown |
| Input fields | Explicit inputs; normalization/reference planes to be supplied |
| Arm phase shifts | Explicit inputs; not mapped to heater voltage |
| Arm losses | Explicit inputs; no measured values supplied |
| SOI dimensions/material indices | Unknown; deliberately not invented |
| Tian SI-4 coefficients | Frozen source-fitted data in 001A; not used here |
| Tidy3D complex S-parameters | Future independent EM evidence; unavailable at this gate |

## Non-goals

No optimizer, parameter fitting, calibration update, automatic coefficient import, material database, thermal model, heater electrical model, wavelength sweep, polarization model, reflections, detector noise, OASIS/GDS layout, or Tidy3D cloud job.

## Verification contract

Tests must establish: ideal coupler unitarity; lossless MZI total-power conservation; balanced 50:50 output difference equals the declared 2 Re(A B*) cross-term; equal phase shifts do not change output powers; nonnegative arm loss does not increase total output power; invalid coupler fractions are rejected.

Passing these tests verifies algebraic implementation only, not a fabricated device.

## Next physical-evidence gate

Before Tidy3D, document source/assumption labels for waveguide cross-section and layer stack, wavelength/polarization, material dispersion, coupler geometry/gap/interaction length/port planes, arm geometry/heater placement, boundary conditions and mesh convergence.

Use the labels tian_reported, source_unknown, eis_assumed, and simulated. Unknowns remain explicit. Extract complex coupler/MZI fields at defined reference planes and estimate cloud cost before submission. Only then compare physical outputs with this analytical reference.


## Four-port scattering lowering

The analytical transfer model now has a reciprocal four-port scattering representation with port order
\([left_0,left_1,right_0,right_1]\). Define the forward transfer block:

\[
U=C(\kappa_{out})\,
\operatorname{diag}(10^{-L_j/20}e^{i\phi_j})\,
C(\kappa_{in}).
\]

The idealized scattering matrix is:

\[
S=\begin{bmatrix}
0 & U^T\\
U & 0
\end{bmatrix}.
\]

The zero diagonal blocks mean that this model assumes no reflections. The transpose in the reverse block is the reciprocal-network convention; it is not a Hermitian transpose. With zero arm loss, the matrix is unitary. With positive arm loss, it remains symmetric (reciprocal) but is subunitary because dissipative channels are not represented as explicit ports.

This is a backend-neutral network lowering target for a later PhotonForge component adapter. Port ordering, reference planes, and the no-reflection assumption must be preserved by that adapter. It is not yet a PhotonForge model, foundry compact model, Tidy3D result, or physical qualification.

The expanded algebraic tests check:
- reciprocity \(S=S^T\);
- lossless unitarity \(S^\dagger S=I\);
- lossy contractivity (eigenvalues of \(S^\dagger S\) do not exceed one);
- agreement of the forward S-block with the existing complex-field evaluator over deterministic randomized cases.

The current tests are software/algebra evidence only. The next adapter gate must compare the PhotonForge component's port-indexed S-matrix against this reference at the same frequency, port ordering, and normalization before any geometry-specific claim is made.
