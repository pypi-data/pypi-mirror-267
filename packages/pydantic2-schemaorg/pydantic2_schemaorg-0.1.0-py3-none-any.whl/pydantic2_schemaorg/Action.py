from __future__ import annotations

from datetime import datetime
from datetime import time
from typing import TYPE_CHECKING

from pydantic.v1 import AnyUrl
from pydantic.v1 import Field

from pydantic2_schemaorg.Thing import Thing


class Action(Thing):
    """An action performed by a direct agent and indirect participants upon a direct object."
     "Optionally happens at a location with the help of an inanimate instrument. The execution"
     "of the action may produce a result. Specific action sub-type documentation specifies"
     "the exact expectation of each argument/role. See also [blog post](http://blog.schema.org/2014/04/announcing-schemaorg-actions.html)"
     "and [Actions overview document](http://schema.org/docs/actions.html).

    See: https://schema.org/Action
    Model depth: 2
    """

    type_: str = Field(default="Action", alias="@type", const=True)
    instrument: list[Thing | str] | Thing | str | None = Field(
        default=None,
        description="The object that helped the agent perform the action. E.g. John wrote a book with *a pen*.",
    )
    participant: None | (
        list[Organization | Person | str] | Organization | Person | str
    ) = Field(
        default=None,
        description="Other co-agents that participated in the action indirectly. E.g. John wrote a book with"
        "*Steve*.",
    )
    provider: None | (
        list[Organization | Person | str] | Organization | Person | str
    ) = Field(
        default=None,
        description="The service provider, service operator, or service performer; the goods producer."
        "Another party (a seller) may offer those services or goods on behalf of the provider."
        "A provider may also serve as the seller.",
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
    object: list[Thing | str] | Thing | str | None = Field(
        default=None,
        description="The object upon which the action is carried out, whose state is kept intact or changed."
        "Also known as the semantic roles patient, affected or undergoer (which change their"
        "state) or theme (which doesn't). E.g. John read *a book*.",
    )
    target: None | (
        list[AnyUrl | URL | EntryPoint | str] | AnyUrl | URL | EntryPoint | str
    ) = Field(
        default=None,
        description="Indicates a target EntryPoint, or url, for an Action.",
    )
    result: list[Thing | str] | Thing | str | None = Field(
        default=None,
        description="The result produced in the action. E.g. John wrote *a book*.",
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
    actionStatus: None | (
        list[ActionStatusType | str] | ActionStatusType | str
    ) = Field(
        default=None,
        description="Indicates the current disposition of the Action.",
    )
    agent: None | (
        list[Organization | Person | str] | Organization | Person | str
    ) = Field(
        default=None,
        description="The direct performer or driver of the action (animate or inanimate). E.g. *John* wrote"
        "a book.",
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
    error: list[Thing | str] | Thing | str | None = Field(
        default=None,
        description="For failed actions, more information on the cause of the failure.",
    )


if TYPE_CHECKING:
    from pydantic2_schemaorg.Thing import Thing
    from pydantic2_schemaorg.Organization import Organization
    from pydantic2_schemaorg.Person import Person
    from pydantic2_schemaorg.DateTime import DateTime
    from pydantic2_schemaorg.Time import Time
    from pydantic2_schemaorg.URL import URL
    from pydantic2_schemaorg.EntryPoint import EntryPoint
    from pydantic2_schemaorg.Text import Text
    from pydantic2_schemaorg.VirtualLocation import VirtualLocation
    from pydantic2_schemaorg.PostalAddress import PostalAddress
    from pydantic2_schemaorg.Place import Place
    from pydantic2_schemaorg.ActionStatusType import ActionStatusType
