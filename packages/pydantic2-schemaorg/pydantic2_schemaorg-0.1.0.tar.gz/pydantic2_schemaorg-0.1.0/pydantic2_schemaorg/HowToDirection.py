from __future__ import annotations

from typing import TYPE_CHECKING

from pydantic.v1 import AnyUrl
from pydantic.v1 import Field

from pydantic2_schemaorg.CreativeWork import CreativeWork
from pydantic2_schemaorg.ListItem import ListItem


class HowToDirection(ListItem, CreativeWork):
    """A direction indicating a single action to do in the instructions for how to achieve a result.

    See: https://schema.org/HowToDirection
    Model depth: 3
    """

    type_: str = Field(default="HowToDirection", alias="@type", const=True)
    supply: None | (list[str | Text | HowToSupply] | str | Text | HowToSupply) = Field(
        default=None,
        description="A sub-property of instrument. A supply consumed when performing instructions or a direction.",
    )
    duringMedia: None | (
        list[AnyUrl | URL | MediaObject | str] | AnyUrl | URL | MediaObject | str
    ) = Field(
        default=None,
        description="A media object representing the circumstances while performing this direction.",
    )
    totalTime: list[Duration | str] | Duration | str | None = Field(
        default=None,
        description="The total time required to perform instructions or a direction (including time to prepare"
        "the supplies), in [ISO 8601 duration format](http://en.wikipedia.org/wiki/ISO_8601).",
    )
    afterMedia: None | (
        list[AnyUrl | URL | MediaObject | str] | AnyUrl | URL | MediaObject | str
    ) = Field(
        default=None,
        description="A media object representing the circumstances after performing this direction.",
    )
    tool: None | (list[str | Text | HowToTool] | str | Text | HowToTool) = Field(
        default=None,
        description="A sub property of instrument. An object used (but not consumed) when performing instructions"
        "or a direction.",
    )
    performTime: list[Duration | str] | Duration | str | None = Field(
        default=None,
        description="The length of time it takes to perform instructions or a direction (not including time"
        "to prepare the supplies), in [ISO 8601 duration format](http://en.wikipedia.org/wiki/ISO_8601).",
    )
    beforeMedia: None | (
        list[AnyUrl | URL | MediaObject | str] | AnyUrl | URL | MediaObject | str
    ) = Field(
        default=None,
        description="A media object representing the circumstances before performing this direction.",
    )
    prepTime: list[Duration | str] | Duration | str | None = Field(
        default=None,
        description="The length of time it takes to prepare the items to be used in instructions or a direction,"
        "in [ISO 8601 duration format](http://en.wikipedia.org/wiki/ISO_8601).",
    )


if TYPE_CHECKING:
    from pydantic2_schemaorg.Text import Text
    from pydantic2_schemaorg.HowToSupply import HowToSupply
    from pydantic2_schemaorg.URL import URL
    from pydantic2_schemaorg.MediaObject import MediaObject
    from pydantic2_schemaorg.Duration import Duration
    from pydantic2_schemaorg.HowToTool import HowToTool
