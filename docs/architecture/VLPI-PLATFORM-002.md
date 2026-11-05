# VLPI-PLATFORM-002 — VLPI-IR Schema + Cold-Start Reconstruction Test

**Project:** Earth ICT, SPC (EIS)  
**Status:** Schema release / cold-start validation  
**Artifact:** VLPI-PLATFORM-002  
**Date:** 2026-10-05

## Purpose

VLPI-PLATFORM-001 established the programming-model architecture and identified VLPI-IR as the missing intermediate representation.

This artifact makes that IR machine-readable and immediately tests whether a cold-start agent can traverse it.

The goal is deliberately narrow:

> Given only the repository, can an agent discover a VLPI-IR program, resolve its state spaces, transformations, RU, Contract, DesignContext, and Evidence references, reconstruct the intended physical computation, and stop at the actual evidence boundary?

This is an information-model and evidence-gating test. It is not a physics result.

## 1. What VLPI-IR represents

VLPI-IR is the technology-independent layer between computational intent and physical realization.

```
application intent
      ↓
VLPI-IR
      ↓
RU graph + state spaces + contracts
      ↓
DesignContext / PDKIdentity
      ↓
CRC / physical realization
      ↓
PVR / OASIS
```

VLPI-IR explicitly represents:

- physical state spaces;
- state representations and domains;
- contract-governed transformations;
- RU references;
- transformation composition and execution order;
- state boundaries;
- regeneration;
- resource and timing requirements;
- technology context references;
- evidence requirements;
- provenance.

It does **not** contain proprietary PDK content.

## 2. Schema status

The schema in `schema/vlpi-ir/vlpi-ir.schema.yaml` is the final schema for **VLPI-PLATFORM-002 v0.1.0**.

"Final" here means the artifact is internally coherent and machine-testable at this version. A future incompatible change requires an explicit schema-version change; it must not silently redefine the meaning of an existing field.

The schema intentionally keeps technology-specific implementation outside the IR. A VLPI-IR program points to a DesignContext; the DesignContext identifies the technology context used for physical realization.

## 3. Cold-start reconstruction

The test fixture in `examples/vlpi-platform-002/ru001-program.yaml` is intentionally small.

It describes one transformation:

```
H_input
   │
   ▼
RU-001
   │
   ▼
H_residual
   │
   ▼
declared state boundary
```

The cold-start agent must reconstruct:

1. The program contains one physical transformation.
2. That transformation resolves to `ru/RU-001/ru.yaml`.
3. RU-001 is a 2×2 MZI physical field transformation.
4. The RU contract resolves to `ru/RU-001/contract.yaml`.
5. The DesignContext resolves to `ru/RU-001/design-context.yaml`.
6. The Evidence manifest resolves to `ru/RU-001/evidence.yaml`.
7. The current status remains **specified**.
8. The evidence result is **not-run**.
9. PDR/PCT/PTV/BIST are **not-run** and foundry review is **not-requested**.
10. No fabrication, measured performance, or physical PASS may be inferred.

The test is therefore not merely "does YAML parse?" It tests the semantic reference graph.

## 4. Evidence boundary

The agent must distinguish two questions:

### Information-model validity

Does the IR instance satisfy the VLPI-IR schema, and do its references resolve?

### Physical/evidence validity

Has the referenced physical transformation actually satisfied its contract?

For this artifact:

- information-model validity: **PASS**;
- physical validation: **NOT RUN**;
- fabrication: **NOT RUN**;
- measurement: **NOT RUN**.

A schema-conformant IR is not evidence that the physical transformation works.

Likewise, existence of an Evidence file is not evidence of physical success.

## 5. Cold-start stopping rule

The reconstruction test must stop at the strongest status actually supported by repository evidence.

For the current fixture that status is:

```
specified
```

The agent must not promote the object to:

- formally verified;
- computationally demonstrated;
- experimentally demonstrated;
- measured;
- fabricated;
- PVR/PDR/PCT/PTV PASS;
- BIST PASS;
- foundry accepted.

## 6. Why this comes before the VLPI compiler

The compiler cannot safely lower an intermediate representation whose semantics are ambiguous.

VLPI-PLATFORM-002 therefore establishes the minimum machine-readable contract between:

```
program intent
    ↕
VLPI-IR
    ↕
RU / Contract / DesignContext / Evidence
```

Only after this graph can be reconstructed from a cold start should EIS implement the next layer:

**VLPI-PLATFORM-003 — VLPI-IR cold-start test hardening / adversarial reconstruction.**

The later compiler artifacts can then consume a defined IR rather than inventing one.

## 7. Failure is evidence

If the cold-start test fails, that failure is itself a repository artifact.

EIS should fix the information model explicitly rather than allowing an AI agent to fill missing semantics from general knowledge.

That preserves the EIS disclosure doctrine:

> Here is the architecture. Here are the contracts. Here are the interfaces. Here are the implementation rules. Here is the verification path. Here is the physical artifact. Make your own.

## 8. Relation to physical realization

VLPI-IR does not replace:

- RU contracts;
- DesignContext / PDKIdentity;
- CRC;
- PVR;
- OASIS;
- physics simulation;
- fabrication;
- BIST.

It provides the machine-readable program layer that connects those artifacts.

