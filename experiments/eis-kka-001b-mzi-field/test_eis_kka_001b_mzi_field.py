import numpy as np
import pytest
from eis_kka_001b_mzi_field import directional_coupler, ideal_balanced_interference, mzi_scattering_matrix, simulate_mzi


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



def test_lossless_four_port_scattering_matrix_is_reciprocal_and_unitary():
    s = mzi_scattering_matrix(
        kappa_in=0.37,
        kappa_out=0.62,
        phase_rad=(0.73, -1.21),
        arm_loss_db=(0.0, 0.0),
    )
    np.testing.assert_allclose(s, s.T, atol=1e-14)
    np.testing.assert_allclose(s.conj().T @ s, np.eye(4), atol=1e-13)


def test_four_port_forward_block_matches_complex_field_model():
    rng = np.random.default_rng(20261127)
    for _ in range(100):
        fields = rng.normal(size=2) + 1j * rng.normal(size=2)
        kappa_in, kappa_out = rng.uniform(size=2)
        phase = rng.uniform(-np.pi, np.pi, size=2)
        loss = rng.uniform(0.0, 2.0, size=2)
        s = mzi_scattering_matrix(
            kappa_in=kappa_in,
            kappa_out=kappa_out,
            phase_rad=phase,
            arm_loss_db=loss,
        )
        result = simulate_mzi(
            fields,
            kappa_in=kappa_in,
            kappa_out=kappa_out,
            phase_rad=phase,
            arm_loss_db=loss,
        )
        np.testing.assert_allclose(s[2:, :2] @ fields, result.output_fields,
                                   rtol=1e-13, atol=1e-13)


def test_lossy_four_port_matrix_is_reciprocal_and_subunitary():
    s = mzi_scattering_matrix(
        kappa_in=0.41,
        kappa_out=0.58,
        phase_rad=(0.2, -0.9),
        arm_loss_db=(0.5, 1.7),
    )
    np.testing.assert_allclose(s, s.T, atol=1e-14)
    eigenvalues = np.linalg.eigvalsh(s.conj().T @ s)
    assert np.all(eigenvalues <= 1.0 + 1e-13)
    assert np.all(eigenvalues >= -1e-13)


def test_four_port_matrix_rejects_invalid_phase_and_loss():
    with pytest.raises(ValueError):
        mzi_scattering_matrix(phase_rad=(0.0, np.nan))
    with pytest.raises(ValueError):
        mzi_scattering_matrix(arm_loss_db=(0.0, -0.1))
