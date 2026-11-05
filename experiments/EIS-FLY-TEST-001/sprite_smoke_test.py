#!/usr/bin/env python3
"""Bounded, non-destructive execution test for EIS-FLY-TEST-001.

Run this from a checkout of the EIS repository inside a newly created Fly.io
Sprite. It checks only the execution environment; it does not prove that
FlexAgent connected to Sprites MCP, and it does not perform physical validation.
"""
from __future__ import annotations

import hashlib
import json
import os
import platform
import subprocess
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path


TEST_ID = "EIS-FLY-TEST-001"
MARKER = "EIS_SPRITE_EXECUTION_OK"
EXPECTED = {
    "sum": 42,
    "product": 144,
    "sorted": [1, 2, 3, 5, 8],
}


def git_value(*args: str) -> str | None:
    try:
        result = subprocess.run(
            ["git", *args],
            check=True,
            capture_output=True,
            text=True,
            timeout=5,
        )
        return result.stdout.strip() or None
    except (OSError, subprocess.SubprocessError):
        return None


def check(name: str, passed: bool, detail: str) -> dict[str, object]:
    return {"name": name, "passed": bool(passed), "detail": detail}


def main() -> int:
    checks: list[dict[str, object]] = []
    root = Path.cwd()
    script_path = Path(__file__).resolve()
    script_sha256 = hashlib.sha256(script_path.read_bytes()).hexdigest()

    checks.append(check(
        "python_runtime",
        sys.version_info >= (3, 10),
        f"python={sys.version.split()[0]}",
    ))
    checks.append(check(
        "sprite_linux_environment",
        platform.system() == "Linux",
        f"system={platform.system()} machine={platform.machine()}",
    ))

    # Deterministic computation: intentionally small, dependency-free, and
    # unrelated to the EIS photonic reference transformation.
    computed = {
        "sum": sum([10, 12, 20]),
        "product": 12 * 12,
        "sorted": sorted([5, 1, 8, 2, 3]),
    }
    checks.append(check(
        "deterministic_computation",
        computed == EXPECTED,
        json.dumps(computed, sort_keys=True),
    ))

    # Write/read/compare in a temporary directory; leave no repository changes.
    try:
        with tempfile.TemporaryDirectory(prefix="eis-fly-test-001-") as temp_dir:
            artifact = Path(temp_dir) / "roundtrip.json"
            artifact.write_text(json.dumps(computed, sort_keys=True), encoding="utf-8")
            reread = json.loads(artifact.read_text(encoding="utf-8"))
            checks.append(check(
                "temporary_file_roundtrip",
                reread == EXPECTED,
                f"artifact_bytes={artifact.stat().st_size}",
            ))
    except Exception as exc:  # evidence must record failures rather than hide them
        checks.append(check("temporary_file_roundtrip", False, f"{type(exc).__name__}: {exc}"))

    head = git_value("rev-parse", "HEAD")
    checks.append(check(
        "repository_revision_available",
        head is not None,
        f"git_head={head or 'unavailable'}",
    ))

    evidence = {
        "test_id": TEST_ID,
        "status": "PASS" if all(item["passed"] for item in checks) else "FAIL",
        "marker": MARKER,
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "runtime": {
            "python": sys.version.split()[0],
            "system": platform.system(),
            "release": platform.release(),
            "machine": platform.machine(),
            "cwd": str(root),
        },
        "repository": {
            "head": head,
            "worktree_status": git_value("status", "--short"),
        },
        "test_script_sha256": script_sha256,
        "checks": checks,
        "computed": computed,
        "limitations": [
            "This script does not prove which agent invoked it.",
            "This script does not prove MCP transport or OAuth compatibility.",
            "This script does not prove the EIS application MCP harness was called.",
            "This script does not establish physical validation, measurement, or PDK acceptance.",
        ],
    }

    print(json.dumps(evidence, indent=2, sort_keys=True))
    print(MARKER if evidence["status"] == "PASS" else "EIS_SPRITE_EXECUTION_FAILED")
    return 0 if evidence["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
