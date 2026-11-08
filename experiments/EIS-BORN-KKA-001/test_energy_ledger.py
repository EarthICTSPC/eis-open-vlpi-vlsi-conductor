import pytest

from energy_ledger import ENERGY_COMPONENTS, EnergyLedger, compare_matched_runs


def ledger(scale=1.0, *, workload="toy-inference-v1", acceptance="accepted-output-v1"):
    return EnergyLedger(
        workload_id=workload,
        acceptance_contract_id=acceptance,
        accepted_useful_transformations=100,
        components_j={name: scale * (index + 1) for index, name in enumerate(sorted(ENERGY_COMPONENTS))},
        optical_loss_fraction=0.2,
    )


def test_energy_per_accepted_transformation_uses_all_components():
    item = ledger()
    expected = sum(item.components_j.values()) / 100
    assert item.joules_per_accepted_transformation == pytest.approx(expected)


def test_matched_comparison_reports_fractional_savings():
    result = compare_matched_runs(ledger(2.0), ledger(1.0))
    assert result.fractional_energy_savings == pytest.approx(0.5)


def test_comparison_rejects_different_workloads():
    with pytest.raises(ValueError, match="workload_id"):
        compare_matched_runs(ledger(), ledger(workload="different"))


def test_comparison_rejects_different_acceptance_contracts():
    with pytest.raises(ValueError, match="acceptance_contract_id"):
        compare_matched_runs(ledger(), ledger(acceptance="different"))


def test_ledger_requires_every_energy_boundary_term():
    item = ledger()
    incomplete = dict(item.components_j)
    incomplete.pop("cooling_j")
    with pytest.raises(ValueError, match="missing"):
        EnergyLedger(
            workload_id=item.workload_id,
            acceptance_contract_id=item.acceptance_contract_id,
            accepted_useful_transformations=100,
            components_j=incomplete,
        )


def test_ledger_rejects_negative_energy():
    item = ledger()
    invalid = dict(item.components_j)
    invalid["laser_wall_plug_j"] = -1.0
    with pytest.raises(ValueError, match="nonnegative"):
        EnergyLedger(
            workload_id=item.workload_id,
            acceptance_contract_id=item.acceptance_contract_id,
            accepted_useful_transformations=100,
            components_j=invalid,
        )


def test_optical_loss_fraction_is_metadata_not_a_summed_energy_term():
    item = ledger()
    assert "optical_loss_fraction" not in item.components_j
    assert item.total_wall_plug_j == pytest.approx(sum(item.components_j.values()))


def test_zero_accepted_outputs_are_rejected():
    item = ledger()
    with pytest.raises(ValueError, match="must be positive"):
        EnergyLedger(
            workload_id=item.workload_id,
            acceptance_contract_id=item.acceptance_contract_id,
            accepted_useful_transformations=0,
            components_j=item.components_j,
        )
