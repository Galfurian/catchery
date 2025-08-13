from catchery.error_handler import get_default_handler, ErrorSeverity
import logging

# Get the default handler.
handler = get_default_handler()

# Set its log level to DEBUG.
handler.get_logger().setLevel(logging.DEBUG)


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
