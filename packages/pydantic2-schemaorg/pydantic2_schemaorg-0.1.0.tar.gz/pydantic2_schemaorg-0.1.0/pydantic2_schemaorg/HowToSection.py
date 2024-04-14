from __future__ import annotations

from typing import TYPE_CHECKING

from pydantic.v1 import Field

from pydantic2_schemaorg.CreativeWork import CreativeWork
from pydantic2_schemaorg.ItemList import ItemList
from pydantic2_schemaorg.ListItem import ListItem


class HowToSection(ItemList, ListItem, CreativeWork):
    """A sub-grouping of steps in the instructions for how to achieve a result (e.g. steps for"
     "making a pie crust within a pie recipe).

    See: https://schema.org/HowToSection
    Model depth: 3
    """

    type_: str = Field(default="HowToSection", alias="@type", const=True)
    steps: None | (
        list[str | Text | CreativeWork | ItemList]
        | str
        | Text
        | CreativeWork
        | ItemList
    ) = Field(
        default=None,
        description="A single step item (as HowToStep, text, document, video, etc.) or a HowToSection (originally"
        "misnamed 'steps'; 'step' is preferred).",
    )


if TYPE_CHECKING:
    from pydantic2_schemaorg.Text import Text
    from pydantic2_schemaorg.CreativeWork import CreativeWork
    from pydantic2_schemaorg.ItemList import ItemList
