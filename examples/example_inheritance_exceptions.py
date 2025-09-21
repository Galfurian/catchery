import logging

from catchery.error_handler import (
    get_default_handler,
    log_error,
    log_info,
    re_raise_chained,
    ErrorSeverity,
)

# Get the default handler.
handler = get_default_handler()

# Set its log level to DEBUG.
handler.get_logger().setLevel(logging.DEBUG)


class Grandparent:
    def __init__(self, value: int):
        if value < 0:
            raise ValueError("Grandparent: Value cannot be negative.")
        self.grandparent_value = value
        log_info(f"Grandparent initialized with value: {self.grandparent_value}")


class Parent(Grandparent):
    @re_raise_chained(
        new_exception_type=RuntimeError,
        message="Parent: Failed to initialize grandparent.",
        severity=ErrorSeverity.HIGH,
        context={"stage": "grandparent_init"},
    )
    def __init__(self, grandparent_value: int, value: int):
        super().__init__(grandparent_value)
        if value < 0:
            raise ValueError("Parent: Value cannot be negative.")
        self.parent_value = value
        log_info(f"Parent initialized with value: {self.parent_value}")


class Child(Parent):
    @re_raise_chained(
        new_exception_type=RuntimeError,
        message="Child: Failed to initialize parent.",
        severity=ErrorSeverity.HIGH,
        context={"stage": "parent_init"},
    )
    def __init__(self, grandparent_value: int, parent_value: int, child_value: str):
        super().__init__(grandparent_value, parent_value)
        if not child_value:
            raise ValueError("Child: Child value cannot be empty.")
        self.child_value = child_value
        log_info(f"Child initialized with value: {self.child_value}")


# =============================================================================
# VALID INITIALIZATIONS
# =============================================================================

print("--- Attempting valid initializations ---\n")

try:
    instance = Grandparent(10)
    print(
        f"Successfully created Grandparent instance with value: "
        f"{instance.grandparent_value}"
    )
except Exception as e:
    print(f"Failed to create Grandparent instance: {e}")

print()

try:
    instance = Parent(10, 7)
    print(
        f"Successfully created Parent instance with values: "
        f"{instance.grandparent_value}, "
        f"{instance.parent_value}"
    )
except Exception as e:
    print(f"Failed to create Parent instance: {e}")

print()

try:
    instance = Child(5, 7, "child_abc")
    print(
        f"Successfully created Child instance with values: "
        f"{instance.grandparent_value}, "
        f"{instance.parent_value}, "
        f"{instance.child_value}"
    )
except Exception as e:
    print(f"Failed to create Child instance: {e}")

# =============================================================================
# INVALID INITIALIZATIONS
# =============================================================================

print("\n--- Attempting invalid initializations ---\n")

try:
    instance = Grandparent(-1)
    print(
        f"Successfully created Grandparent instance (should have failed): "
        f"{instance.grandparent_value}"
    )
except Exception as e:
    print(f"Failed to create Grandparent instance as expected: {e}")

print()

try:
    instance = Parent(1, -1)
    print(
        f"Successfully created Parent instance (should have failed): "
        f"{instance.grandparent_value}, "
        f"{instance.parent_value}"
    )
except Exception as e:
    print(f"Failed to create Parent instance as expected: {e}")

print()

try:
    instance = Child(-1, 1, "child_xyz")
    print(
        f"Successfully created Child instance (grandparent init should have failed): "
        f"{instance.grandparent_value}, "
        f"{instance.parent_value}, "
        f"{instance.child_value}"
    )
except Exception as e:
    print(f"Failed to create Child instance as expected (grandparent init): {e}")

print()

try:
    instance = Child(1, -1, "child_xyz")
    print(
        f"Successfully created Child instance (parent init should have failed): "
        f"{instance.grandparent_value}, "
        f"{instance.parent_value}, "
        f"{instance.child_value}"
    )
except Exception as e:
    print(f"Failed to create Child instance as expected (parent init): {e}")
