"""Lower validated EIS optical-netlist JSON into a PhotonForge netlist.

This is a topology adapter. It does not invent cells, geometry, PDK data,
material properties, or simulation models. Unknown component kinds fail closed.
"""
from __future__ import annotations

from typing import Any, Mapping


EVIDENCE_CLASSES = {\n    "tianReported",\n    "sourceInterpretation",\n    "eisArchitectureChoice",\n    "sourceUnknown",\n    "eisAssumed",\n    "simulated",\n}\n\nSUPPORTED_KINDS = {
    "laser",
    "mmi1x2",
    "mmi2x2",
    "fanoutTree",
    "mziCell",
    "balancedPhotodetector",
}


def _port_ref(value: Mapping[str, Any], where: str) -> tuple[str, str]:
    if not isinstance(value, Mapping):
        raise ValueError(f"{where} must be an object")
    instance_id = value.get("instanceId")
    port_name = value.get("portName")
    if not isinstance(instance_id, str) or not instance_id:
        raise ValueError(f"{where}.instanceId must be a non-empty string")
    if not isinstance(port_name, str) or not port_name:
        raise ValueError(f"{where}.portName must be a non-empty string")
    return instance_id, port_name


def validate_netlist(document: Mapping[str, Any]) -> None:
    if document.get("schemaVersion") != 1:
        raise ValueError("unsupported EIS netlist schemaVersion")
    if not isinstance(document.get("name"), str) or not document["name"]:
        raise ValueError("netlist name is required")
    instances = document.get("instances")
    connections = document.get("connections")
    inputs = document.get("inputs")
    outputs = document.get("outputs")
    if not all(isinstance(x, list) for x in (instances, connections, inputs, outputs)):
        raise ValueError("instances, connections, inputs, and outputs must be arrays")

    by_id: dict[str, Mapping[str, Any]] = {}
    for item in instances:
        if not isinstance(item, Mapping):
            raise ValueError("each instance must be an object")
        instance_id, kind, ports = item.get("id"), item.get("kind"), item.get("ports")
        if not isinstance(instance_id, str) or not instance_id:
            raise ValueError("instance id must be a non-empty string")
        if instance_id in by_id:
            raise ValueError(f"duplicate instance id: {instance_id}")
        if kind not in SUPPORTED_KINDS:
            raise ValueError(f"unsupported component kind: {kind}")
        if not isinstance(ports, list) or not ports or not all(
            isinstance(p, str) and p for p in ports
        ):
            raise ValueError(f"{instance_id}: ports must be non-empty strings")
        if len(set(ports)) != len(ports):
            raise ValueError(f"{instance_id}: duplicate port name")
        by_id[instance_id] = item

    def exists(ref: tuple[str, str]) -> bool:
        iid, pname = ref
        return iid in by_id and pname in by_id[iid]["ports"]

    used: set[tuple[str, str]] = set()
    for index, edge in enumerate(connections):
        if not isinstance(edge, Mapping):
            raise ValueError(f"connections[{index}] must be an object")
        source = _port_ref(edge.get("source"), f"connections[{index}].source")
        target = _port_ref(edge.get("target"), f"connections[{index}].target")
        if source == target:
            raise ValueError(f"connections[{index}] is a self-connection")
        if not exists(source) or not exists(target):
            raise ValueError(f"connections[{index}] references an undeclared port")
        if source in used or target in used:
            raise ValueError("a component port is used by more than one connection")
        used.add(source)
        used.add(target)

    boundary: list[tuple[str, str]] = []
    for group_name, group in (("inputs", inputs), ("outputs", outputs)):
        for index, raw in enumerate(group):
            ref = _port_ref(raw, f"{group_name}[{index}]")
            if not exists(ref):
                raise ValueError(f"{group_name}[{index}] references an undeclared port")
            boundary.append(ref)
    if len(set(boundary)) != len(boundary):
        raise ValueError("duplicate top-level boundary port")


def lower_to_photonforge(
    document: Mapping[str, Any],
    component_registry: Mapping[str, Any],
) -> dict[str, Any]:
    """Return the PhotonForge component_from_netlist input dictionary.

    component_registry maps EIS component kind strings to concrete PhotonForge
    Component objects. No generic placeholder cells are substituted.
    """
    validate_netlist(document)
    pf_instances: dict[str, Any] = {}
    for item in document["instances"]:
        kind = item["kind"]
        if kind not in component_registry:
            raise KeyError(
                f"no approved PhotonForge cell registered for EIS kind {kind!r}"
            )
        pf_instances[item["id"]] = component_registry[kind]

    virtual_connections = []
    for edge in document["connections"]:
        src = _port_ref(edge["source"], "source")
        dst = _port_ref(edge["target"], "target")
        virtual_connections.append((src, dst))

    # Boundary-port export is intentionally returned as metadata until the
    # PhotonForge version-specific top-level port mapping is pinned and tested.
    return {
        "instances": pf_instances,
        "virtual connections": virtual_connections,
    }


def lower_and_build(document: Mapping[str, Any], component_registry: Mapping[str, Any]):
    """Build a PhotonForge component after the caller supplies approved cells."""
    import photonforge as pf

    lowered = lower_to_photonforge(document, component_registry)
    return pf.component_from_netlist(lowered)
