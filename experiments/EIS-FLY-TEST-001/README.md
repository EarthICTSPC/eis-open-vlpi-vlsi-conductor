# EIS-FLY-TEST-001 — Sprites MCP + independent agent acceptance

**Owner:** Earth ICT, SPC (EIS)  
**Purpose:** Determine whether FlexCompute/FlexAgent can use Fly.io's official Sprites MCP endpoint to create and control a Sprite, execute a bounded test there, and return reproducible evidence.

## What this experiment does—and does not—test

The official Sprites MCP endpoint is `https://sprites.dev/mcp`. It uses Streamable HTTP and OAuth 2.1. The agent/client must complete the required authorization itself.

This experiment has two separate acceptance layers:

1. **Connection and control:** FlexAgent uses the official Sprites MCP tools to list Sprites, create one dedicated test Sprite, execute commands inside it, and retrieve the command result.
2. **Workload execution:** The agent checks out this repository inside that Sprite and runs `sprite_smoke_test.py`, then returns the complete JSON evidence and exit status.

A local run, a GitHub Actions run, a screenshot of configuration, or an agent's unsupported assertion does not satisfy layer 1. The smoke test alone does not prove layer 1; actual tool-call results must be recorded.

This is a software execution test only. It is not an EIS photonic physical validation test and does not alter the frozen OPENLLM-GITHUB2VLPI-002 Experiment A.

## Safety boundaries

- Use a dedicated test Sprite with a name prefix such as `eis-fly-test-001-`.
- Grant only the Sprites permissions needed for this experiment. Creating and executing in a Sprite requires write access; do not grant broader access than needed.
- Do not provide GitHub write tokens, foundry PDKs, production secrets, or unrelated credentials to the Sprite.
- Do not change organization-wide network policy.
- Do not deploy a Fly Machine or change the existing `fly.toml` as part of this test.
- Do not destroy any pre-existing Sprite. After evidence has been collected, destroy only the exact test Sprite created for this run if the operator authorizes cleanup.
- Keep tool results and error messages. An authentication or compatibility failure is a valid experiment result.

## Procedure

### A. Verify the actual agent connection

Ask the FlexCompute/FlexAgent operator to configure the client for the remote MCP server at:

```text
https://sprites.dev/mcp
```

Complete the official OAuth authorization flow in the actual FlexAgent environment if its client supports it. Do not paste access tokens into prompts, source files, logs, or this repository.

Using the actual FlexAgent tool interface—not a substitute script—perform these actions in order:

1. Call the Sprites list operation (commonly named `list_sprites`). Record the tool name, success/failure, and redacted result. An empty list can still mean successful authentication.
2. Create one uniquely named Sprite using the dedicated prefix `eis-fly-test-001-`.
3. Call the Sprite command execution operation (commonly named `exec`) in that exact Sprite.
4. Capture stdout, stderr, and exit status from the actual tool result.

If the client cannot configure a remote Streamable HTTP MCP server, cannot complete OAuth, or cannot invoke the tools, stop and record the precise failure. Do not claim compatibility based on documentation alone.

### B. Run the bounded workload inside the Sprite

Inside the test Sprite, run the following commands using its command-execution tool. Adapt only the repository clone path if needed; do not change the test script.

```bash
set -eu
git clone https://github.com/EarthICTSPC/eis-open-vlpi-pdk.git
cd eis-open-vlpi-pdk
git rev-parse HEAD
python3 experiments/EIS-FLY-TEST-001/sprite_smoke_test.py
```

Capture the full JSON output and tool-reported exit code. The expected final marker is:

```text
EIS_SPRITE_EXECUTION_OK
```

The script should report `"status": "PASS"` and all checks should have `"passed": true`. Preserve the repository HEAD and `test_script_sha256` printed in the JSON.

### C. Independent review

The reviewer checks:

- the actual FlexAgent tool calls show authenticated access to Sprites MCP;
- the create/exec actions target the same newly created Sprite;
- the remote command output contains the expected marker;
- the script's JSON reports PASS and all checks pass;
- the captured exit code is zero;
- the evidence includes repository HEAD and script hash;
- the output contains no leaked credentials.

If any item is missing, report **INCOMPLETE** or **FAIL**, not PASS.

## Evidence record

Create a JSON evidence record following `evidence.schema.json`. Include redacted tool-call evidence and the complete smoke-test JSON. Do not include bearer tokens, OAuth codes, cookies, or secret environment values.

Required outcome values:

- `PASS`: both MCP connection/control and workload execution were observed and reviewed.
- `FAIL`: an attempted required action failed.
- `INCOMPLETE`: the experiment was not run, or evidence is insufficient to decide.

## Interpretation

A PASS supports this narrow conclusion only:

> The identified FlexCompute/FlexAgent session successfully used the official Sprites MCP interface to control a Sprite and execute the specified bounded workload under the recorded conditions.

It does not establish general agent capability, persistent production-service reliability, EIS MCP harness compatibility, physical validation, or any photonic performance claim.

## Deliverables

1. Actual MCP tool-call trace or a redacted transcript.
2. Full smoke-test JSON.
3. Exit status and any stderr.
4. Evidence JSON conforming to the schema.
5. Short human review identifying any gaps.
