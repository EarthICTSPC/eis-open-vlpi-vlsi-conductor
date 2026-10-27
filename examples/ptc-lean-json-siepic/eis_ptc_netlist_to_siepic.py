#!/usr/bin/env python3
"""Validate EIS-PTC-Netlist-v0 JSON and emit a deterministic placement plan.

This consumer intentionally does not emit GDS. A safe physical backend requires
an explicit, installed PDK adapter, real component factories, port mappings,
and routing failures treated as errors rather than silently ignored.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

FORMAT = "EIS-PTC-Netlist-v0"
KINDS = {"laser", "mmi1x2", "mmi2x2", "mzi", "bpd", "waveguide"}
IDENTIFIER = re.compile(r"^[A-Za-z][A-Za-z0-9_.-]*$")


class NetlistError(ValueError):
    """Invalid or internally inconsistent logical netlist."""


def load_netlist(path: Path) -> dict[str, Any]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise NetlistError(f"cannot read valid JSON from {path}: {exc}") from exc
    validate_netlist(data)
    return data


def _require_string(obj: dict[str, Any], key: str, where: str) -> str:
    value = obj.get(key)
    if not isinstance(value, str) or not value.strip():
        raise NetlistError(f"{where}.{key} must be a non-empty string")
    return value


def validate_netlist(data: Any) -> None:
    if not isinstance(data, dict):
        raise NetlistError("top-level JSON value must be an object")
    if data.get("format") != FORMAT:
        raise NetlistError(f"format must be {FORMAT!r}")
    for key in ("source", "pdk_target", "note"):
        _require_string(data, key, "root")
    components = data.get("components")
    connections = data.get("connections")
    if not isinstance(components, list) or not isinstance(connections, list):
        raise NetlistError("components and connections must be arrays")

    ids: set[str] = set()
    for i, comp in enumerate(components):
        where = f"components[{i}]"
        if not isinstance(comp, dict):
            raise NetlistError(f"{where} must be an object")
        cid = _require_string(comp, "id", where)
        if not IDENTIFIER.fullmatch(cid):
            raise NetlistError(f"{where}.id has invalid characters: {cid!r}")
        if cid in ids:
            raise NetlistError(f"duplicate component id: {cid}")
        ids.add(cid)
        kind = _require_string(comp, "kind", where)
        if kind not in KINDS:
            raise NetlistError(f"{where}.kind is unsupported: {kind!r}")
        phases = comp.get("phases")
        if not isinstance(phases, list) or any(not isinstance(p, str) for p in phases):
            raise NetlistError(f"{where}.phases must be an array of strings")

    seen_edges: set[tuple[str, str, str, str]] = set()
    for i, edge in enumerate(connections):
        where = f"connections[{i}]"
        if not isinstance(edge, dict):
            raise NetlistError(f"{where} must be an object")
        src = _require_string(edge, "from", where)
        src_port = _require_string(edge, "fromPort", where)
        dst = _require_string(edge, "to", where)
        dst_port = _require_string(edge, "toPort", where)
        if src not in ids:
            raise NetlistError(f"{where}.from references unknown component {src!r}")
        if dst not in ids:
            raise NetlistError(f"{where}.to references unknown component {dst!r}")
        if src == dst:
            raise NetlistError(f"{where} has a self-connection on {src!r}")
        key = (src, src_port, dst, dst_port)
        if key in seen_edges:
            raise NetlistError(f"duplicate connection: {key!r}")
        seen_edges.add(key)


def placement_plan(data: dict[str, Any], x_pitch: float = 60.0,
                   y_pitch: float = 80.0) -> list[dict[str, Any]]:
    """Stable illustrative row placement grouped by numeric final ID suffix.

    This is a schematic placement heuristic, not topology-aware routing or
    photonic layout optimization.
    """
    groups: dict[int, list[dict[str, Any]]] = {}
    for comp in data["components"]:
        match = re.search(r"_(\d+)$", comp["id"])
        row = int(match.group(1)) if match else 0
        groups.setdefault(row, []).append(comp)

    plan: list[dict[str, Any]] = []
    for row in sorted(groups):
        # Preserve Lean/source order within a row; do not sort by kind.
        for col, comp in enumerate(groups[row]):
            plan.append({
                "id": comp["id"],
                "kind": comp["kind"],
                "x_um": col * x_pitch,
                "y_um": row * y_pitch,
                "phases": comp["phases"],
            })
    return plan


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("netlist", type=Path, help="EIS-PTC-Netlist-v0 JSON file")
    parser.add_argument("--x-pitch", type=float, default=60.0)
    parser.add_argument("--y-pitch", type=float, default=80.0)
    parser.add_argument("--write-plan", type=Path, help="write plan JSON (no GDS)")
    args = parser.parse_args(argv)
    if args.x_pitch <= 0 or args.y_pitch <= 0:
        parser.error("placement pitches must be positive")

    try:
        data = load_netlist(args.netlist)
        plan = placement_plan(data, args.x_pitch, args.y_pitch)
    except NetlistError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2

    print(f"Validated {len(data['components'])} components, "
          f"{len(data['connections'])} connections")
    print(f"PDK target (declarative only): {data['pdk_target']}")
    print(f"Evidence boundary: {data['note']}")
    print("Placement plan (schematic only; no PDK cells or GDS generated):")
    for item in plan:
        print(f"  {item['id']:20} {item['kind']:10} "
              f"@ ({item['x_um']:.1f}, {item['y_um']:.1f}) um")
    if args.write_plan:
        args.write_plan.write_text(
            json.dumps({"format": FORMAT, "placement": plan}, indent=2) + "\n",
            encoding="utf-8",
        )
        print(f"Wrote placement plan: {args.write_plan}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
