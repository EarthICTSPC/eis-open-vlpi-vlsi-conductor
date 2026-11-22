# EIS-TIAN-KKA-LIFT-001A — Source Ledger and Calibration Contract

**Owner:** Earth ICT, SPC  
**Version:** 0.1.0  
**Status:** Source snapshot frozen; interpretation and EIS transfer gates remain open  
**Branch:** \`eis-tian-kka-lift-001a-source-freeze\`  
**Primary source:** Tian et al., *Photonic Transformer Chip: Interference Is All You Need*, PhotoniX 6, 45 (2025), DOI: [10.1186/s43074-025-00182-7](https://doi.org/10.1186/s43074-025-00182-7).

## Purpose

Freeze the source facts and calibration model from Tian et al. before writing or running a new KKA optimizer. This package is a source-controlled reproduction baseline, not an EIS device qualification and not a claim that Tian's fitted parameters transfer to a different foundry or process.

This package is deliberately upstream of:

- \`EIS-KKA-001\` scalar interference/operator contract;
- \`EIS-PTC-MZI-001\` technology-independent three-heater MZI cell;
- any SOI/GF/AMF/TSMC PDK mapping;
- any optimization, array scaling, OASIS generation or fabrication.

## Frozen artifacts

1. \`source-ledger.yaml\` — source identity, source facts, provenance classes, open interpretation items.
2. \`table-s1-calibration.yaml\` — the ten Table S1 row records, retaining the shared coefficients and the row-order ambiguity.
3. \`calibration-contract.md\` — SI-3/SI-4 calibration equations, scope, required records, and acceptance gates.

## Source freeze and integrity

The supplementary PDF used for transcription is identified by SHA-256 in \`source-ledger.yaml\`. The article PDF is also identified there. A changed source file requires a new source revision and a reviewed ledger diff; do not silently edit frozen source values.

## Critical interpretation rules

- Tian's SI-4 empirical calibration observable is a fitted scalar interference response. It is **not** a complete complex device transfer function \(T_\mathrm{device}(V,\lambda,T)\).
- SI-4 Eq. (S13), not the simplified Eq. (S12), is the source-faithful non-ideal fit form.
- Table S1 contains fitted parameters, not raw measurement traces.
- The source does not explicitly state units for the Table S1 coefficients or the normalization of the fitted observable. These remain unresolved; do not invent units.
- Table S1 gives ten rows for ten \(A_i/B_i\) groups but does not print an individual group label beside each row. Row-to-index assignment is therefore retained as an explicit mapping assumption, not silently treated as measured fact.
- The paper's phase-error statistic uses ambiguous variance/\(\sigma\) language. The reported numbers are preserved verbatim in meaning; any derived bit-precision claim is blocked until the statistic is clarified.
- The reported Tian values are not GF, AMF, TSMC or EIS SOI process parameters. EIS characterization must create a separate dataset and parameter namespace.

## Provenance vocabulary

The original EIS ledger vocabulary is retained:

- \`tian_measured\`
- \`tian_fitted\`
- \`tian_assumed\`
- \`tian_projected\`
- \`eis_assumed\`
- \`eis_derived\`
- \`eis_verified\`
- \`gap\`

No source-derived value may be promoted to \`eis_verified\`. A fit is not raw measurement; a source report is not an EIS replication; formal proof is not physical validation.

## Freeze rule

The source snapshot is frozen at version 0.1.0. Corrections to transcription require a documented source correction and version increment. New EIS measurements, fitted parameters, process-specific models, or interpretation decisions are added as new records or new versions; they do not overwrite Tian's source records.

## Explicitly blocked

No KKA optimization code, optimizer tuning, physical-device simulation, or foundry-specific model fitting is authorized by this source freeze alone. The next gate is a human-reviewed source/contract review, followed by an independently implemented single-MZI reproduction.
