"""Utilities for using `pint`'s unit-wrapped quantities"""
import enum
import functools
import io
import numbers
import typing

import pint


@enum.unique
class EngineeringSystems(enum.Enum):
    """Engineering unit systems

    Enum values are `pint` system definitions specifying the unit overrides used
    in the system - for example, the `si_engineering` system overrides SI with
    the millimeter as the base unit of length.

    Enum names should be the same as the name given to the system in the definition
    (the enum value).
    """

    si_engineering = """
        @system si_engineering using SI
            millimeter
        @end
    """
    us_engineering = """
        @system us_engineering using US
            thou
        @end
    """

    @classmethod
    def system_names(cls) -> typing.List[str]:
        """Get the names of the defined systems"""
        return [element.name for element in list(cls)]


def get_registry(
    system: typing.Optional[EngineeringSystems] = None,
) -> pint.UnitRegistry:
    """Get a unit registry, with optional default unit system

    A part library module should not specify a unit system, and a model script
    should - this enables specific models to drive the choice of default unit
    systems.

    Args:
        system: The engineering system to use; if `None`, the existing default
            system will be used
    """
    found_registry = pint.get_application_registry()

    if system:
        found_registry.load_definitions(io.StringIO(system.value))
        found_registry.default_system = system.name

    return found_registry


def _to_base_magnitude(
    arg: typing.Union[pint.Quantity, typing.Any]
) -> typing.Union[numbers.Number, typing.Any]:
    """Convert a quantity to base units & get its magnitude

    Non-quantity args are returned unchanged
    """
    if isinstance(arg, pint.Quantity):
        return arg.to_base_units().magnitude
    return arg


def args_to_base_magnitude(func):
    """Convert any `Quantity` args or kwargs into magnitudes in base units

    This is intended to be used as follows:

        def part(workplane, dimension: pint.Quantity = default_value):
            return _part(workplane, dimension)

        @args_to_base_magnitude
        def _part(workplane, dimension: float):
            ...

    The decorator & the combination of a public & private function allows the
    part's interface to be defined with unit-wrapped quantities, and ensures
    that all parts used by a model (as long as they share the same unit
    registry - see `get_registry`) use the same units when actually constructing
    `cadquery` shapes.
    """

    @functools.wraps(func)
    def with_base_units(*args, **kwargs):
        return func(
            *(_to_base_magnitude(arg) for arg in args),
            **{
                kwarg_key: _to_base_magnitude(kwarg_value)
                for kwarg_key, kwarg_value in kwargs.items()
            }
        )

    return with_base_units
