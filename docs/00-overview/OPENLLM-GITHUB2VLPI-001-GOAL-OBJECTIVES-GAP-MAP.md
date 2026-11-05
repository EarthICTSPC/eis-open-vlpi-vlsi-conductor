# OPENLLM-GITHUB2VLPI-001: Goal, Objectives, and Evidence Gap Map

**Project:** Earth ICT, SPC (EIS)  
**Repository:** `EarthICTSPC/eis-open-vlpi-pdk`  
**Status:** Engineering artifact / open for independent critique  
**Purpose:** Establish a common target for EIS and independent LLM collaborators without prematurely selecting the computational ontology, compiler architecture, field algebra, agent population, or physical implementation.

---

## 1. Purpose

EIS is developing an open technical-disclosure layer for Very Large Photonic Infrastructure (VLPI).

The repository already establishes a physical-computing disclosure and verification path:

```text
Physical principle
      ↓
Physical state
      ↓
Transformation
      ↓
RU contract
      ↓
Physical primitives
      ↓
Composition
      ↓
Technology mapping
      ↓
CRC
      ↓
Physics simulation
      ↓
PVR / PDR / PCT / PTV
      ↓
OASIS
      ↓
Foundry review
      ↓
Fabrication
      ↓
BIST / State Boundary measurement
      ↓
Replication
      ↓
Useful computational service
      ↓
VLPI
```

This artifact adds a second engineering objective around that physical-computing path:

> **Use MCP-enabled AI agents to make the open VLPI design space accessible to open LLMs, and progressively establish whether those LLMs can discover, execute, verify, and ultimately drive useful photonic physical computation.**

The intended direction is **openLLM-GitHub2VLPI**.

This document does not prescribe the answer to the physical-computation problem. It defines what must be demonstrated before EIS may claim that the openLLM-GitHub2VLPI objective has been achieved.

---

## 2. Vision

### Vision

**An Earth-first ICT future in which useful computation can be performed by scalable, verifiable physical-computing infrastructure with substantially reduced dependence on unnecessary electronic state movement, energy dissipation, heat management, and associated infrastructure burden.**

VLPI is the physical-computing direction being investigated by EIS.

The vision is broader than any one device, PDK, agent, model, compiler, or implementation.

The vision is not evidence that the desired infrastructure has already been achieved.

---

## 3. Mission

### Mission

**Earth ICT, SPC develops and openly discloses the architecture, contracts, interfaces, verification methods, design tools, and physical artifacts required to investigate and independently implement VLPI physical-computing systems.**

The mission includes building an open technical path by which AI systems can participate in that engineering process.

The repository therefore serves two related purposes:

1. enable technically skilled independent implementation and verification of EIS physical-computing concepts; and
2. provide a machine-discoverable engineering environment in which AI agents and open LLMs can interact with those concepts without silently converting them into conventional digital-computing assumptions.

---

## 4. Goal

### Goal: openLLM-GitHub2VLPI

**Enable open LLMs, operating through MCP-enabled AI agents and the EIS GitHub technical environment, to discover, reason about, execute, verify, and progressively drive the VLPI design/verification workflow—while preserving explicit evidence boundaries—until a complete end-to-end path to useful physical photonic computation can be demonstrated.**

Conceptually:

```text
Open LLM
   ↓
MCP-enabled AI agent
   ↓
GitHub / open technical artifacts
   ↓
EIS-VLPI-MCP
   ↓
VLPI discovery / compatibility / transformation / verification
   ↓
physical design
   ↓
physics evidence
   ↓
fabrication / measurement
   ↓
verified physical transformation
   ↓
useful computational service
```

This is a **goal**, not a current capability claim.

In particular, the current repository does not establish that an open LLM has already executed useful computation on fabricated photonic hardware.

---

## 5. Objectives

The goal is decomposed into engineering objectives so that progress can be measured without conflating software execution, computational evidence, and physical evidence.

### Objective 1 — Machine-discoverable VLPI

Make VLPI concepts, contracts, capabilities, evidence states, and technology interfaces discoverable through machine-readable repository artifacts and MCP interfaces.

**Evidence target:**
- stable schemas/contracts;
- MCP discovery;
- reproducible capability descriptions;
- explicit evidence classifications;
- independent client discovery.

**Not sufficient:**
- prose documentation alone;
- an architecture diagram;
- an LLM claiming that it understands the repository.

---

### Objective 2 — Agent-executable VLPI interfaces

Enable an MCP-enabled AI agent to invoke permitted VLPI operations through stable interfaces.

**Evidence target:**
- tool discovery;
- valid invocation;
- deterministic or explicitly characterized results;
- execution record;
- error handling;
- evidence classification for each result.

**Not sufficient:**
- a tool existing in source code without successful execution;
- an LLM generating a plausible tool call;
- simulated physical claims presented as physical evidence.

---

### Objective 3 — Open-LLM interoperability

Demonstrate that multiple independent open LLMs can use the same public VLPI interface without being given an EIS-selected expected answer.

Candidate models may include open DeepSeek and other independently selected open models.

**Evidence target:**
- at least two independently configured open LLMs;
- same public repository/interface;
- same task specification;
- independently generated outputs;
- captured tool traces and evidence classification;
- differences preserved rather than normalized away.

**Not sufficient:**
- one model producing the expected answer;
- a prompt containing the expected agent population or ontology;
- human correction silently inserted between model output and execution.

---

### Objective 4 — Evidence-preserving AI engineering

Ensure that agent/LLM activity cannot silently promote:

- reference-model behavior to physical behavior;
- capability compatibility to fabrication;
- simulation to measurement;
- design target to demonstrated result;
- repository presence to physical verification.

**Evidence target:**
- machine-readable evidence states;
- explicit not-run state;
- promotion rules;
- reproducible execution records;
- independent review.

This objective is foundational to all later objectives.

---

### Objective 5 — Agent discovery of the physical design space

Determine whether AI agents can discover useful physical transformations, constraints, compositions, and verification actions from the design space rather than merely executing an EIS-predefined compiler or agent hierarchy.

**Evidence target:**
- independent derivations;
- disagreement analysis;
- machine-checkable contracts;
- reproducible candidate generation/evaluation;
- demonstrated reduction or discovery advantage where claimed.

**Not sufficient:**
- an invented swarm ontology;
- a predefined compiler architecture;
- a conventional matrix/vector/MAC decomposition imposed in advance;
- a plausible LLM-generated taxonomy.

The ontology must be allowed to emerge from reproducible engineering requirements.

---

### Objective 6 — Close the physical-design loop

Connect agent-discovered or agent-selected transformations to physical design, simulation, verification, and ultimately physical fabrication/measurement.

**Evidence target:**
- contract → technology mapping;
- executable physical design generation;
- physics simulation;
- PVR/PDR/PCT/PTV;
- machine-readable physical artifact;
- fabrication boundary;
- measured state-boundary evidence;
- comparison against the RU contract.

---

### Objective 7 — Demonstrate useful photonic computation

Demonstrate that a verified physical transformation or composition provides useful computational service on physical photonic infrastructure.

**Evidence target:**
- identified workload/service;
- physical artifact;
- measured operation;
- state-boundary evidence;
- reproducible performance/energy/error measurements;
- evidence connecting the physical transformation to the claimed useful service.

This is substantially beyond GitHub2VLPI-002.

---

## 6. Current demonstrated capabilities

The following are the capabilities established by the current EIS engineering record and should be kept separate from the open gaps below.

### 6.1 Public open technical-disclosure layer

The EIS repository is publicly accessible and is structured as an enabling technical-disclosure layer containing contracts, schemas, interfaces, verification methodology, reproducibility tooling, and physical-design artifacts where publication is permitted.

**Evidence state:** specified / public repository artifact.

---

### 6.2 Machine-readable VLPI architecture and contracts

The repository defines a Replicable Unit (RU) abstraction and a working state/transform/contract framework.

The current working abstraction is:

```text
S_RU = (H, T, R, B, G, C)
```

This is a working architectural abstraction. It is **not** established here as the only possible physical ontology.

**Evidence state:** specified.

---

### 6.3 EIS-VLPI-MCP discovery and execution

GitHub2VLPI-002 established an MCP server that can be launched through stdio and exposes six tools:

- `vlpi_discover`
- `vlpi_pdk_list`
- `vlpi_pdk_capabilities`
- `vlpi_validate_compatibility`
- `vlpi_run_pdk001`
- `vlpi_run_ru001_reference`

The successful run is frozen in the GitHub2VLPI-002 evidence record.

**Evidence state:** computationally demonstrated for the defined reference execution.

---

### 6.4 Reference RU-001 phase sweep

GitHub2VLPI-002 executed the defined five-phase reference sweep:

| Phase | Observed residualPower |
|---:|---:|
| 0 | 0.0 |
| π/2 | 0.9999999999999998 |
| π | 1.9999999999999996 |
| 3π/2 | 1.0 |
| 2π | 2.999519565323715e-32 |

The frozen interpretation records:

- cancellation at zero;
- maximum residual near π;
- zero residual power at zero;
- maximum observed residual power near 2 at π;
- five phase samples.

**Evidence state:** computationally demonstrated reference behavior.

This does **not** establish a unique physical field equation, fabricated-device behavior, measured optical behavior, or physical energy conservation.

---

### 6.5 PDK capability compatibility

The same execution demonstrated capability classification for the defined PDK matrix, including compatible, incompatible, and not-run cases.

The matrix distinguishes capability compatibility from physical validation.

**Evidence state:** computationally demonstrated capability classification.

---

### 6.6 Explicit evidence boundary

GitHub2VLPI-002 explicitly prohibited promotion of its results to:

- fabricated;
- measured;
- PVR PASS;
- BIST PASS;
- foundry accepted;
- physically verified.

**Evidence state:** specified/computationally exercised evidence doctrine.

---

### 6.7 Independent disagreement analysis

EIS-SWARM-001-A compared independent LLM-derived interpretations and deliberately preserved disagreement.

A key unresolved issue is whether the five-point reference sweep uniquely determines an exact field/residual functional. The independent derivations did not justify silently promoting one proposed formula into the EIS ontology.

**Evidence state:** independent analytical review / unresolved.

---

## 7. Open gaps

The following gaps separate the current demonstrated capabilities from the openLLM-GitHub2VLPI goal.

| ID | Gap | Current state | Evidence required to close |
|---|---|---|---|
| G-001 | Open LLM → MCP interoperability | Open | Independent open-LLM execution traces using the public MCP interface |
| G-002 | Multiple-model reproducibility | Open | Same task executed by multiple independently configured open LLMs |
| G-003 | LLM-independent interface semantics | Partial | Demonstrate that models can discover/use interfaces without EIS-specific expected answers |
| G-004 | GitHub → agent → VLPI closed loop | Partial | End-to-end reproducible task from repository discovery through executable VLPI result |
| G-005 | Agent discovery of physical transformations | Early research | Independent derivation + executable evaluation + evidence classification |
| G-006 | Minimum formal transformation vocabulary | Candidate 4-tuple proposed; not yet established | Independent execution test + sufficiency/minimality analysis + discriminating experiment/observation + formal contract |
| G-007 | Exact reference field/residual functional | Unresolved | Observation sufficient to distinguish competing functional interpretations |
| G-008 | Compiler requirements | Deliberately unresolved | Requirements generated by demonstrated physical design transformations |
| G-009 | Physical-design generation | Open | Contract-to-layout executable path with reproducible PVR/PCT/PTV evidence |
| G-010 | Physics validation | Open | Full-wave/appropriate physics simulation tied to the same contract and artifact |
| G-011 | Physical RU fabrication | Open | Fabricated identified artifact |
| G-012 | State-boundary measurement/BIST | Open | Measurement/BIST record for identified physical artifact |
| G-013 | Replicated physical computation | Open | Independent replication with contract/evidence comparison |
| G-014 | Useful computational service | Open | Measured physical service tied to a defined workload and evidence chain |
| G-015 | Energy/environmental system evidence | Open | Measured/system-level evidence supporting any claimed energy, heat, infrastructure, or CO₂e benefit |

---

## 8. Evidence required to close the gaps

### 8.1 Software/LLM layer

A valid openLLM-GitHub2VLPI software demonstration should record at minimum:

```text
model identity
model configuration
prompt/task specification
repository revision
MCP interface revision
tool discovery trace
tool invocation trace
tool results
agent decisions
errors/retries
evidence classification
final output
```

The experiment should permit another reviewer to determine what came from the model, what came from the tool, and what was supplied by a human.

---

### 8.2 Transformation-discovery layer

A valid transformation-discovery experiment should distinguish:

```text
observed result
      ↓
candidate interpretation
      ↓
formal contract
      ↓
executable test
      ↓
discriminating observation
      ↓
accepted / rejected / unresolved
```

An LLM-generated mathematical explanation is not, by itself, evidence that the corresponding physical transformation exists.

---

### 8.3 Physical-design layer

A valid physical-design closure should establish a traceable chain:

```text
contract
  ↓
technology context / PDK identity
  ↓
physical primitives
  ↓
layout
  ↓
PVR / PDR / PCT / PTV
  ↓
OASIS
  ↓
foundry boundary
  ↓
fabrication
  ↓
measurement / BIST
  ↓
state-boundary acceptance
```

The exact tools and physical representation remain technology-dependent.

---

### 8.4 Useful-service layer

A claim of useful photonic computation requires more than successful optical device operation.

At minimum, the evidence must identify:

- the useful computational service;
- the physical transformation performing it;
- the input/output state definition;
- the acceptance boundary;
- measured error/accuracy;
- relevant timing/throughput;
- relevant energy/resource measurements;
- reproducibility conditions.

---

## 9. What GitHub2VLPI-002 already establishes

GitHub2VLPI-002 establishes a bounded and reproducible **reference-computation/MCP execution boundary**.

It demonstrates that:

1. an EIS MCP server can be discovered and executed through the defined stdio interface;
2. the defined VLPI tools can be invoked;
3. a reference RU-001 phase sweep can execute;
4. reference residual observations can be produced;
5. PDK capability compatibility can be classified;
6. incompatible and not-run states can be represented;
7. evidence boundaries can be preserved;
8. the result can be frozen as an auditable engineering artifact.

It does **not** establish:

- an open LLM performing the execution;
- model-independent agent behavior;
- a physical optical transformation;
- a fabricated RU;
- measured optical behavior;
- BIST PASS;
- foundry acceptance;
- physical validation;
- useful photonic computation;
- an end-to-end openLLM-GitHub2VLPI system.

---

## 10. What must be demonstrated before claiming openLLM-GitHub2VLPI

EIS should not claim the complete openLLM-GitHub2VLPI capability until an evidence chain exists across all required layers.

### Minimum claim boundary

```text
Open LLM
   ↓
independent MCP-enabled agent
   ↓
public EIS GitHub artifacts
   ↓
VLPI-MCP discovery
   ↓
VLPI operation
   ↓
reproducible result
```

This would support an **openLLM-GitHub2VLPI software/integration demonstration**, but not yet a physical-computing claim.

### Full physical claim boundary

A stronger claim requires:

```text
Open LLM
   ↓
agent
   ↓
GitHub / MCP
   ↓
VLPI transformation discovery/design
   ↓
formal contract
   ↓
physical design
   ↓
physics evidence
   ↓
fabrication
   ↓
measurement / BIST
   ↓
verified physical transformation
   ↓
useful computational service
```

Only after this chain is demonstrated should EIS make a full end-to-end claim involving open LLMs driving useful physical photonic computation.

---

## 11. What remains outside the current evidence boundary

The following remain outside the current evidence boundary and must not be inferred from the repository, GitHub2VLPI-002, or SWARM-001-A:

### Physical claims

- fabricated photonic hardware;
- measured optical fields;
- measured state retention;
- measured thermal behavior;
- measured error probability;
- foundry acceptance;
- wafer yield;
- stacked-wafer operation;
- hyperscale operation.

### Performance/environmental claims

- universal energy advantage;
- universal heat elimination;
- infrastructure-scale power reduction;
- CO₂e reduction demonstrated by hardware;
- superiority to GPUs or other compute systems for a defined useful workload.

### Computational ontology

- a unique field algebra;
- a unique field representation;
- a mandatory matrix/vector representation;
- a mandatory MAC representation;
- a mandatory Boolean representation;
- a unique agent population;
- a unique swarm decomposition;
- a compiler architecture.

### AI/agent claims

- open LLM autonomy;
- model-independent reasoning;
- reliable autonomous physical-design discovery;
- autonomous fabrication;
- safe autonomous modification of physical process parameters;
- general-purpose AI running natively on VLPI.

### RU/LLM workload claims

- fully optical attention;
- optical top-k selection;
- optical LLM inference;
- agent branching as a demonstrated photonic workload;
- RU-002 as experimentally demonstrated.

---

## 12. The current research question

The current engineering question should remain deliberately narrower than the final goal:

> **What is the smallest formal and executable vocabulary required for an independent AI agent to discover, execute, verify, and compose the physical transformations actually demanded by the VLPI design space?**

This question must be answered from evidence.

It must not be answered by deciding in advance that the answer is:

- a conventional compiler;
- a matrix algebra;
- a Boolean instruction set;
- an analog-MAC abstraction;
- a fixed swarm;
- a preselected field algebra.

---

## 12.1 Candidate minimal executable vocabulary: (S, T, O, C)

An independent LLM review proposed the following candidate minimal vocabulary:

```text
State        S
Transition   T
Observation  O
Contract     C
```

Conceptually:

```text
State       ::= representation of a physical configuration
Transition  ::= parameterized process mapping input state to output state
Observation ::= recorded observation of a state under specified conditions
Contract    ::= predicate determining acceptance
```

The proposed role mapping is:

| Agent capability | Candidate element |
|---|---|
| Discover | S + O |
| Execute | T |
| Verify | C |
| Compose | S + T |

The proposal also maps the candidate vocabulary against the current RU abstraction:

| RU element | Candidate vocabulary | Current classification |
|---|---|---|
| H | S | compatible abstraction |
| T | T | compatible abstraction |
| R | — | not currently forced |
| B | C | compatible as an acceptance relation |
| G | — | not currently forced |
| C | C | compatible abstraction |

### Important epistemic qualification

The 4-tuple is **not promoted as proven minimal merely because it is intuitively sufficient**.

The current evidence supports the need to represent states, transformations, observations/results, and acceptance conditions at the engineering level, but it does not yet establish that:

- all four must be independent primitives;
- Observation cannot be derived from State plus an execution/evaluation record;
- Contract cannot be represented as metadata attached to another object;
- Composition requires no additional relation or typing structure;
- the four-tuple is sufficient for every transformation in the VLPI design space;
- the four-tuple is minimal under a formally defined notion of minimality.

Therefore the correct current status is:

> **(S, T, O, C) is a strong candidate minimal vocabulary for independent critique and experimental testing, not a newly adopted EIS ontology.**

This distinction is important because the purpose of SWARM-001-A is to discover the smallest vocabulary demanded by the design space rather than to select a preferred abstraction by inspection.

### Minimality test

A candidate vocabulary can only become an engineering result if an experiment can attempt to use it without importing a richer ontology.

The proposed next test is:

```text
independent open LLM / agent
          ↓
(S, T, O, C)-only task specification
          ↓
discover candidate transformation
          ↓
execute transition
          ↓
record observation
          ↓
evaluate contract
          ↓
compose with another accepted transition
```

The experiment must publish:

- the exact task specification;
- the model and agent identity;
- the repository revision;
- the vocabulary definition supplied to the agent;
- raw observations;
- transition inputs and outputs;
- contract evaluations;
- composition attempts;
- failures and retries;
- human interventions, if any;
- evidence classification.

A successful run would provide evidence of **sufficiency for that bounded task**. It would not by itself prove global minimality.

### Discriminating questions

The experiment should explicitly test:

1. Can the agent perform the task without assuming a Boolean, matrix/vector, MAC, or predefined field algebra?
2. Can the same State representation be used across a composed transition boundary?
3. Can Observation be removed or derived without loss of reproducibility or verification?
4. Can Contract be removed or folded into another element without loss of explicit acceptance?
5. Does composition require a new relation/type beyond State and Transition?
6. Do R-like constraint reduction or G-like regeneration emerge as independently necessary operations?
7. Does the physical design space introduce a required primitive not present in (S, T, O, C)?

The answers—not the elegance of the tuple—should determine the next ontology revision.

---

## 13. Independent LLM review target

This artifact is intended to be given, unchanged, to:

- DeepSeek;
- Grok;
- Claude;
- open DeepSeek instances;
- future open LLM collaborators;
- independent human technical reviewers.

The reviewer should be asked:

1. Which statements are directly established by the current artifacts?
2. Which statements are only architectural specifications?
3. Which gaps are incorrectly classified as open, partial, or closed?
4. What evidence is actually sufficient to close each gap?
5. Which proposed evidence requirements introduce assumptions not forced by the current design?
6. What is the smallest experiment that distinguishes competing interpretations?
7. What claims should remain prohibited?
8. Does the goal require a compiler at all?
9. Does the goal require a fixed agent population?
10. What physical evidence is necessary before the software demonstration can legitimately be connected to physical photonic computation?

A reviewer must not be given an expected ontology or expected agent population.

Disagreement is evidence about specification stability; it is not evidence of physical truth.

---

## 14. Engineering status

### Established

- Public EIS VLPI repository.
- Open technical-disclosure model.
- Machine-readable architecture/contracts.
- EIS-VLPI-MCP discovery and execution.
- GitHub2VLPI-002 frozen computational evidence.
- Explicit capability/not-run/evidence classifications.
- Independent LLM disagreement analysis.

### In progress

- Independent LLM population derivation.
- Minimum formal transformation vocabulary.
- Open-LLM/MCP interoperability.
- GitHub-to-agent-to-VLPI execution loop.
- Discriminating experiments for unresolved reference transformations.

### Not established

- Physical RU validation.
- Fabricated/Measured/BIST evidence.
- End-to-end openLLM-GitHub2VLPI physical computation.
- Useful computational service on VLPI hardware.
- Environmental/system-level benefit from measured hardware.

---

## 15. Governing principle

> **EIS is not building a compiler so that photonics can imitate conventional computing. EIS is building the open LLM, agent, GitHub, MCP, contract, verification, and physical-design path that allows the physical design space to determine what computational abstractions are actually required.**

Therefore:

> **Discover the ontology. Do not design it prematurely.**

And:

> **A successful software execution is evidence of software execution. It is not evidence of physical photonic computation unless the physical evidence chain has also been closed.**

---

## 16. Relationship to existing EIS artifacts

This artifact should be read together with:

- `README.md`
- `docs/00-overview/INDEPENDENT_LLM_REVIEW_GUIDE.md`
- `docs/00-overview/EIS_Open_VLPI_Disclosure_Doctrine.md`
- `evidence/github2vlpi-002/FROZEN-EMPIRICAL-EVIDENCE.json`
- `evidence/github2vlpi-002/github2vlpi-002-run.json`
- `docs/architecture/EIS-SWARM-001-A-DISAGREEMENT.md`

Those artifacts remain authoritative for their respective evidence and disclosure boundaries.

This document does not supersede the frozen GitHub2VLPI-002 evidence record or the disagreement analysis. It provides the common engineering target against which future LLM and human review can be performed.

---

**Earth ICT, SPC (EIS)**  
*Open physical-computing infrastructure for an Earth-first ICT future.*
