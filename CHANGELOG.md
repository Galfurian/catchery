# Changelog

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