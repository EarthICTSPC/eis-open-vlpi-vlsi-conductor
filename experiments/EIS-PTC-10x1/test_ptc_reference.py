"""Conformance tests for the Tian PTC ideal MZI transfer equations."""

import math
from pathlib import Path

from ptc_reference import MZIControls, bpd_output, mzi_field, mzi_field_amplitude, mzi_field_phase


def test_zero_internal_phases_give_half_amplitude_and_quarter_pi_phase():
    controls = MZIControls(external=0.0, internal_a=0.0, internal_b=0.0)
    assert math.isclose(mzi_field_amplitude(1.0, controls), 0.5, abs_tol=1e-14)
    assert math.isclose(mzi_field_phase(controls), math.pi / 4.0, abs_tol=1e-14)


def test_external_phase_control_shifts_output_phase():
    base = MZIControls(external=0.0, internal_a=0.2, internal_b=-0.1)
    shifted = MZIControls(external=0.37, internal_a=0.2, internal_b=-0.1)
    assert math.isclose(
        mzi_field_phase(shifted) - mzi_field_phase(base),
        0.37,
        abs_tol=1e-14,
    )


def test_signed_cosine_is_not_clipped():
    controls = MZIControls(external=0.0, internal_a=0.0, internal_b=math.pi)
    amplitude = mzi_field_amplitude(1.0, controls)
    assert amplitude < 0.0
    expected = amplitude * complex(
        math.cos(mzi_field_phase(controls)),
        math.sin(mzi_field_phase(controls)),
    )
    assert abs(mzi_field(1.0, controls) - expected) < 1e-14


def test_bpd_reference_case_matches_supplement_equation():
    a = MZIControls(external=math.pi / 2.0, internal_a=0.0, internal_b=0.0)
    b = MZIControls(external=0.0, internal_a=0.0, internal_b=0.0)
    assert math.isclose(bpd_output(1.0, 1.0, a, b), 0.5, abs_tol=1e-14)


def test_bpd_is_antisymmetric_under_operand_swap():
    a = MZIControls(external=0.31, internal_a=-0.22, internal_b=0.41)
    b = MZIControls(external=-0.17, internal_a=0.28, internal_b=-0.36)
    forward = bpd_output(1.3, 0.7, a, b)
    reverse = bpd_output(0.7, 1.3, b, a)
    assert math.isclose(forward, -reverse, rel_tol=1e-13, abs_tol=1e-13)


def test_bpd_zero_when_either_incident_field_is_zero():
    a = MZIControls(external=0.4, internal_a=0.1, internal_b=-0.2)
    b = MZIControls(external=-0.3, internal_a=0.2, internal_b=0.5)
    assert bpd_output(0.0, 1.0, a, b) == 0.0
    assert bpd_output(1.0, 0.0, a, b) == 0.0


def test_reference_functions_have_lean_formal_anchors():
    root = Path(__file__).parents[2]
    lean = (root / "EISKKA" / "PTCPrototype.lean").read_text(encoding="utf-8")
    for theorem in (
        "mziFieldAmplitude_zero",
        "mziFieldAmplitude_scale",
        "mziFieldPhase_external_shift",
        "bpdOutput_zero_A",
        "bpdOutput_zero_B",
        "bpdOutput_swap_neg",
        "total_mzi_count_is_eleven",
        "total_phase_shifter_count_is_thirty_three",
    ):
        assert f"theorem {theorem}" in lean
