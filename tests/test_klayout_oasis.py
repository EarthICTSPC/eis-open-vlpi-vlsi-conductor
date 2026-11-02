"""Smoke tests for the KLayout-backed OASIS adapter.

These tests run only in an environment with the pinned KLayout Python module.
They validate serialization/reopen behavior, not DRC, LVS, or PDK compliance.
"""

import pytest

kdb = pytest.importorskip("klayout.db")

from backend.klayout_oasis import export_oasis_and_reopen


def test_oasis_round_trip_preserves_basic_structure(tmp_path):
    layout = kdb.Layout()
    layout.dbu = 0.001
    layer = layout.layer(1, 0)
    top = layout.create_cell("EIS_MZI_TEST")
    top.shapes(layer).insert(kdb.Box(0, 0, 1000, 450))

    output = tmp_path / "mzi_smoke.oas"
    report = export_oasis_and_reopen(
        layout,
        output,
        required_top_cells=("EIS_MZI_TEST",),
    )

    assert output.is_file()
    assert report.output_bytes > 0
    assert report.database_unit_um == pytest.approx(0.001)
    assert report.top_cells == ("EIS_MZI_TEST",)
    assert report.layer_count == 1
    assert report.shape_count == 1


def test_rejects_non_oasis_extension(tmp_path):
    layout = kdb.Layout()
    with pytest.raises(ValueError, match="OASIS output"):
        export_oasis_and_reopen(layout, tmp_path / "layout.gds")
