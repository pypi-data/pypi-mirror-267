from __future__ import annotations

from typing import TYPE_CHECKING

from pydantic.v1 import Field
from pydantic.v1 import StrictBool

from pydantic2_schemaorg.PublicationEvent import PublicationEvent


class BroadcastEvent(PublicationEvent):
    """An over the air or online broadcast event.

    See: https://schema.org/BroadcastEvent
    Model depth: 4
    """

    type_: str = Field(default="BroadcastEvent", alias="@type", const=True)
    videoFormat: list[str | Text] | str | Text | None = Field(
        default=None,
        description="The type of screening or video broadcast used (e.g. IMAX, 3D, SD, HD, etc.).",
    )
    broadcastOfEvent: list[Event | str] | Event | str | None = Field(
        default=None,
        description="The event being broadcast such as a sporting event or awards ceremony.",
    )
    isLiveBroadcast: None | (
        list[StrictBool | Boolean | str] | StrictBool | Boolean | str
    ) = Field(
        default=None,
        description="True if the broadcast is of a live event.",
    )
    subtitleLanguage: None | (
        list[str | Text | Language] | str | Text | Language
    ) = Field(
        default=None,
        description="Languages in which subtitles/captions are available, in [IETF BCP 47 standard format](http://tools.ietf.org/html/bcp47).",
    )


if TYPE_CHECKING:
    from pydantic2_schemaorg.Text import Text
    from pydantic2_schemaorg.Event import Event
    from pydantic2_schemaorg.Boolean import Boolean
    from pydantic2_schemaorg.Language import Language
