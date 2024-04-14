from __future__ import annotations

from typing import TYPE_CHECKING

from pydantic.v1 import Field
from pydantic.v1 import StrictFloat
from pydantic.v1 import StrictInt

from pydantic2_schemaorg.InformAction import InformAction


class RsvpAction(InformAction):
    """The act of notifying an event organizer as to whether you expect to attend the event.

    See: https://schema.org/RsvpAction
    Model depth: 6
    """

    type_: str = Field(default="RsvpAction", alias="@type", const=True)
    additionalNumberOfGuests: None | (
        list[StrictInt | StrictFloat | Number | str]
        | StrictInt
        | StrictFloat
        | Number
        | str
    ) = Field(
        default=None,
        description="If responding yes, the number of guests who will attend in addition to the invitee.",
    )
    rsvpResponse: None | (
        list[RsvpResponseType | str] | RsvpResponseType | str
    ) = Field(
        default=None,
        description="The response (yes, no, maybe) to the RSVP.",
    )
    comment: list[Comment | str] | Comment | str | None = Field(
        default=None,
        description="Comments, typically from users.",
    )


if TYPE_CHECKING:
    from pydantic2_schemaorg.Number import Number
    from pydantic2_schemaorg.RsvpResponseType import RsvpResponseType
    from pydantic2_schemaorg.Comment import Comment
