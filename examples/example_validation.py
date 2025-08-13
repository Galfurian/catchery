from catchery.error_handler import get_default_handler
from catchery.validation import ensure_object
import logging

# Get the default handler.
handler = get_default_handler()

# Set its log level to DEBUG.
handler.get_logger().setLevel(logging.DEBUG)

# --- Example 1: Basic Type Checking ---
print("\n" + "=" * 80 + "\n# Example 1: Basic Type Checking\n\n")

# Value is correct type
result1 = ensure_object(
    obj=10,
    name="age",
    expected_type=int,
)
print(f"age (int): {result1}\n")

# Value is incorrect type, no default, no conversion
result2 = ensure_object(
    obj="hello",
    name="count",
    expected_type=int,
    default=42,
)
print(f"count (int, default 42): {result2}\n")

# --- Example 2: Using Default Values ---
print("\n" + "=" * 80 + "\n# Example 2: Using Default Values\n\n")

# Value is incorrect type, with default
result3 = ensure_object(
    obj="abc",
    name="score",
    expected_type=int,
    default=0,
)
print(f"score (int, default 0): {result3}\n")

# Value is None, not allowed, with default
result4 = ensure_object(
    obj=None,
    name="username",
    expected_type=str,
    default="guest",
)
print(f"username (str, default 'guest'): {result4}\n")

# --- Example 3: Type Conversion ---
print("\n" + "=" * 80 + "\n# Example 3: Type Conversion\n\n")

# String to int conversion
result5 = ensure_object(
    obj="123",
    name="id_str",
    expected_type=int,
)
print(f"id_str (converted to int): {result5}\n")

# Float to int conversion
result6 = ensure_object(
    obj=45.67,
    name="temp_float",
    expected_type=int,
)
print(f"temp_float (converted to int): {result6}\n")

# Int to string conversion
result7 = ensure_object(
    obj=987,
    name="code_int",
    expected_type=str,
)
print(f"code_int (converted to str): {result7}\n")

# --- Example 4: Custom Validator ---
print("\n" + "=" * 80 + "\n# Example 4: Custom Validator\n\n")


def is_positive(value):
    return value > 0


# Valid value
result8 = ensure_object(
    obj=50,
    name="positive_num",
    expected_type=int,
    validator=is_positive,
)
print(f"positive_num (valid): {result8}\n")

# Invalid value, with default
result9 = ensure_object(
    obj=-10,
    name="positive_num_invalid",
    expected_type=int,
    default=1,
    validator=is_positive,
)
print(f"positive_num_invalid (invalid, default 1): {result9}\n")

# --- Example 5: Allowing None ---
print("\n" + "=" * 80 + "\n# Example 5: Allowing None\n\n")

# None value explicitly allowed
result10 = ensure_object(
    obj=None,
    name="optional_setting",
    expected_type=bool,
    allow_none=True,
)
print(f"optional_setting (None allowed): {result10}\n")

# None value not allowed, but type hint includes None
result11 = ensure_object(
    obj=None,
    name="nullable_str",
    expected_type=(str, type(None)),
    allow_none=True,
)
print(f"nullable_str (None allowed, type hint): {result11}\n")

# --- Example 6: Multiple Expected Types ---
print("\n" + "=" * 80 + "\n# Example 6: Multiple Expected Types\n\n")

result12 = ensure_object(
    obj=100,
    name="numeric_value",
    expected_type=(int, float),
)
print(f"numeric_value (int): {result12}\n")

result13 = ensure_object(
    obj=100.5,
    name="numeric_value_float",
    expected_type=(int, float),
)
print(f"numeric_value_float (float): {result13}\n")

result14 = ensure_object(
    obj="200",
    name="numeric_value_str_to_int",
    expected_type=(int, float),
)
print(f"numeric_value_str_to_int (str converted to int): {result14}\n")

# --- Example 7: Custom Converter ---
print("\n" + "=" * 80 + "\n# Example 7: Custom Converter\n\n")

result15 = ensure_object(
    obj=7.5,
    name="double_int",
    expected_type=int,
    converter=lambda value: int(value * 2),
)
print(f"double_int (custom converter): {result15}\n")

# --- Example 8: Combined Scenario (Conversion + Validation) ---
print("\n" + "=" * 80 + "\n# Example 8: Combined Scenario\n\n")


def is_even(value):
    return value % 2 == 0


result16 = ensure_object(
    obj="4",
    name="even_number_str",
    expected_type=int,
    validator=is_even,
)
print(f"even_number_str (converted and valid): {result16}\n")

result17 = ensure_object(
    obj="5",
    name="odd_number_str",
    expected_type=int,
    default=0,
    validator=is_even,
)
print(f"odd_number_str (converted, invalid, default to 0): {result17}\n")
