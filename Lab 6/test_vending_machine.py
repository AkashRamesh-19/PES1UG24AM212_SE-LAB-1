
import pytest

from vending_machine import make_change, purchase, select_item


def test_invalid_item():
    assert select_item("water", {}, 100) == "invalid"


def test_sold_out_item():
    assert select_item("cola", {"cola": 0}, 200) == "sold_out"


def test_insufficient_credit():
    assert select_item("cola", {"cola": 2}, 100) == "insufficient"


def test_valid_item_selection():
    assert select_item("cola", {"cola": 2}, 150) == "ok"


def test_no_change_needed():
    assert make_change(0) == []


def test_make_change_using_multiple_coin_values():
    assert make_change(185) == [100, 50, 25, 10]


def test_negative_change_raises_value_error():
    with pytest.raises(ValueError, match="negative amount"):
        make_change(-1)


def test_unrepresentable_change_returns_none():
    assert make_change(3) is None


def test_purchase_with_invalid_item():
    assert purchase("water", {}, 200) == ("invalid", [])


def test_purchase_sold_out_item():
    assert purchase("cola", {"cola": 0}, 200) == ("sold_out", [])


def test_purchase_with_insufficient_credit():
    assert purchase("cola", {"cola": 2}, 100) == ("insufficient", [])


def test_purchase_without_exact_change():
    assert purchase("cola", {"cola": 2}, 153) == ("no_exact_change", [])


def test_successful_purchase_updates_stock():
    stock = {"cola": 2}
    result = purchase("cola", stock, 150)

    assert result == ("dispensed", [])
    assert stock["cola"] == 1


def test_successful_purchase_returns_change():
    stock = {"chips": 2}
    result = purchase("chips", stock, 200)

    assert result == ("dispensed", [100])
    assert stock["chips"] == 1
