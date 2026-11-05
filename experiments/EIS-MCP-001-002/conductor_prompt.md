# Conductor prompts — EIS-MCP-001 and EIS-MCP-002

Use one prompt at a time. The conductor must report observations, not infer a PASS from its own narrative.

## Prompt A — EIS-MCP-001: dual-server discovery

You are the test conductor for Earth ICT, SPC (EIS), experiment EIS-MCP-001.

Goal: determine whether this single Claude Code host can independently initialize, discover, and safely call tools from both (1) Fly's official Sprites MCP integration and (2) the currently documented FlexCompute Tidy3D/FlexAgent integration.

Rules:
- Do not create/destroy Sprites, start simulations, edit designs, or perform other state-changing/costly calls.
- Do not print or record secrets, tokens, API keys, environment variables, or private config.
- Treat each server independently. Do not describe this as MCP-to-MCP communication or agent-to-agent communication.
- If a harmless FlexCompute tool is not obvious, stop and report BLOCKED rather than improvising.

Procedure:
1. Report host/client version and the two configured server identifiers.
2. For each server, report initialization status and the tool names returned by discovery.
3. Call one harmless read-only Sprites tool (prefer list accessible Sprites).
4. Call one harmless read-only FlexCompute tool. State the tool name and why it is harmless.
5. Return sanitized results, exact safe error messages, timestamps, and the outcome.
6. Assign PASS only if both integrations independently initialize, expose tools, and return a result or structured attributable error from the harmless call. Otherwise use FAIL, BLOCKED, or INCOMPLETE as defined in the runbook.

Return a compact evidence record conforming to evidence.schema.json. Do not invent missing fields. Never include credentials.

## Prompt B — EIS-MCP-002: client-in-Sprite

You are the test conductor for Earth ICT, SPC (EIS), experiment EIS-MCP-002.

First ask the operator to choose the server target:
- A: a documented remote FlexCompute MCP endpoint that a process inside a Sprite can reach; or
- B: a Tidy3D MCP server launched locally inside the Sprite.

Do not claim target A exists unless its official documentation and endpoint are supplied or verified. A plugin installed into Claude Code may be a local stdio integration, not a remotely addressable service.

Safety:
- Use a new Sprite with the `eis-mcp-002-` prefix and the narrowest available token permissions.
- Do not create more than one Sprite for the test.
- Do not launch simulations, make design changes, broaden network policy, or expose credentials.
- Do not destroy the Sprite without explicit human approval.
- Use a bounded timeout and stop on unexpected cost, permission, or network behavior.

Procedure:
1. Record the chosen target, official documentation reference, endpoint/transport (not credentials), client library/version, runtime versions, and auth mechanism category.
2. Create the dedicated Sprite via the official Sprites MCP server.
3. Execute the client from *inside the Sprite*. Record proof of where it ran (sanitized shell output and Sprite identity).
4. Initialize the target MCP server, discover tools, and invoke exactly one harmless read-only tool.
5. Capture sanitized protocol stages and errors. Separate DNS/TLS/network, OAuth/authentication, MCP initialization, tool discovery, and tool invocation failures.
6. Do not switch target A to B silently. If A has no documented reachable endpoint, report BLOCKED_NO_DOCUMENTED_REMOTE_ENDPOINT; B may be run only as a separately labeled local subtest.
7. Return the evidence record and outcome. PASS for target A requires the inside-Sprite process to complete initialization, discovery, and a harmless tool call against the remote endpoint. Target B may only return PASS_LOCAL_MCP_SUBTEST.

Do not infer protocol success from package installation, a successful shell command, a host-level Claude Code integration, or the conductor's own summary. Evidence must include actual client call results.
