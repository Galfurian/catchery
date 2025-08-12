# Changelog

## 0.0.2 - 2025-08-12

### Fixed

- Resolved TypeError in `_create_app_error` by ensuring `_get_thread_context` always returns a dictionary.
- Enhanced `ensure_list_of_type` to correctly handle non-list inputs, logging a warning and returning a default empty list.
- Updated test assertions in `test_validation.py` to match the revised log messages.
- Resolved all E501 (line too long) linting errors in `src/catchery/validation.py` by reformatting long lines.

## 0.0.1 - Initial Release

- Initial project setup.
- Core error handling and validation utilities.
