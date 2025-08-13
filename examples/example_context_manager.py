from catchery.error_handler import (
    get_default_handler,
    log_warning,
    log_error,
)
import logging

# Get the default handler.
handler = get_default_handler()

# Set its log level to DEBUG.
handler.get_logger().setLevel(logging.DEBUG)

with handler.Context(session_id="xyz789", user_role="admin"):
    log_error("Admin action failed due to permission denied.")
    log_warning("Configuration file missing.", context={"file": "config.ini"})
