"""KLayout-backed OASIS export with a reopen sanity check.

This module deliberately does not implement the OASIS binary format. It expects
an already-built KLayout Layout object and delegates serialization to KLayout.

The checks here are structural smoke checks, not DRC, LVS, optical connectivity,
or fabrication qualification.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

try:
    import klayout.db as kdb
except ImportError as exc:  # pragma: no cover - environment dependent
    raise ImportError(
        "KLayout Python module is required. Install/use the pinned KLayout "
        "environment documented by the selected technology adapter."
    ) from exc


@dataclass(frozen=True)
class LayoutExportReport:
    output_path: str
    database_unit_um: float
    top_cells: tuple[str, ...]
    layer_count: int
    shape_count: int
    output_bytes: int


def _shape_count(layout: "kdb.Layout") -> int:
    count = 0
    for cell in layout.each_cell():
        for layer_index in layout.layer_indexes():
            count += sum(1 for _ in cell.shapes(layer_index).each())
    return count


def export_oasis_and_reopen(
    layout: "kdb.Layout",
    output_path: str | Path,
    *,
    required_top_cells: Iterable[str] = (),
) -> LayoutExportReport:
    """Write OASIS using KLayout, reopen it, and check basic structural identity.

    This function does not claim DRC/LVS cleanliness or process qualification.
    Coordinates and layer semantics must already be established by a pinned PDK.
    """
    path = Path(output_path)
    if path.suffix.lower() not in {".oas", ".oasis"}:
        raise ValueError("OASIS output must use .oas or .oasis extension")
    if layout.dbu <= 0:
        raise ValueError("KLayout database unit must be positive")

    expected_tops = tuple(sorted(cell.name for cell in layout.top_cells()))
    missing = set(required_top_cells) - set(expected_tops)
    if missing:
        raise ValueError(f"Required top cells are absent: {sorted(missing)}")

    path.parent.mkdir(parents=True, exist_ok=True)
    layout.write(str(path))

    if not path.is_file() or path.stat().st_size == 0:
        raise RuntimeError("KLayout did not produce a non-empty OASIS file")

    reopened = kdb.Layout()
    reopened.read(str(path))

    reopened_tops = tuple(sorted(cell.name for cell in reopened.top_cells()))
    if reopened.dbu != layout.dbu:
        raise RuntimeError(
            f"Database unit changed during export: {layout.dbu} -> {reopened.dbu}"
        )
    if reopened_tops != expected_tops:
        raise RuntimeError(
            f"Top-cell identity changed during export: {expected_tops} -> {reopened_tops}"
        )

    original_layers = len(list(layout.layer_indexes()))
    reopened_layers = len(list(reopened.layer_indexes()))
    if reopened_layers != original_layers:
        raise RuntimeError(
            f"Layer-index count changed during export: {original_layers} -> {reopened_layers}"
        )

    original_shapes = _shape_count(layout)
    reopened_shapes = _shape_count(reopened)
    if reopened_shapes != original_shapes:
        raise RuntimeError(
            f"Shape count changed during export: {original_shapes} -> {reopened_shapes}"
        )

    return LayoutExportReport(
        output_path=str(path),
        database_unit_um=float(reopened.dbu),
        top_cells=reopened_tops,
        layer_count=reopened_layers,
        shape_count=reopened_shapes,
        output_bytes=path.stat().st_size,
    )
