from src.catchery.validation import ensure_value

# --- Example 1: Basic Type Checking ---
print("---" + "Example 1: Basic Type Checking ---")
# Value is correct type
result1 = ensure_value(10, "age", int)
print(f"age (int): {result1}")

# Value is incorrect type, no default, no conversion
result2 = ensure_value("hello", "count", int)
print(f"count (int, expected None): {result2}")

# --- Example 2: Using Default Values ---
print("\n" + "--- Example 2: Using Default Values ---")
# Value is incorrect type, with default
result3 = ensure_value("abc", "score", int, default=0)
print(f"score (int, default 0): {result3}")

# Value is None, not allowed, with default
result4 = ensure_value(None, "username", str, default="guest")
print(f"username (str, default 'guest'): {result4}")

# --- Example 3: Type Conversion ---
print("\n" + "--- Example 3: Type Conversion ---")
# String to int conversion
result5 = ensure_value("123", "id_str", int)
print(f"id_str (converted to int): {result5}")

# Float to int conversion
result6 = ensure_value(45.67, "temp_float", int)
print(f"temp_float (converted to int): {result6}")

# Int to string conversion
result7 = ensure_value(987, "code_int", str)
print(f"code_int (converted to str): {result7}")

# --- Example 4: Custom Validator ---
print("\n" + "--- Example 4: Custom Validator ---")
def is_positive(value):
    return value > 0

# Valid value
result8 = ensure_value(50, "positive_num", int, validator=is_positive)
print(f"positive_num (valid): {result8}")

# Invalid value, with default
result9 = ensure_value(-10, "positive_num_invalid", int, default=1, validator=is_positive)
print(f"positive_num_invalid (invalid, default 1): {result9}")

# --- Example 5: Allowing None ---
print("\n" + "--- Example 5: Allowing None ---")
# None value explicitly allowed
result10 = ensure_value(None, "optional_setting", bool, allow_none=True)
print(f"optional_setting (None allowed): {result10}")

# None value not allowed, but type hint includes None
result11 = ensure_value(None, "nullable_str", (str, type(None)), allow_none=True)
print(f"nullable_str (None allowed, type hint): {result11}")

# --- Example 6: Multiple Expected Types ---
print("\n" + "--- Example 6: Multiple Expected Types ---")
result12 = ensure_value(100, "numeric_value", (int, float))
print(f"numeric_value (int): {result12}")

result13 = ensure_value(100.5, "numeric_value_float", (int, float))
print(f"numeric_value_float (float): {result13}")

result14 = ensure_value("200", "numeric_value_str_to_int", (int, float))
print(f"numeric_value_str_to_int (str converted to int): {result14}")

# --- Example 7: Custom Converter ---
print("\n" + "--- Example 7: Custom Converter ---")
def to_double_int(value):
    return int(value * 2)

result15 = ensure_value(7.5, "double_int", int, converter=to_double_int)
print(f"double_int (custom converter): {result15}")

# --- Example 8: Combined Scenario (Conversion + Validation) ---
print("\n" + "--- Example 8: Combined Scenario ---")
def is_even(value):
    return value % 2 == 0

result16 = ensure_value("4", "even_number_str", int, validator=is_even)
print(f"even_number_str (converted and valid): {result16}")

result17 = ensure_value("5", "odd_number_str", int, default=0, validator=is_even)
print(f"odd_number_str (converted, invalid, default): {result17}")
