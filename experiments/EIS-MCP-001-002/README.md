# EIS-MCP-001 / EIS-MCP-002 — MCP Integration and Remote Execution

**Status:** experiment specifications only; not executed  
**Repository:** Earth ICT, SPC (EIS)  
**Safety posture:** least privilege, bounded workload, human-reviewed evidence

## Why these are separate experiments

MCP is a protocol for a host/client to discover and invoke tools exposed by servers. Two MCP servers appearing in one AI host does **not**, by itself, prove that one server can call another, that two autonomous agents communicate, or that a client inside a remote Sprite can reach an MCP server.

Keep these claims separate:

1. **EIS-MCP-001 — Dual-server host discovery:** one Claude Code host configures both the official Fly Sprites MCP integration and the FlexCompute Tidy3D/FlexAgent integration. Verify initialization, tool discovery, and harmless independent calls from each integration.
2. **EIS-MCP-002 — Client-in-Sprite protocol test:** a client process executing *inside a dedicated Sprite* attempts to initialize and call a separately identified MCP server over the network. Record the exact server, transport, auth method, package, and call results. This test must not be marked PASS merely because Claude Code on the host can see both integrations.

A third optional path—running the Tidy3D MCP server inside the Sprite and connecting a client to it locally—tests local MCP transport, not remote access to a FlexAgent server. Label that path accurately.

## Grounded package note

The supplied fact-check reports that PyPI currently resolves `tidy3d-mcp` (including version `0.16.12` and `0.16.7`) and `tidy3d` (reported `2.12.0`). These are package-existence observations, not proof of compatibility, correct command-line behavior, authentication, or a remotely reachable FlexAgent endpoint. Recheck versions and package documentation at execution time.

The candidate invocation

```bash
uvx --from 'tidy3d-mcp>=0.16.7' tidy3d-mcp
```

is only a candidate until the installed package's documented entry point and `--help` output confirm it. Do not assume `tidy3d-mcp` and `uvx tidy3d mcp` are interchangeable.

## EIS-MCP-001 — Dual-server discovery

### Objective

Determine whether the same Claude Code host can initialize both configured MCP integrations and independently discover and invoke one harmless tool from each.

### Setup

- Configure the official Fly Sprites MCP endpoint: `https://sprites.dev/mcp`, using the provider-supported OAuth flow.
- Configure the FlexCompute-supported Tidy3D/FlexAgent plugin or MCP integration using its current official instructions.
- Do not paste OAuth tokens, API keys, environment dumps, or private configuration into the evidence record.
- Capture product/plugin versions, host version, timestamp, and the server identifiers shown by the host. Redact secrets.

### Procedure

1. Ask the host to show its configured MCP servers and their connection status.
2. For each server separately, record initialization/connection status and the tool names returned by discovery.
3. Invoke one harmless read-only tool from Sprites, such as listing accessible Sprites. Do not create or destroy a Sprite in this first experiment.
4. Invoke one harmless FlexCompute tool that does not start a costly simulation or require a design mutation. If no safe tool is available, record that and stop; do not improvise a billable run.
5. Capture sanitized tool results and any protocol/auth errors.
6. Repeat discovery once after a clean host restart if practical.

### PASS criteria

- Both integrations independently initialize in the same host session.
- Each server exposes a discoverable tool list.
- One harmless tool call to each server returns a result or a structured, attributable server error.
- Evidence identifies the host, each server/integration, and exact calls without secrets.

A host-level PASS proves only that the host can use both configured integrations. It does **not** prove MCP-to-MCP calls, cross-agent communication, remote Sprite-to-FlexAgent connectivity, or a photonic design result.

## EIS-MCP-002 — Client running inside a Sprite

### Objective

Test whether a process running inside a newly created, dedicated Fly Sprite can connect to and call the intended MCP server over the network. Name the exact server under test before execution.

### Preconditions

- EIS-MCP-001 has been recorded, or the operator documents why it was skipped.
- The operator has authorized access to Fly Sprites and to the selected MCP server.
- Use a restricted Fly token where available: limit it to a unique `eis-mcp-002-` Sprite name prefix, minimal scopes, a low create limit, and a short expiry.
- Use only a dedicated Sprite with a unique experiment prefix. Do not destroy any Sprite that was not created for this run.
- Do not put credentials in source control, command arguments, shell history, screenshots, or evidence JSON. Prefer provider-supported secret injection.
- Set a time/cost limit before starting. Do not start a Tidy3D/FlexCompute simulation as part of protocol smoke testing.

### Crucial server-identity decision

Choose and record exactly one target for the primary test:

**A. Remote server target (the stronger claim):** a documented, independently reachable FlexCompute MCP server endpoint, if FlexCompute provides one for the intended account/product. The process inside the Sprite must initiate the connection itself and complete the supported authentication flow. Do not infer that a Claude Code plugin automatically exposes a remotely reachable endpoint; many plugin integrations launch a local stdio server.

**B. Local-in-Sprite target (a narrower claim):** install and launch the documented Tidy3D MCP package inside the Sprite, then connect a test MCP client to that local process using its supported transport. This validates MCP client/server behavior inside the Sprite, but **does not** demonstrate that a remote FlexAgent service is reachable from the Sprite.

Do not switch from A to B after a failure and report one undifferentiated PASS. If A is unavailable, record `BLOCKED_NO_DOCUMENTED_REMOTE_ENDPOINT` and optionally run B as a separately labeled subtest.

### Bounded procedure

1. Create one dedicated Sprite through the official Sprites MCP integration.
2. Record the Sprite identifier, creation time, runtime/OS, and the method used to enter it. Do not record credentials.
3. Inside the Sprite, record Python and `uv` versions, network/DNS reachability to the selected server (without logging secrets), and the exact documented package/command used.
4. Use a maintained MCP client compatible with the target transport. Perform protocol initialization and tool discovery.
5. Make one harmless, read-only tool call. Do not launch an expensive simulation, modify a production design, or request broad network access.
6. Capture sanitized initialization, discovery, call, response, and error evidence. Distinguish protocol errors, authentication errors, network errors, and missing server/tool errors.
7. Stop the test process. Keep the Sprite for inspection by default; cleanup is a separate human-approved action.

### PASS criteria

For target A, PASS requires the process executing inside the Sprite to initialize with the identified remote MCP server, discover its tools, and complete one harmless tool call, with reproducible sanitized evidence.

For target B, report only `PASS_LOCAL_MCP_SUBTEST`; do not call it a remote FlexAgent connectivity PASS.

A package installation or a local smoke script alone is not a PASS. A Claude Code host successfully using Sprites MCP from outside the Sprite is not a PASS for this experiment.

## Evidence discipline

Use `evidence.schema.json` for a structured record. Store raw logs only after reviewing and redacting secrets, personal data, and unrelated workspace contents. Preserve exact error text where safe. Hashes can establish artifact identity but do not independently establish correctness.

Allowed outcomes:

- `PASS`: all acceptance criteria for the named target are met.
- `FAIL`: the test ran and an acceptance criterion failed.
- `BLOCKED`: a prerequisite, endpoint, access grant, or safe tool was unavailable.
- `INCOMPLETE`: evidence or required steps are missing.
- `PASS_LOCAL_MCP_SUBTEST`: local-in-Sprite MCP works, but remote FlexAgent reachability was not established.

## Non-claims

Neither experiment proves agent autonomy, agent-to-agent messaging, correctness of photonic simulations, physical validation, energy/CO₂e benefits, or readiness for production. These experiments test integration boundaries and protocol behavior only.
