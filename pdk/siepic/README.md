# SiEPIC technology adapter — identity policy

**Current state:** blocked pending an explicitly selected and pinned SiEPIC process revision.

This directory must not imply that a generic layer-number table is an authoritative PDK. Layer numbers, datatypes, layer purposes, cross-sections, component names, and process options are technology-revision-specific.

## Required pin record

Before enabling layout generation, add a machine-readable record containing:

- upstream repository URL;
- immutable commit SHA or release tag;
- license identifier and license-file path;
- selected process/technology name;
- supported process modules;
- KLayout version;
- SiEPIC-Tools version;
- gdsfactory version, if used;
- layer-map source path and content hash;
- component-library source path and content hash;
- known limitations and unsupported devices.

## Rules

1. Do not combine SiEPIC EBeam and CUMEC CSiP-180AL assumptions without a separately documented and verified process adapter.
2. Do not infer the existence of heaters, metal stacks, vias, germanium detectors, or probe pads from layer numbers.
3. Use the selected PDK's component and port definitions rather than hard-coded port offsets.
4. Preserve upstream licenses and notices; do not relicense third-party PDK content.
5. Keep confidential foundry PDK data outside the public repository unless redistribution is explicitly authorized.
6. A pinned PDK is not automatically fabrication-qualified for an EIS design.

## Activation criterion

The adapter may move from `blocked-unpinned` to `pinned-unverified` only after the immutable upstream revision, license, process target, layer map, and component inventory are recorded. It may be called `layout-verified` only after the relevant layout and independent checks pass.
