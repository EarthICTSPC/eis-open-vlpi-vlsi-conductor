import numpy as np
import pytest
from eis_kka_001b_mzi_field import directional_coupler, ideal_balanced_interference, simulate_mzi


def test_directional_coupler_is_unitary():
    for kappa in (0.0, 0.1, 0.5, 0.9, 1.0):
        c = directional_coupler(kappa)
        np.testing.assert_allclose(c.T @ c, np.eye(2), atol=1e-14)


def test_lossless_mzi_conserves_total_power():
    ein = np.array([1.0 + 0.2j, 0.3 - 0.4j])
    result = simulate_mzi(ein, kappa_in=0.37, kappa_out=0.62,
                          phase_rad=(0.73, -1.21), arm_loss_db=(0.0, 0.0))
    np.testing.assert_allclose(result.output_powers.sum(),
                               np.abs(ein).dot(np.abs(ein)),
                               rtol=1e-13, atol=1e-13)


def test_balanced_output_difference_is_cross_term():
    a, b = 0.7 + 0.2j, -0.1 + 0.8j
    result = simulate_mzi([a, b], kappa_in=0.0, kappa_out=0.5)
    np.testing.assert_allclose(result.balanced_difference,
                               ideal_balanced_interference(*result.arm_fields), atol=1e-14)


def test_equal_arm_phase_shift_does_not_change_output_powers():
    ein = np.array([1.0 + 0.0j, 0.4 + 0.2j])
    a = simulate_mzi(ein, phase_rad=(0.0, 0.0))
    b = simulate_mzi(ein, phase_rad=(0.8, 0.8))
    np.testing.assert_allclose(a.output_powers, b.output_powers, atol=1e-14)


def test_arm_loss_does_not_increase_total_power():
    ein = np.array([1.0 + 0.0j, 0.0 + 0.0j])
    ideal, lossy = simulate_mzi(ein), simulate_mzi(ein, arm_loss_db=(3.0, 0.0))
    assert lossy.output_powers.sum() <= ideal.output_powers.sum() + 1e-14


def test_invalid_coupler_fraction_rejected():
    with pytest.raises(ValueError):
        directional_coupler(1.01)
