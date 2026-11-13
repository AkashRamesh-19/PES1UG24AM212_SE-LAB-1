from hypothesis import given, strategies as st
import pytest

from vending_machine import change_due, parse_coins, slot_position


# Valid inputs are generated at scale so each property is checked against many
# values, including large integer boundaries.


@given(st.lists(st.integers(min_value=0, max_value=10**200), min_size=1, max_size=30))
def test_parse_coins_returns_the_input_integers(values):
    csv = ",".join(str(value) for value in values)
    assert parse_coins(csv) == values


@given(st.sampled_from(["", "1,,3", ",1", "1,", "one,two", "-1", "١"]))
def test_parse_coins_rejects_malformed_or_negative_values(csv):
    with pytest.raises(ValueError):
        parse_coins(csv)


@given(st.one_of(st.none(), st.integers(), st.lists(st.text())))
def test_parse_coins_rejects_non_string_input(value):
    with pytest.raises(TypeError):
        parse_coins(value)


@given(st.characters(min_codepoint=65, max_codepoint=90), st.integers(min_value=1, max_value=10**200))
def test_slot_position_maps_valid_codes_to_zero_based_positions(row, column):
    assert slot_position(f"{row}{column}") == (ord(row) - ord("A"), column - 1)


@given(st.sampled_from(["", "B", "B0", "B-1", "7", "BB", "B١", "A1x"]))
def test_slot_position_rejects_malformed_codes(code):
    with pytest.raises(ValueError):
        slot_position(code)


@given(st.one_of(st.none(), st.integers(), st.lists(st.text())))
def test_slot_position_rejects_non_string_input(value):
    with pytest.raises(TypeError):
        slot_position(value)


@given(
    st.integers(min_value=0, max_value=10**200),
    st.integers(min_value=0, max_value=10**200),
)
def test_change_due_reports_five_coin_count_when_payment_covers_price(paid, price):
    if paid < price:
        paid, price = price, paid
    assert change_due(f"{paid}/{price}") == f"{(paid - price) // 5} five-coins"


@given(st.sampled_from(["", "100", "/10", "10/", "1/2/3", "one/2", "10/-1", "١/0"]))
def test_change_due_rejects_malformed_or_negative_amounts(payment):
    with pytest.raises(ValueError):
        change_due(payment)


@given(st.integers(min_value=0, max_value=10**50))
def test_change_due_rejects_payment_below_price(amount):
    with pytest.raises(ValueError):
        change_due(f"{amount}/{amount + 1}")


@given(st.one_of(st.none(), st.integers(), st.lists(st.text())))
def test_change_due_rejects_non_string_input(value):
    with pytest.raises(TypeError):
        change_due(value)
