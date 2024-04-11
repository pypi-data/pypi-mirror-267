"""
Wrapping strategies

Different Fortran types need different strategies for wrapping.
We capture these here.
"""
from __future__ import annotations

from fgen.fortran_parsing import FortranDataType
from fgen.wrapping_strategies.array_deferred_size import (
    WrappingStrategyArrayDeferredSize,
)
from fgen.wrapping_strategies.character import (
    WrappingStrategyCharacter,
)
from fgen.wrapping_strategies.character_deferred_size import (
    WrappingStrategyCharacterDeferredSize,
)
from fgen.wrapping_strategies.default import WrappingStrategyDefault
from fgen.wrapping_strategies.derived_type import (
    WrappingStrategyDerivedType,
)
from fgen.wrapping_strategies.enum import WrappingStrategyEnum
from fgen.wrapping_strategies.interface import WrappingStrategyLike
from fgen.wrapping_strategies.logical import (
    WrappingStrategyLogical,
)
from fgen.wrapping_strategies.passing_to_fortran_steps import (
    PassingToFortranSteps,
)


def get_wrapping_strategy(  # noqa: PLR0911
    fortran_data_type: FortranDataType,
) -> WrappingStrategyLike:
    """
    Get wrapping strategy for a given :obj:`FortranDataType`

    Parameters
    ----------
    fortran_data_type
        :obj:`FortranDataType` for which to get the wrapping strategy

    Returns
    -------
        Wrapping strategy object
    """
    if fortran_data_type.is_derived_type:
        return WrappingStrategyDerivedType()

    if fortran_data_type.is_array and fortran_data_type.has_deferred_size:
        return WrappingStrategyArrayDeferredSize()

    if fortran_data_type.is_character:
        if fortran_data_type.has_deferred_size:
            return WrappingStrategyCharacterDeferredSize()
        else:
            return WrappingStrategyCharacter()

    if fortran_data_type.is_logical:
        return WrappingStrategyLogical()

    if fortran_data_type.is_enum:
        return WrappingStrategyEnum()

    return WrappingStrategyDefault()


__all__ = [
    "PassingToFortranSteps",
    "WrappingStrategyArrayDeferredSize",
    "WrappingStrategyCharacter",
    "WrappingStrategyCharacterDeferredSize",
    "WrappingStrategyDefault",
    "WrappingStrategyDerivedType",
    "WrappingStrategyLike",
    "WrappingStrategyLogical",
    "get_wrapping_strategy",
]
