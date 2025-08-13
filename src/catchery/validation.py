"""
This module contains support functions for validating data.
"""

import json
from typing import Any, Callable, Dict, Union

from .error_handler import get_default_handler, ErrorSeverity, log_warning

# =============================================================================
# SUPPORT FUNCTIONS
# =============================================================================


def _get_type_display_name(obj_or_type: Any) -> str:
    """
    Returns a human-readable name for a given object's type or a type itself.
    Handles cases where expected_type might be a tuple of types.

    Args:
        obj_or_type (Any): The object or type to get the display name for.

    Returns:
        str: The human-readable name of the type.
    """
    if isinstance(obj_or_type, type):
        return obj_or_type.__name__
    elif isinstance(obj_or_type, tuple):
        return f"({', '.join(_get_type_display_name(t) for t in obj_or_type)})"
    else:
        return type(obj_or_type).__name__


def _attempt_default_conversion(
    obj: Any,
    expected_type: Any,
    name: str,
    ctx: dict[str, Any],
) -> Any | None:
    """
    Attempts to perform a default conversion for common types (str, int, float).
    Logs a warning if conversion fails.

    Args:
        obj (Any): The object to convert.
        expected_type (Any): The expected type to convert to.
        name (str): The name of the object, used for logging.
        ctx (dict[str, Any]): The context for logging.

    Returns:
        Any | None: The converted object or None if conversion failed.
    """
    try:
        if expected_type is str and not isinstance(obj, str):
            return str(obj)
        elif expected_type is int and not isinstance(obj, int):
            return int(obj)
        elif expected_type is float and not isinstance(obj, float):
            return float(obj)
        elif expected_type is bool and not isinstance(obj, bool):
            return bool(obj)
    except (ValueError, TypeError) as e:
        log_warning(
            f"Default conversion of '{name}' "
            f"to {_get_type_display_name(expected_type)} "
            f"failed: {e}. Using default.",
            {**ctx, "error_details": str(e)},
        )
    return None


# =============================================================================
# VALIDATION FUNCTIONS
# =============================================================================


def validate_object(
    obj: Any,
    name: str,
    context: Dict[str, Any] | None = None,
    attributes: list[str] | None = None,
) -> Any:
    """
    Validates that an object exists and optionally has required
    attributes/methods.

    This function checks if the provided `obj` is not `None`. If `attributes` is
    provided, it further checks if the object possesses all specified
    attributes. If any validation fails, an error is logged, and a `ValueError`
    is raised.

    Args:
        obj: The object to validate. name: The human-readable name for the
        object, used in error messages. context: An optional dictionary of
        additional context for logging. attributes: An optional list of strings,
        where each string is the name of an attribute or method that `obj` must
        possess.

    Returns:
        The validated object if all checks pass.

    Raises:
        ValueError: If the object is `None` or is missing any of the
        `attributes`.
    """
    # Get the default handler.
    handler = get_default_handler()

    # Prepare an enriched context.
    ctx = {
        **(context or {}),
        "param_name": name,
        "object_attempted": obj,
    }

    # If the object is None, log an error.
    if obj is None:
        message = f"Required object '{name}' is None"
        handler.handle(
            error=message,
            severity=ErrorSeverity.HIGH,
            context={**ctx, "error_details": message},
            exception=Exception(message),
            raise_exception=True,
        )
        # We will not reach this line, due to the exception.

    ctx["actual_type"] = _get_type_display_name(type(obj))

    # If we have attributes to check, validate them.
    if attributes:

        # Gather missing attributes.
        missing_attrs: list[str] = []
        for attribute in attributes:
            if not hasattr(obj, attribute):
                missing_attrs.append(attribute)

        # If any attributes are missing, log an error.
        if missing_attrs:
            message = f"{name} missing required attributes: {missing_attrs}"
            handler.handle(
                error=message,
                severity=ErrorSeverity.HIGH,
                context={**ctx, "error_details": message},
                exception=Exception(message),
                raise_exception=True,
            )
            # We will not reach this line, due to the exception.

    # If we reach here, the object is valid.
    return obj


def validate_type(
    obj: Any,
    name: str,
    expected_type: type,
    context: dict[str, Any] | None = None,
) -> Any:
    """
    Validates that a object is of the specified type.

    If the validation fails, an error is logged and a ValueError is raised.

    Args:
        object: The object to validate. expected_type: The expected type (e.g.,
        str, int, list, etc.). name: The name of the parameter being validated,
        used in error messages. context: An optional dictionary of additional
        context for logging.

    Returns:
        The validated object if it is of the expected type.

    Raises:
        ValueError: If the object is not of the expected type.
    """
    # First, validate that the object is not None.
    validate_object(obj, name, context)

    # Then, check the type.
    if not isinstance(obj, expected_type):
        # Get the handler.
        handler = get_default_handler()

        # Get the typename of the received object.
        actual_type_name = _get_type_display_name(type(obj))

        # Get the typename of the expected type.
        expected_type_name = _get_type_display_name(expected_type)

        # Build the message.
        message = (
            f"Invalid {name}: expected {expected_type_name}, " f"got {actual_type_name}"
        )

        handler.handle(
            error=message,
            severity=ErrorSeverity.HIGH,
            context={
                **(context or {}),
                "param_name": name,
                "object_attempted": obj,
                "expected_type": expected_type_name,
                "actual_type": actual_type_name,
                "error_details": message,
            },
            exception=ValueError(message),
            raise_exception=True,
        )
        # We will not reach this line, due to the exception.

    # If we reach here, the object is valid.
    return obj


# =============================================================================
# CONVERSION FUNCTIONS
# =============================================================================


def ensure_object(
    obj: Any,
    name: str,
    expected_type: Union[Any, tuple[Any, ...]],
    default: Any | None = None,
    context: Dict[str, Any] | None = None,
    allow_none: bool = False,
    validator: Callable[[Any], bool] | None = None,
    converter: Callable[[Any], Any] | None = None,
) -> Any | None:
    """
    Ensures a object is of the specified type, converting or using a default if
    necessary.

    This function attempts to validate and/or convert the provided `object` to
    `expected_type`. If `object` is None and `allow_none` is False, it returns
    `default`. If `object` is not of `expected_type` and a `converter` is
    provided, it attempts conversion. If conversion fails or `object` is still
    not of `expected_type`, it returns `default`. If a `validator` is provided,
    the object (or converted object) must pass the validation. Warnings are logged
    for invalid values or failed conversions.

    Args:
        object: The object to be ensured. name: The human-readable name for the
        object, used in log messages. expected_type: The expected type(s) (e.g.,
        str, int, (int, float)). default: The default object to return if `object`
        is invalid or cannot be converted. context: An optional dictionary of
        additional context for logging. allow_none: If True, `None` is
        considered a valid object if it matches `expected_type`
                    or if `None` is explicitly in `expected_type`. If False,
                    `None` is treated as an invalid object unless `default` is
                    `None`.
        validator: An optional callable that takes the object and returns True if
        valid, False otherwise. converter: An optional callable that takes the
        object and attempts to convert it to `expected_type`.

    Returns:
        The validated and/or converted object, or the `default` object.
    """
    # Get the type name.
    actual_type_name = _get_type_display_name(type(obj))

    # Get the expected_type name.
    expected_type_name = _get_type_display_name(expected_type)

    # Make sure the context is valid.
    ctx: dict[str, Any] = {
        **(context or {}),
        "param_name": name,
        "object_attempted": obj,
        "actual_type": actual_type_name,
        "expected_type": expected_type_name,
    }

    # Store the object.
    processed_object = obj

    # Handle None object.
    if obj is None:
        if allow_none and (
            (isinstance(expected_type, tuple) and None in expected_type)
            or expected_type is type(None)
        ):
            return None
        log_warning(
            f"'{name}' is None and not allowed for expected type(s) "
            f"{expected_type_name}. Using default.",
            ctx,
        )
        return default

    # Attempt conversion if a converter is provided or for common types.
    if not isinstance(processed_object, expected_type):
        log_warning(
            f"'{name}' is not of expected type(s) {expected_type_name}. Attempting conversion.",
            ctx,
        )
        if converter:
            try:
                processed_object = converter(obj)
                if not isinstance(processed_object, expected_type):
                    log_warning(
                        f"Converter for '{name}' returned wrong type. "
                        f"Expected {expected_type_name}, "
                        f"got {_get_type_display_name(type(processed_object))}. "
                        f"Using default.",
                        ctx,
                    )
                    return default
            except Exception as e:
                log_warning(
                    f"Conversion of '{name}' failed: {e}. Using default.",
                    {**ctx, "error_details": str(e)},
                )
                return default
        elif isinstance(expected_type, tuple):
            # Try converting to one of the types in the tuple
            for t in expected_type:
                processed_object = _attempt_default_conversion(obj, t, name, ctx)
                if processed_object is not None:
                    break
            if processed_object is None:
                log_warning(
                    f"No converter provided and cannot perform default conversion "
                    f"for '{name}'. Using default.",
                    ctx,
                )
                return default
        else:
            # For single expected_type.
            processed_object = _attempt_default_conversion(
                obj, expected_type, name, ctx
            )
            if not processed_object:
                return default

    # Apply validator if provided
    if validator:
        try:
            if not validator(processed_object):
                log_warning(
                    f"'{name}' failed validation. Using default.",
                    ctx,
                )
                return default
        except Exception as e:
            log_warning(
                f"Validator for '{name}' raised an exception: {e}. Using default.",
                {**ctx, "error_details": str(e)},
            )
            return default

    return processed_object


def ensure_string(
    obj: Any,
    name: str,
    default: str = "",
    context: dict[str, Any] | None = None,
) -> str:
    """
    Ensures a object is a string, converting it if possible or using a default.

    This function attempts to convert the provided `object` to a string. If the
    `object` is not already a string, a warning is logged. If conversion is not
    possible (e.g., `object` is `None` and no default is provided), the specified
    `default` string is returned.

    Args:
        obj: The object to be ensured as a string. name: The name of the
        parameter being processed, used in log messages. default: The default
        string object to return if `object` cannot be converted or is `None`.
        Defaults to an empty string. context: An optional dictionary of
        additional context for logging.

    Returns:
        The `object` as a string, or the `default` string if conversion fails.
    """
    if not isinstance(obj, str):
        log_warning(
            f"{name} should be string, got: {_get_type_display_name(type(obj))}, converting",
            {
                **(context or {}),
                "param_name": name,
                "object_attempted": obj,
                "actual_type": _get_type_display_name(type(obj)),
                "expected_type": "str",
                "default_object_used": default,
            },
        )
        return str(obj) if obj is not None else default
    return obj


def ensure_non_negative_int(
    obj: Any,
    name: str,
    default: int = 0,
    context: dict[str, Any] | None = None,
) -> int:
    """
    Ensures a object is a non-negative integer, correcting it if necessary.

    This function attempts to convert the provided `object` to an integer and
    ensures it is not negative. If the `object` is not an integer, is negative,
    or cannot be converted, a warning is logged, and the specified `default`
    object is returned or the object is clamped to 0 if it's a negative number.

    Args:
        obj: The object to be ensured as a non-negative integer. name: The name
        of the parameter being processed, used in log messages. default: The
        default integer object to return if `object` is invalid. Defaults to 0.
        context: An optional dictionary of additional context for logging.

    Returns:
        The corrected non-negative integer object.
    """
    if not isinstance(obj, int) or obj < 0:
        log_warning(
            f"{name} must be non-negative integer, got: {obj}, "
            f"correcting to {default}",
            {
                **(context or {}),
                "param_name": name,
                "object_attempted": obj,
                "actual_type": _get_type_display_name(type(obj)),
                "expected_type": "int",
                "default_object_used": default,
            },
        )
        return max(0, int(obj) if isinstance(obj, (int, float)) else default)
    return obj


def ensure_int_in_range(
    obj: Any,
    name: str,
    min_val: int,
    max_val: int | None = None,
    default: int | None = None,
    context: dict[str, Any] | None = None,
) -> int:
    """
    Ensures a object is an integer within a specified range, correcting it if
    necessary.

    This function attempts to convert the provided `obj` to an integer and
    checks if it falls within the `min_val` and `max_val` (inclusive). If the
    `obj` is not an integer, is outside the range, or cannot be converted, a
    warning is logged, and the object is corrected to `min_val`, `max_val`, or
    the specified `default`.

    Args:
        obj: The object to be ensured as an integer within the range. name: The
        name of the parameter being processed, used in log messages. min_val:
        The minimum allowed integer object (inclusive). max_val: The maximum
        allowed integer object (inclusive). If `None`, there is no upper limit.
        default: The default integer object to return if `obj` is invalid or
        out of range. If `None`, `min_val` is used as the default. context: An
        optional dictionary of additional context for logging.

    Returns:
        The corrected integer object within the specified range.
    """
    if default is None:
        default = min_val

    if (
        not isinstance(obj, int)
        or obj < min_val
        or (max_val is not None and obj > max_val)
    ):
        range_desc = (
            f">= {min_val}" if max_val is None else f"between {min_val} and {max_val}"
        )
        log_warning(
            f"{name} must be integer {range_desc}, got: {obj}, "
            f"correcting to {default}",
            {
                **(context or {}),
                "param_name": name,
                "object_attempted": obj,
                "actual_type": _get_type_display_name(type(obj)),
                "expected_type": "int",
                "min_val": min_val,
                "max_val": max_val,
                "default_object_used": default,
            },
        )

        # Try to convert and clamp
        try:
            converted = int(obj) if isinstance(obj, (int, float)) else default
            if converted < min_val:
                return min_val
            elif max_val is not None and converted > max_val:
                return max_val
            else:
                return converted
        except (ValueError, TypeError):
            return default
    return obj


def ensure_list_of_type(
    values: list[Any] | None,
    name: str,
    expected_type: Union[Any, tuple[Any, ...]],
    default: list[Any] | None = None,
    context: Dict[str, Any] | None = None,
    allow_none: bool = False,
    validator: Callable[[Any], bool] | None = None,
    converter: Callable[[Any], Any] | None = None,
) -> list[Any]:
    """
    Ensures values is a list containing items of a specified type, correcting if
    needed.

    This function validates that `values` is a list. It then iterates through
    the list to ensure each item is of `expected_type`. Invalid items are either
    converted using a `converter` function, or a default conversion is attempted
    for common types (str, int, float). Items can also be validated with a
    `validator` function. Warnings are logged for invalid items, but execution
    continues with a cleaned list.

    Args:
        values: The list of values to validate, expected to be a list.
        name: The name of the parameter being processed, used in log messages.
        expected_type: The `type` that all items in the list should conform to.
        default: The default list to return if `values` is `None` or not a list.
            Defaults to an empty list.
        context: An optional dictionary of additional context for
            logging.
        allow_none: If `True`, `None` values are allowed in the list.
        validator: An optional callable that takes an item of `expected_type`
            and returns `True` if the item is valid, `False` otherwise.
        converter: An optional callable that takes an item and attempts to
            convert it to `expected_type`. If conversion fails or returns a
            wrong type, the item is skipped.

    Returns:
        A new list containing only the valid and/or converted items of
        `expected_type`.
    """
    if default is None:
        default = []

    if not isinstance(values, list):
        log_warning(
            f"{name} should be list, got: {_get_type_display_name(type(values))}, using default",
            {
                **(context or {}),
                "param_name": name,
                "object_attempted": values,
                "actual_type": _get_type_display_name(type(values)),
                "expected_type": "list",
                "default_object_used": default,
            },
        )
        return default

    # Make sure the context is valid.
    ctx: dict[str, Any] = {
        **(context or {}),
        "param_name": name,
        "object_attempted": values,
        "actual_type": _get_type_display_name(type(values)),
        "expected_type": _get_type_display_name(expected_type),
    }

    # Ensure all items are of the expected type
    cleaned_list: list[Any] = []

    for i, item in enumerate(values):
        if isinstance(item, expected_type):
            # Item is correct type, now validate if validator is provided
            if validator and not validator(item):
                log_warning(
                    f"{name}[{i}] failed validation, " f"skipping item: {item}",
                    {
                        **ctx,
                        "index": i,
                        "object_attempted": item,
                        "error_details": "Item failed validation",
                    },
                )
                # Skip invalid items
                continue
            else:
                cleaned_list.append(item)
        else:
            item_ctx: dict[str, Any] = {
                **ctx,
                "index": i,
                "object_attempted": item,
            }
            converted = ensure_object(
                obj=item,
                name=f"{name}[{i}]",
                expected_type=expected_type,
                default=None,
                context=item_ctx,
                allow_none=allow_none,
                converter=converter,
                validator=validator,
            )
            if converted is not None or allow_none:
                cleaned_list.append(converted)
            else:
                log_warning(
                    f"{name}[{i}] failed validation, " f"skipping item: {item}",
                    {
                        **ctx,
                        "index": i,
                        "object_attempted": item,
                        "error_details": "Item failed validation and could not be converted",
                    },
                )

    return cleaned_list


def safe_get_attribute(obj: Any, name: str, default: Any = None) -> Any:
    """
    Safely retrieves an attribute from an object, returning a default object if
    not found.

    This function attempts to get the attribute named `name` from `obj`. If
    `obj` is `None` or the attribute does not exist, a warning is logged, and
    the specified `default` object is returned instead.

    Args:
        obj: The object from which to retrieve the attribute. name: The name of
        the attribute to retrieve. default: The default object to return if the
        attribute is not found or `obj` is `None`. Defaults to `None`.

    Returns:
        The object of the attribute if found, otherwise the `default` object.
    """
    if obj is None:
        return default

    if hasattr(obj, name):
        return getattr(obj, name)
    else:
        log_warning(
            f"{_get_type_display_name(type(obj))} missing attribute '{name}', "
            f"using default: {default}",
            {
                "param_name": name,
                "object_attempted": obj,
                "actual_type": _get_type_display_name(type(obj)),
                "default_object_used": default,
                "error_details": f"Missing attribute '{name}'",
            },
        )
        return default
