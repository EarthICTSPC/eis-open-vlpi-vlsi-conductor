import json, tempfile, unittest
from pathlib import Path
from harness.mock_pdk import MockPDKAdapter
from harness.pdk_adapter import PDKStatus, write_result
from harness.siep_ic_adapter import SiEPICAdapter

class PDKAdapterTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(); self.root = Path(self.tmp.name)
        self.layout = self.root / "candidate.oas"; self.layout.write_bytes(b"fixture-layout-bytes")
    def tearDown(self): self.tmp.cleanup()
    def test_mock_pass_fail_not_inferred_from_scale(self):
        passed = MockPDKAdapter().run(self.layout, design_id="PTC-small", scale="small")
        failed = MockPDKAdapter(fail_codes=("MOCK-SPACING-001",)).run(self.layout, design_id="PTC-512", scale="512")
        same_rules = MockPDKAdapter().run(self.layout, design_id="PTC-4K", scale="4K")
        self.assertEqual(passed.status, PDKStatus.PASS); self.assertEqual(failed.status, PDKStatus.FAIL)
        self.assertEqual(same_rules.status, PDKStatus.PASS)
    def test_inconclusive_when_check_not_run(self):
        result = MockPDKAdapter(inconclusive_checks=("optical-model",)).run(self.layout, design_id="PTC-small", checks=("manifest", "optical-model"))
        self.assertEqual(result.status, PDKStatus.INCONCLUSIVE); self.assertEqual(result.checks_not_executed, ("optical-model",))
    def test_manifest_serializes_and_binds_hash(self):
        result = MockPDKAdapter().run(self.layout, design_id="PTC-small")
        payload = json.loads(write_result(result, self.root / "evidence" / "result.json").read_text())
        self.assertEqual(payload["status"], "PASS"); self.assertEqual(payload["design_sha256"], result.design_sha256)
    def test_siep_success_is_inconclusive_without_parser(self):
        result = SiEPICAdapter("python -c 'print(42)'").run(self.layout, design_id="PTC-small", output_dir=self.root / "siep")
        self.assertEqual(result.status, PDKStatus.INCONCLUSIVE)
        self.assertTrue(all(Path(p).is_file() for p in result.report_paths))
    def test_missing_tool_is_inconclusive(self):
        result = SiEPICAdapter("eis-command-does-not-exist").run(self.layout, design_id="PTC-small", output_dir=self.root / "missing")
        self.assertEqual(result.status, PDKStatus.INCONCLUSIVE)
        self.assertTrue(any(f.code == "TOOL-NOT-FOUND" for f in result.findings))

if __name__ == "__main__": unittest.main()
