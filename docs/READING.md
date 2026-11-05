# Reading List: Photonic Computing and AI

**Purpose:** Maintain a small, growing, annotated reading list for the scientific and engineering work informing Earth ICT, SPC (EIS) and the open VLPI architecture.

This is a reading list, not an EIS endorsement of every claim in a cited work. Keep reported results, simulations, projections, and EIS hypotheses clearly distinguished. Add citations as the work is read and assessed.

## Photonic attention and transformer computation

### 1. Photonic transformer chip: interference is all you need

- **Authors:** Ye Tian et al.
- **Published in:** *PhotoniX*, volume 6, article 45 (2025).
- **DOI:** [10.1186/s43074-025-00182-7](https://doi.org/10.1186/s43074-025-00182-7)
- **Full text:** [Springer Nature article](https://link.springer.com/article/10.1186/s43074-025-00182-7)
- **Why read it:** Presents a photonic transformer chip using runtime-programmable optical interference and a proposed Kramers–Kronig attention (KKA) mechanism. Relevant to EIS investigation of interference-native computation, balanced detection, attention semantics, and the boundary between mathematical equivalence and physical implementation.
- **Reading questions for EIS:**
  1. Which properties are derived analytically, numerically simulated, or experimentally measured?
  2. What exactly is the computational primitive and what does the paper count as an operation?
  3. How are amplitude–phase coupling, fabrication variation, programming non-ideality, and thermal crosstalk represented?
  4. Which parts of the attention mechanism are optical, and which functions remain electronic?
  5. What can be reproduced using an open, independently specified RU contract and an authorized PDK?
- **Evidence caution:** The paper's reported experimental prototype results and projected scaling figures are different evidence categories. Do not treat a projected peak capability as measured throughput, or infer EIS performance from the paper.

## Photonic similarity and KV-cache selection

### 2. PRISM: Photonic Similarity Engine for KV Cache Block Selection in Long-Context LLM Inference

- **Authors / version:** Verify from the cited manuscript's current metadata when reviewing or citing it.
- **Manuscript:** [arXiv HTML, version 2](https://arxiv.org/html/2603.21576v2)
- **Why read it:** Proposes using photonic broadcast-and-weight similarity evaluation to select key–value cache blocks for long-context LLM inference. Relevant to EIS RU-002, optical similarity states, memory traffic, top-k selection, and heterogeneous optical/electronic state boundaries.
- **Reading questions for EIS:**
  1. Which operations are performed optically, and which remain electronic (including top-k and KV fetch)?
  2. What is the assumed signature, weight-bank, wavelength, and resonator capacity?
  3. Which latency and energy figures are measured versus simulated or projected?
  4. What are the calibration, thermal-control, fabrication-tolerance, and scaling assumptions?
  5. Does the proposed O(1) optical selection claim include the complete end-to-end service, or only the optical evaluation stage?
- **Evidence caution:** Treat the manuscript's stated simulation, benchmark, and scaling claims according to their stated methods and system boundaries. Do not describe a proposed or simulated design as a fabricated, measured EIS implementation.

## Suggested reading-record format

For each new reference, record:

- Full citation and stable DOI / arXiv / publisher URL
- Version and access date, where relevant
- Research question and claimed contribution
- Relevant equations, physical primitives, and computational semantics
- Evidence classification: **formal derivation**, **numerical simulation**, **physical measurement**, **projection**, or **author hypothesis**
- Assumptions, system boundary, and unresolved limitations
- Reproducibility artifacts and licensing / access constraints
- Specific implications for EIS contracts, CRC, RU definitions, PDK mapping, or experiments

**EIS principle:** Read broadly; cite precisely; separate what a paper proves, simulates, measures, and projects.
