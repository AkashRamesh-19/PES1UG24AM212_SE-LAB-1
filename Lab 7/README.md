# Lab 7 - Fuzz Testing

## Objective

Use property-based testing to discover and fix input-validation bugs in the vending-machine application.

## What is fuzz testing?

Fuzz testing supplies a program with many generated, unexpected, or malformed inputs to expose crashes and incorrect behavior. Hypothesis is a Python property-based testing library: tests describe expected properties, and Hypothesis generates and minimizes examples that violate them.

## Functions tested

- `parse_coins(coins_csv)` parses a non-empty comma-separated list of non-negative ASCII integers.
- `slot_position(code)` converts one ASCII row letter and a positive column number into a zero-based `(row, column)` tuple.
- `change_due(payment)` accepts a `paid/price` string when both are non-negative whole numbers and payment covers the price; it returns the number of five-unit coins, preserving the starter output format.

Each function raises `TypeError` for non-string input and `ValueError` for malformed or invalid string input.

## Install

```bash
python -m pip install hypothesis pytest
```

## Run the application

```bash
python vending_machine.py
```

Enter values in the prompted formats, such as `5,10,25`, `B7`, and `200/150`.

## Run the tests

```bash
python -m pytest -v -ra test_vending_machine.py
```

The 10 Hypothesis tests generate valid lists, slot codes, and payment values, and exercise malformed strings and unexpected data types.

## Bugs found and fixed

The starter code relied on unchecked `.split()` calls and direct `int()` conversion. As a result, non-string values raised accidental `AttributeError` or `IndexError`; blank and malformed fields failed inconsistently; negative coin/amount values and zero slot columns could be accepted; Unicode digits and non-ASCII row characters were not consistently rejected; and underpayment could produce a misleading change result.

The fixed code checks types and input structure before parsing, accepts ASCII decimal digits only, rejects negative values and invalid slot columns, and prevents change calculation when payment is below price. Valid input behavior and output formatting remain compatible with the starter application.

See [REPORT.md](REPORT.md) for the issue/fix table and before-and-after results. Actual command outputs are recorded as text under `evidence/`; those files are execution transcripts, not screenshots.

