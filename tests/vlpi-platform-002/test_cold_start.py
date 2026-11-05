#!/usr/bin/env python3
"""VLPI-PLATFORM-002: schema validation and cold-start reconstruction."""

from pathlib import Path
import sys

import yaml
from jsonschema import Draft202012Validator


ROOT = Path(__file__).resolve().parents[2]
IR_SCHEMA = ROOT / "schema" / "vlpi-ir" / "vlpi-ir.schema.yaml"
IR_FIXTURE = ROOT / "examples" / "vlpi-platform-002" / "ru001-program.yaml"

REQUIRED_REFS = {
    "ru": ROOT / "ru" / "RU-001" / "ru.yaml",
    "contract": ROOT / "ru" / "RU-001" / "contract.yaml",
    "context": ROOT / "ru" / "RU-001" / "design-context.yaml",
    "evidence": ROOT / "ru" / "RU-001" / "evidence.yaml",
}


def load_yaml(path: Path):
    with path.open("r", encoding="utf-8") as handle:
        return yaml.safe_load(handle)


def assert_ref(ref: str):
    path = ROOT / ref.split("#", 1)[0]
    assert path.is_file(), f"Unresolved repository reference: {ref}"


def main():
    schema = load_yaml(IR_SCHEMA)
    ir = load_yaml(IR_FIXTURE)
    errors = sorted(Draft202012Validator(schema).iter_errors(ir), key=lambda e: list(e.path))
    assert not errors, "\n".join(
        f"{'.'.join(map(str, e.path))}: {e.message}" for e in errors
    )

    obj = ir["vlpiIR"]

    # Cold-start graph reconstruction.
    transform = obj["transformations"][0]
    assert transform["ruRef"] == "ru/RU-001/ru.yaml"
    assert transform["contractRef"] == "ru/RU-001/contract.yaml"
    assert transform["inputs"] == ["H_input"]
    assert transform["outputs"] == ["H_residual"]
    assert obj["graph"]["executionOrder"] == ["T_RU001"]

    for ref in [
        transform["ruRef"],
        transform["contractRef"],
        obj["technology"]["designContextRef"],
        *obj["evidence"]["evidenceRefs"],
    ]:
        assert_ref(ref)

    ru = load_yaml(REQUIRED_REFS["ru"])["replicableUnit"]
    contract = load_yaml(REQUIRED_REFS["contract"])["contract"]
    context = load_yaml(REQUIRED_REFS["context"])["designContext"]
    evidence = load_yaml(REQUIRED_REFS["evidence"])["evidence"]

    # Reconstruct the physical object from the graph.
    assert ru["identity"]["name"] == "RU-001"
    assert ru["transformation"]["physicalMechanism"].startswith("coherent optical interference")
    assert {p["name"] for p in ru["opticalInterfaces"]["ports"]} >= {
        "in_a", "in_b", "out_residual"
    }
    assert contract["identity"]["status"] == "specified"
    assert context["verification"]["status"] == "specified"
    assert evidence["status"] == "specified"
    assert evidence["result"]["outcome"] == "not-run"

    # Evidence boundary: information-model PASS is not physical PASS.
    assert obj["identity"]["status"] == "specified"
    assert obj["evidence"]["minimumStatus"] == "specified"
    assert obj["evidence"]["physicalValidationRequired"] is True
    assert context["verification"]["pdrRef"] == "not-run"
    assert context["verification"]["pctRef"] == "not-run"
    assert context["verification"]["ptvRef"] == "not-run"
    assert context["verification"]["bistRef"] == "not-run"
    assert context["verification"]["foundryReview"] == "not-requested"

    forbidden = (
        "fabricated",
        "measured performance",
        "pvr pass",
        "pdr/pct/ptv pass",
        "bist pass",
        "foundry accepted",
    )
    corpus = "\n".join(
        p.read_text(encoding="utf-8").lower()
        for p in [IR_FIXTURE, *REQUIRED_REFS.values()]
    )
    for term in forbidden:
        assert term not in corpus, f"Evidence-boundary violation: {term}"

    print(
        "VLPI-PLATFORM-002 PASS: IR schema-conformant, cold-start graph reconstructed, "
        "physical evidence boundary preserved."
    )


if __name__ == "__main__":
    try:
        main()
    except AssertionError as exc:
        print(f"VLPI-PLATFORM-002 FAIL: {exc}", file=sys.stderr)
        raise SystemExit(1)
