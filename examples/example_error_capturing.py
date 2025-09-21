import logging

from catchery.error_handler import (
    get_default_handler,
    log_error,
    log_info,
    log_warning,
)

# Get the default handler.
handler = get_default_handler()

# Set its log level to DEBUG.
handler.get_logger().setLevel(logging.DEBUG)


def function_that_logs() -> None:
    log_info("This is an informational message from a function.")


with handler.CaptureErrors(handler) as captured_errors:
    log_error("Error during batch processing.", context={"batch_id": "B1"})
    log_warning("Invalid input received.", context={"input_data": "bad_data"})
    function_that_logs()
    log_info("Operation completed successfully.")

print(f"Captured {len(captured_errors)} errors:")
for err in captured_errors:
    print(
        f"  - Message: {err.message}, "
        f"Severity: {err.severity.value}, "
        f"Context: {err.context}"
    )
