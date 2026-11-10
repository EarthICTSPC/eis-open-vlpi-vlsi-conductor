"""Structural checks for the EIS logical port-map instance."""
import json
from pathlib import Path


def test_port_map_has_three_heater_pairs_and_two_optical_outputs():
    root = Path(__file__).parents[2]
    data = json.loads((root / "schema/ptc-mzi/port-map.v0.1.json").read_text())
    optical = data["optical_ports"]
    electrical = data["electrical_ports"]
    assert len([p for p in optical if p["direction"] == "output"]) == 2
    assert len(electrical) == 6
    assert data["constraints"]["heater_circuit_count"] == 3
    assert data["constraints"]["detector_included"] is False
    assert data["constraints"]["geometry_backend"] == "NOT_SELECTED"


def test_port_schema_and_instance_are_json_documents():
    root = Path(__file__).parents[2]
    schema = json.loads((root / "schema/ptc-mzi/port-map.schema.json").read_text())
    instance = json.loads((root / "schema/ptc-mzi/port-map.v0.1.json").read_text())
    assert schema["$schema"].endswith("2020-12/schema")
    assert instance["cell_id"] == "EIS-PTC-MZI-001"
