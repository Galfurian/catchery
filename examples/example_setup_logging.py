import logging
import os

from catchery.error_handler import setup_catchery_logging, log_error, log_info

# Define log file paths
APP_LOG_FILE = "app_setup_visual.log"

# Clean up log files if they exist from a previous run
if os.path.exists(APP_LOG_FILE):
    os.remove(APP_LOG_FILE)

# Set up catchery logging using the new convenience function
handler = setup_catchery_logging(
    level=logging.DEBUG,
    text_log_path=APP_LOG_FILE,
    use_json_logging=True, # Example of using JSON formatting for the main logger
)

print(f"Logging visual errors to {APP_LOG_FILE}\n")

# Log some messages using the convenience functions
log_info("Application started via setup_catchery_logging.", context={"version": "1.1"})
log_error(
    "A critical error occurred during setup.",
    context={
        "module": "initialization",
        "error_code": 101,
    },
    exception=RuntimeError("Failed to load configuration"),
)
log_info("Application finished.")

print(f"Errors logged. Check the content of {APP_LOG_FILE}\n")

# To ensure the file handler is flushed and closed, especially in short-lived scripts,
# you can explicitly call the shutdown method.
handler.shutdown()

# Read the content of the visual log file to verify
print(f"Content of {APP_LOG_FILE}:\n")
with open(APP_LOG_FILE, "r", encoding="utf-8") as f:
    print(f.read())

# Clean up log files after demonstration
os.remove(APP_LOG_FILE)
print(f"\nCleaned up {APP_LOG_FILE}")
