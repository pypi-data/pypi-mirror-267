from __future__ import annotations

from datetime import date
from datetime import datetime
from datetime import time
from typing import TYPE_CHECKING

from pydantic.v1 import Field

from pydantic2_schemaorg.StructuredValue import StructuredValue


class OpeningHoursSpecification(StructuredValue):
    """A structured value providing information about the opening hours of a place or a certain"
     "service inside a place. The place is __open__ if the [[opens]] property is specified,"
     "and __closed__ otherwise. If the value for the [[closes]] property is less than the value"
     "for the [[opens]] property then the hour range is assumed to span over the next day.

    See: https://schema.org/OpeningHoursSpecification
    Model depth: 4
    """

    type_: str = Field(default="OpeningHoursSpecification", alias="@type", const=True)
    validFrom: None | (
        list[datetime | DateTime | date | Date | str]
        | datetime
        | DateTime
        | date
        | Date
        | str
    ) = Field(
        default=None,
        description="The date when the item becomes valid.",
    )
    dayOfWeek: list[DayOfWeek | str] | DayOfWeek | str | None = Field(
        default=None,
        description="The day of the week for which these opening hours are valid.",
    )
    closes: list[time | Time | str] | time | Time | str | None = Field(
        default=None,
        description="The closing hour of the place or service on the given day(s) of the week.",
    )
    opens: list[time | Time | str] | time | Time | str | None = Field(
        default=None,
        description="The opening hour of the place or service on the given day(s) of the week.",
    )
    validThrough: None | (
        list[datetime | DateTime | date | Date | str]
        | datetime
        | DateTime
        | date
        | Date
        | str
    ) = Field(
        default=None,
        description="The date after when the item is not valid. For example the end of an offer, salary period,"
        "or a period of opening hours.",
    )


if TYPE_CHECKING:
    from pydantic2_schemaorg.DateTime import DateTime
    from pydantic2_schemaorg.Date import Date
    from pydantic2_schemaorg.DayOfWeek import DayOfWeek
    from pydantic2_schemaorg.Time import Time
