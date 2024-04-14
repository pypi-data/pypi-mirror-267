from __future__ import annotations

from typing import TYPE_CHECKING

from pydantic.v1 import Field

from pydantic2_schemaorg.DefinedTermSet import DefinedTermSet


class CategoryCodeSet(DefinedTermSet):
    """A set of Category Code values.

    See: https://schema.org/CategoryCodeSet
    Model depth: 4
    """

    type_: str = Field(default="CategoryCodeSet", alias="@type", const=True)
    hasCategoryCode: None | (list[CategoryCode | str] | CategoryCode | str) = Field(
        default=None,
        description="A Category code contained in this code set.",
    )


if TYPE_CHECKING:
    from pydantic2_schemaorg.CategoryCode import CategoryCode
