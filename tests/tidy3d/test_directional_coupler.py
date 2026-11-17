import json
from pathlib import Path

import pytest

from tidy3d_bridge.directional_coupler import (
    build_directional_coupler,
    validate_spec,
)

SPEC_PATH = Path(__file__).parents[2] / "examples" / "tidy3d" / "eis_soi_dc_spec.json"


@pytest.fixture
def spec():
    return json.loads(SPEC_PATH.read_text(encoding="utf-8"))


def test_lean_emitted_spec_is_well_formed(spec):
    values = validate_spec(spec)
    assert values["wavelength_nm"] == 1550
    assert values["core_width_nm"] == 450
    assert values["gap_nm"] == 200
    assert values["coupling_length_nm"] == 8000


def test_rejects_wrong_phasor_convention(spec):
    spec["phasor_convention"] = "exp(-i omega t)"
    with pytest.raises(ValueError, match="phasor"):
        validate_spec(spec)


def test_rejects_nonpositive_gap(spec):
    spec["gap_nm"] = "0"
    with pytest.raises(ValueError, match="positive"):
        validate_spec(spec)


def test_builds_native_tidy3d_simulation_without_submission(spec):
    sim, metadata = build_directional_coupler(spec)
    assert len(sim.sources) == 1
    assert len(sim.monitors) == 2
    assert len(sim.structures) == 4
    assert metadata["cloud_submission"] == "not_submitted"
    assert metadata["output_ports"] == ["through", "cross"]
    assert metadata["frequency_count"] == 31
