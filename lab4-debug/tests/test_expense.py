from decimal import Decimal
import pytest
from expense import load_expenses, total_expenses, discounted_total


def test_load_from_another_directory(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    assert len(load_expenses()) == 2


def test_string_amounts():
    assert total_expenses([{"amount": "60.00"}, {"amount": "40.00"}]) == Decimal("100.00")


def test_empty_expenses():
    assert total_expenses([]) == Decimal("0.00")


def test_negative_amount():
    with pytest.raises(ValueError):
        total_expenses([{"amount": "-1"}])


def test_exact_discount_boundary():
    assert discounted_total(Decimal("100")) == Decimal("90.00")


def test_below_boundary():
    assert discounted_total(Decimal("99")) == Decimal("99.00")


def test_above_boundary():
    assert discounted_total(Decimal("120")) == Decimal("108.00")


def test_decimal_precision():
    assert total_expenses([{"amount": "0.1"}, {"amount": "0.2"}]) == Decimal("0.30")
