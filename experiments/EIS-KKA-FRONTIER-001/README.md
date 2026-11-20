# EIS-KKA-FRONTIER-001 — Qwen3-8B model-to-hardware map

**Status:** initial model/configuration mapping and numerical surrogate added; not yet CI-verified, trained, simulated or physically measured.  
**Parent:** `eis-kka-contract-001-lean` (KKA conventions and physical acceptance contract).  
**Baseline:** `Qwen/Qwen3-8B`, immutable configuration revision recorded in `models/qwen3-8b/manifest.json`.

## 1. Frozen configuration snapshot

The checked-in `config.json` is copied from the pinned Hugging Face revision recorded in the manifest. It is a configuration snapshot, not a local weight snapshot. Before training or benchmark claims, download and hash all weight shards, tokenizer assets, generation configuration and the exact modeling source at that same revision.

| Parameter | Value |
|---|---:|
| Hidden size | 4,096 |
| Transformer layers | 36 |
| Query heads | 32 |
| KV heads | 8 |
| Head dimension | 128 |
| GQA ratio | 4 query heads per KV head |
| MLP intermediate size | 12,288 |
| Vocabulary | 151,936 |
| Config `max_position_embeddings` | 40,960 |
| Config dtype | BF16 |

**Context-length discrepancy:** the model card describes 32,768 native context and 131,072 with YaRN, while the pinned configuration snapshot declares `max_position_embeddings=40960` and `rope_scaling=null`. These are not silently reconciled here. The effective supported context must be verified against the pinned model implementation, tokenizer and model-card revision before long-context experiments.

Model card declares approximately 8.2B parameters and Apache-2.0 licensing. Verify the license files and terms at the exact pinned revision before redistribution.

## 2. Exact attention tensor dimensions

For batch size (B), sequence length (S), query head count (H_q=32), KV head count (H_{kv}=8), and head dimension (D=128):

- Hidden input: ([B,S,4096])
- Query: ([B,32,S,128])
- Key: ([B,8,S,128])
- Value: ([B,8,S,128])
- Attention scores: ([B,32,S_q,S_k])
- Attention output: ([B,32,S_q,128])

Four consecutive query heads share one KV head:

`kv_head(q_head) = floor(q_head / 4)`.

The Q/K/V/O projection weight shapes, using `[out_features, in_features]`, are:

| Projection | Weight shape | Parameters |
|---|---:|---:|
| Q | [4096, 4096] | 16,777,216 |
| K | [1024, 4096] | 4,194,304 |
| V | [1024, 4096] | 4,194,304 |
| O | [4096, 4096] | 16,777,216 |
| **Total per layer** | | **41,943,040** |

Across 36 layers, these attention projections contain 1,509,949,440 parameters. The first photonic experiment does **not** move these projections to VLPI. They remain electronic until a separate costed mapping is justified.

## 3. First logical tile

Define a tile as 64 query positions × 64 key positions for each query head:

- 4,096 score positions per query head.
- 131,072 score positions across 32 query heads.
- 524,288 scalar feature-pair terms per head for a 128-dimensional QK reduction.
- 16,777,216 scalar feature-pair terms across all query heads.
- The corresponding 64×64 value aggregation has the same scalar pair-term count for 128 value channels.

These are mathematical cardinalities, **not** counts of MZIs, modulators, detectors, optical cycles or fabricated devices.

For one tile block, the logical field-value payload before any complex/quadrature encoding is:
- Q: 32×64×128 = 262,144 scalars.
- K: 8×64×128 = 65,536 scalars.
- V: 8×64×128 = 65,536 scalars.

GQA shares K/V among four query heads. The physical broadcast, buffering, modulation and detector topology remain open design questions.

## 4. KV-cache implication

The configuration implies 2×8×128 = 2,048 KV elements per token per layer. At BF16 this is 4,096 bytes per token per layer, excluding allocator, block-table and runtime overhead.

Across 36 layers:
- At 32,768 tokens: approximately 4.5 GiB per sequence.
- At 40,960 tokens: approximately 5.625 GiB per sequence.

These are raw tensor-storage estimates, not measured serving memory. KV cache remains a VLSI/memory-system responsibility in the first hybrid design. This is why a fast photonic attention score tile alone does not solve decode-time system performance.

## 5. Operation allocation

**Initial VLPI/KKA research boundary**
- Encode Q/K scalar drives as complex fields through an explicit amplitude/phase response.
- Interfere encoded Q and K fields.
- Recover the ideal signed cross-term through balanced detection.
- Return attention scores to the electronic subsystem.

**Initial VLSI boundary**
- Token embeddings and output projection.
- Q/K/V/O projections.
- Q/K normalization and rotary positional processing as required by the pinned model implementation.
- Causal masking and SoftMax.
- KV-cache storage, indexing, update and retrieval.
- Value aggregation and output projection.
- RMSNorm, residuals, SwiGLU/MLP, sampling, scheduling and control.
- Calibration, telemetry, conversion and fault handling.

This boundary is deliberately conservative. A later experiment may move value aggregation or other operations only with a separate mathematical contract and measured system benefit.

## 6. Trainable KKA-compatible numerical core

`eis_kka_ref/torch_attention.py` adds a trainable GQA-compatible core that accepts Q/K/V tensors after the model's own projections, normalization and positional encoding.

Its explicitly synthetic surrogate is:

[
A(u)=\operatorname{sigmoid}(u),\qquad
\phi(u)=\kappa\ln A(u),\qquad
E(u)=A(u)e^{i\phi(u)}.
]

The per-query-head `kappa` is trainable. The ideal balanced score is:

[
s_{ij}=\frac{2\operatorname{Re}\sum_d E(q_{id})\overline{E(k_{jd})}}{\sqrt D}.
]

SoftMax, causal masking and value aggregation remain explicit electronic reference operations. This is an experimental differentiable surrogate—not Tian's full PTC equation, not a Kramers–Kronig material solver, not a calibrated device transfer curve and not a drop-in Qwen3 replacement. It must later accept measured complex-transfer tables and calibrated uncertainty.

## 7. Formal boundary

`EISKKA/Frontier001.lean` imports the existing KKA contract and formalizes:
- Qwen3 GQA head-sharing map and range.
- Query and KV projection widths.
- 64×64 score cardinalities.
- QK and AV scalar feature-pair counts.
- KV-cache element count per token per layer.

It does not prove model quality, the approximation of SoftMax by KKA, physical device behavior, timing, energy or an optical implementation.

## 8. Required next gates

1. CI compiles the Lean module and passes the existing axiom/proof checks.
2. Python shape tests pass against the checked-in config.
3. Optional PyTorch tests verify output shapes, normalized probabilities and gradient flow through `kappa`.
4. Load the exact pinned model implementation and verify all model-specific attention operations (including normalization and RoPE) before replacing any layer.
5. Train only a controlled attention-layer experiment; compare against the original layer under matched inputs and report output error and downstream quality.
6. Profile prefill and decode separately, including KV-cache traffic.
7. Only then freeze a physical 64×64 tile contract.

No weights have been trained, no full model has been adapted, no FlexCompute job has been submitted and no physical result is claimed.
