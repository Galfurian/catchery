import logging

from catchery.error_handler import (
    get_default_handler,
    log_error,
    log_info,
    re_raise_chained,
    ErrorSeverity,
    ChainedReRaiseError,  # Import ChainedReRaiseError
)

# Get the default handler.
handler = get_default_handler()

# Set its log level to DEBUG.
handler.get_logger().setLevel(logging.DEBUG)


class Grandparent:
    @re_raise_chained(
        message="Grandparent: Failed to initialize.",  # message is now first
        severity=ErrorSeverity.HIGH,
        context=lambda self, value: {
            "gp_value": value,
        },
    )
    def func_gp(self, value: int) -> "Grandparent":
        if value < 0:
            raise ValueError("Grandparent: Value cannot be negative.")
        self.gp_value = value
        log_info(f"Grandparent initialized with value: {self.gp_value}")
        return self


class Parent(Grandparent):

    @re_raise_chained(
        message="Parent: Failed to initialize.",  # message is now first
        severity=ErrorSeverity.HIGH,
        context=lambda self, gp_value, value: {
            "gp_value": gp_value,
            "p_value": value,
        },
    )
    def func_p(self, gp_value: int, value: int) -> "Parent":
        super().func_gp(gp_value)
        if value < 0:
            raise ValueError("Parent: Value cannot be negative.")
        self.p_value = value
        log_info(f"Parent initialized with value: {self.p_value}")
        return self


class Child(Parent):
    @re_raise_chained(
        message="Child: Failed to initialize.",  # message is now first
        severity=ErrorSeverity.HIGH,
        context=lambda self, gp_value, p_value, c_value: {
            "gp_value": gp_value,
            "p_value": p_value,
            "c_value": c_value,
        },
    )
    def func_c(self, gp_value: int, p_value: int, c_value: str) -> "Child":
        super().func_p(gp_value, p_value)
        if not c_value:
            raise ValueError("Child: Child value cannot be empty.")
        self.c_value = c_value
        log_info(f"Child initialized with value: {self.c_value}")
        return self


# =============================================================================
# VALID INITIALIZATIONS
# =============================================================================

print("--- Attempting valid initializations ---\n")

try:
    instance = Grandparent().func_gp(10)
    print(
        f"Successfully created Grandparent instance with value: " f"{instance.gp_value}"
    )
except Exception as e:
    print(f"Failed to create Grandparent instance: {e}")

print()

try:
    instance = Parent().func_p(10, 7)
    print(
        f"Successfully created Parent instance with values: "
        f"{instance.gp_value}, "
        f"{instance.p_value}"
    )
except Exception as e:
    print(f"Failed to create Parent instance: {e}")

print()

try:
    instance = Child().func_c(10, 5, "c_value")
    print(
        f"Successfully created Child instance with values: "
        f"{instance.gp_value}, "
        f"{instance.p_value}, "
        f"{instance.c_value}"
    )
except Exception as e:
    print(f"Failed to create Child instance: {e}")

# =============================================================================
# INVALID INITIALIZATIONS
# =============================================================================

print("\n--- Attempting invalid initializations ---\n")

try:
    instance = Child().func_c(-1, 1, "child")
    print(
        f"Successfully created Child instance (grandparent init should have failed): "
        f"{instance.gp_value}, "
        f"{instance.p_value}, "
        f"{instance.c_value}"
    )
except Exception as e:
    print(f"Failed to create Child instance as expected (grandparent init): {e}")

print()

try:
    instance = Child().func_c(1, -1, "child_xyz")
    print(
        f"Successfully created Child instance (parent init should have failed): "
        f"{instance.gp_value}, "
        f"{instance.p_value}, "
        f"{instance.c_value}"
    )
except Exception as e:
    print(f"Failed to create Child instance as expected (parent init): {e}")

print()

try:
    instance = Child().func_c(0, 1, None)
    print(
        f"Successfully created Child instance (child init should have failed): "
        f"{instance.gp_value}, "
        f"{instance.p_value}, "
        f"{instance.c_value}"
    )
except Exception as e:
    print(f"Failed to create Child instance as expected (child init): {e}")
