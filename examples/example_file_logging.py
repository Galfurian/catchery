import logging
import os

from catchery.error_handler import ErrorHandler, ErrorSeverity, log_error, log_info

# Define a log file path
LOG_FILE = "app_errors.log"

# Clean up the log file if it exists from a previous run
if os.path.exists(LOG_FILE):
    os.remove(LOG_FILE)

# Get the default handler, specifying a log file
# This will create a FileHandler for the logger used by the ErrorHandler
handler = ErrorHandler(text_log_path=LOG_FILE)

# Set its log level to DEBUG to capture all messages
handler.get_logger().setLevel(logging.DEBUG)

print(f"Logging errors to {LOG_FILE}\n")

# Log some messages using the handler and convenience functions
log_info("Application started.", context={"version": "1.0"})
log_error(
    "Failed to connect to external service.",
    context={
        "service": "payment_gateway",
        "attempt": 1,
        "error_code": "CONN_REFUSED",
    },
    exception=ConnectionRefusedError("Connection refused by remote host"),
)
log_info("Processing complete.")

# You can also use the handler directly
handler.handle(
    "A warning occurred during data validation.",
    severity=ErrorSeverity.MEDIUM,
    context={
        "data_id": "XYZ123",
        "validation_rule": "non_empty",
    },
)

print(f"Errors logged. Check the content of {LOG_FILE}\n")

# To ensure the file handler is flushed and closed, especially in short-lived scripts,
# you can explicitly call the shutdown method.
handler.shutdown()

# Read the content of the log file to verify
print(f"Content of {LOG_FILE}:\n")
with open(LOG_FILE, "r", encoding="utf-8") as f:
    print(f.read())

# Clean up the log file after demonstration
os.remove(LOG_FILE)
print(f"\nCleaned up {LOG_FILE}")
