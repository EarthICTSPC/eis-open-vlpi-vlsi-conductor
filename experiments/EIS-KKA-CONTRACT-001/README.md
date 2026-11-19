# EIS-KKA-CONTRACT-001 — Canonical KKA conventions and primitive acceptance contract

**Status:** draft formal contract and evidence schema; not a physical qualification result.

## Authority and separation

- Lean4 is authoritative for mathematical definitions, ideal identities, and the logical acceptance predicate.
- Python remains an independent executable numerical reference. It is not generated from Lean and is not itself a proof.
- The JSON Schema defines the exchange format for experiment manifests and qualification evidence.
- Physical measurements determine whether a manufactured implementation satisfies the contract. A Lean proof or simulation cannot substitute for measurement.

## Frozen conventions

### Phasor and field amplitude

The EIS phasor convention is E_phys(t) = Re{E_phasor exp(+i omega t)}.

A transfer is H(u) = A(u) exp(i phi(u)), where A is field-amplitude transmission, not intensity transmission. Intensity/power is proportional to |E|². The experiment manifest must state physical field/power normalization and units.

Phase is in radians. The phase reference, output port, drive variable, bias, wavelength, temperature, and operating interval are device-specific manifest fields.

### KKA trajectory

The canonical convention is kappa_A = d phi / d ln(A).

For drive parameter u, where derivatives exist, A(u) > 0, and dA/du is nonzero:

kappa_A(u) = (d phi/du) / ((dA/du)/A).

For intensity I proportional to A²:

kappa_I = d phi / d ln(I) = kappa_A / 2.

This is a trajectory descriptor, not by itself a device model or proof of an activation law. Do not infer a universal KKA response from a material name, generic MZI topology, or nominal PDK cell. The amplitude and phase functions must be measured or explicitly supplied by a model.

### Balanced-detector normalization

For ideal 50:50 outputs:

E_plus = (a+b)/sqrt(2), E_minus = (a-b)/sqrt(2).

Thus P_plus = |a+b|²/2 and P_minus = |a-b|²/2.

With polarity I_plus - I_minus, matched responsivity R, and ideal branches:

I_plus - I_minus = 2 R Re(a conj(b)).

The cross term is signed and must not be clipped. If |E|² is expressed in watts, R is A/W. If fields are dimensionless normalized envelopes, responsivity is A per normalized-power unit. The experiment must declare which interpretation applies.

The nonideal reference model preserves separate branch gains and offsets:
I_diff = R(g_plus P_plus - g_minus P_minus) + o_plus - o_minus.

### Acceptance and evidence

A physical pass requires physically measured evidence, device/process/layout identity, instrument identity and calibration record, calibration procedure record, operating point, sample count, raw-data SHA-256, residual, standard uncertainty, visibility, insertion loss, and all numerical acceptance limits satisfied.

Formal, simulated and synthetic records are useful but cannot produce a physical pass. Unknown values remain unknown/null; they are not zero.

## Physlib relationship

Physlib currently supplies foundations in electromagnetism, waves, frequency/wavelength, polarization and mathematical physics. Its Physlib/Optics/Basic.lean explicitly describes the optics directory as a placeholder. EIS should use reusable Mathlib/Physlib results where suitable while keeping the device-level KKA contract in the EIS repository. A small generic optics contribution can be proposed upstream after discussion on Lean Zulip.

## Files

- EISKKA/Contract001.lean: formal conventions and acceptance predicate.
- EISKKA/Bench001A.lean: Tian ideal interference identity and operation ledger.
- acceptance.schema.json: machine-readable physical evidence manifest.
- Python reference extensions are maintained separately in the EIS Python package and independently tested.

## Explicit non-claims

This contract does not claim that a particular GF/AMF/CUMEC process supports the primitive, that a physical device satisfies the ideal model, that Tian Eq. (2) is universally exact, or that KKA provides energy savings. Those require separate simulation, measurement, matched-workload and system-boundary evidence.
