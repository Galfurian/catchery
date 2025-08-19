import logging
import os
import json

from catchery.error_handler import ErrorHandler, ErrorSeverity, log_error, log_info

# Define log file paths
APP_LOG_FILE = "app_errors_visual.log"
JSON_LOG_FILE = "app_errors_structured.jsonl"

# Clean up log files if they exist from a previous run
if os.path.exists(APP_LOG_FILE):
    os.remove(APP_LOG_FILE)
if os.path.exists(JSON_LOG_FILE):
    os.remove(JSON_LOG_FILE)

# Get the default handler, specifying both a visual log file and a structured JSON log file
handler = ErrorHandler(
    text_log_path=APP_LOG_FILE,
    json_log_path=JSON_LOG_FILE,
)

# Set its log level to DEBUG to capture all messages
handler.get_logger().setLevel(logging.DEBUG)

print(f"Logging visual errors to {APP_LOG_FILE}")
print(f"Logging structured errors to {JSON_LOG_FILE}\n")

# Log some messages using the handler and convenience functions
log_info("Application started.", context={"version": "1.0", "env": "dev"})
log_error(
    "Failed to process user data.",
    context={
        "user_id": 123,
        "data_source": "api",
        "reason": "invalid_format",
    },
    exception=ValueError("Data format mismatch"),
)
log_info("Processing complete.")

# You can also use the handler directly
handler.handle(
    "A critical system component failed.",
    severity=ErrorSeverity.CRITICAL,
    context={
        "component": "database_service",
        "action": "startup",
        "error_code": 500,
    },
    exception=RuntimeError("DB connection pool exhausted"),
)

print(f"Errors logged. Check the content of {APP_LOG_FILE} and {JSON_LOG_FILE}\n")

# To ensure the file handlers are flushed and closed, especially in short-lived scripts,
# you can explicitly call the shutdown method.
handler.shutdown()

# Read the content of the visual log file to verify
print(f"Content of {APP_LOG_FILE}:\n")
with open(APP_LOG_FILE, "r", encoding="utf-8") as f:
    print(f.read())

# Read the content of the structured JSON log file to verify
print(f"Content of {JSON_LOG_FILE}:\n")
with open(JSON_LOG_FILE, "r", encoding="utf-8") as f:
    for line in f:
        try:
            print(json.dumps(json.loads(line), indent=2))
        except json.JSONDecodeError as e:
            print(f"Invalid JSON line: {line.strip()} - {e}")

# Clean up log files after demonstration
os.remove(APP_LOG_FILE)
os.remove(JSON_LOG_FILE)
print(f"\nCleaned up {APP_LOG_FILE} and {JSON_LOG_FILE}")
