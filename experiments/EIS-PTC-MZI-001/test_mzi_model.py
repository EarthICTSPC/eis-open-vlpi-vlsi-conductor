import math

import pytest

from mzi_model import (
    MZIControls,
    MZIParameters,
    ThermalState,
    advance_thermal_state,
    evaluate_mzi,
    heater_power,
    ideal_field_amplitude,
    ideal_field_phase,
    target_heater_phases,
)


@pytest.fixture
def synthetic_params():
    # Synthetic regression fixture only. These are not Tian or EIS measurements.
    return MZIParameters(
        wavelength_m=1.55e-6,
        effective_index=2.4,
        propagation_loss_db_per_m=100.0,
        interaction_length_m=1.0e-3,
        coupler1_split_ratio=0.5,
        coupler2_split_ratio=0.5,
        coupler1_excess_loss_db=0.0,
        coupler2_excess_loss_db=0.0,
        heater_resistance_ohm=(100.0, 100.0, 100.0),
        heater_tempco_per_K=(0.0, 0.0, 0.0),
        phase_efficiency_rad_per_W=(2.0, 2.0, 2.0),
        thermal_coupling=((1.0, 0.1, 0.0), (0.1, 1.0, 0.1), (0.0, 0.1, 1.0)),
        thermal_time_constant_s=(1e-3, 2e-3, 3e-3),
        parameter_evidence="SYNTHETIC_TEST_FIXTURE",
    )


def test_ideal_transfer_zero_controls():
    c = MZIControls(0.0, 0.0, 0.0)
    assert math.isclose(ideal_field_amplitude(1.0, c), 0.5, abs_tol=1e-14)
    assert math.isclose(ideal_field_phase(c), math.pi / 4.0, abs_tol=1e-14)


def test_signed_amplitude_is_preserved():
    c = MZIControls(0.0, 0.0, math.pi)
    assert ideal_field_amplitude(1.0, c) < 0.0


def test_three_heater_power_and_thermal_coupling(synthetic_params):
    powers = (0.1, 0.2, 0.3)
    phases = target_heater_phases(powers, synthetic_params)
    assert phases == pytest.approx((0.24, 0.72, 0.68))


def test_heater_power_uses_v_squared_over_r():
    assert heater_power(2.0, 100.0) == pytest.approx(0.04)


def test_thermal_state_converges_toward_target(synthetic_params):
    start = ThermalState((0.0, 0.0, 0.0))
    target = (1.0, 2.0, 3.0)
    after = advance_thermal_state(start, target, 0.01, synthetic_params)
    assert all(0.0 < x < y for x, y in zip(after.phase_rad, target))


def test_thermal_state_does_not_change_at_zero_dt(synthetic_params):
    start = ThermalState((0.1, 0.2, 0.3))
    assert advance_thermal_state(start, (1.0, 2.0, 3.0), 0.0, synthetic_params) == start


def test_nonideal_model_reduces_amplitude_by_propagation_loss(synthetic_params):
    c = MZIControls(0.0, 0.0, 0.0)
    result = evaluate_mzi(1.0, c, synthetic_params)
    expected = 0.5 * 10.0 ** (-(100.0 * 1e-3) / 20.0)
    assert result.signed_amplitude == pytest.approx(expected)
    assert result.model_evidence == "SYNTHETIC_TEST_FIXTURE"


def test_balanced_couplers_have_unit_visibility(synthetic_params):
    result = evaluate_mzi(1.0, MZIControls(0, 0, 0), synthetic_params)
    assert result.signed_amplitude == pytest.approx(0.5 * 10 ** (-0.1 / 20))


def test_invalid_coupler_ratio_is_rejected(synthetic_params):
    bad = MZIParameters(**{**synthetic_params.__dict__, "coupler1_split_ratio": 1.0})
    with pytest.raises(ValueError):
        bad.validate()
