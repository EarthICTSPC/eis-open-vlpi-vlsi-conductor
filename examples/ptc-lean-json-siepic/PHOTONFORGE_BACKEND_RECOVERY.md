# PhotonForge local backend recovery — EIS PTC project

The PhotonForge browser dashboard uses a local server for local design work. A dashboard badge reading **“Local server • offline”** means the browser is not currently connected to the backend. A project prompt cannot repair that connection by itself.

## Recovery sequence

Follow the official PhotonForge GUI setup guide: https://www.flexcompute.com/photonforge/learning-center/presentation/getting-started/

1. In Chrome, open site controls for `photonforge.simulation.cloud` and allow **Local network access**. If Chrome presents an explicit permission prompt, allow it. Reload the page.
2. In the Python environment selected for PhotonForge, check whether the package is installed:
   ```bash
   python -m pip show photonforge
   ```
3. If it is not installed, review the official install instructions and confirm the intended Python environment before installing:
   ```bash
   python -m pip install photonforge
   ```
4. Start the local backend in a terminal:
   ```bash
   photonforge-server
   ```
   Keep that terminal open while using the browser GUI.
5. Return to the PhotonForge Projects page and wait for the badge to indicate that the local server is connected. If it remains offline, capture the terminal error and check the official troubleshooting guide before changing ports, firewall settings, or permissions.

Do not paste authentication tokens, credentials, or private environment values into project notes.

## Create the project after the backend connects

1. Click **+ New project**.
2. Project name: `EIS-PTC-01 — Lean Netlist to PhotonForge`
3. Description: `Earth ICT, SPC exploratory PTC project. Traceable Lean logical netlist to PhotonForge schematic/layout; first milestone is one MZI and verified named-port mapping. No foundry tapeout or performance claim.`
4. Keep visibility **Private**.
5. Submit, then choose **+ New application → Schematic editor** if that option is present.
6. Paste the prompt from `PHOTONFORGE_PTC_PROJECT_PROMPT.md` into the agent/workbench where instructions are accepted. If the GUI has no prompt field, use the prompt in the connected AI coding agent rather than assuming the project description is an agent instruction.

## PDK policy for the first milestone

The previous JSON consumer was framed around a SiEPIC EBeam-style open backend, but EIS's longer-term preferred direction remains SiN/TFLN. Do not treat the EBeam example as a final material-stack decision. For the first software interface test, use whichever supported open PDK is actually installed and label the result as an interface prototype. Record the exact PDK identity and version.

Do not launch Tidy3D, FDTD, EME, or other paid simulations during backend recovery or project creation. Start with topology, port mapping, and circuit-level validation.
