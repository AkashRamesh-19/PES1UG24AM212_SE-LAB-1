# Lab 5 — Static Code Analysis Issue Log

**Student Name:** Akash Ramesh  
**SRN:** PES1UG24AM212  
**Lab:** 5 — Static Code Analysis

## 1. Objective

The objective of this lab was to analyze a Python electricity billing application using Pylint, Bandit and Flake8. These tools were used to identify code-quality issues, potential security vulnerabilities and coding-style violations. The identified issues were corrected, and the application was analyzed again to verify the improvements.

## 2. Tools Used

| Tool | Purpose |
|---|---|
| Pylint | Identifies programming errors, naming issues and code-quality problems. |
| Bandit | Detects common security vulnerabilities and unsafe coding practices. |
| Flake8 | Checks Python code for PEP 8 formatting and style violations. |

## 3. Static Code Analysis Issue Log

| Tool | Issue / Rule | Original Location | Description | Fix Applied |
|---|---|---|---|---|
| Pylint | Naming conventions | Functions such as `readMeters()`, `calculateUnits()` and `generateBill()` | Function and variable names did not follow the recommended Python snake_case convention. | Renamed functions and variables using snake_case, such as `read_meters()` and `generate_bill()`. |
| Bandit | Hard-coded password (B105 pattern) | `CLERK_PASSWORD` declaration | A password was directly stored in the source code, exposing sensitive information. | Removed the hard-coded password from the application. |
| Bandit | Shell command execution (B602 pattern) | Original `syncMeter()` function | The application used `os.system()` to execute a curl command constructed using string concatenation, creating a potential command-injection risk. | Removed the unused shell-based helper function and its associated import. |
| Bandit | Unsafe XML parsing (B314 pattern) | Original `readMeters()` function | The standard XML parser was used to process XML input that could potentially be untrusted. | Replaced the standard XML parser with `defusedxml.ElementTree`. |
| Python correctness | Mutable default argument | Original `generateBill()` function | The function used `extras={}` as a default argument, which could cause the same dictionary to be shared between function calls. | Changed the default to `None` and initialized a new dictionary inside the function. |
| Flake8 | Formatting and whitespace | Multiple locations | The original code contained inconsistent spacing, long statements and formatting violations. | Corrected spacing, indentation and line formatting, and wrapped long statements. |
| Pylint | Documentation and maintainability | Module and function definitions | Missing documentation made the code more difficult to understand and maintain. | Added module and function docstrings. |

*Note: The Bandit identifiers above indicate the standard rule patterns associated with the findings. Verify exact diagnostic codes and original line numbers against the before-analysis reports if required.*

## 4. Fixes and Improvements

The following improvements were made:

1. Converted function and variable names to snake_case.
2. Removed the hard-coded password.
3. Removed the unsafe shell command execution function.
4. Replaced the standard XML parser with `defusedxml`.
5. Corrected the mutable default dictionary argument.
6. Added documentation to the module and functions.
7. Improved spacing, indentation and line formatting.
8. Used explicit UTF-8 encoding when writing JSON output.

## 5. Before-and-After Analysis

| Tool | Before Analysis | After Analysis |
|---|---|---|
| Pylint | Multiple code-quality issues were reported. | Final Pylint rating improved to 10.00/10. |
| Bandit | Security-related findings were reported. | Identified security issues were addressed in the updated code. |
| Flake8 | Multiple formatting and style violations were reported. | The after-analysis report contained no remaining Flake8 issues. |

## 6. Conclusion

The electricity billing application was analyzed using Pylint, Bandit and Flake8. Multiple code-quality, security and formatting issues were identified and corrected. The final Pylint score reached 10.00/10, and the final Flake8 report contained no remaining issues. This lab demonstrated the importance of using static analysis tools to produce cleaner, safer and more maintainable Python applications.
