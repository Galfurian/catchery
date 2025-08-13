import logging

from catchery.error_handler import (
    ErrorSeverity,
    get_default_handler,
    log_critical,
    log_error,
    log_info,
    log_warning,
)

# Get the default handler.
handler = get_default_handler()

# Set its log level to DEBUG.
handler.get_logger().setLevel(logging.DEBUG)

# In this example we use directly the handler.
handler.handle("This is a low severity informational message.", ErrorSeverity.LOW)

print('\n')

# Here, instead, we use the convenience functions.
log_info("This is another info message using the convenience function.")

log_warning("A potential issue was detected.", context={"component": "auth"})

print()

# We can also provide a context.
log_error(
    "Failed to process user request.", context={"user_id": 123, "request_id": "abc"}
)

print()

# We can also provide an exception, but ask to not raise it.
log_critical(
    "Database connection lost!",
    context={"db_host": "localhost"},
    exception=ConnectionError("No DB connection"),
    raise_exception=False,
)

print()

# Or we can provide the exception, and catch it.
try:
    log_critical(
        "Database connection lost!",
        context={"db_host": "localhost"},
        exception=ConnectionError("No DB connection"),
        raise_exception=True,
    )
except ConnectionError as e:
    print(f"Caught exception: {e}")
