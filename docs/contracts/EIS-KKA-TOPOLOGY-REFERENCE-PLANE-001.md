# EIS-KKA-TOPOLOGY-REFERENCE-PLANE-001

**Status:** Draft engineering contract  
**Applies to:** EIS-KKA-COMPONENT-001A and subsequent Tian KKA lowering work  
**Authority boundary:** Tian source equations and verified source statements remain the source record; EIS-derived topology and normalization assumptions must be identified as such.

## 1. Purpose

This contract prevents a mathematically consistent lowering model from silently becoming an asserted physical reconstruction of Tian's Photonic Transformer Chip (PTC).

It defines the topology distinctions, field symbols, reference-plane questions, and evidence gates that must be resolved before a full PhotonForge MZI lowering is accepted.

## 2. Source and formalization boundaries

### 2.1 Tian source record

Primary source: Tian et al., *Photonic Transformer Chip: Interference Is All You Need*, PhotoniX 6, 45 (2025), DOI [10.1186/s43074-025-00182-7](https://doi.org/10.1186/s43074-025-00182-7).

The EIS source audit has independently transcribed and numerically checked SI-1 Eqs. S2–S4. The main paper describes the externally coupled optical input being divided into two portions: one portion is split among the A paths, while the other is modulated as B and broadcast to the M ports. The paper also describes MZI signal and monitor outputs and balanced-detection arrangements.

These statements support a high-level multi-branch architecture. They do not, by themselves, identify the exact upstream splitter ratio, the SI-1 field reference planes, or every normalization convention needed to identify each equation's (E_{in}) with a physical node.

### 2.2 PhysLib lifting boundary

Inspected source:
- Repository: `EarthICTSPC/physlib`
- File: `PhyslibAlpha/Optics/Interference.lean`
- Commit: `57f57b6`
- Full file permalink: https://github.com/EarthICTSPC/physlib/blob/57f57b6/PhyslibAlpha/Optics/Interference.lean

The file defines:

```lean
noncomputable def opticalCrossTerm (a b : ℂ) : ℝ :=
  ⟪b, a⟫_ℝ
```

and proves the algebraic identity for `Complex.normSq (a + b)` using that cross term. Its module documentation explicitly avoids assuming a particular waveguide, coupler, modulator, or detector implementation.

Important consequences:

1. The inspected Lean file contains no `E_in`, `E_I`, or `E_W` source-normalization symbol.
2. The lifting therefore makes no pre-split/post-split commitment for Tian's `E_in`.
3. `noncomputable` is a Lean executability annotation; it does not mean the mathematical cross term is undefined or physically unknown.
4. The Lean definition is the real inner product / real cross term, equivalent under the documented convention to `Re(a * conj b)`.

The EIS branch-source convention in this contract is therefore a lowering-side refinement/modeling convention, not a redefinition of a symbol already fixed in this Lean file.

### 2.3 Real cross term versus Tian quadrature term

The PhysLib identity concerns:

[
2\operatorname{Re}(a\overline b).
]

The audited Tian SI-1 Eq. S4 is:

[
P_{out}=2\operatorname{Im}(E_I'\overline{E_W'}).
]

These are related by an explicit phase rotation:

[
2\operatorname{Im}(E_I'\overline{E_W'})
=
2\operatorname{Re}((-iE_I')\overline{E_W'}).
]

Thus the quadrature observable can be represented using the real-cross-term formalization only after explicitly rotating one field by (-\pi/2), or by adding a separately named quadrature-cross-term definition and proving the relation. Do not silently identify S4 with the unrotated real cross term.

This is a mathematical bridge candidate; its exact Lean implementation and proof remain pending.

## 3. Field symbols and normalization

The following names are reserved to prevent ambiguous reuse of `E_in`:

| Symbol | Meaning | Status |
|---|---|---|
| `E_src` | Common optical field at the declared upstream source reference plane, before I/W division | EIS contract symbol |
| `E_I,in` | Field at the I-branch input reference plane, after upstream division | EIS contract symbol |
| `E_W,in` | Field at the W-branch input reference plane, after upstream division | EIS contract symbol |
| `E_I'` | Complex field appearing in Tian SI-1 S2 | Source equation symbol |
| `E_W'` | Complex field appearing in Tian SI-1 S3 | Source equation symbol |
| `E_{in}^{Tian}` | Literal `E_in` as used in SI-1 S2/S3; physical reference plane not yet resolved | Source symbol, interpretation open |

For an ideal lossless upstream splitter, EIS may model:

[
E_{I,in}=\sqrt{\eta}\,E_{src},\qquad
E_{W,in}=\sqrt{1-\eta}\,E_{src},
]

where `eta` is the I-branch power fraction and (0\leq\eta\leq1).

**Do not equate** `E_src`, `E_I,in`, `E_W,in`, and `E_in^Tian` until source reference planes and normalization are documented.

## 4. Topology decomposition

The following elements must remain distinct in diagrams, models, tests, and contracts.

### T0 — Common optical input

Externally coupled input field at the upstream reference plane. Its normalization and reference plane must be specified.

### T1 — Upstream I/W branch division

Divides the common input into the I and W computational branches. The physical ratio is currently **UNRESOLVED**. Cell 15 does not qualify this physical splitter.

### T2 — I and W branch modulators

The I branch generates the query-side field; the W branch generates the weight/key-side field according to the source architecture. Preserve source-specific phase and amplitude conventions.

### T3 — Internal MZI couplers and phase shifters

These are internal to each MZI and must not be confused with T1. The paper describes MZI internal 1×2 and 2×2 MMI couplers as 50:50 components and describes external and internal phase shifters. Exact port ordering, phase conventions, and reference planes still require a complete source-to-model mapping.

### T4 — MZI signal and monitor outputs

Keep signal and monitor ports distinct. A pair of outputs belonging to one MZI is not automatically the same pair as the I/W computational branches.

### T5 — I/W interference and detection

The final interference and detection stage must reproduce the source's S4 observable and the paper's stated detector arrangement. Preserve the distinction between:
- the two fields participating in the I/W interference;
- the signal/monitor outputs of each MZI;
- the detector/grating-coupler reference planes; and
- the electrical or optical observable used by the acceptance test.

No detector gain, responsivity, offset, loss, or power normalization is implied by the field identity alone.

## 5. Cell 15 frozen evidence

Evidence record: [cell-15-splitter-ratio.json](../../evidence/EIS-KKA-COMPONENT-001A/cell-15-splitter-ratio.json).

Run parameters:
- 10,000 samples
- seed 20261129
- `eta` sweep: 0.25 through 0.75 in increments of 0.05
- tolerance: (10^{-11})
- both output ports of each ideal unitary MZI included in power accounting
- no phase fitting, amplitude fitting, or phase remapping

At `eta = 0.50`:
- I RMS relative field error: (7.157\times10^{-17})
- I maximum relative field error: (4.238\times10^{-16})
- W RMS relative field error: (7.083\times10^{-17})
- W maximum relative field error: (5.132\times10^{-16})
- maximum relative total-power error: (6.494\times10^{-16})

Acceptance:
- Equal-split S2/S3 field equivalence: PASS
- Power conservation across sweep: PASS
- All tested off-center ratios mismatch both source fields: PASS

**Permitted conclusion:** Under the EIS-derived ideal two-branch model and the explicit convention that `E_src` is the common pre-split field, `eta = 0.50` is required to reproduce both SI-1 S2 and S3 branch fields.

**Not permitted:** claiming that Cell 15 proves the fabricated upstream splitter is physically 50:50, or that Tian's SI-1 `E_in` has been conclusively located at the common pre-split plane.

Evidence classification: **computationally-demonstrated** for this model. It is not a Lean proof, physical measurement, EM/FDTD qualification, foundry-PDK qualification, or fabricated-device result.

## 6. Required reference-plane ledger

Before full PhotonForge lowering, the source-to-model mapping must identify:

| Plane | Required definition | Current status |
|---|---|---|
| RP0 | External input / common source field plane | Exact SI-1 correspondence unresolved |
| RP1-I | I-branch input immediately after upstream division | Physical splitter ratio unresolved |
| RP1-W | W-branch input immediately after upstream division | Physical splitter ratio unresolved |
| RP2-I | I-branch MZI/modulator input plane | Port mapping and normalization to verify |
| RP2-W | W-branch MZI/modulator input plane | Port mapping and normalization to verify |
| RP3-S/M | Each MZI signal and monitor output plane | Complete port mapping required |
| RP4 | Final interference/detection planes | S4 and detector convention mapping required |

Each plane definition must include field direction, port label, complex amplitude normalization, phase reference, and whether the field is before or after any coupler, modulator, propagation loss, or detector.

## 7. Lifting/lowering bridge requirements

The EIS lowering must not claim formal instantiation merely because numerical values satisfy the same algebraic identity.

Required bridge work:

1. Preserve the PhysLib real-cross-term definition and its existing scope.
2. Define a separately named quadrature observable or an explicit (-\pi/2) phase-rotation mapping.
3. State the EIS source symbols `E_src`, `E_I,in`, `E_W,in`, and `E_in^Tian` without aliasing them prematurely.
4. Prove the relevant field-to-cross-term mapping in Lean before labeling the lowering as formally verified against the lifting.
5. Keep the Cell 15 numerical result labeled computationally demonstrated, not formally verified.

A bridge note in PhysLib may be proposed upstream after review; this EIS contract does not modify or prescribe changes to the PhysLib repository.

## 8. Acceptance gates before full PhotonForge MZI lowering

- [ ] Source topology diagram distinguishes T1 upstream branch division from T3 internal MZI couplers.
- [ ] SI-1 `E_in` reference-plane interpretation is supported by source evidence or explicitly remains an assumption.
- [ ] Complete two-output MZI port ordering and complex field convention are documented.
- [ ] Signal and monitor outputs are mapped separately.
- [ ] S2/S3 complex field equivalence is reproduced using the original source equations.
- [ ] S4 quadrature observable is reproduced with an explicit convention.
- [ ] Power conservation is checked over all relevant ports, with loss assumptions stated.
- [ ] Lean bridge is proved or clearly left as a proposed mapping.
- [ ] Physical PDK/EM and measured-device claims remain gated on actual evidence.

## 9. Current decision

**Cell 15 is frozen as a passing mathematical evidence record.**

The upstream I/W splitter ratio remains an explicit unresolved physical parameter. An equal split is a derived requirement only under the declared common-pre-split `E_src` convention used in the tested model.

The next engineering activity is source-topology and reference-plane resolution—not another splitter sweep and not yet full PhotonForge lowering.
