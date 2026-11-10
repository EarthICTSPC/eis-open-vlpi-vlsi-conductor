"""Source-level checks for the frozen PTC prototype topology contract."""

import json
from pathlib import Path


def load_topology():
    path = Path(__file__).parents[2] / "architecture" / "ptc10x1" / "topology.json"
    return json.loads(path.read_text(encoding="utf-8"))


def test_ptc_topology_matches_published_inventory():
    topology = load_topology()
    inventory = topology["mzi_inventory"]

    assert topology["target"]["output_channel_count"] == 10
    assert inventory["input_side_A"]["count"] == 10
    assert inventory["shared_weight_side_B"]["count"] == 1
    assert inventory["total_count"] == 11
    assert inventory["phase_shifters_per_mzi"]["total"] == 3
    assert inventory["total_phase_shifters"] == 33


def test_shared_weight_path_and_passive_detector_boundary():
    topology = load_topology()
    optical = topology["optical_topology"]

    assert optical["B_branch"]["fanout_outputs"] == 10
    detector = optical["per_output_channel"]["balanced_detection"]
    assert detector["method_in_published_passive_prototype"].startswith("paired grating-coupler")
    assert detector["on_chip_balanced_photodiode"] is False
    assert detector["detector_pair_count"] == 10
    assert detector["grating_coupler_output_count"] == 20


def test_original_fab_is_not_selected_as_eis_backend():
    topology = load_topology()
    assert topology["published_process_facts"]["original_fab"] == "CUMEC CSiP-180AL"
    assert topology["technology_mapping"]["eis_backend"] == "unselected"
    assert topology["technology_mapping"]["foundry_rights_confirmed"] is False
