# Changelog

## 0.6.2 - 2025-08-20

### Features

- Added a mechanism to suppress validation warnings from `ensure` functions.

### Refactor

- Consolidated `_attempt_default_conversion` and `_attempt_conversion` into `_attempt_conversion_with_fallback`.
- Updated `ensure_object` to use the new conversion function.
- Improved `_attempt_conversion_with_fallback` to correctly handle tuple expected types.
- Updated `log_warning` calls in validation functions to include a flag for validation warnings.

## 0.6.1 - 2025-08-19

### Features

- Added `setup_catchery_logging` for simplified configuration.
- Implemented incremental JSON logging for structured `AppError` objects.

### Refactor

- Renamed `log_file_path` to `text_log_path` and `error_json_log_path` to `json_log_path` for clarity.
- Refactored error message construction in `re_raise_chained`.
- Ensured immutability of `AppError` context by deep copying it.
- Enhanced robustness of JSON logging by using a shared `_safe_json_serialize` utility.

### Documentation

- Revamped `README.md` with comprehensive documentation and refactored Quick Start examples.

## 0.5.0 - 2025-08-14

### Features

- Added `re_raise_chained` decorator for robust exception chaining.

## 0.4.0 - 2025-08-14

### Features

- Added `ensure_enum` function for robust Enum member validation and conversion.

## 0.3.0 - 2025-08-14

### Refactor

- Improved context management and validation logic in error handler and validation modules.
- Refactored validation and error handling, including renaming global handler functions and validation functions.
- Extracted `_get_type_display_name` for better type name formatting.
- Simplified the error handler and introduced a single default converter.
- Improved type hinting and validation logic across the core.

### Fixed

- Resolved TypeError and E501 linting issues in the error handler.

## 0.0.2 - 2025-08-12

### Fixed

- Resolved TypeError in `_create_app_error` by ensuring `_get_thread_context` always returns a dictionary.
- Enhanced `ensure_list_of_type` to correctly handle non-list inputs, logging a warning and returning a default empty list.
- Updated test assertions in `test_validation.py` to match the revised log messages.
- Resolved all E501 (line too long) linting errors in `src/catchery/validation.py` by reformatting long lines.

## 0.0.1 - Initial Release

- Initial project setup.
- Core error handling and validation utilities.
