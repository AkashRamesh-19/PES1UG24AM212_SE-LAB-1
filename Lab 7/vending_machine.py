"""Input parsing helpers for a small vending machine exercise."""

import re


_ASCII_UNSIGNED_INTEGER = re.compile(r"[0-9]+\Z")


def _require_text(value, argument_name):
    """Require a string argument and report the public argument name."""
    if not isinstance(value, str):
        raise TypeError(f"{argument_name} must be a string")


def _parse_nonnegative_integer(text, description):
    """Parse an ASCII decimal integer that is zero or greater."""
    if not _ASCII_UNSIGNED_INTEGER.fullmatch(text):
        raise ValueError(f"{description} must be a non-negative whole number")
    try:
        return int(text, 10)
    except ValueError as exc:
        # Python limits extremely long decimal conversions to protect against
        # denial-of-service inputs. Keep that failure in our documented API.
        raise ValueError(f"{description} is too large to parse") from exc


def parse_coins(coins_csv):
    """Parse a non-empty CSV string of non-negative ASCII integer values.

    Surrounding whitespace around each value is ignored. Empty fields,
    negative values, Unicode digits, and non-string inputs are rejected.
    """
    _require_text(coins_csv, "coins_csv")
    if not coins_csv.strip():
        raise ValueError("coins_csv must contain at least one coin value")

    coins = []
    for index, item in enumerate(coins_csv.split(","), start=1):
        value = item.strip()
        if not value:
            raise ValueError(f"coin value {index} is empty")
        coins.append(_parse_nonnegative_integer(value, f"coin value {index}"))
    return coins


def slot_position(code):
    """Convert a slot like ``B7`` to a zero-based (row, column) tuple.

    Rows are ASCII letters A-Z (case-insensitive); columns are positive ASCII
    integers. Invalid codes raise ValueError and non-string inputs TypeError.
    """
    _require_text(code, "code")
    if len(code) < 2 or not ("A" <= code[0].upper() <= "Z"):
        raise ValueError("code must start with one ASCII letter from A to Z")

    column_text = code[1:]
    if not _ASCII_UNSIGNED_INTEGER.fullmatch(column_text):
        raise ValueError("code must end with a positive ASCII column number")
    column = _parse_nonnegative_integer(column_text, "column number")
    if column == 0:
        raise ValueError("column number must be greater than zero")

    return ord(code[0].upper()) - ord("A"), column - 1


def change_due(payment):
    """Return the count of five-unit coins for a ``paid/price`` string.

    Amounts must be non-negative ASCII whole numbers, and payment must cover
    the price. The result keeps the starter program's five-coin output format.
    """
    _require_text(payment, "payment")
    parts = payment.split("/")
    if len(parts) != 2:
        raise ValueError("payment must contain exactly one '/' separator")

    paid = _parse_nonnegative_integer(parts[0].strip(), "paid amount")
    price = _parse_nonnegative_integer(parts[1].strip(), "price")
    if paid < price:
        raise ValueError("paid amount must be greater than or equal to price")

    return f"{(paid - price) // 5} five-coins"


def main():
    """Run each vending-machine helper interactively with valid user input."""
    print("==== Running parse_coins ====")
    user_input = input("Enter coin values as CSV (e.g. 5,10,25): ")
    result = parse_coins(user_input)
    print("Coins:", result)

    print("\n==== Running slot_position ====")
    user_input = input("Enter a slot code (e.g. B7): ")
    result = slot_position(user_input)
    print("Row and Column:", result)

    print("\n==== Running change_due ====")
    user_input = input("Enter paid/price (e.g. 200/150): ")
    result = change_due(user_input)
    print("Change Due:", result)


if __name__ == "__main__":
    main()
