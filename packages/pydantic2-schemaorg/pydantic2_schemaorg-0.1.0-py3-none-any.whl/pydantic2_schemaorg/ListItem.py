from __future__ import annotations

from typing import TYPE_CHECKING

from pydantic.v1 import Field

from pydantic2_schemaorg.Intangible import Intangible


class ListItem(Intangible):
    """An list item, e.g. a step in a checklist or how-to description.

    See: https://schema.org/ListItem
    Model depth: 3
    """

    type_: str = Field(default="ListItem", alias="@type", const=True)
    item: list[Thing | str] | Thing | str | None = Field(
        default=None,
        description="An entity represented by an entry in a list or data feed (e.g. an 'artist' in a list of 'artists').",
    )
    previousItem: None | (list[ListItem | str] | ListItem | str) = Field(
        default=None,
        description="A link to the ListItem that precedes the current one.",
    )
    position: None | (
        list[int | Integer | str | Text] | int | Integer | str | Text
    ) = Field(
        default=None,
        description="The position of an item in a series or sequence of items.",
    )
    nextItem: list[ListItem | str] | ListItem | str | None = Field(
        default=None,
        description="A link to the ListItem that follows the current one.",
    )


if TYPE_CHECKING:
    from pydantic2_schemaorg.Thing import Thing
    from pydantic2_schemaorg.Integer import Integer
    from pydantic2_schemaorg.Text import Text
