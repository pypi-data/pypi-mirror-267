from __future__ import annotations

from datetime import date
from datetime import datetime
from datetime import time
from typing import TYPE_CHECKING

from pydantic.v1 import AnyUrl
from pydantic.v1 import Field
from pydantic.v1 import StrictBool

from pydantic2_schemaorg.Intangible import Intangible


class ActionAccessSpecification(Intangible):
    """A set of requirements that must be fulfilled in order to perform an Action.

    See: https://schema.org/ActionAccessSpecification
    Model depth: 3
    """

    type_: str = Field(default="ActionAccessSpecification", alias="@type", const=True)
    eligibleRegion: None | (
        list[str | Text | GeoShape | Place] | str | Text | GeoShape | Place
    ) = Field(
        default=None,
        description="The ISO 3166-1 (ISO 3166-1 alpha-2) or ISO 3166-2 code, the place, or the GeoShape for"
        "the geo-political region(s) for which the offer or delivery charge specification is"
        "valid. See also [[ineligibleRegion]].",
    )
    availabilityEnds: None | (
        list[datetime | DateTime | date | Date | time | Time | str]
        | datetime
        | DateTime
        | date
        | Date
        | time
        | Time
        | str
    ) = Field(
        default=None,
        description="The end of the availability of the product or service included in the offer.",
    )
    category: None | (
        list[
            (
                AnyUrl
                | URL
                | str
                | Text
                | CategoryCode
                | Thing
                | PhysicalActivityCategory
            )
        ]
        | AnyUrl
        | URL
        | str
        | Text
        | CategoryCode
        | Thing
        | PhysicalActivityCategory
    ) = Field(
        default=None,
        description="A category for the item. Greater signs or slashes can be used to informally indicate a"
        "category hierarchy.",
    )
    availabilityStarts: None | (
        list[datetime | DateTime | date | Date | time | Time | str]
        | datetime
        | DateTime
        | date
        | Date
        | time
        | Time
        | str
    ) = Field(
        default=None,
        description="The beginning of the availability of the product or service included in the offer.",
    )
    requiresSubscription: None | (
        list[StrictBool | Boolean | MediaSubscription | str]
        | StrictBool
        | Boolean
        | MediaSubscription
        | str
    ) = Field(
        default=None,
        description="Indicates if use of the media require a subscription (either paid or free). Allowed values"
        "are ```true``` or ```false``` (note that an earlier version had 'yes', 'no').",
    )
    ineligibleRegion: None | (
        list[str | Text | GeoShape | Place] | str | Text | GeoShape | Place
    ) = Field(
        default=None,
        description="The ISO 3166-1 (ISO 3166-1 alpha-2) or ISO 3166-2 code, the place, or the GeoShape for"
        "the geo-political region(s) for which the offer or delivery charge specification is"
        "not valid, e.g. a region where the transaction is not allowed. See also [[eligibleRegion]].",
    )
    expectsAcceptanceOf: None | (list[Offer | str] | Offer | str) = Field(
        default=None,
        description="An Offer which must be accepted before the user can perform the Action. For example, the"
        "user may need to buy a movie before being able to watch it.",
    )


if TYPE_CHECKING:
    from pydantic2_schemaorg.Text import Text
    from pydantic2_schemaorg.GeoShape import GeoShape
    from pydantic2_schemaorg.Place import Place
    from pydantic2_schemaorg.DateTime import DateTime
    from pydantic2_schemaorg.Date import Date
    from pydantic2_schemaorg.Time import Time
    from pydantic2_schemaorg.URL import URL
    from pydantic2_schemaorg.CategoryCode import CategoryCode
    from pydantic2_schemaorg.Thing import Thing
    from pydantic2_schemaorg.PhysicalActivityCategory import PhysicalActivityCategory
    from pydantic2_schemaorg.Boolean import Boolean
    from pydantic2_schemaorg.MediaSubscription import MediaSubscription
    from pydantic2_schemaorg.Offer import Offer
