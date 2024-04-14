from __future__ import annotations

from pydantic.v1 import Field

from pydantic2_schemaorg.CreativeWork import CreativeWork
from pydantic2_schemaorg.ItemList import ItemList
from pydantic2_schemaorg.ListItem import ListItem


class HowToStep(ItemList, ListItem, CreativeWork):
    """A step in the instructions for how to achieve a result. It is an ordered list with HowToDirection"
     "and/or HowToTip items.

    See: https://schema.org/HowToStep
    Model depth: 3
    """

    type_: str = Field(default="HowToStep", alias="@type", const=True)
