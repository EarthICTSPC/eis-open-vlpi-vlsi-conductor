# GF / AMF technical-support questions — EIS-KKA-64-001

**Status:** Draft for EIS review and secure transmission.  
**Confidentiality:** Send through the existing GF customer contact or approved secure support channel. Do not put GF replies containing restricted information in this public repository.

## Executive context

Earth ICT, SPC (EIS) has executed an NDA with GlobalFoundries for photonic design. EIS is evaluating a Kramers–Kronig-assisted interference (KKA) photonic attention-processing tile. Tian et al. have demonstrated a small 10×1 photonic transformer prototype; EIS's challenge is scaling toward a logical 64-query × 64-key attention block for a minimum viable photonic attention engine.

The 64×64 label is a logical workload dimension, not yet a physical MZI/cell count. EIS is defining the physical mapping and system energy boundary.

## Priority 1 — NDA, PDK and design enablement

1. Does the executed EIS–GF NDA cover the acquired AMF Singapore photonics PDKs, device models, process design rules and technical support? If not, what addendum or separate agreement is required?
2. Which exact PDK releases can EIS access for GF 45SPCLO and AMF SOI, PECVD SiN-on-SOI and LPCVD SiN-on-SOI?
3. For each kit, which release, process options, simulator versions and supported design environments are current?
4. Is AMFSiP 5.0.luceda3 the current supported AMF kit for EIS's intended work, or is there a newer/internal release?
5. Which parts of the Luceda/IPKISS, Keysight ADS, Cadence, Synopsys and other flows are supported and licensed for EIS?
6. May EIS use an independent Lean4/Python specification and verification flow and generate layouts/netlists through supported APIs? What restrictions apply to generated outputs and derived data?
7. What may be retained in EIS's private repositories, and what (if anything) may be published in a public architecture/interface repository?

## Priority 2 — KKA primitive and phase control

8. Which platform can implement an MZI with one external and two independently controlled internal phase sections, or an equivalent characterized topology?
9. Please identify available thermo-optic, carrier depletion/injection, electro-optic or other phase-control options by platform.
10. For each candidate: phase efficiency, insertion loss, voltage/current, static power, tuning speed/time constant, linearity, hysteresis, drift and reliability.
11. Are characterized complex transfer functions (amplitude and phase) available versus wavelength, bias, temperature and optical input power?
12. Are measured thermal interaction matrices or validated electro-thermal models available for adjacent phase shifters?
13. Which device mechanisms can produce controlled amplitude–phase coupling relevant to KKA? What operating range and limitations apply?
14. Are there integrated balanced photodetector options, or should EIS plan external/differential detection? Please provide responsivity, bandwidth, noise and saturation information.

## Priority 3 — SOI and SiN platform strategy

15. Are AMF SOI, PECVD SiN-on-SOI and LPCVD SiN-on-SOI separate process options or can any be integrated in one qualified process flow?
16. Is there a qualified SOI-compute / SiN-distribution integration path? If yes, what are the transition structures, measured loss, process variation and design restrictions?
17. Which platform is preferred for active KKA computation and which for low-loss optical distribution, based on characterized device data rather than transceiver headline bandwidth?
18. What are measured propagation loss, bend loss, crossing loss and coupler loss for the relevant wavelengths and geometries?

## Priority 4 — 64×64 scaling constraints

19. What maximum customer die area, reticle allocation and MPW options are available on each candidate process?
20. What are the design rules for waveguide width/spacing, bend radii, crossings, MMIs, heater geometry, metal routing, pads and optical I/O?
21. Has GF/AMF fabricated programmable MZI arrays or photonic circuits with hundreds/thousands of independently controlled phase elements? What scaling lessons can be shared?
22. What are realistic thermal-crosstalk, phase-drift, electrical fan-out, calibration and yield constraints at this scale?
23. What hierarchical tiling, wavelength distribution, detector placement and control architecture would GF recommend?
24. What test structures should be included in the first MPW vehicle to de-risk a larger array?

## Priority 5 — Models, simulation and manufacturing

25. Are process-corner, Monte Carlo and statistical compact models available for the selected platform?
26. Can circuit simulation model complex field transfer, thermal coupling, detector noise and process variation in a common flow?
27. What are the recommended foundry sign-off checks and supported DRC/LVS/extraction tools?
28. What is the recommended MPW or prototype route, submission cadence, design review process and typical schedule?
29. Can GF assign a photonics design-enablement engineer and, if appropriate, coordinate a joint review with the Singapore/AMF photonics team?
30. Would GF consider a technical evaluation of a KKA-based photonic attention engine for energy-constrained transformer inference?

## Requested initial meeting outcome

EIS proposes a first technical review focused on:
- NDA/PDK access scope and exact kit versions;
- the best candidate platform for a characterized KKA phase/interference primitive;
- thermal versus non-thermal control options;
- whether SOI and SiN can be combined in a qualified flow;
- the key physical constraints for a logical 64×64 attention tile;
- a recommended first foundry test vehicle and design-enablement contact.

## EIS architecture boundary

EIS intends to use Lean4 as the mathematical specification authority, Python as the executable reference, and foundry PDKs as physical implementation backends. The public portion will contain technology-independent contracts, open schemas and synthetic conformance models. Foundry-specific confidential IP will remain within the authorized environment.
