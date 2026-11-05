# EIS-SOFTMAX-001 — Learned Attention Without Explicit Softmax

**Status:** Proposed experiment contract; not proof-checked, simulated, or physically measured.  
**Purpose:** Define a reproducible, bounded experiment comparing conventional softmax attention with a KKA-style interference-native attention candidate, with sigmoid attention as an independent alternative.  
**Principle:** The goal is not merely to remove the softmax operator. The candidate must preserve useful task performance while improving a defined system metric.

## Hypothesis

A trainable transformer whose attention computation is designed around KKA-style interference may learn representations that provide useful attention behavior without an explicit conventional softmax stage. This is a hypothesis, not an established result for language models or EIS hardware.

## Required comparisons

1. Conventional Transformer attention with softmax (baseline).
2. KKA-style interference-native attention with no explicit softmax stage.
3. Sigmoid attention as an independent softmax-replacement baseline.

Keep the task, data split, model scale, training budget, seed policy, and evaluation protocol matched as closely as the algorithms permit. Record any unavoidable differences.

## Precision matrix

- Training: BF16 and FP16 profiles where supported.
- Digital inference: W4A16 and W4A8 profiles.
- Do not assume every softmax intermediate should be 4-bit. Record the actual precision used by each operation.
- The optical candidate has no automatic digital bit-width. Characterize representation error, optical noise, phase/amplitude control, drift, detector uncertainty, and any digital state-boundary precision separately.

## Acceptance evidence

For every candidate, record:
- task quality and an explicit acceptable quality tolerance;
- attention/output behavior and numerical error;
- latency and throughput under the same workload;
- total system energy, including compute, laser, modulation, detection, control, memory, and conversion overhead where applicable;
- thermal behavior and the scope of the thermal model;
- configuration, dataset, source revision, seed, tool versions, hashes, and evidence provenance.

An experiment is only a success if quality remains within the predefined tolerance and the claimed improvement in energy, latency, or thermal behavior is supported by comparable evidence. A proof, a successful request submission, a simulator result, and a physical measurement are distinct evidence classes.

## Lean4 gate

RequestProject/Softmax/Model.lean defines the candidate methods, precision profiles, evidence fields, and a minimal simulation-request gate. The gate is an initial contract scaffold; compilation and theorem checking must be run in the repository's pinned Lean toolchain before calling it proof-checked. A Lean theorem only establishes properties of this formal model.

## Lowering to FlexCompute / FlexAgent

Lower the experiment into a **request packet**, not an assumed upstream API call:

- **Action intent:** prepare a bounded numerical experiment for the conventional baseline and digital attention alternatives; keep KKA algorithmic reference evaluation separate from physical optical-device simulation.
- **Required request identity:** source revision, adapter version, candidate/model configuration hash, dataset hash, seed, simulator/tool identity and version, resource budget, and authorization.
- **First stage:** run software/reference-model comparisons for conventional softmax, sigmoid attention, and KKA-style attention at BF16/FP16 training and W4A16/W4A8 inference where supported.
- **Second stage:** only after an explicit device model, geometry, materials/PDK identity, boundary conditions, and budget are supplied, prepare a physical simulation request. Do not convert an abstract KKA algorithm into an invented photonic layout.
- **Result handling:** record provider job ID, request hash, status, logs, result artifact hashes, warnings, and evidence class. Timeout means unknown/in-flight until reconciled; do not blindly duplicate dispatch.
- **Stop conditions:** missing credentials or endpoint; unknown tool capability; unpinned PDK/material model; missing budget/authorization; malformed result; or any claim that lacks its required evidence.

## Current execution state

- Formal contract: drafted.
- Lean compilation/proof check: **not run**.
- Reference training/evaluation: **not run**.
- FlexCompute/FlexAgent capability discovery: **not performed in this action**.
- Simulation request: **not dispatched**.
- Numerical simulation / physical measurement: **none**.

The connected GitHub integration can create repository artifacts, but no FlexCompute/FlexAgent execution endpoint is available in this turn. Therefore this artifact records the lowering contract and the conditions for dispatch; it does not claim a simulator job was launched.
