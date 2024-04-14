from __future__ import annotations

from datetime import date
from datetime import datetime
from typing import TYPE_CHECKING

from pydantic.v1 import AnyUrl
from pydantic.v1 import Field

from pydantic2_schemaorg.UserInteraction import UserInteraction


class UserComments(UserInteraction):
    """UserInteraction and its subtypes is an old way of talking about users interacting with"
     "pages. It is generally better to use [[Action]]-based vocabulary, alongside types"
     "such as [[Comment]].

    See: https://schema.org/UserComments
    Model depth: 4
    """

    type_: str = Field(default="UserComments", alias="@type", const=True)
    commentTime: None | (
        list[datetime | DateTime | date | Date | str]
        | datetime
        | DateTime
        | date
        | Date
        | str
    ) = Field(
        default=None,
        description="The time at which the UserComment was made.",
    )
    replyToUrl: None | (list[AnyUrl | URL | str] | AnyUrl | URL | str) = Field(
        default=None,
        description="The URL at which a reply may be posted to the specified UserComment.",
    )
    commentText: list[str | Text] | str | Text | None = Field(
        default=None,
        description="The text of the UserComment.",
    )
    creator: None | (
        list[Organization | Person | str] | Organization | Person | str
    ) = Field(
        default=None,
        description="The creator/author of this CreativeWork. This is the same as the Author property for"
        "CreativeWork.",
    )
    discusses: None | (list[CreativeWork | str] | CreativeWork | str) = Field(
        default=None,
        description="Specifies the CreativeWork associated with the UserComment.",
    )


if TYPE_CHECKING:
    from pydantic2_schemaorg.DateTime import DateTime
    from pydantic2_schemaorg.Date import Date
    from pydantic2_schemaorg.URL import URL
    from pydantic2_schemaorg.Text import Text
    from pydantic2_schemaorg.Organization import Organization
    from pydantic2_schemaorg.Person import Person
    from pydantic2_schemaorg.CreativeWork import CreativeWork
