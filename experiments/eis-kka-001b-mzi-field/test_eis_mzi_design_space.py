import copy

import pytest

from eis_mzi_design_space import build_search_request, validate_design_space


def valid_spec():
    return {
        "schemaVersion": 1,
        "name": "EIS exploratory MZI search test fixture",
        "pdk": {"name": "fixture-only", "version": "0", "source": "unit-test fixture"},
        "variables": [
            {
                "name": "mmi_length", "unit": "um", "mode": "free",
                "lower": 10.0, "upper": 100.0,
                "boundEvidence": "eisApprovedBound",
                "boundSource": "unit-test fixture only", "boundRevision": "test-1",
            },
            {"name": "waveguide_width", "unit": "nm", "mode": "fixed", "value": 450},
        ],
        "objectives": [
            {"metric": "insertion_loss", "direction": "minimize", "unit": "dB",
             "definition": "fixture metric at defined reference planes"},
            {"metric": "footprint", "direction": "minimize", "unit": "um2",
             "definition": "fixture footprint metric"},
        ],
        "selectionPolicy": "pareto",
        "hardConstraints": [],
    }


def test_valid_design_space_builds_engine_neutral_request():
    request = build_search_request(valid_spec())
    assert request["contract"] == "EIS-MZI-DesignSpace-v1"
    assert request["search_policy"]["may_expand_bounds"] is False


def test_missing_numeric_bounds_fail_closed():
    spec = valid_spec()
    del spec["variables"][0]["upper"]
    with pytest.raises(ValueError, match="upper bound"):
        validate_design_space(spec)


def test_unproven_bound_fails_closed():
    spec = valid_spec()
    spec["variables"][0]["boundEvidence"] = "guess"
    with pytest.raises(ValueError, match="bound evidence"):
        validate_design_space(spec)


def test_optimizer_cannot_use_scalar_score_policy():
    spec = valid_spec()
    spec["selectionPolicy"] = "weighted_sum"
    with pytest.raises(ValueError, match="pareto"):
        validate_design_space(spec)


def test_duplicate_variable_names_rejected():
    spec = valid_spec()
    spec["variables"].append(copy.deepcopy(spec["variables"][0]))
    with pytest.raises(ValueError, match="unique"):
        validate_design_space(spec)
