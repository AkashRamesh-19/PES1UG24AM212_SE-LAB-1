# Lab 7 - Fuzz Testing for Input Validation Bugs

## Student

- **Name:** Akash Ramesh
- **SRN:** PES1UG24AM212
- **University:** PES University
- **Course:** Software Engineering Lab
- **Lab:** 7 - Fuzzing for Input Validation Bugs

## Objective

Use property-based fuzz testing to expose input-validation problems in the vending-machine helpers, then define and implement predictable behavior for malformed inputs.

## Tools

Python, pytest, Hypothesis, Git, and the supplied vending-machine starter project.

## Application overview

The original program defines `parse_coins`, `slot_position`, and `change_due`, plus an interactive `main()` that asks the user for one input for each function. The starter code used direct string splitting and integer conversion without checking input types or formats.

## Methodology

The test suite uses Hypothesis `@given` strategies to generate lists of large non-negative integers, slot rows and columns, payment and price pairs, and unexpected Python types. Targeted malformed examples cover empty fields, Unicode digits, missing or extra separators, negative and zero values, and invalid slot codes. Assertions describe the intended return values or the exact exception class for invalid inputs.

The completed tests were run against the untouched application first. That run established the failures before the implementation changed. After recording it, the application was hardened and the same tests were rerun.

## Issues and fixes

| Function | Input / Bug | Original Behaviour | Expected Behaviour | Fix Applied |
|---|---|---|---|---|
| `parse_coins` | `None` or another non-string | Raised incidental `AttributeError` | Raise `TypeError` | Validate the input type before string operations. |
| `parse_coins` | Empty CSV, blank fields, non-numeric text | Returned an empty list or raised a low-level conversion error | Raise `ValueError` with a clear message | Require at least one value and validate every trimmed CSV field. |
| `parse_coins` | Negative values or Unicode digits | Negative values were accepted; Unicode decimal digits could be parsed | Accept only non-negative ASCII whole numbers | Match each value against ASCII digits before conversion. |
| `slot_position` | Empty or non-string input | Raised incidental `IndexError` | Raise `ValueError` for malformed strings and `TypeError` for wrong types | Check type, row letter, and column syntax before indexing or conversion. |
| `slot_position` | `B0`, negative, extra or Unicode column characters | Could produce invalid coordinates or inconsistent exceptions | Require one ASCII letter A-Z and a positive ASCII column | Validate the complete format and reject zero or malformed columns. |
| `change_due` | `None`, missing/extra separators, blank or non-numeric amounts | Raised incidental exceptions from split/conversion | Raise `TypeError` or clear `ValueError` | Validate type, require exactly one slash, then validate both amounts. |
| `change_due` | Negative amount or payment below price | Could return misleading change | Reject invalid amounts and underpayment with `ValueError` | Require non-negative whole numbers and `paid >= price`. |
| All parsers | Extremely long decimal input | Python may reject conversion at its safety limit | Raise a documented `ValueError` | Convert the interpreter's long-integer limit error into a clear validation error. |

## Before-and-after test results

| Run | Result |
|---|---|
| Original application, 10 Hypothesis tests | 7 failed, 3 passed. Failures exposed malformed input, invalid coordinates, unexpected types, negative values, and underpayment. |
| Fixed application, 10 Hypothesis tests | 10 passed. |

The fixed application was also run interactively with `5,10,25`, `B7`, and `200/150`; it printed `[5, 10, 25]`, `(1, 6)`, and `10 five-coins`.

The pytest environment emitted 13 deprecation warnings from an installed third-party LangSmith plugin; they did not affect the test results.

Execution transcripts are preserved in `evidence/`. They are plain text captured from actual command runs. They are not screenshots. Genuine terminal screenshots were not captured in this run, so this report does not represent text transcripts as screenshots.

## Observations

Hypothesis reduced failures to small examples such as `None`, an empty slot code, `B0`, a negative amount, and underpayment. These cases pointed to missing type, structure, and domain checks in the starter implementation. Testing valid inputs alongside invalid inputs confirmed that the existing valid output format was preserved.

## Conclusion

Property-based tests exposed defects across all three input parsers before any application changes were made. Adding explicit type, format, and range validation replaced accidental runtime errors and invalid results with consistent `TypeError` and `ValueError` behavior. The final 10-test suite passes, including generated valid values and targeted malformed cases.

