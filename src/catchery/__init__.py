"""
Catchery is a Python library for building robust and scalable applications.
"""

from .error_handler import (
    AppError,
    ErrorHandler,
    ErrorSeverity,
    log_critical,
    log_error,
    log_info,
    log_warning,
    safe_operation,
    set_default_handler,
    get_default_handler,
)
from .validation import (
    validate_object,
    validate_type,
    ensure_object,
    ensure_string,
    ensure_non_negative_int,
    ensure_int_in_range,
    ensure_list_of_type,
    safe_get_attribute,
)

__all__ = [
    "AppError",
    "ErrorHandler",
    "ErrorSeverity",
    "log_info",
    "log_warning",
    "log_error",
    "log_critical",
    "safe_operation",
    "set_default_handler",
    "get_default_handler",
    # Validation functions.
    "validate_object",
    "validate_type",
    "ensure_object",
    "ensure_string",
    "ensure_non_negative_int",
    "ensure_int_in_range",
    "ensure_list_of_type",
    "safe_get_attribute",
]
