# Lab 6 — Code and Branch Coverage Analysis

**Student Name:** Akash Ramesh  
**SRN:** PES1UG24AM212  
**Lab:** 6 — Code and Branch Coverage Analysis

## 1. Objective

The objective of this lab was to analyze the test coverage of a Python vending machine application using pytest and coverage.py.

The lab involved writing additional test cases to achieve at least 90% code coverage and at least 90% branch coverage. The test cases were designed to exercise different application functions, decision conditions and possible execution paths.

## 2. Tools Used

| Tool | Purpose |
|---|---|
| Python | Programming language used for the vending machine application. |
| pytest | Framework used to execute automated test cases. |
| coverage.py | Tool used to measure statement and branch coverage. |

## 3. Application Overview

The vending machine application contains three main functions:

| Function | Description |
|---|---|
| `select_item()` | Checks whether the selected item exists, is in stock and has sufficient credit. |
| `make_change()` | Calculates the change to be returned using available coin denominations. |
| `purchase()` | Handles the purchase process, updates stock and returns the change. |

The application supports three products:

| Item | Price |
|---|---:|
| Cola | 150 |
| Chips | 100 |
| Candy | 75 |

Available coin denominations are 100, 50, 25, 10 and 5.

## 4. Code Coverage Test Cases

The first stage involved creating additional test cases to execute all statements in the vending machine application.

The following scenarios were tested:

| Test Case | Function | Expected Result |
|---|---|---|
| Invalid item selection | `select_item()` | Returns `invalid`. |
| Sold-out item | `select_item()` | Returns `sold_out`. |
| Insufficient credit | `select_item()` | Returns `insufficient`. |
| Valid item selection | `select_item()` | Returns `ok`. |
| Zero change | `make_change()` | Returns an empty list. |
| Multiple coin values | `make_change()` | Returns the correct coin combination. |
| Negative change | `make_change()` | Raises `ValueError`. |
| Unrepresentable change | `make_change()` | Returns `None`. |
| Invalid purchase | `purchase()` | Returns `invalid`. |
| Sold-out purchase | `purchase()` | Returns `sold_out`. |
| Insufficient purchase credit | `purchase()` | Returns `insufficient`. |
| Purchase without exact change | `purchase()` | Returns `no_exact_change`. |
| Successful purchase without change | `purchase()` | Dispenses item and decreases stock. |
| Successful purchase with change | `purchase()` | Dispenses item, decreases stock and returns change. |

### Code Coverage Execution

```bash
python -m coverage erase
python -m coverage run -m pytest CodeCoverageTest_30_vending_machine.py
python -m coverage report -m
```

### Code Coverage Results

| File | Statements | Missed | Coverage |
|---|---:|---:|---:|
| CodeCoverageTest_30_vending_machine.py | 37 | 0 | 100% |
| vending_machine.py | 30 | 0 | 100% |
| **TOTAL** | **67** | **0** | **100%** |

**Test execution result:** 14 tests passed.

All 67 measured statements were executed, with zero missed statements.

## 5. Branch Coverage Test Cases

The second stage involved measuring branch coverage by executing the application with branch tracking enabled.

The tests covered alternate decision outcomes, including:

- Valid and invalid item selections.
- Items that are in stock and sold out.
- Sufficient and insufficient credit.
- Negative and non-negative change amounts.
- Exact and unrepresentable change.
- Successful and unsuccessful purchases.
- Successful purchases with and without change.

### Branch Coverage Execution

```bash
python -m coverage erase
python -m coverage run --branch -m pytest BranchCoverageTest_30_vending_machine.py
python -m coverage report -m
```

### Branch Coverage Results

| File | Statements | Missed | Branches | Partial Branches | Coverage |
|---|---:|---:|---:|---:|---:|
| BranchCoverageTest_30_vending_machine.py | 35 | 0 | 0 | 0 | 100% |
| vending_machine.py | 30 | 0 | 18 | 0 | 100% |
| **TOTAL** | **65** | **0** | **18** | **0** | **100%** |

**Test execution result:** 14 tests passed.

All 18 measured application branches were exercised, with zero partial branches.

## 6. Difference Between Code Coverage and Branch Coverage

| Code Coverage | Branch Coverage |
|---|---|
| Measures whether executable statements have been executed. | Measures whether decision outcomes have been executed. |
| Identifies statements that were never reached during testing. | Identifies decision branches that were not fully exercised. |
| Does not necessarily prove that all conditional outcomes were tested. | Provides additional information about conditional execution paths. |
| Achieved 100% in this lab. | Achieved 100% in this lab. |

## 7. Observations

1. The initial tests were expanded to cover invalid inputs, stock conditions, credit validation and purchase outcomes.
2. The `make_change()` function was tested with negative, zero, exact and unrepresentable amounts.
3. Successful purchase tests verified that stock was correctly reduced.
4. Branch coverage confirmed that all 18 measured application branches were exercised.
5. Both test stages achieved 100% coverage, exceeding the minimum requirement of 90%.

**Warnings:** The pytest execution displayed 13 DeprecationWarnings originating from the installed LangSmith package. These warnings did not cause test failures or reduce the reported coverage.

## 8. Conclusion

The vending machine application was successfully tested using pytest and coverage.py. The code coverage stage achieved 100% statement coverage, while the branch coverage stage achieved 100% coverage across all 18 measured application branches.

A total of 14 tests passed in each stage. The results exceeded the minimum 90% requirement and demonstrated how statement and branch coverage can be used together to evaluate the effectiveness of automated test cases.
