from __future__ import annotations

from typing import TYPE_CHECKING

from pydantic.v1 import Field

from pydantic2_schemaorg.Thing import Thing


class StupidType(Thing):
    """A StupidType for testing.

    See: https://schema.org/StupidType
    Model depth: 2
    """

    type_: str = Field(default="StupidType", alias="@type", const=True)
    stupidProperty: None | (
        list[QuantitativeValue | str] | QuantitativeValue | str
    ) = Field(
        default=None,
        description="This is a StupidProperty! - for testing only.",
    )


if TYPE_CHECKING:
    from pydantic2_schemaorg.QuantitativeValue import QuantitativeValue
