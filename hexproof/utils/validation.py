"""
* Utils: Validation
"""
from functools import lru_cache
from typing import Type, TypeVar

from pydantic import ConfigDict, BaseModel
from pydantic_core import ErrorDetails

# Generic types
M = TypeVar("M", bound=BaseModel)


def format_validation_error_report(errors: list[ErrorDetails], dedupe: bool = True) -> str:
    """Return a sorted list of formatted validation errors.

    Args:
        errors: The errors to format.
        dedupe: Whether or not to remove duplicate errors.

    Returns:
        A sorted list of formatted validation errors.
    """
    grouped: list[tuple[str, str]] = []
    seen: set[tuple[str, str, str]] = set()

    def _loc_to_dot_sep(loc: tuple[str | int, ...]) -> str:
        path = ''
        for i, x in enumerate(loc):
            if isinstance(x, str):
                if i > 0:
                    path += '.'
                path += x
            elif isinstance(x, int):
                path += '[]'
            else:
                raise TypeError('Unexpected type')
        return path

    # Check and format each error report
    for e in errors:
        _reason = e.get("type", "unknown_error")
        _path = _loc_to_dot_sep(e.get("loc", ()))
        _input_value = e.get("input", None)
        _input_type = type(_input_value).__name__
        # Check if we've already reported this field issue
        if dedupe:
            key = (_reason, _path, _input_type)
            if key in seen:
                continue
            seen.add(key)
        grouped.append((_path, f"{_path} / {_reason} / {_input_type} / {_input_value}"))

    # Return output
    return '\n'.join(v for k, v in sorted(sorted(grouped, key=lambda x: x[0]), key=lambda x: len(x[0])))


@lru_cache(maxsize=None)
def get_model_strict_fields(model: Type[M]) -> Type[M]:
    """Return a cached subclass of `model` that forbids extra fields.

    Args:
        model: The model to create a modified subclass of.

    Returns:
        The modified subclass model.
    """
    base_cfg = dict(getattr(model, "model_config", {}))
    base_cfg["extra"] = "forbid"
    strict_cfg = ConfigDict(**base_cfg)

    StrictModel = type(
        f"{model.__name__}ForbidExtra",
        (model,),
        {"model_config": strict_cfg})
    return StrictModel  # type: ignore[return-value]


def validate_model_data(model: Type[M], data: object, *, strict_fields: bool = True) -> M:
    """Validate a model against a dataset with optional changes to model configuration.

    Args:
        model: The model to validate.
        data: The data to validate.
        strict_fields: Whether or not to forbid extra fields present in the model data.

    Returns:
        A validated model instance.
    """
    cls = get_model_strict_fields(model) if strict_fields else model
    return cls.model_validate(data)
