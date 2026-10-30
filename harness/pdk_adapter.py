"""Evidence-bearing adapter result model; separate from foundry acceptance."""
from __future__ import annotations
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from enum import Enum
import hashlib, json
from pathlib import Path
from typing import Optional

class PDKStatus(str, Enum):
    PASS = "PASS"
    FAIL = "FAIL"
    INCONCLUSIVE = "INCONCLUSIVE"

@dataclass(frozen=True)
class PDKFinding:
    code: str
    severity: str
    message: str
    source: str = "adapter"
    evidence_ref: Optional[str] = None

@dataclass(frozen=True)
class PDKRunResult:
    adapter_id: str
    adapter_version: str
    status: PDKStatus
    design_id: str
    design_sha256: str
    pdk_name: str
    pdk_version: Optional[str]
    checks_requested: tuple
    checks_executed: tuple
    checks_not_executed: tuple
    findings: tuple = ()
    report_paths: tuple = ()
    limitations: tuple = ()
    started_at: str = ""
    completed_at: str = ""

    def to_json(self):
        payload = asdict(self)
        payload["status"] = self.status.value
        payload["findings"] = [asdict(f) for f in self.findings]
        return json.dumps(payload, indent=2, sort_keys=True)

def sha256_file(path):
    h = hashlib.sha256()
    with Path(path).open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()

def utc_now():
    return datetime.now(timezone.utc).isoformat()

def write_result(result, output_path):
    target = Path(output_path)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(result.to_json() + "\\n", encoding="utf-8")
    return target
