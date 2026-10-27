import importlib.util
import json
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
SPEC = importlib.util.spec_from_file_location(
    "eis_ptc_netlist_to_siepic", HERE / "eis_ptc_netlist_to_siepic.py"
)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC and SPEC.loader
SPEC.loader.exec_module(MODULE)


class NetlistConsumerTests(unittest.TestCase):
    def setUp(self):
        self.data = MODULE.load_netlist(HERE / "fixtures" / "ptc10x1_minimal.json")

    def test_fixture_validates(self):
        MODULE.validate_netlist(self.data)
        self.assertEqual(len(self.data["components"]), 6)
        self.assertEqual(len(self.data["connections"]), 7)

    def test_unknown_component_reference_rejected(self):
        bad = json.loads(json.dumps(self.data))
        bad["connections"][0]["to"] = "missing"
        with self.assertRaisesRegex(MODULE.NetlistError, "unknown component"):
            MODULE.validate_netlist(bad)

    def test_duplicate_component_id_rejected(self):
        bad = json.loads(json.dumps(self.data))
        bad["components"].append(dict(bad["components"][0]))
        with self.assertRaisesRegex(MODULE.NetlistError, "duplicate component"):
            MODULE.validate_netlist(bad)

    def test_unsupported_kind_rejected(self):
        bad = json.loads(json.dumps(self.data))
        bad["components"][0]["kind"] = "magic_laser"
        with self.assertRaisesRegex(MODULE.NetlistError, "unsupported"):
            MODULE.validate_netlist(bad)

    def test_placement_is_deterministic(self):
        first = MODULE.placement_plan(self.data)
        second = MODULE.placement_plan(self.data)
        self.assertEqual(first, second)
        self.assertEqual([x["id"] for x in first],
                         [x["id"] for x in self.data["components"]])

    def test_duplicate_connection_rejected(self):
        bad = json.loads(json.dumps(self.data))
        bad["connections"].append(dict(bad["connections"][0]))
        with self.assertRaisesRegex(MODULE.NetlistError, "duplicate connection"):
            MODULE.validate_netlist(bad)


if __name__ == "__main__":
    unittest.main()
