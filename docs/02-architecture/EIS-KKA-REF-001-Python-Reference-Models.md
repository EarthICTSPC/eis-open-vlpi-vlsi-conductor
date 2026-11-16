# EIS-KKA-REF-001 — Python Reference Models

**Owner:** Earth ICT, SPC (EIS)  
**Status:** Initial implementation; software tests define the evidence boundary  
**Parent:** EIS-KKA-001 — Interference Operator and Physical-Response Contract

## Purpose

Provide a platform-independent executable reference for complex field transfer, analytical KKA activation, balanced two-port interference and deterministic known-answer tests.

This package is a mathematical/software reference. It is not a foundry PDK, calibrated instrument model, or evidence that an EIS SOI device realizes the modeled response.

## Frozen conventions

### Complex field transfer

The amplitude in ComplexTransfer is a non-negative **field-amplitude** transmission coefficient, not intensity transmission:

    H = A exp(j phi)
    E_out = H E_in

The phase response is supplied by the caller. No platform-specific transfer law is assumed.

### KKA activation

    f_NL(A) = A cos(phi(A) + theta_n) / cos(theta_n)

The phase_response callable returns radians. A near-zero denominator is rejected. The code does not infer phi(A) from a material name or assume an arbitrary MZI response is material-level Kramers–Kronig coupling.

### Balanced detector

    E_plus  = (a + b) / sqrt(2)
    E_minus = (a - b) / sqrt(2)

Therefore:

    |E_plus|^2 - |E_minus|^2 = 2 Re(a b*)

With equal branch gains and zero offsets:

    I_plus - I_minus = R * 2 Re(a b*)

The signed differential output is preserved. Branch gains, responsivity and offsets are explicit parameters. Noise, bandwidth, saturation, thermal effects and calibration uncertainty are not yet modeled.

## Tests and known-answer cases

Run from the repository root:

    python -m unittest discover -s tests -v

Coverage includes transfer round-trips, activation identity and nonzero phase, singular normalization rejection, constructive/destructive/quadrature interference, unequal amplitudes, zero-arm behavior, a deterministic phase sweep, and detector gain/offset handling.

The ideal cross-term convention is **2 Re(a b*)**. Total coherent intensity **|a+b|^2** remains distinct and is not returned by the balanced detector model.

## Evidence boundary and next work

Passing tests establishes only E2 software-tested behavior for these mathematical models. It does not establish physical behavior (E3/E4), a particular SOI transfer curve, a complete tensor-level KKA attention contract, or energy/latency advantages.

Next extensions should be driven by measured or explicitly sourced data: complex transfer extraction versus operating context, uncertainty propagation, dynamic response, detector bandwidth/noise, and calibrated nonidealities. Unknown physical parameters remain unknown.
