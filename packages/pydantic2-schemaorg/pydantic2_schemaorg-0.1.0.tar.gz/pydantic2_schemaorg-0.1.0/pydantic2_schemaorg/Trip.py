from __future__ import annotations

from datetime import datetime
from datetime import time
from typing import TYPE_CHECKING

from pydantic.v1 import Field

from pydantic2_schemaorg.Intangible import Intangible


class Trip(Intangible):
    """A trip or journey. An itinerary of visits to one or more places.

    See: https://schema.org/Trip
    Model depth: 3
    """

    type_: str = Field(default="Trip", alias="@type", const=True)
    departureTime: None | (
        list[datetime | DateTime | time | Time | str]
        | datetime
        | DateTime
        | time
        | Time
        | str
    ) = Field(
        default=None,
        description="The expected departure time.",
    )
    tripOrigin: list[Place | str] | Place | str | None = Field(
        default=None,
        description="The location of origin of the trip, prior to any destination(s).",
    )
    offers: None | (list[Offer | Demand | str] | Offer | Demand | str) = Field(
        default=None,
        description="An offer to provide this item&#x2014;for example, an offer to sell a product, rent the"
        "DVD of a movie, perform a service, or give away tickets to an event. Use [[businessFunction]]"
        "to indicate the kind of transaction offered, i.e. sell, lease, etc. This property can"
        "also be used to describe a [[Demand]]. While this property is listed as expected on a number"
        "of common types, it can be used in others. In that case, using a second type, such as Product"
        "or a subtype of Product, can clarify the nature of the offer.",
    )
    itinerary: None | (list[ItemList | Place | str] | ItemList | Place | str) = Field(
        default=None,
        description="Destination(s) ( [[Place]] ) that make up a trip. For a trip where destination order is"
        "important use [[ItemList]] to specify that order (see examples).",
    )
    provider: None | (
        list[Organization | Person | str] | Organization | Person | str
    ) = Field(
        default=None,
        description="The service provider, service operator, or service performer; the goods producer."
        "Another party (a seller) may offer those services or goods on behalf of the provider."
        "A provider may also serve as the seller.",
    )
    arrivalTime: None | (
        list[datetime | DateTime | time | Time | str]
        | datetime
        | DateTime
        | time
        | Time
        | str
    ) = Field(
        default=None,
        description="The expected arrival time.",
    )
    partOfTrip: list[Trip | str] | Trip | str | None = Field(
        default=None,
        description="Identifies that this [[Trip]] is a subTrip of another Trip. For example Day 1, Day 2, etc."
        "of a multi-day trip.",
    )
    subTrip: list[Trip | str] | Trip | str | None = Field(
        default=None,
        description="Identifies a [[Trip]] that is a subTrip of this Trip. For example Day 1, Day 2, etc. of a"
        "multi-day trip.",
    )


if TYPE_CHECKING:
    from pydantic2_schemaorg.DateTime import DateTime
    from pydantic2_schemaorg.Time import Time
    from pydantic2_schemaorg.Place import Place
    from pydantic2_schemaorg.Offer import Offer
    from pydantic2_schemaorg.Demand import Demand
    from pydantic2_schemaorg.ItemList import ItemList
    from pydantic2_schemaorg.Organization import Organization
    from pydantic2_schemaorg.Person import Person
