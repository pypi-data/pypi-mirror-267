from __future__ import annotations

from datetime import datetime
from datetime import time
from typing import TYPE_CHECKING

from pydantic.v1 import Field

from pydantic2_schemaorg.StructuredValue import StructuredValue


class InteractionCounter(StructuredValue):
    """A summary of how users have interacted with this CreativeWork. In most cases, authors"
     "will use a subtype to specify the specific type of interaction.

    See: https://schema.org/InteractionCounter
    Model depth: 4
    """

    type_: str = Field(default="InteractionCounter", alias="@type", const=True)
    userInteractionCount: None | (
        list[int | Integer | str] | int | Integer | str
    ) = Field(
        default=None,
        description="The number of interactions for the CreativeWork using the WebSite or SoftwareApplication.",
    )
    interactionService: None | (
        list[SoftwareApplication | WebSite | str] | SoftwareApplication | WebSite | str
    ) = Field(
        default=None,
        description="The WebSite or SoftwareApplication where the interactions took place.",
    )
    startTime: None | (
        list[datetime | DateTime | time | Time | str]
        | datetime
        | DateTime
        | time
        | Time
        | str
    ) = Field(
        default=None,
        description="The startTime of something. For a reserved event or service (e.g. FoodEstablishmentReservation),"
        "the time that it is expected to start. For actions that span a period of time, when the action"
        "was performed. E.g. John wrote a book from *January* to December. For media, including"
        "audio and video, it's the time offset of the start of a clip within a larger file. Note that"
        "Event uses startDate/endDate instead of startTime/endTime, even when describing"
        "dates with times. This situation may be clarified in future revisions.",
    )
    location: None | (
        list[str | Text | VirtualLocation | PostalAddress | Place]
        | str
        | Text
        | VirtualLocation
        | PostalAddress
        | Place
    ) = Field(
        default=None,
        description="The location of, for example, where an event is happening, where an organization is located,"
        "or where an action takes place.",
    )
    endTime: None | (
        list[datetime | DateTime | time | Time | str]
        | datetime
        | DateTime
        | time
        | Time
        | str
    ) = Field(
        default=None,
        description="The endTime of something. For a reserved event or service (e.g. FoodEstablishmentReservation),"
        "the time that it is expected to end. For actions that span a period of time, when the action"
        "was performed. E.g. John wrote a book from January to *December*. For media, including"
        "audio and video, it's the time offset of the end of a clip within a larger file. Note that"
        "Event uses startDate/endDate instead of startTime/endTime, even when describing"
        "dates with times. This situation may be clarified in future revisions.",
    )
    interactionType: list[Action | str] | Action | str | None = Field(
        default=None,
        description="The Action representing the type of interaction. For up votes, +1s, etc. use [[LikeAction]]."
        "For down votes use [[DislikeAction]]. Otherwise, use the most specific Action.",
    )


if TYPE_CHECKING:
    from pydantic2_schemaorg.Integer import Integer
    from pydantic2_schemaorg.SoftwareApplication import SoftwareApplication
    from pydantic2_schemaorg.WebSite import WebSite
    from pydantic2_schemaorg.DateTime import DateTime
    from pydantic2_schemaorg.Time import Time
    from pydantic2_schemaorg.Text import Text
    from pydantic2_schemaorg.VirtualLocation import VirtualLocation
    from pydantic2_schemaorg.PostalAddress import PostalAddress
    from pydantic2_schemaorg.Place import Place
    from pydantic2_schemaorg.Action import Action
