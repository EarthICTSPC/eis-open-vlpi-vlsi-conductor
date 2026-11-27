# EIS-KKA-SOFTMAX-ELIMINATION-001A
## Tian 10×1 Computational Baseline

**Status:** Draft work package; implementation and reproduction not yet run  
**Parent contract:** EIS-KKA-SOFTMAX-ELIMINATION-001  
**Depends on:** EIS-KKA-TOPOLOGY-REFERENCE-PLANE-001; EIS-KKA-SOURCE-MAPPING-001  
**Repository:** EarthICTSPC/eis-open-vlpi-vlsi-conductor  
**Primary source:** Tian et al., *Photonic Transformer Chip: Interference Is All You Need*, PhotoniX 6, 45 (2025), DOI: [10.1186/s43074-025-00182-7](https://doi.org/10.1186/s43074-025-00182-7)

---

## 1. Objective

Reproduce, as faithfully and transparently as the public source permits, the Tian KKA-versus-standard-attention computational comparison associated with the 10×1 PTC processing-unit array.

The central question is:

> Can the KKA attention path perform the declared useful workload with no conventional SoftMax operation in that attention path, while meeting predeclared functional and task-level acceptance criteria?

This work package establishes a reproducible computational baseline. It does **not** claim that the work has already been reproduced, that an ideal mathematical model is a physical chip, or that KKA is an exact identity for conventional SoftMax on every input.

## 2. Terminology and scope guard

The paper describes a PTC with a 10×1 processing-unit array. For the numerical ViT example, it reports an input tensor of size 10×10, query/key/value weight matrices of size 10×10, and two attention heads of size 10×5.

Do not silently interpret “10×1” as a 10-token sequence, a 10×10 MZI mesh, or a 10-head attention model. Preserve the paper's distinction between:
- the physical PTC processing-unit array designation (10×1);
- the numerical ViT tensor shapes (including X and Wq/Wk/Wv at 10×10);
- the two-head decomposition (each head 10×5); and
- the physical experiment's 100-sample MNIST evaluation.

The scope is **attention SoftMax elimination**. It does not prohibit unrelated output-probability formatting or loss functions outside the attention path. Any such operation must be separately named and located in the graph.

## 3. Source-reported baseline facts

The following are source-reported targets and must not be presented as EIS-reproduced results until independently rerun.

### 3.1 Numerical ViT comparison

The paper reports:
- MNIST task.
- ViT with two multi-head attention heads.
- 28×28 input images.
- Images reshaped into 49 flattened 4×4 patches.
- Patch representation mapped to 10 dimensions; the article describes a 10×50 feature size at this stage.
- Learnable one-dimensional positional embeddings.
- Layer normalization and a further linear transformation to a 10×10 representation for the PTC-aligned attention calculation.
- Q, K, V weight matrices of size 10×10.
- Two heads, each with size 10×5.
- KKA attention substituted for standard self-attention in the comparison model.
- Reported numerical MNIST accuracy: KKA-ViT 96.79%; standard-attention ViT 96.31%.

The paper describes KKA as:
\[
\operatorname{SoftMax}(Q^T K/\sqrt{d})V
\sim
(Q_{\mathrm{KKA}}^T\,\square\,K_{\mathrm{KKA}})
\,\square\,V_{\mathrm{KKA}}.
\]

The symbol \(\square\) denotes the paper's interference operation. The relation is an approximation / learning-capability claim, not a universal algebraic equality.

### 3.2 Physical PTC evaluation

The paper separately reports:
- 100 randomly selected MNIST test samples for the PTC experiment.
- 10,000 attention-matrix elements in the experiment-versus-prediction comparison (10×10×100).
- Mean normalized experiment-prediction error: 8.923×10⁻⁴.
- Standard deviation: 0.00613.
- Reported effective precision: approximately 8.3 bits.
- Reported KKA-ViT PTC inference accuracy: 94% on those 100 samples.

These are paper-reported physical results. They are not the acceptance threshold for a new EIS device, nor are they interchangeable with the full-dataset numerical result.

### 3.3 Training details available in the article

The article reports PyTorch, stochastic gradient descent, momentum 0.9, weight decay 0.0001, MNIST mini-batch size 128, and two attention heads. It describes backpropagation training.

The exact random seeds, all optimizer/scheduler settings, epoch counts for the MNIST run, full architecture details, exact preprocessing implementation, and complete numerical data are not established by the article text currently captured in this work package. The article says numerical data and a public code version are available from the authors on reasonable request; SI-13 contains pseudocode.

**Do not invent missing hyperparameters.** Obtain and archive SI-13 and the full supporting-information training details. Request the authors' code/data if necessary. If any source detail remains unavailable, record it as an EIS reproduction choice rather than attributing it to Tian.

## 4. Baseline tracks

Keep three tracks separate.

### Track A — Source-faithful numerical reproduction

Recreate the published PyTorch ViT comparison:
1. Standard-attention reference.
2. KKA attention replacement.
3. Same declared data split, preprocessing, model dimensions, training budget, optimizer, and evaluation procedure wherever the source specifies them.
4. Separate model checkpoints and full configuration manifests.
5. Record any unavailable source setting as unresolved or as an explicit EIS choice.

This track tests the computational claim without requiring a photonic simulator.

### Track B — SoftMax-free inference graph audit

For the KKA model:
1. Export or capture the deployed inference graph.
2. Identify the attention subgraph and its operators.
3. Confirm there is no conventional SoftMax in the KKA attention path.
4. Inspect runtime operator traces for hidden SoftMax calls or fallback paths.
5. Record every remaining normalization and nonlinear operator, its location, and its purpose.
6. Distinguish the attention path from output-probability and loss-related operations.

A graph that merely renames SoftMax, invokes it through a helper, or falls back to it at runtime fails this gate.

### Track C — PTC 10×1 physical-result comparison

Only after Tracks A and B are reproducible:
1. Compare the numerical prediction for the same 100 selected MNIST test samples with the source-reported PTC measurements, if the underlying sample-level data can be obtained.
2. Preserve the 10×10 attention-element comparison separately from end-task classification accuracy.
3. Record calibration, phase programming, thermal crosstalk compensation, normalization, and measurement details.
4. If raw data cannot be obtained, label the published 94% and error statistics as literature reference values only. Do not claim an independent reproduction.

PhotonForge ideal-circuit work and later physical device modeling are downstream lowering tasks; neither substitutes for Tracks A or B.

## 5. Required configuration manifest

Every run must produce a machine-readable manifest containing at least:

- Work-package ID and contract revision.
- Source article and supporting-information revision/hash.
- Code repository, commit, and working-tree status.
- Python, PyTorch, CUDA/backend, and dependency versions.
- Dataset source, checksums, split, preprocessing, and sample ordering.
- Model architecture and tensor-shape ledger.
- Attention implementation identifier (standard_attention or tian_kka).
- Exact KKA equation/mapping revision and domain restrictions.
- Random seeds for initialization, data shuffling, and evaluation.
- Optimizer, learning rate, scheduler, momentum, weight decay, batch size, epochs, and stopping rule.
- Checkpoint hashes.
- Inference graph export and operator inventory.
- Evaluation metrics and per-sample outputs.
- Evidence classification and artifact hashes.

Missing values must be explicit null / UNRESOLVED, not silently defaulted.

## 6. Acceptance test matrix

| ID | Test | Procedure | Acceptance condition |
|---|---|---|---|
| 001A-T01 | Source-shape ledger | Encode all reported tensor and head dimensions | Shapes match source; ambiguities explicitly recorded |
| 001A-T02 | Dataset integrity | Verify MNIST source, checksums, split, preprocessing, and sample order | Deterministic and fully manifested |
| 001A-T03 | Standard-attention baseline | Train/evaluate reference ViT | Reproducible run with complete configuration and metrics |
| 001A-T04 | KKA baseline | Train/evaluate the KKA-substituted ViT | Reproducible run with complete configuration and metrics |
| 001A-T05 | Apples-to-apples comparison | Compare models under matched data, architecture outside attention, and declared training budget | Differences limited to documented attention substitution and unavoidable declared settings |
| 001A-T06 | Attention SoftMax exclusion | Inspect KKA inference graph and runtime trace | No conventional SoftMax in KKA attention path |
| 001A-T07 | Operator audit | Inventory all attention-path operations | Every operation identified; no hidden SoftMax or undocumented fallback |
| 001A-T08 | Functional output comparison | Compare KKA and standard-attention outputs on the same evaluation inputs | Pre-registered output metrics and tolerances pass |
| 001A-T09 | Task-level comparison | Compare MNIST test accuracy and per-class metrics | Pre-registered task threshold passes |
| 001A-T10 | Determinism / repeatability | Repeat evaluation from pinned checkpoints and data order | Outputs and metrics reproducible within declared numerical tolerance |
| 001A-T11 | Physical-reference comparison | Compare against source PTC data only if raw paired data are available | Sample-level comparison; otherwise literature-only status |
| 001A-T12 | Provenance completeness | Validate manifest and artifact hashes | No missing mandatory provenance fields |

### Threshold policy

Do not set a post hoc tolerance to force a pass. Before the first acceptance run, freeze:
- output-error metric(s) and thresholds;
- task-accuracy floor and allowed difference from the standard-attention baseline;
- repeatability tolerance;
- treatment of stochastic training variation; and
- the exact evaluation split.

The paper's 96.79%, 96.31%, and 94% are source-reported comparison points, not automatic EIS acceptance thresholds. A reproduction target and a new EIS product requirement are different decisions.

## 7. Required artifacts

The work package is not complete until it contains:

1. source-ledger.md — exact source facts, page/figure/equation locations, and unresolved details.
2. baseline-config.yaml — fully populated run configuration; no silent defaults.
3. standard_attention and tian_kka model implementations or pinned external source references.
4. softmax_audit.json — graph operator inventory and runtime trace result.
5. metrics.json — per-run and comparison metrics.
6. evidence-manifest.json — versions, hashes, provenance, and evidence classifications.
7. Reproduction instructions sufficient for an independent operator to rerun the work.

No artifact may label a literature-reported value as measured by EIS.

## 8. Decision gates

- **A — Source details frozen:** SI-13 and relevant supplementary details reviewed; missing training settings classified.
- **B — Numerical reference reproduced:** standard-attention and KKA numerical runs complete and manifested.
- **C — SoftMax-free inference accepted:** graph and runtime audits pass.
- **D — Functional comparison accepted:** predeclared output and task thresholds pass.
- **E — Physical reference reconciled:** raw PTC data compared if obtainable; otherwise literature-only status recorded.
- **F — Lowering handoff:** computational contract and known numerical error budget handed to PhotonForge/physical-lowering work.

No physical component simulation is required to pass Gates A–D.

## 9. Known limitations and explicit non-claims

- The KKA relation is an approximation supported by theory, numerical training, and the reported PTC experiment; it is not claimed as an exact pointwise replacement for SoftMax for all tensors.
- A trained model with good accuracy does not alone establish that SoftMax was absent from its inference path; the graph/runtime audit is mandatory.
- A SoftMax-free attention path does not mean the entire model contains no nonlinearities or normalization.
- The reported 94% physical accuracy is based on 100 selected MNIST test samples, not the full 10,000-image test set.
- The reported numerical accuracy and physical-chip accuracy must remain separate.
- This work package does not establish energy advantage. Energy measurement belongs to the later system-boundary gate.

## 10. Immediate execution order

1. Retrieve and archive the publisher supporting information, especially SI-13 and the training details.
2. Build the source-ledger and resolve the exact 10×1 / 10×10 / two-head shape interpretation.
3. Obtain the authors' public code/data if available; otherwise document a source-faithful reimplementation plan.
4. Freeze training/evaluation configuration and thresholds before running.
5. Implement and run the standard-attention and KKA numerical baselines.
6. Perform the KKA inference graph and runtime SoftMax audit.
7. Report PASS / FAIL / BLOCKED for every test; do not proceed to physical lowering as if a blocked computational gate had passed.

**Governing result:** A successful 10×1 baseline is evidence of useful SoftMax-free KKA attention on a reproducible workload. It is not yet evidence of a qualified photonic implementation or an energy advantage.
