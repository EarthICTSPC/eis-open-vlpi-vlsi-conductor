"""Frozen numerical reference for EIS-TIAN-KKA-LIFT-001A.

Source: Tian et al. (2025), Supplementary Information, SI-4 Eq. (S13),
Table S1.

This implements the source-reported scalar fitted response. It is not a
complex optical transfer function and is not a physical-device simulator.
Coefficient units and observable normalization are unspecified in the source.

Do not silently alter the equation or coefficients. Changes require a
separately reviewed revision with source, rationale, and regression evidence.
"""

from __future__ import annotations

import numpy as np

SOURCE_EQUATION = "Tian et al. (2025) SI-4 Eq. (S13)"
SOURCE_TABLE = "Table S1"

T = {
    "a1": 0.0730,
    "b": 4.5760,
    "a2": 0.0638,
    "rows": {
        "S1-row-01": {"c": 0.1210, "d": 4.1363, "e": -0.0159},
        "S1-row-02": {"c": 0.1135, "d": 3.7057, "e": 0.0059},
        "S1-row-03": {"c": 0.1115, "d": -3.4004, "e": 0.0079},
        "S1-row-04": {"c": 0.1152, "d": 0.1490, "e": -0.0058},
        "S1-row-05": {"c": 0.1161, "d": 5.2457, "e": 0.0002},
        "S1-row-06": {"c": 0.1187, "d": -3.5212, "e": 0.0086},
        "S1-row-07": {"c": 0.1186, "d": -9.9666, "e": 0.0161},
        "S1-row-08": {"c": 0.1203, "d": -0.5490, "e": -0.0128},
        "S1-row-09": {"c": 0.1238, "d": 0.5386, "e": -0.0098},
        "S1-row-10": {"c": 0.1305, "d": 3.9400, "e": -0.0007},
    },
}


def tian_si4_s13(
    VA: np.ndarray | float,
    VB: np.ndarray | float,
    row: str,
) -> np.ndarray:
    """Evaluate Tian SI-4 Eq. (S13) for one Table S1 fitted entry."""
    p = T["rows"][row]
    return (
        np.cos(T["a1"] * np.asarray(VB) ** 2 + T["b"])
        * np.cos(
            p["c"] * np.asarray(VA) ** 2
            - T["a2"] * np.asarray(VB) ** 2
            + p["d"]
        )
        + p["e"]
    )


def validate_table_s1(
    points: int = 281,
    voltage_min: float = 0.0,
    voltage_max: float = 7.0,
) -> dict[str, dict[str, object]]:
    """Run the illustrative-grid finite/shape check for all ten Table S1 rows.

    The voltage grid is an EIS test fixture, not asserted to be Tian's
    experimental sampling grid.
    """
    va = np.linspace(voltage_min, voltage_max, points)
    vb = np.linspace(voltage_min, voltage_max, points)
    va_grid, vb_grid = np.meshgrid(va, vb)

    results = {}
    for row in T["rows"]:
        response = tian_si4_s13(va_grid, vb_grid, row)
        results[row] = {
            "shape": response.shape,
            "finite": bool(np.isfinite(response).all()),
            "min": float(response.min()),
            "max": float(response.max()),
        }
    return results


if __name__ == "__main__":
    results = validate_table_s1()
    print(f"{SOURCE_EQUATION} — {SOURCE_TABLE} validation")
    print("-" * 65)
    for row, result in results.items():
        print(
            f"{row:12s} | shape={result['shape']} | "
            f"finite={result['finite']} | "
            f"min={result['min']: .6f} | max={result['max']: .6f}"
        )

    assert len(results) == 10
    assert all(r["shape"] == (281, 281) for r in results.values())
    assert all(r["finite"] for r in results.values())
    print("\nPASS: all ten Table S1 entries evaluated.")
