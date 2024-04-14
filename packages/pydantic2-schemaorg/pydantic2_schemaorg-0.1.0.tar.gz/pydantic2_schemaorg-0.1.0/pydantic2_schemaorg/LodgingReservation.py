from __future__ import annotations

from datetime import datetime
from datetime import time
from typing import TYPE_CHECKING

from pydantic.v1 import Field

from pydantic2_schemaorg.Reservation import Reservation


class LodgingReservation(Reservation):
    """A reservation for lodging at a hotel, motel, inn, etc. Note: This type is for information"
     "about actual reservations, e.g. in confirmation emails or HTML pages with individual"
     "confirmations of reservations.

    See: https://schema.org/LodgingReservation
    Model depth: 4
    """

    type_: str = Field(default="LodgingReservation", alias="@type", const=True)
    checkinTime: None | (
        list[datetime | DateTime | time | Time | str]
        | datetime
        | DateTime
        | time
        | Time
        | str
    ) = Field(
        default=None,
        description="The earliest someone may check into a lodging establishment.",
    )
    checkoutTime: None | (
        list[datetime | DateTime | time | Time | str]
        | datetime
        | DateTime
        | time
        | Time
        | str
    ) = Field(
        default=None,
        description="The latest someone may check out of a lodging establishment.",
    )
    numChildren: None | (
        list[int | Integer | QuantitativeValue | str]
        | int
        | Integer
        | QuantitativeValue
        | str
    ) = Field(
        default=None,
        description="The number of children staying in the unit.",
    )
    numAdults: None | (
        list[int | Integer | QuantitativeValue | str]
        | int
        | Integer
        | QuantitativeValue
        | str
    ) = Field(
        default=None,
        description="The number of adults staying in the unit.",
    )
    lodgingUnitDescription: None | (list[str | Text] | str | Text) = Field(
        default=None,
        description="A full description of the lodging unit.",
    )
    lodgingUnitType: None | (
        list[str | Text | QualitativeValue] | str | Text | QualitativeValue
    ) = Field(
        default=None,
        description="Textual description of the unit type (including suite vs. room, size of bed, etc.).",
    )


if TYPE_CHECKING:
    from pydantic2_schemaorg.DateTime import DateTime
    from pydantic2_schemaorg.Time import Time
    from pydantic2_schemaorg.Integer import Integer
    from pydantic2_schemaorg.QuantitativeValue import QuantitativeValue
    from pydantic2_schemaorg.Text import Text
    from pydantic2_schemaorg.QualitativeValue import QualitativeValue
