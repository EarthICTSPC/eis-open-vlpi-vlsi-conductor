# VLPI-TYPED-INTERFACE-RULE-001
## Foundational rule: typed computational and physical interfaces

**Status:** Proposed foundational ecosystem rule — pending review and acceptance  
**Owner:** Earth ICT, SPC (EIS)  
**Scope:** VLPI contracts, CRC composition, Lean 4 models, software references, simulation, physical implementations, and evidence records

## Normative rule

> Every computational interface shall declare its semantic type, representation domain, physical quantity, shape, units where applicable, precision, validity conditions, and provenance. Every change of representation shall be an explicit, typed transformation. CRC shall reject incompatible compositions before costly physical simulation; Lean 4 shall verify the corresponding formal typing and contract properties. Physical conformance shall require separately identified simulation or measurement evidence.

Implementations should treat this as a cross-cutting ecosystem invariant, not a component-specific convention.

## 1. Interface type record

Each interface field shall declare, where applicable:

- **Semantic type:** what the value means (for example, query vector, normalized relevance score, candidate identity, winner token, attention result).
- **Representation domain:** electronic digital, electronic analog, photonic/optical, or another explicitly named domain.
- **Physical or numerical quantity:** bit vector, integer code, voltage, current, complex optical field amplitude, optical power, phase, or other declared quantity.
- **Shape:** scalar, vector, tensor, set, stream, token, or structured record, including dimensions and cardinality constraints.
- **Units and scale:** SI or other explicit units, normalization, valid range, and reference convention where applicable.
- **Precision and uncertainty:** bit width, quantization, tolerances, noise/error bounds, and calibration uncertainty where applicable.
- **Validity conditions:** preconditions, validity flags, operating envelope, timing/state requirements, and failure/indeterminate behavior.
- **Provenance:** source workload, model/configuration identity, implementation version, calibration, and whether the value is specified, synthetic, software-generated, simulated, or measured.

Fields that do not apply should be explicitly marked not applicable with a reason; they should not be silently omitted or filled with misleading defaults.

## 2. Domain distinctions

At minimum, the type model shall distinguish:

- `ElectronicDigital<T>`: discrete encoded values, including digital scores, IDs, configuration and evidence.
- `ElectronicAnalog<T, Unit>`: electrical quantities such as voltage and current.
- `PhotonicOptical<FieldAmplitude>`: optical field amplitude, including the declared complex representation and relevant optical conditions.
- `PhotonicOptical<Power>`: optical power, with units and reference plane.
- `PhotonicOptical<Phase>`: optical phase under a declared convention.
- `VerifiedBoundary<T, Contract>`: a value accepted only after the named state-boundary contract has been checked.

These names are illustrative type constructors. Implementations may use different syntax, but must preserve the distinctions. In particular, optical field amplitude is not optical power; an electrical analog signal is not a digital code; and a digital code that controls a modulator is not itself an optical field.

## 3. Explicit representation transformations

A representation change shall be represented as an explicit typed primitive with a contract, parameters, operating envelope, latency, energy/resource accounting where applicable, and evidence status.

Illustrative signatures:

```text
DAC:
  ElectronicDigital<Code>
  -> ElectronicAnalog<Voltage>

Modulator:
  ElectronicAnalog<DriveVoltage>
  -> PhotonicOptical<FieldAmplitude>

Photodetector:
  PhotonicOptical<FieldAmplitude>
  -> ElectronicAnalog<Current>

ADC:
  ElectronicAnalog<Current>
  -> ElectronicDigital<Code>
```

These signatures are schematic. Real devices require richer parameters and contracts. A chain may not omit conversion stages merely because the semantic payload remains the same.

## 4. CRC composition gate

Before expensive FDTD/EM simulation or netlist emission, CRC shall check:

1. **Semantic compatibility:** the producer's meaning satisfies the consumer's requirement.
2. **Representation compatibility:** adjacent representations match, or a declared typed transformation bridges them.
3. **Shape and quantity compatibility:** dimensions, units, scale, and physical quantity are compatible.
4. **Contract compatibility:** precision, uncertainty, validity, operating-envelope, timing, state, loss, and other required constraints are satisfiable.
5. **Provenance completeness:** assumptions and values are labeled by evidence class and source.

A type match is necessary but not sufficient for physical validity. If any mandatory check fails or remains unresolved, the composition shall be rejected or explicitly marked blocked before the expensive job or physical artifact is emitted. The system shall report which check failed and preserve a machine-readable rejection record.

## 5. Lean 4 verification boundary

Lean 4 models shall encode the same semantic and representation distinctions and the admissible typed transformations. Formal obligations should include, where relevant:

- incompatible producer/consumer representations cannot be composed without a declared transformation;
- quantities such as field amplitude and power cannot be silently substituted;
- dimensions and units satisfy the primitive's declared preconditions;
- a winner decision cannot be accepted without a valid, correctly typed winner identity;
- a pipeline is accepted only if its modeled state-boundary and resource contracts hold;
- a rejected composition cannot reach the netlist-emission or simulation-launch authorization state.

Lean 4 proves properties of the formal model and its assumptions. It does not, by itself, prove that a fabricated device conforms to the model. Physical conformance requires separately identified evidence and explicit comparison with the contract.

## 6. Latency-budget rejection acceptance test

Use a dedicated over-budget fixture with:

- end-to-end latency ceiling: `200.0 ps`;
- DAC: `10.0 ps`;
- modulator: `5.0 ps`;
- PRISM: `40.0 ps`;
- thresholder: `30.0 ps`;
- KKA: `120.0 ps`;
- photodetector: `15.0 ps`;
- ADC: `8.0 ps`;
- input contribution: `0.0 ps`.

Under the fixture's explicitly declared **serial additive latency model**, total latency is `228.0 ps`, exceeding the ceiling by `28.0 ps`.

The preflight test passes only if all of the following hold:

1. The latency quantities are typed and use compatible time units.
2. The declared timing composition model is used.
3. The pipeline is rejected because `228.0 ps > 200.0 ps`.
4. The rejection is machine-readable and names the failed budget contract.
5. No PDK netlist is emitted.
6. No FDTD/EM simulation is launched.
7. The evidence record identifies the fixture, configuration, calculated total, budget, result, and reason.

This fixture validates the gatekeeper's behavior, not any real component's latency. If a later architecture overlaps, pipelines, or parallelizes stages, its timing composition must use a separately declared and verified model; the additive sum must not be assumed universally.

## 7. Evidence classes and physical conformance

Each parameter and result shall be labeled at minimum as one of:

- `specified`
- `synthetic`
- `software_reference`
- `simulated`
- `measured`
- `unknown`

Do not present synthetic test values as workload requirements, simulated performance as measured performance, or a formal proof as physical validation. Preserve the experiment identity, versions, assumptions, and relevant input/output hashes.

## 8. Application to EIS Photonic-LLM

The Digital Twin, EIS-PRISM, EIS-Thresholder, and EIS-KKA interfaces shall each declare typed inputs and outputs. In particular:

- PRISM scores must specify whether they are digital values, analog electrical signals, optical power, optical field representations, or another declared encoding.
- The thresholder must declare its comparison input representation, indifference policy, fault behavior, and winner-identity representation.
- KKA must declare the representation of query, key/value data, selection tokens, and attention outputs.
- Any electronic/optical conversion must appear as an explicit typed stage with its own contract and resource accounting.
- A detector-free optical path and an analog optoelectronic path must remain distinct architecture variants unless evidence establishes otherwise.

## 9. Acceptance status

This document proposes a foundational rule. It does not claim that all current repository components, Lean proofs, orchestrator checks, or physical implementations already satisfy it. Adoption requires review, implementation in the shared type schema and CRC/Lean models, automated negative tests, and traceable evidence.
