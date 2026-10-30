# EIS-PDK-ADAPTER-001 — Mock PDK and SiEPIC adapter boundary

Status: reference implementation v0.1.0. Evidence class: software harness, not physical-design validation. Related contract: EIS-CONTRACT-FAB-001.

## Purpose and authority boundary

The adapter vocabulary is PASS, FAIL, and INCONCLUSIVE. These describe checks actually run; they are not predictions about scale or manufacturability. A PDK adapter reports tool evidence. EIS-CONTRACT-FAB-001 binds a subsequent foundry submission and decision to the exact artifact and SHA-256. Only the foundry may issue foundry acceptance. Local PDK PASS does not imply optical functionality, yield, foundry acceptance, or manufacturing release.

## Mock adapter

harness/mock_pdk.py supplies deterministic fixtures. Failures are explicitly injected; scale labels are metadata and never determine the result. The mock adapter evaluates no actual geometry, DRC/LVS/DFM rules, or optics.

## SiEPIC/KLayout adapter

harness/siep_ic_adapter.py runs only an explicit command supplied by the operator, preserves stdout/stderr, timeout or missing-executable evidence, layout hash, and exit status. It assumes no undocumented SiEPIC API and does not bundle a PDK. A zero exit code remains INCONCLUSIVE until a reviewed parser validates the actual report format and maps reports to named checks.

Example: construct SiEPICAdapter with an operator-reviewed KLayout command using {layout} and {outdir} placeholders, then call run(layout_path, design_id, output_dir). Verify command flags against the installed KLayout version and provide a reviewed script. No PASS is claimed until a versioned parser validates the report.

## Evidence and scale ladder

Record frozen design ID/revision, layout SHA-256, source commit, PDK identity/version, tool versions, checks requested/executed/not executed, status, findings, raw reports, and limitations. Preserve each run's artifacts; revisions get new identities.

1. Small PTC: establish invocation and evidence capture.
2. 64 and 128: freeze designs and compare consistent acceptance criteria.
3. 512: enumerate satisfied, failed, and unevaluated requirements.
4. 4K: require explicit resource budget and experiment plan.
5. Target PDK: use authorized foundry-owned checks and decision records.

INCONCLUSIVE is required when evidence or tool support is missing. Never infer PASS or FAIL from the desired project narrative.
