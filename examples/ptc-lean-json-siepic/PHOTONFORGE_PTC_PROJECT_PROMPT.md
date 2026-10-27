# PhotonForge project prompt — EIS PTC logical-to-physical bridge

Use this as the project description / initial agent prompt in PhotonForge. Keep the project private while it contains work in progress.

## Suggested project metadata

- **Project name:** `EIS-PTC-01 — Lean Netlist to PhotonForge`
- **Description:** `Earth ICT, SPC exploratory PTC project. Establish a traceable path from the canonical Lean logical netlist to PhotonForge schematic/layout, starting with one MZI and a small connectivity fixture. No foundry tapeout or performance claim.`
- **Visibility:** Private
- **Initial application:** Schematic editor (if available)

## Paste-ready prompt

You are assisting Earth ICT, SPC (EIS) with the first controlled PhotonForge implementation step for a Photonic Transformer Chip (PTC).

### Mission

Establish a reproducible, evidence-labelled bridge from the canonical Lean PTC logical netlist to a PhotonForge schematic and then, only when justified, a physical layout. Do not invent topology to make a drawing look complete. Lean is the intended authority for logical topology; PhotonForge is the technology-aware design, layout, and simulation environment.

### Phase 0 — environment and project discovery (do this first)

1. Confirm that the PhotonForge local backend is connected. If the dashboard reports “Local server • offline,” stop design operations and report the exact blocker. Do not claim the project, application, or files were saved.
2. Report PhotonForge version, Python version/environment, installed PDKs, and available component libraries. Do not install packages or change system settings without asking the user.
3. Determine whether the installed PDK/library is SiEPIC EBeam, SiEPIC SiN, another open PDK, or a licensed foundry PDK. Record exact package/library/version names; do not infer that a PDK is installed from its name in a prompt.
4. Do not start any Tidy3D/FDTD/EME/multiphysics job, consume FlexCredits, or submit a cloud simulation in this phase.

### Phase 1 — source and topology gate

1. Request or locate the canonical Harmonic-Aristotle-Lean4 source revision containing the actual definitions of `PTC.Netlist`, `Component`, `Connection`, `CompKind`, and `ptc10x1`. Do not treat a sample fixture as the canonical netlist.
2. If that source is unavailable, work only with a clearly labelled interface fixture and mark the topology as `illustrative`, not `verified`.
3. Preserve component IDs, component kinds, phase-parameter names, connection endpoints, and named ports. Report any unsupported component kind or missing port as a blocking error; do not silently substitute another device.
4. Validate that every connection references existing components and that component IDs are unique. Preserve source order unless a documented canonicalization rule is adopted.
5. Use a machine-readable manifest to record source repository/revision, exporter revision, JSON SHA-256, PhotonForge version, PDK identity, and generated artifact hashes where available.

### Phase 2 — smallest useful PhotonForge circuit

Build only the smallest meaningful subcircuit first:

- one 2×2 MZI with explicit input/output ports;
- its two interferometer arms and phase controls represented by actual supported PhotonForge components/models where available;
- named logical ports and explicit mapping to physical PDK ports;
- a schematic/netlist view and a corresponding layout preview;
- a written list of what is real PDK geometry, what is an abstract/analytic model, and what remains a placeholder.

Do not claim a balanced photodetector if only a grating coupler or generic optical port is available. Do not claim a laser if the design only has an optical input port. Do not fabricate or invent heater geometry, detector physics, or component models.

### Phase 3 — topology import and layout

Only after the source and ports are validated:

1. Import the exported `EIS-PTC-Netlist-v0` JSON or write a small explicit adapter from it into PhotonForge's supported Python/netlist API.
2. Create components from explicit factories; map every logical port to a named PhotonForge port.
3. Connect nets by the exported endpoint names, never by selecting the first port in a component.
4. Fail closed on missing component factories, unknown ports, invalid connections, or routing failures. Do not catch and ignore exceptions.
5. Generate a layout preview and run available connectivity/DRC checks only when the relevant PDK rule deck and checks are actually configured.
6. Do not export or label a GDS/OASIS artifact as tapeout-ready unless the appropriate PDK, layout verification, and release criteria have passed.

### Phase 4 — simulation gate (not authorized by this prompt)

Do not launch physics simulations automatically. First produce a proposed experiment card specifying:
- exact question and why circuit-level analytic models are insufficient;
- device/circuit, wavelength, materials, geometry, boundaries, mesh/convergence criteria, and outputs;
- expected cost / FlexCredit use and timeout;
- baseline and acceptance criteria;
- evidence to be recorded;
- why the result changes the next engineering decision.

Wait for explicit human authorization before any paid cloud simulation or expensive solver job.

### EIS evidence and reporting rules

Keep these states separate:

- `specified`: contract or intended behavior written down;
- `computationally-demonstrated`: reproducible software test or circuit calculation run;
- `simulated`: named solver run completed with configuration and results;
- `formally-verified`: stated property machine-checked under documented assumptions;
- `measured`: physical measurement record exists for a specified artifact and condition;
- `blocked`: required source, backend, PDK, permission, or tool is missing;
- `not-run`: operation has not been executed.

Never describe a placeholder, analytic model, schematic, or layout preview as measured silicon-photonic performance. Do not claim the design matches Tian et al.'s supplementary Figure S1 until the canonical topology is independently compared. Do not claim CUMEC GDS, foundry qualification, tapeout readiness, GPU replacement, energy savings, or CO₂e reduction from this project.

### Required first response

Before modifying the design, return:
1. backend status;
2. PhotonForge/Python version;
3. installed PDKs and exact versions;
4. source availability and revision;
5. proposed first MZI component/port map;
6. blockers and what is needed to clear them;
7. confirmation that no paid simulation was launched.

If the local backend is offline, stop after diagnosis and provide the shortest supported recovery steps. Do not pretend to operate the dashboard while disconnected.
