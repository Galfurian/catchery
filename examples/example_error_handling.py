from catchery.error_handler import (
    get_default_handler,
    ErrorSeverity,
    log_info,
    log_warning,
    log_error,
    log_critical,
)
from logging import Formatter

handler = get_default_handler()

# --- Example 1: Basic Error Handling ---
print("--- Example 1: Basic Error Handling ---")
handler.handle(
    "This is a low severity informational message.", severity=ErrorSeverity.LOW
)
log_info("This is another info message using the convenience function.")
log_warning("A potential issue was detected.", context={"component": "auth"})
log_error(
    "Failed to process user request.", context={"user_id": 123, "request_id": "abc"}
)
log_critical(
    "Database connection lost!",
    context={"db_host": "localhost"},
    exception=ConnectionError("No DB connection"),
)

# --- Example 2: Using Context Manager ---
print("\n--- Example 2: Using Context Manager ---")
with handler.Context(session_id="xyz789", user_role="admin"):
    log_error("Admin action failed due to permission denied.")
    log_warning("Configuration file missing.", context={"file": "config.ini"})

# --- Example 3: Capturing Errors for Testing/Inspection ---
print("\n--- Example 3: Capturing Errors ---")
with handler.CaptureErrors(handler) as captured_errors:
    log_error("Error during batch processing.", context={"batch_id": "B1"})
    log_warning("Invalid input received.", context={"input_data": "bad_data"})
    log_info(
        "Operation completed successfully."
    )  # This will also be captured if AppError is used for all severities

print(f"Captured {len(captured_errors)} errors:")
for err in captured_errors:
    print(
        f"  - Message: {err.message}, Severity: {err.severity.value}, Context: {err.context}"
    )

# --- Example 4: Safe Execution with Default Value ---
print("\n--- Example 4: Safe Execution ---")


def risky_operation(should_fail: bool):
    if should_fail:
        raise ValueError("Something went wrong in risky_operation!")
    return "Operation successful!"


result_success = handler.safe_execute(
    lambda: risky_operation(False),
    default="Fallback value",
    error_message="Risky operation failed (expected success)",
    severity=ErrorSeverity.HIGH,
)
print(f"Result of successful operation: {result_success}")

result_failure = handler.safe_execute(
    lambda: risky_operation(True),
    default="Fallback value",
    error_message="Risky operation failed (expected failure)",
    severity=ErrorSeverity.HIGH,
)
print(f"Result of failed operation: {result_failure}")

# --- Example 5: Demonstrating Exception Chaining (handle method) ---
print("\n--- Example 5: Exception Chaining ---")
try:
    raise TypeError("Original type error")
except TypeError as e:
    handler.handle(
        "An error occurred during data processing.",
        severity=ErrorSeverity.HIGH,
        exception=ValueError("Data format invalid"),
        raise_exception=True,
        chain_exception=e,
    )
except Exception as e:
    print(f"Caught re-raised exception: {e}")
    if e.__cause__:
        print(f"  Caused by: {e.__cause__}")
    else:
        print("  No cause found.")
