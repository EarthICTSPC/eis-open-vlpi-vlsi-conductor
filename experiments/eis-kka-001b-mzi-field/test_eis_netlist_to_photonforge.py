import copy
import json
from pathlib import Path

import pytest

from eis_netlist_to_photonforge import (
    lower_to_photonforge, lower_with_manifest, validate_netlist,
)


EXAMPLE = Path(__file__).parents[2] / "schema" / "examples" / "eis_tian_ptc_10_output_exploratory.json"


def load_example():
    return json.loads(EXAMPLE.read_text())


def test_example_topology_counts():
    doc = load_example()
    validate_netlist(doc)
    mzis = [x for x in doc["instances"] if x["kind"] == "mziCell"]
    assert len(mzis) == 11
    assert sum(int(next(p["value"] for p in x["parameters"] if p["name"] == "phase_shifters"))
               for x in mzis) == 33
    assert len([x for x in doc["instances"] if x["kind"] == "balancedPhotodetector"]) == 10


def test_duplicate_instance_rejected():
    doc = load_example()
    doc["instances"].append(copy.deepcopy(doc["instances"][0]))
    with pytest.raises(ValueError, match="duplicate instance"):
        validate_netlist(doc)


def test_unknown_port_rejected():
    doc = load_example()
    doc["connections"][0]["target"]["portName"] = "not_a_port"
    with pytest.raises(ValueError, match="undeclared port"):
        validate_netlist(doc)


def test_reused_connection_port_rejected():
    doc = load_example()
    doc["connections"].append(copy.deepcopy(doc["connections"][0]))
    with pytest.raises(ValueError, match="more than one connection"):
        validate_netlist(doc)


def test_missing_cell_fails_closed():
    doc = load_example()
    with pytest.raises(KeyError, match="no approved PhotonForge cell"):
        lower_to_photonforge(doc, {})


def test_missing_parameter_evidence_rejected():
    doc = load_example()
    doc["instances"][1]["parameters"][0]["evidence"] = "unclassified"
    with pytest.raises(ValueError, match="evidence class"):
        validate_netlist(doc)


def test_lowering_sidecar_preserves_source_evidence():
    doc = load_example()
    kinds = {item["kind"] for item in doc["instances"]}
    registry = {kind: object() for kind in kinds}
    result = lower_with_manifest(doc, registry)
    assert len(result["photonforge_netlist"]["instances"]) == len(doc["instances"])
    assert result["eis_manifest"]["instances"] == doc["instances"]
    assert result["eis_manifest"]["outputs"] == doc["outputs"]
