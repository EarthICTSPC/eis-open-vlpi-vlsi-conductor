import cmath
import math
import random

import pytest

from born_reference import (
    born_attention,
    born_score,
    born_score_from_quadratures,
    kka_bilinear_bridge,
    kka_cross_term,
    measured_bilinear_readout,
    overlap,
)


def test_overlap_uses_conjugated_key():
    q = [1 + 2j, 3 - 1j]
    k = [2 - 1j, -1 + 4j]
    assert overlap(q, k) == sum(a * b.conjugate() for a, b in zip(q, k))


def test_born_score_is_fourth_power_of_overlap_magnitude():
    q = [1 + 1j, 2 - 1j]
    k = [2 + 0.5j, -1 + 2j]
    z = overlap(q, k)
    assert born_score(q, k) == pytest.approx(abs(z) ** 4, rel=1e-13, abs=1e-13)


def test_quadrature_reconstruction_equals_complex_magnitude_score():
    z = 0.75 - 1.25j
    assert born_score_from_quadratures(z.real, z.imag) == pytest.approx(abs(z) ** 4)


def test_attention_weights_are_nonnegative_and_sum_to_one():
    q = [1 + 0.2j, -0.3 + 0.8j]
    keys = [
        [1 + 0j, 0.5 + 0.1j],
        [0.2 - 0.7j, 1.1 + 0.3j],
        [-0.4 + 0.2j, 0.1 - 0.9j],
    ]
    weights = born_attention(q, keys)
    assert all(w >= 0.0 for w in weights)
    assert all(w <= 1.0 for w in weights)
    assert math.fsum(weights) == pytest.approx(1.0, abs=1e-14)


def test_attention_is_invariant_to_common_query_amplitude_scaling():
    q = [0.5 + 0.25j, 1.0 - 0.5j]
    keys = [[1 + 0j, 0.2 + 0.1j], [0.1 + 0.3j, -0.4 + 0.2j]]
    original = born_attention(q, keys)
    scaled = born_attention([3j * value for value in q], keys)
    assert scaled == pytest.approx(original, rel=1e-12, abs=1e-12)


def test_attention_rejects_zero_denominator_without_epsilon_fallback():
    with pytest.raises(ValueError, match="positive denominator"):
        born_attention([0j, 0j], [[1 + 0j, 2 + 0j], [0.5j, 1j]])


def test_attention_rejects_mismatched_dimensions():
    with pytest.raises(ValueError, match="dimensions must match"):
        born_score([1 + 0j], [1 + 0j, 2 + 0j])


def test_nonfinite_inputs_are_rejected():
    with pytest.raises(ValueError, match="finite"):
        overlap([complex(float("inf"), 0)], [1 + 0j])


def test_kka_bilinear_bridge_matches_measured_product():
    rng = random.Random(20261107)
    for _ in range(500):
        x = complex(rng.uniform(-2, 2), rng.uniform(-2, 2))
        y = complex(rng.uniform(-2, 2), rng.uniform(-2, 2))
        assert kka_bilinear_bridge(x, y) == pytest.approx(
            measured_bilinear_readout(x, y), abs=1e-14
        )


def test_kka_cross_term_is_signed():
    assert kka_cross_term(1 + 0j, 1 + 0j) == pytest.approx(2.0)
    assert kka_cross_term(1 + 0j, -1 + 0j) == pytest.approx(-2.0)
    assert kka_cross_term(1 + 0j, 1j) == pytest.approx(0.0)


def test_overlap_conjugation_convention():
    q = [1 + 2j, -0.5 + 0.25j]
    k = [0.2 - 1j, 2 + 0.5j]
    assert overlap(q, k) == pytest.approx(
        sum(qi * ki.conjugate() for qi, ki in zip(q, k))
    )
