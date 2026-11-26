# EIS Conductor — Agent Operating Instructions

This repository is the versioned engineering record for Earth ICT, SPC (EIS) VLPI/VLSI work. Agents must use the repository as the primary project context; do not assume that chat history, an agent's memory, or a prior conversational summary is authoritative.

## Required cold-start sequence

1. Read this file.
2. Read [the EIS Conductor Charter](docs/00-overview/EIS_CONDUCTOR_CHARTER.md).
3. Read [the Engineering Memory Index](docs/00-overview/EIS_ENGINEERING_MEMORY_INDEX.yaml).
4. Read the [Open VLPI Disclosure Doctrine](docs/00-overview/EIS_Open_VLPI_Disclosure_Doctrine.md).
5. Read the task-specific issue, contract, source ledger, experiment, and evidence records identified by the index.
6. Confirm the current branch, commit, relevant contract revision/hash, and whether referenced PRs are merged or still drafts before relying on their contents.

If required context is missing or contradictory, report the gap and stop the affected task. Do not fill it with plausible assumptions.

## Authority and trust

- EIS-approved contracts define intended semantics, assumptions, tolerances, and acceptance criteria.
- Lean 4 is the formal authority where a contract explicitly designates a Lean definition/theorem as authoritative. A proof establishes only the proposition under its definitions and assumptions.
- Agents and external tools execute bounded tasks and return claims plus artifacts. Their self-reported PASS is not acceptance.
- The Conductor independently validates provenance, hashes, schemas, required tests, and contract-specific evidence.
- Keep tool-reported status separate from Conductor gate status.
- Use only the gate outcomes `ACCEPT`, `REJECT`, or `INCONCLUSIVE`; missing or ambiguous evidence is not a pass.
- A successful API call, passing software test, formal proof, simulation, layout export, foundry review, fabrication, and measurement are distinct evidence events.

## Evidence distinctions

Preserve the repository's existing evidence states and task-specific classifications. Do not collapse:
- source-reported, fitted, assumed, projected, derived, verified, and gap/provenance labels;
- specified, formally verified, computationally demonstrated, simulated, fabricated, and measured outcomes;
- a tool's reported result and the Conductor's independent acceptance decision.

Never promote a fitted source value to a raw measurement, a formal proof to physical validation, a simulation to measurement, or an OASIS export to DRC/LVS/foundry acceptance.

## Bounded execution and approvals

Agents may inspect, summarize, draft, test, and run explicitly authorized local/deterministic tasks within their assigned scope.

Explicit EIS approval is required before:
- paid or externally metered compute/simulation;
- foundry or third-party submission, contact, or disclosure;
- use or transfer of NDA/confidential PDK data;
- fabrication, MPW, packaging, procurement, or spending;
- changing a canonical contract, acceptance threshold, evidence policy, or permission boundary;
- merging a PR or making a consequential external commitment.

Do not expose credentials, private keys, access tokens, NDA PDK contents, proprietary process rules, restricted compact models, or confidential simulation artifacts in this public repository or in unauthorized agent prompts.

## Git workflow

- Treat `main` as the reviewed baseline.
- Work on a named task branch and submit a PR.
- Do not push directly to `main`, merge your own PR, close unrelated issues/PRs, rewrite history, or force-push.
- Do not silently edit another workstream's contract or acceptance criteria.
- Preserve failures, rejected candidates, unresolved source ambiguities, and not-run states.
- Before proposing a change, check for existing issues, PRs, schemas, and artifacts. Extend the existing work rather than duplicating it.

## Required task report

Every completed or blocked task should report:
1. task ID and bounded scope;
2. base commit and contract ID/revision/hash;
3. inputs and hashes (or explicitly unavailable hashes);
4. tool/agent identity and version;
5. actions performed and resource/approval state;
6. output artifact paths and hashes;
7. tests and independent verification performed;
8. tool-reported outcome;
9. Conductor gate outcome and reasons;
10. assumptions, limitations, unresolved gaps, and proposed next action.

The next action is a proposal until authorized by the appropriate EIS decision-maker.
