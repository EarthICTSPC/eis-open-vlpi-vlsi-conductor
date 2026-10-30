"""Synthetic PDK fixture. Scale never determines the outcome."""
from pathlib import Path
from .pdk_adapter import PDKFinding, PDKRunResult, PDKStatus, sha256_file, utc_now

class MockPDKAdapter:
    adapter_id = "EIS-MOCK-PDK"
    adapter_version = "0.1.0"
    def __init__(self, fail_codes=(), inconclusive_checks=(), pdk_name="EIS-MOCK-PDK", pdk_version="fixture-1"):
        self.fail_codes = tuple(fail_codes)
        self.inconclusive_checks = tuple(inconclusive_checks)
        self.pdk_name, self.pdk_version = pdk_name, pdk_version
    def run(self, layout_path, *, design_id, checks=("manifest", "mock_geometry"), scale=None):
        path, started = Path(layout_path), utc_now()
        requested = tuple(checks)
        if not path.is_file() or path.stat().st_size == 0:
            return PDKRunResult(self.adapter_id, self.adapter_version, PDKStatus.INCONCLUSIVE, design_id, "", self.pdk_name, self.pdk_version, requested, (), requested, (PDKFinding("INPUT-MISSING", "ERROR", "Layout missing or empty; no checks run."),), limitations=("No real geometry or PDK rules evaluated.",), started_at=started, completed_at=utc_now())
        findings = tuple(PDKFinding(c, "ERROR", "Synthetic failure explicitly injected by fixture.", "mock-fixture") for c in self.fail_codes)
        not_run = tuple(c for c in requested if c in self.inconclusive_checks)
        executed = tuple(c for c in requested if c not in not_run)
        status = PDKStatus.FAIL if findings else (PDKStatus.INCONCLUSIVE if not_run or not executed else PDKStatus.PASS)
        limitations = ["Synthetic fixture only; not DRC/LVS/DFM, optical simulation, or foundry acceptance."]
        if scale: limitations.append("Scale label %r is metadata only; it does not determine outcome." % scale)
        return PDKRunResult(self.adapter_id, self.adapter_version, status, design_id, sha256_file(path), self.pdk_name, self.pdk_version, requested, executed, not_run, findings, limitations=tuple(limitations), started_at=started, completed_at=utc_now())
