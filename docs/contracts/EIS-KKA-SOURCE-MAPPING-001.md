# EIS-KKA-SOURCE-MAPPING-001

**Status:** Source audit completed at ideal-equation level; physical calibration remains open  
**Parent work:** EIS-KKA-TOPOLOGY-REFERENCE-PLANE-001  
**Purpose:** Resolve the SI-1 E_in reference plane and define the exact algebraic mapping from Tian SI-1 S4 to the PhysLib real-cross-term abstraction.

## 1. Executive result

Two questions that had been open are now resolved at the source-equation / ideal-diagram level:

1. **Tian E_in:** SI-1 Figure S1 labels E_in at the laser, before the first MMI. That MMI divides the common input into the I and W MZI branches. Eqs. S2 and S3 both carry the factor E_in/sqrt(2). Therefore, in the ideal SI-1 model, E_in is the common pre-split input field and the upstream branch division is nominally equal.
2. **Tian S4 to PhysLib:** S4 is a quadrature cross term. It is exactly representable by PhysLib's real cross term after an explicit -pi/2 rotation of one formal field argument:
   P_out = 2 Im(E_I' conj(E_W')) = 2 Re((-i E_I') conj(E_W')) = 2 opticalCrossTerm(-i E_I', E_W').

These are source-backed ideal mathematical mappings. They do not qualify the as-fabricated splitter, MMI, grating couplers, detector, or full PDK implementation.

## 2. Primary source evidence: SI-1 Figure S1

Publisher-hosted supplementary PDF:
https://static-content.springer.com/esm/art:10.1186%2Fs43074-025-00182-7/MediaObjects/43074_2025_182_MOESM1_ESM.pdf

Relevant evidence:
- PDF page 2 (zero-based page index 1), Figure S1.
- Figure caption: the structure corresponds to one output port of the PTC.
- Figure labels E_in at the laser, upstream of the first MMI.
- The first MMI has two output paths feeding the upper I MZI and lower W MZI.
- The MZI outputs are labeled E_I and E_W, which enter a final MMI followed by BPD.
- The equations immediately below the diagram are SI-1 S2, S3, and S4.

The PDF's extracted text also states that the PTC structure consists of MMI, 1xN split tree, MZI, MMI, and BPD; the image is essential to reading the particular one-output topology and locating E_in.

### 2.1 Reference-plane conclusion

The ideal source diagram places the E_in reference plane at the laser output / input to the first MMI. It is not a per-MZI branch-input symbol in Figure S1.

The equations are:

S2:
E_I' = E_I exp(i theta_1)
     = (E_in/sqrt(2)) cos((theta_3-theta_2)/2 + pi/4)
       exp(i(theta_1 + (theta_3+theta_2)/2 + pi/4))

S3:
E_W' = E_W exp(i theta_W)
     = (E_in/sqrt(2)) cos((theta_6-theta_5)/2 + pi/4)
       exp(i(theta_4 + (theta_6+theta_5)/2 + pi/4))

The shared E_in/sqrt(2) coefficient agrees with the two-branch equal-amplitude split shown in Figure S1. Under the ideal lossless convention, that is a 50:50 power division.

**Physical qualification caveat:** SI-4 explicitly says fabrication imperfections can induce non-even 50:50 beam splitting and non-uniform grating-coupling efficiency, degrading interference contrast. Therefore the ideal source split is nominally equal, but the actual fabricated input-MMI ratio is not proven to be exactly 50:50 by S2/S3. SI-4's note is about fabrication-induced splitter imbalance in the chip's interference path; it does not, in the cited sentence, localize that imbalance specifically to the first input MMI. A physical model must expose the relevant branch/coupler transfer coefficients as calibrated parameters.

## 3. Topology and reference planes

Keep the following optical elements distinct:

| ID | Element | Source-supported interpretation |
|---|---|---|
| RP0 | Laser / common input | E_in label in Figure S1, before first MMI |
| T1 | First/upstream MMI | Divides common input into I and W MZI branches in the ideal diagram |
| T2-I | I MZI | External phase theta_1 and internal phases theta_2, theta_3; generates E_I' |
| T2-W | W MZI | External phase theta_4 and internal phases theta_5, theta_6; generates E_W' |
| T3 | Final MMI | Combines the I/W fields before BPD in Figure S1 |
| T4 | BPD | Balanced output P_out in S4; practical passive demonstration uses paired grating-coupler power measurements |

The internal MMI couplers inside each MZI are not the upstream T1 splitter and are not the final T3 combiner. A diagram or model that collapses these into one generic "50:50 coupler" loses topology information.

## 4. Algebraic derivation of the S4 observable

Define the total field phases:

alpha_I = theta_1 + (theta_3 + theta_2)/2 + pi/4
alpha_W = theta_4 + (theta_6 + theta_5)/2 + pi/4

Then:

E_I' = E_I exp(i alpha_I)
E_W' = E_W exp(i alpha_W),

where E_I and E_W are the signed real amplitude coefficients appearing in S2/S3.

Their complex product is:

E_I' conj(E_W') = E_I E_W exp(i(alpha_I-alpha_W)).

Therefore:

2 Im(E_I' conj(E_W')) = 2 E_I E_W sin(alpha_I-alpha_W).

Since:

alpha_I-alpha_W = theta_1-theta_4
                  + (theta_3+theta_2)/2
                  - (theta_6+theta_5)/2,

this is exactly Tian SI-1 Eq. S4:

P_out = 2 E_I E_W sin(theta_1-theta_4
        + (theta_3+theta_2)/2 - (theta_6+theta_5)/2).

No approximation or fitting is used in this identity.

## 5. Mapping to PhysLib

Inspected PhysLib source:
- Repository: EarthICTSPC/physlib
- File: PhyslibAlpha/Optics/Interference.lean
- Commit: 57f57b689e1ca47393e0bef6d4c21995e39654ef
- Definition: Optics.opticalCrossTerm (a b : Complex) := real inner product of b and a.
- Module documentation states this is equivalent to Re(a * conj b).

By the elementary complex identity Re(-i z) = Im(z), we obtain:

opticalCrossTerm(-i E_I', E_W')
  = Re((-i E_I') conj(E_W'))
  = Im(E_I' conj(E_W')).

Thus the exact S4 mapping is:

P_out = 2 * opticalCrossTerm(-i E_I', E_W').

An equivalent convention rotates the second argument by +pi/2:

P_out = 2 * opticalCrossTerm(E_I', i E_W').

Choose one convention and freeze it in the EIS interface. The first form is used in this contract.

### 5.1 Important interpretation

The factor -i is an explicit **algebraic phase-coordinate transformation** used to map the quadrature observable to the real-cross-term abstraction. It is not a claim that an additional physical phase shifter must be inserted into the chip. The source's S4 and final-MMI/BPD topology determine the measured quadrature.

PhysLib's theorem about normSq(a+b) establishes the generic real cross-term identity. It does not itself model:
- the SI-1 upstream MMI;
- MZI transfer functions or their port ordering;
- the final MMI's scattering matrix;
- detector responsivity, gain, offset, noise, or calibration;
- physical balanced-detection implementation.

The EIS bridge can instantiate the **algebraic cross-term component** of S4. It must not claim that the complete optical/detection circuit has been formally verified by that theorem alone.

## 6. Lean bridge target (proof pending)

The exact mathematical target for the Lean bridge is:

[
\operatorname{opticalCrossTerm}(-iE_I',E_W')
=\operatorname{Im}(E_I'\overline{E_W'}).
]

Consequently:

[
P_{out}=2\,\operatorname{opticalCrossTerm}(-iE_I',E_W').
]

This section is a theorem specification, not a claim that a Lean theorem has already been compiled or proved. The lifting collaborator and EIS must agree where the theorem belongs: in PhysLib as a general quadrature-to-real-cross-term lemma, or in an EIS-side module importing the existing PhysLib definition.

Before marking the bridge formally verified:
1. Pin the exact Lean and Mathlib toolchain.
2. Check the expression against the actual `Optics.opticalCrossTerm` definition and its inner-product convention.
3. Prove the identity without `sorry`.
4. Connect the S2/S3 source field definitions to the fields used by the bridge theorem.
5. Keep detector gain, responsivity, offsets, noise, and calibration outside this algebraic theorem unless separately modeled and proved.

A robust source-level theorem should state S4 using the explicit S2/S3 phase and signed-amplitude definitions, then derive the generic quadrature identity. That connects the complete source equations rather than merely proving a generic identity for arbitrary complex fields.

## 7. Evidence classification and remaining unknowns

| Claim | Classification | Status |
|---|---|---|
| SI-1 E_in is shown before first MMI | source-image verified | PASS |
| Ideal SI-1 branch fields use E_in/sqrt(2) | source-equation verified | PASS |
| Ideal upstream division is equal | source diagram + equation implication | PASS |
| Cell 15 reproduces equal-split S2/S3 | computationally demonstrated | PASS |
| Actual fabricated upstream MMI is exactly 50:50 | physical measurement | NOT ESTABLISHED |
| SI-1 S4 equals the quadrature cross term | algebraically derived from source equations | PASS |
| S4 maps to PhysLib real cross term with -i rotation | exact algebraic mapping | DERIVED; Lean proof pending |
| Complete MMI/MZI/BPD implementation is formally verified | formal + physical evidence | NOT ESTABLISHED |
| Foundry PDK / EM / measured-device qualification | physical evidence | NOT ESTABLISHED |

## 8. Required next gates

1. Add the explicit SI-1 source mapping to the EIS contract and preserve the original Cell 15 evidence unchanged.
2. Have the lifting collaborator review the exact -i phase-rotation bridge and decide whether it belongs as a theorem in PhysLib or an EIS-side theorem importing PhysLib.
3. Compile the candidate Lean theorem against the pinned toolchain; no sorry in an accepted theorem.
4. Build the complete two-output MZI transfer model with explicit port order, input/output reference planes, and the distinction between signal and monitor ports.
5. Model the final MMI and BPD separately. Do not treat the S4 algebraic identity as a complete detector model.
6. Keep actual upstream splitter imbalance and grating-coupling imbalance as calibrated physical parameters.

## 9. Decision

The ideal source reference plane is resolved: SI-1 Figure S1 places E_in before the upstream MMI, and S2/S3 encode the nominal equal split. The as-fabricated split remains unmeasured.

The S4-to-PhysLib bridge is algebraically exact under the explicit -i field rotation. Its Lean proof and the full MZI/MMI/BPD lowering remain pending.

**Do not proceed to physical qualification claims.** Proceed to the Lean bridge proof and complete two-output MZI lowering with source-mapped reference planes.
