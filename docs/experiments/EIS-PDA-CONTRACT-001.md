# EIS-PDA-CONTRACT-001 — Contract-Governed Photonic Design Automation

**Status:** Proposed, software-first experiment  
**Architectural reference:** L. Chung, “LLM-assisted agentic workflow for silicon photonic design automation,” Optics Express, DOI: 10.1364/OE.604609; supplement DOI: 10.6084/m9.figshare.33390811.  
**Repository issue:** #undefined

## 1. Purpose

Determine whether EIS can make an LLM-assisted photonic design workflow preserve computational meaning from a natural-language request through typed requirements, formal acceptance, deterministic lowering, execution, and evidence capture.

Chung's work is an architectural reference for constrained routing, explicit parameter mapping, database-backed case reuse, and simulation fallback. EIS is not adopting its IPKISS/n8n stack or treating its reported workflow success rates as physical-design validation.

## 2. EIS authority model

1. **LLM interface:** proposes candidate requirements and classifies intent. It is advisory.
2. **Lean4 formal authority:** defines operation semantics, invariants, preconditions, and acceptance. It is not replaceable by prompts, model confidence, or API success.
3. **Deterministic lowering:** converts an accepted typed request into a canonical device/reference-model request.
4. **Execution adapters:** initially a software reference backend. Future SOI/KKA PDK, simulator, layout, and measurement adapters remain separate and replaceable.
5. **Evidence record:** binds each outcome to the request, contract revision, toolchain, test vector, artifact, and acceptance decision.

A simulator output is evidence to be checked against a contract; it is not itself a proof. A PDK constrains physical realizability; it does not redefine the computation.

## 3. Initial computational reference

Use the existing scalar KKA operation:

$$ X(a,b)=2\\operatorname{Re}(a\\overline b) $$

The request schema must explicitly identify complex-number representation, conjugation convention, units/normalization where applicable, operation version, and provenance. Do not silently assume a missing required parameter or reinterpret a signed real cross-term as a complete complex overlap.

## 4. Three-flow comparison

| Flow | Responsibility split | What it tests |
|---|---|---|
| A-flow | LLM selects and parameterizes an allowed reference operation | Unconstrained tool selection and parameter extraction |
| B-flow | Deterministic parser, typed mapping, explicit routing and rules | Reliability gained by deterministic orchestration |
| EIS contract-gated | LLM proposes; Lean4 gates; deterministic lowering executes | Whether formal authority prevents semantically invalid requests reaching execution |

All flows use the same frozen request corpus, operation definitions, test vectors, and scoring rules. Do not compare unlike workloads or count API invocation as computational correctness.

## 5. Work packages

### WP1 — Freeze the test corpus

Create valid, invalid, boundary, malformed, ambiguous, missing-field, and unsupported-operation requests. Record expected normalized request or expected rejection reason before running any flow. Keep a held-out subset for final comparison.

### WP2 — Typed request and formal gate

Define a versioned typed request with operation identifier and contract version; complex inputs and representation convention; units and normalization convention where applicable; required and optional fields; source/provenance and parser version; and explicit unknown, unsupported, and invalid outcomes.

Bind admissibility to the existing Lean4 scalar KKA contract. No LLM-produced proof, self-reported confidence, or downstream success can override the formal gate.

### WP3 — Deterministic lowering and reference execution

Lower accepted requests into a canonical, stable representation. Identical normalized inputs and tool versions must produce byte-identical serialized requests. Execute a dependency-free software reference implementation and test it against independently prepared expected vectors.

### WP4 — Evidence and provenance

For each case, retain the original natural-language request; extracted candidate fields and parser/classifier version; normalized typed request or rejection; Lean4 contract revision and gate result; deterministic lowering output; execution backend/version and inputs; output, checks, and acceptance result.

A future backend must additionally bind PDK identity/version, device model versions, solver settings, layout artifacts, and foundry-rule results. Do not claim those future records exist in this experiment.

### WP5 — Benchmark and decision

Report correct operation selection; parameter fidelity including units and complex conventions; contract acceptance/rejection correctness; false acceptance and false rejection separately; unsupported-assumption detection; deterministic reproducibility; latency and LLM token use; accepted-result rate and human-review burden.

The primary measure is the rate of **correctly accepted engineering requests**, not tool-call success alone.

## 6. Acceptance criteria

- [ ] Lean4 remains the acceptance authority.
- [ ] Every input is accepted as a typed canonical request or rejected with a machine-readable reason.
- [ ] No silent defaults for required fields.
- [ ] Units, complex representation, conjugation convention, and operation identity are explicit.
- [ ] Identical normalized inputs/tool versions lower reproducibly.
- [ ] Tests cover valid, invalid, boundary, malformed, ambiguous, missing, and unsupported inputs.
- [ ] A/B/EIS flows use the same frozen corpus and scoring rules.
- [ ] False acceptance and false rejection are separately reported.
- [ ] Every outcome has traceable provenance.
- [ ] Synthetic data is labeled synthetic; software results are not represented as device measurements.

## 7. Gates

- **G0 — Corpus freeze:** cases, expected outcomes, scoring rules, and held-out split reviewed.
- **G1 — Formal gate:** Lean4 contract binding and typed request schema reviewed; build and axiom audit pass.
- **G2 — Deterministic execution:** canonical lowering and reference tests pass.
- **G3 — Benchmark:** all three flows run against the same corpus; machine-readable report generated.
- **G4 — Review/decision:** independent review determines whether to revise, stop, or design a separate SOI/KKA backend adapter.

## 8. Explicit exclusions

This work does not authorize fabrication, MPW booking, foundry engagement, PDK download or ingestion, NDA-data use, paid simulation, FlexCompute jobs, DRC/LVS claims, or physical-performance claims. No adoption of n8n, IPKISS, PostgreSQL/pgvector, Ollama, or a particular LLM is required.

## 9. Decision sought

Approve the contract-governed workflow as the EIS reference architecture only if the benchmark shows that formal gating reduces false acceptance without making valid engineering requests unusably difficult to express. Otherwise revise the schema and gate before any physical backend work.