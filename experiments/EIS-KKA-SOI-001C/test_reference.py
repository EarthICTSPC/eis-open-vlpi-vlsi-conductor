"""Deterministic tests for the EIS scalar interference reference."""
from __future__ import annotations

import json
import math
import re
from pathlib import Path

import pytest

from kka_reference import (
    cross_term,
    cross_term_after_transfers,
    propagate,
    total_intensity,
)

HERE = Path(__file__).resolve().parent
VECTORS = json.loads((HERE / "vectors.json").read_text(encoding="utf-8"))
ATOL = VECTORS["tolerance"]["absolute"]
RTOL = VECTORS["tolerance"]["relative"]
LEAN_VECTOR_SOURCE = HERE.parents[1] / "EISKKA" / "ConformanceVectors.lean"
LEAN_VECTOR_TEXT = LEAN_VECTOR_SOURCE.read_text(encoding="utf-8")
LEAN_THEOREMS = set(re.findall(r"\\btheorem\\s+([A-Za-z0-9_]+)", LEAN_VECTOR_TEXT))


def test_each_json_vector_has_a_matching_lean_theorem_anchor():
    for vector in VECTORS["vectors"] + VECTORS["transfer_vectors"]:
        assert vector["lean_theorems"], vector["id"]
        for theorem in vector["lean_theorems"]:
            assert theorem in LEAN_THEOREMS, (vector["id"], theorem)


def z(pair: list[float]) -> complex:
    return complex(pair[0], pair[1])


@pytest.mark.parametrize("vector", VECTORS["vectors"], ids=lambda v: v["id"])
def test_hand_computable_interference_vectors(vector):
    a, b = z(vector["a"]), z(vector["b"])
    assert cross_term(a, b) == pytest.approx(vector["cross"], abs=ATOL, rel=RTOL)
    assert total_intensity(a, b) == pytest.approx(vector["total"], abs=ATOL, rel=RTOL)


@pytest.mark.parametrize("vector", VECTORS["transfer_vectors"], ids=lambda v: v["id"])
def test_transfer_vectors(vector):
    result = propagate(z(vector["field"]), z(vector["transfer"]))
    expected = z(vector["output"])
    assert result.real == pytest.approx(expected.real, abs=ATOL, rel=RTOL)
    assert result.imag == pytest.approx(expected.imag, abs=ATOL, rel=RTOL)


def test_cross_term_matches_independent_intensity_difference():
    pairs = [
        (1 + 2j, -0.5 + 0.25j),
        (2 - 3j, 4 + 1j),
        (-1 + 0.5j, 0.25 - 2j),
    ]
    for a, b in pairs:
        independent = abs(a + b) ** 2 - abs(a) ** 2 - abs(b) ** 2
        assert cross_term(a, b) == pytest.approx(independent, abs=ATOL, rel=RTOL)


def test_symmetry_and_conjugation_invariance():
    a, b = 0.7 - 1.2j, -0.3 + 0.9j
    expected = cross_term(a, b)
    assert cross_term(b, a) == pytest.approx(expected, abs=ATOL, rel=RTOL)
    assert cross_term(a.conjugate(), b.conjugate()) == pytest.approx(
        expected, abs=ATOL, rel=RTOL
    )


def test_phase_relation_and_bound():
    amp_a, amp_b = 1.7, 0.8
    for delta in (0.0, math.pi / 2, math.pi, -math.pi / 2, 0.37):
        a = amp_a * complex(math.cos(delta), math.sin(delta))
        b = complex(amp_b, 0.0)
        expected = 2 * amp_a * amp_b * math.cos(delta)
        value = cross_term(a, b)
        assert value == pytest.approx(expected, abs=ATOL, rel=RTOL)
        assert abs(value) <= 2 * abs(a) * abs(b) + ATOL


def test_signed_cross_term_is_not_clipped():
    assert cross_term(1 + 0j, -1 + 0j) == -2.0


@pytest.mark.parametrize("bad", [complex(float("nan"), 0), complex(0, float("inf"))])
def test_non_finite_fields_rejected(bad):
    with pytest.raises(ValueError):
        cross_term(bad, 1 + 0j)


@pytest.mark.parametrize("bad", [complex(float("nan"), 0), complex(0, float("-inf"))])
def test_non_finite_transfer_rejected(bad):
    with pytest.raises(ValueError):
        propagate(1 + 0j, bad)


def test_non_numeric_input_rejected():
    with pytest.raises(TypeError):
        cross_term("not-a-field", 1 + 0j)


def test_independent_operand_transfers():
    a, b = 1 + 0j, 1j
    ta, tb = 0.5j, 2 + 0j
    expected = cross_term(ta * a, tb * b)
    assert cross_term_after_transfers(a, b, ta, tb) == pytest.approx(
        expected, abs=ATOL, rel=RTOL
    )
