"""Conservative command boundary for operator-configured SiEPIC/KLayout checks.
A zero exit code remains INCONCLUSIVE until a reviewed report parser exists.
A nonzero process exit is also INCONCLUSIVE: tool failure is not a geometry finding.
"""
import shlex, subprocess
from pathlib import Path
from .pdk_adapter import PDKFinding, PDKRunResult, PDKStatus, sha256_file, utc_now

class SiEPICAdapter:
    adapter_id = "EIS-SIEPIC-KLAYOUT"
    adapter_version = "0.1.0"
    def __init__(self, command, *, pdk_name="SiEPIC-open-PDK", pdk_version=None, timeout_seconds=900):
        if not command.strip(): raise ValueError("Provide an explicit operator-reviewed command.")
        self.command, self.pdk_name, self.pdk_version = command, pdk_name, pdk_version
        self.timeout_seconds = timeout_seconds
    def run(self, layout_path, *, design_id, output_dir, checks=("layout-open", "configured-checks")):
        layout, out = Path(layout_path).resolve(), Path(output_dir).resolve()
        out.mkdir(parents=True, exist_ok=True)
        requested, started = tuple(checks), utc_now()
        if not layout.is_file() or layout.stat().st_size == 0:
            return PDKRunResult(self.adapter_id, self.adapter_version, PDKStatus.INCONCLUSIVE, design_id, "", self.pdk_name, self.pdk_version, requested, (), requested, (PDKFinding("INPUT-MISSING", "ERROR", "Layout missing or empty; tool not invoked."),), started_at=started, completed_at=utc_now())
        stdout_path, stderr_path = out / "tool.stdout.txt", out / "tool.stderr.txt"
        command = self.command.replace("{layout}", str(layout)).replace("{outdir}", str(out))
        findings, executed, not_run = [], (), requested
        try:
            proc = subprocess.run(shlex.split(command), cwd=str(out), capture_output=True, text=True, timeout=self.timeout_seconds, check=False)
            stdout_path.write_text(proc.stdout, encoding="utf-8")
            stderr_path.write_text(proc.stderr, encoding="utf-8")
            executed = ("tool-invocation",)
            status = PDKStatus.INCONCLUSIVE
            if proc.returncode:
                findings.append(PDKFinding("TOOL-EXIT-NONZERO", "ERROR", "Configured tool exited with status %d; design checks are not classified." % proc.returncode, "process", str(stderr_path)))
            else:
                findings.append(PDKFinding("REPORT-PARSER-NOT-CONFIGURED", "INFO", "Process succeeded, but no reviewed report parser is configured.", "adapter", str(stdout_path)))
        except subprocess.TimeoutExpired as exc:
            stdout_path.write_text(str(exc.stdout or ""), encoding="utf-8")
            stderr_path.write_text(str(exc.stderr or ""), encoding="utf-8")
            status = PDKStatus.INCONCLUSIVE
            findings.append(PDKFinding("TOOL-TIMEOUT", "ERROR", "Tool timeout; check result unknown.", "process", str(stderr_path)))
        except FileNotFoundError as exc:
            stdout_path.write_text("", encoding="utf-8")
            stderr_path.write_text(str(exc), encoding="utf-8")
            status = PDKStatus.INCONCLUSIVE
            findings.append(PDKFinding("TOOL-NOT-FOUND", "ERROR", "Configured executable not found.", "process", str(stderr_path)))
        reports = tuple(str(p) for p in (stdout_path, stderr_path) if p.exists())
        return PDKRunResult(self.adapter_id, self.adapter_version, status, design_id, sha256_file(layout), self.pdk_name, self.pdk_version, requested, executed, not_run, tuple(findings), reports, ("Tool process status is not a DRC/LVS/optical verdict without a reviewed parser.", "This adapter does not constitute foundry acceptance."), started_at=started, completed_at=utc_now())
