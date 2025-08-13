import logging
import traceback

from catchery.error_handler import get_default_handler, log_critical

# Get the default handler.
handler = get_default_handler()

# Set its log level to DEBUG.
handler.get_logger().setLevel(logging.DEBUG)

# This is how exception chaining works.
try:
    try:
        log_critical(
            "Database connection lost!",
            context={"db_host": "localhost"},
            exception=ConnectionError("No DB connection"),
            raise_exception=True,
        )
    except ConnectionError as chained:
        log_critical(
            "We failed to connect to the database.",
            exception=RuntimeError("Failed to connect"),
            raise_exception=True,
            chain_exception=chained,
        )
except RuntimeError as e:
    print(f"Caught exception: {e}")
    traceback.print_exc()
