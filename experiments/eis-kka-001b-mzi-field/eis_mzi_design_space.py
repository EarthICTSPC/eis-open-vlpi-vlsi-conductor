"""Fail-closed validation for EIS MZI optimization design-space manifests.

Defines the admissible search contract. It does not select numeric bounds,
create PhotonForge cells, or submit FlexCompute/Tidy3D jobs.
"""
from __future__ import annotations

from typing import Any, Mapping

BOUND_EVIDENCE = {"pdkConstraint", "eisApprovedBound"}
OBJECTIVES = {
    "insertion_loss", "output_imbalance", "interference_contrast",
    "bandwidth", "footprint", "heater_power", "thermal_crosstalk",
    "fabrication_robustness",
}


def validate_design_space(spec: Mapping[str, Any]) -> None:
    if spec.get("schemaVersion") != 1:
        raise ValueError("unsupported design-space schemaVersion")
    if not isinstance(spec.get("name"), str) or not spec["name"]:
        raise ValueError("design-space name is required")
    pdk = spec.get("pdk")
    if not isinstance(pdk, Mapping):
        raise ValueError("target PDK identity is required")
    if not all(isinstance(pdk.get(k), str) and pdk[k]
               for k in ("name", "version", "source")):
        raise ValueError("PDK name, version, and source are required")

    variables = spec.get("variables")
    if not isinstance(variables, list) or not variables:
        raise ValueError("at least one design variable is required")
    names: set[str] = set()
    for index, variable in enumerate(variables):
        where = f"variables[{index}]"
        if not isinstance(variable, Mapping):
            raise ValueError(f"{where} must be an object")
        name, unit, mode = variable.get("name"), variable.get("unit"), variable.get("mode")
        if not isinstance(name, str) or not name or name in names:
            raise ValueError(f"{where}: variable name must be non-empty and unique")
        names.add(name)
        if not isinstance(unit, str) or not unit:
            raise ValueError(f"{where}: physical unit is required")
        if mode not in {"free", "fixed"}:
            raise ValueError(f"{where}: mode must be free or fixed")
        if mode == "fixed":
            if "value" not in variable:
                raise ValueError(f"{where}: fixed variable requires value")
            continue
        lower, upper = variable.get("lower"), variable.get("upper")
        if not isinstance(lower, (int, float)) or isinstance(lower, bool):
            raise ValueError(f"{where}: free variable requires numeric lower bound")
        if not isinstance(upper, (int, float)) or isinstance(upper, bool):
            raise ValueError(f"{where}: free variable requires numeric upper bound")
        if lower >= upper:
            raise ValueError(f"{where}: lower bound must be less than upper bound")
        if variable.get("boundEvidence") not in BOUND_EVIDENCE:
            raise ValueError(f"{where}: bound evidence must be pdkConstraint or eisApprovedBound")
        if not isinstance(variable.get("boundSource"), str) or not variable["boundSource"]:
            raise ValueError(f"{where}: boundSource is required")
        if not isinstance(variable.get("boundRevision"), str) or not variable["boundRevision"]:
            raise ValueError(f"{where}: boundRevision is required")

    objectives = spec.get("objectives")
    if not isinstance(objectives, list) or not objectives:
        raise ValueError("at least one objective is required")
    for index, objective in enumerate(objectives):
        if not isinstance(objective, Mapping):
            raise ValueError(f"objectives[{index}] must be an object")
        if objective.get("metric") not in OBJECTIVES:
            raise ValueError(f"objectives[{index}]: unsupported metric")
        if objective.get("direction") not in {"minimize", "maximize"}:
            raise ValueError(f"objectives[{index}]: direction must be minimize or maximize")
        if not isinstance(objective.get("unit"), str) or not objective["unit"]:
            raise ValueError(f"objectives[{index}]: unit is required")
        if not isinstance(objective.get("definition"), str) or not objective["definition"]:
            raise ValueError(f"objectives[{index}]: frozen metric definition is required")

    if spec.get("selectionPolicy") != "pareto":
        raise ValueError("selectionPolicy must be pareto; undocumented scalar ranking is prohibited")
    if not isinstance(spec.get("hardConstraints"), list):
        raise ValueError("hardConstraints must be an array")


def build_search_request(spec: Mapping[str, Any]) -> dict[str, Any]:
    """Return an engine-neutral request only after the full domain is validated."""
    validate_design_space(spec)
    return {
        "contract": "EIS-MZI-DesignSpace-v1",
        "design_space": dict(spec),
        "search_policy": {
            "selection": "pareto",
            "may_change_fixed_values": False,
            "may_expand_bounds": False,
            "may_change_acceptance_criteria": False,
            "preserve_source_evidence": True,
        },
    }
