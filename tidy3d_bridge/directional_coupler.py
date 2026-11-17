"""Translate the Lean4 EIS SOI directional-coupler spec into Tidy3D.

No credentials are read here and no cloud job is submitted by construction.
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

NM_PER_UM = 1000.0
REQUIRED = {
    "schema_version", "spec_id", "wavelength_nm", "core_width_nm",
    "core_height_nm", "gap_nm", "coupling_length_nm", "access_length_nm",
    "box_thickness_nm", "substrate_thickness_nm", "core_permittivity",
    "oxide_permittivity", "domain_x_nm", "domain_y_nm", "domain_z_nm",
    "domain_center_z_nm", "grid_steps_per_wavelength", "wavelength_min_nm",
    "wavelength_max_nm", "wavelength_samples", "evidence_class",
    "process_status", "phasor_convention", "geometry_authority",
    "solver_authority", "launch_policy",
}


def load_spec(path: str | Path) -> dict[str, Any]:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def validate_spec(spec: dict[str, Any]) -> dict[str, float]:
    missing = sorted(REQUIRED - spec.keys())
    if missing:
        raise ValueError(f"Missing Lean-emitted fields: {missing}")
    if spec["schema_version"] != "0.1":
        raise ValueError(f"Unsupported schema version: {spec['schema_version']}")
    if spec["phasor_convention"] != "exp(+i omega t)":
        raise ValueError("Unexpected EIS phasor convention")
    if spec["launch_policy"] != "explicit_user_action_required":
        raise ValueError("Simulation launch policy must require explicit user action")
    if spec["evidence_class"] not in {"assumed", "simulated", "fitted", "measured"}:
        raise ValueError("Unknown evidence class")

    numeric = [
        "wavelength_nm", "core_width_nm", "core_height_nm", "gap_nm",
        "coupling_length_nm", "access_length_nm", "box_thickness_nm",
        "substrate_thickness_nm", "domain_x_nm", "domain_y_nm", "domain_z_nm",
        "grid_steps_per_wavelength", "wavelength_min_nm",
        "wavelength_max_nm", "wavelength_samples",
        "core_permittivity", "oxide_permittivity",
    ]
    values: dict[str, float] = {}
    for key in numeric:
        try:
            values[key] = float(spec[key])
        except (TypeError, ValueError, KeyError) as exc:
            raise ValueError(f"{key} must be numeric") from exc
        if values[key] <= 0:
            raise ValueError(f"{key} must be positive")

    try:
        values["domain_center_z_nm"] = float(spec["domain_center_z_nm"])
    except (TypeError, ValueError) as exc:
        raise ValueError("domain_center_z_nm must be numeric") from exc

    required_x = values["coupling_length_nm"] + 2 * values["access_length_nm"]
    if values["domain_x_nm"] <= required_x:
        raise ValueError("x-domain must exceed coupling length plus both access sections")
    if values["wavelength_max_nm"] <= values["wavelength_min_nm"]:
        raise ValueError("wavelength sweep must have positive span")
    if int(values["wavelength_samples"]) < 2:
        raise ValueError("wavelength_samples must be at least 2")
    if spec["process_status"] == "illustrative_not_foundry_PDK":
        print("WARNING: ASSUMED illustrative values; not a foundry-qualified process.")
    return values


def _smoothstep(t):
    return t * t * (3.0 - 2.0 * t)


def _arm_vertices(np, xs, center_ys, width):
    """Closed xy polygon for a constant-width, smoothly transitioned arm."""
    lower = [(float(x), float(y - width / 2)) for x, y in zip(xs, center_ys)]
    upper = [(float(x), float(y + width / 2)) for x, y in zip(xs[::-1], center_ys[::-1])]
    return lower + upper


def build_directional_coupler(spec: dict[str, Any]):
    """Return (simulation, metadata); build only, do not submit."""
    v = validate_spec(spec)
    import numpy as np
    import tidy3d as td

    um = lambda key: v[key] / NM_PER_UM
    c0 = td.C_0
    lambda0_um = um("wavelength_nm")
    freq0 = c0 / lambda0_um
    lambda_min_um = um("wavelength_min_nm")
    lambda_max_um = um("wavelength_max_nm")
    freqs = np.linspace(c0 / lambda_max_um, c0 / lambda_min_um,
                        int(v["wavelength_samples"]))

    width = um("core_width_nm")
    height = um("core_height_nm")
    gap = um("gap_nm")
    arm_offset = (width + gap) / 2
    coupling_length = um("coupling_length_nm")
    access_length = um("access_length_nm")
    box_t = um("box_thickness_nm")
    substrate_t = um("substrate_thickness_nm")
    z_center = v["domain_center_z_nm"] / NM_PER_UM
    domain = (um("domain_x_nm"), um("domain_y_nm"), um("domain_z_nm"))

    # Both arms are far apart in the access regions and parallel at the
    # declared gap only over the declared coupling length. Smoothstep
    # transitions provide a first-order adiabatic approach/exit geometry.
    half_coupler = coupling_length / 2
    x_left = -half_coupler - access_length
    x_right = half_coupler + access_length
    left_x = np.linspace(x_left, -half_coupler, 17, endpoint=True)
    center_x = np.linspace(-half_coupler, half_coupler, 17, endpoint=True)[1:]
    right_x = np.linspace(half_coupler, x_right, 17, endpoint=True)[1:]
    xs = np.concatenate([left_x, center_x, right_x])
    ys_abs = []
    for x in xs:
        if x < -half_coupler:
            t = (x - x_left) / access_length
            separation_center = um("domain_y_nm") * 0.0 + 1.5 - (1.5 - arm_offset) * _smoothstep(t)
        elif x > half_coupler:
            t = (x - half_coupler) / access_length
            separation_center = arm_offset + (1.5 - arm_offset) * _smoothstep(t)
        else:
            separation_center = arm_offset
        ys_abs.append(separation_center)
    ys_abs = np.asarray(ys_abs)

    lower_y = -float(np.interp(-6.5, xs, ys_abs))
    upper_y = float(np.interp(6.5, xs, ys_abs))

    silicon = td.Medium(permittivity=v["core_permittivity"])
    oxide = td.Medium(permittivity=v["oxide_permittivity"])
    box_center_z = -height / 2 - box_t / 2
    substrate_center_z = -height / 2 - box_t - substrate_t / 2

    structures = [
        td.Structure(
            geometry=td.Box(center=(0, 0, box_center_z),
                            size=(td.inf, td.inf, box_t)),
            medium=oxide, name="buried_oxide",
        ),
        td.Structure(
            geometry=td.Box(center=(0, 0, substrate_center_z),
                            size=(td.inf, td.inf, substrate_t)),
            medium=silicon, name="silicon_substrate",
        ),
        td.Structure(
            geometry=td.PolySlab(
                vertices=_arm_vertices(np, xs, -ys_abs, width),
                axis=2, slab_bounds=(-height / 2, height / 2),
            ),
            medium=silicon, name="lower_waveguide",
        ),
        td.Structure(
            geometry=td.PolySlab(
                vertices=_arm_vertices(np, xs, ys_abs, width),
                axis=2, slab_bounds=(-height / 2, height / 2),
            ),
            medium=silicon, name="upper_waveguide",
        ),
    ]

    mode_spec = td.ModeSpec(num_modes=1, target_neff=2.4)
    source = td.ModeSource(
        center=(-6.5, lower_y, 0),
        size=(0, 0.8, 1.8),
        source_time=td.GaussianPulse(freq0=freq0, fwidth=freq0 / 15),
        direction="+", mode_spec=mode_spec, mode_index=0,
        name="lower_arm_input",
    )
    monitor_size = (0, 1.2, 1.8)
    monitors = [
        td.ModeMonitor(
            center=(6.5, -upper_y, 0), size=monitor_size,
            freqs=freqs, mode_spec=mode_spec, name="through",
        ),
        td.ModeMonitor(
            center=(6.5, upper_y, 0), size=monitor_size,
            freqs=freqs, mode_spec=mode_spec, name="cross",
        ),
    ]

    sim = td.Simulation(
        center=(0, 0, z_center), size=domain, medium=oxide,
        structures=structures, sources=[source], monitors=monitors,
        grid_spec=td.GridSpec.auto(
            min_steps_per_wvl=int(v["grid_steps_per_wavelength"]),
            wavelength=lambda_min_um,
        ),
        boundary_spec=td.BoundarySpec.all_sides(boundary=td.PML()),
        run_time=2.0e-12,
    )
    metadata = {
        "spec_id": spec["spec_id"],
        "frequency_count": len(freqs),
        "wavelength_min_um": lambda_min_um,
        "wavelength_max_um": lambda_max_um,
        "arm_center_separation_at_coupler_um": 2 * arm_offset,
        "coupling_length_um": coupling_length,
        "access_length_um_each_side": access_length,
        "input_port": "lower_arm_input",
        "output_ports": ["through", "cross"],
        "evidence_class": spec["evidence_class"],
        "process_status": spec["process_status"],
        "cloud_submission": "not_submitted",
    }
    return sim, metadata


def launch_cloud(simulation, task_name: str, path: str = "data/eis_dc.hdf5"):
    """Explicitly submit an already-reviewed simulation to FlexCompute cloud."""
    import tidy3d.web as web
    return web.run(simulation, task_name=task_name, path=path, verbose=True)
