
import pytest

from vending_machine import make_change, purchase, select_item


def test_invalid_item():
    assert select_item("water", {}, 100) == "invalid"


def test_sold_out_item():
    assert select_item("cola", {"cola": 0}, 200) == "sold_out"


def test_insufficient_credit():
    assert select_item("cola", {"cola": 2}, 100) == "insufficient"


def test_valid_item():
    assert select_item("cola", {"cola": 2}, 150) == "ok"


def test_negative_change():
    with pytest.raises(ValueError, match="negative amount"):
        make_change(-1)


def test_zero_change():
    assert make_change(0) == []


def test_multiple_coin_change():
    assert make_change(185) == [100, 50, 25, 10]


def test_unrepresentable_change():
    assert make_change(3) is None


def test_purchase_invalid_item():
    assert purchase("water", {}, 200) == ("invalid", [])


def test_purchase_sold_out():
    assert purchase("cola", {"cola": 0}, 200) == ("sold_out", [])


def test_purchase_insufficient_credit():
    assert purchase("cola", {"cola": 2}, 100) == ("insufficient", [])


def test_purchase_no_exact_change():
    assert purchase("cola", {"cola": 2}, 153) == ("no_exact_change", [])


def test_successful_purchase_without_change():
    stock = {"cola": 2}
    assert purchase("cola", stock, 150) == ("dispensed", [])
    assert stock["cola"] == 1


def test_successful_purchase_with_change():
    stock = {"chips": 2}
    assert purchase("chips", stock, 200) == ("dispensed", [100])
    assert stock["chips"] == 1
