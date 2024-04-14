from __future__ import annotations

from typing import TYPE_CHECKING

from pydantic.v1 import Field

from pydantic2_schemaorg.Trip import Trip


class BusTrip(Trip):
    """A trip on a commercial bus line.

    See: https://schema.org/BusTrip
    Model depth: 4
    """

    type_: str = Field(default="BusTrip", alias="@type", const=True)
    arrivalBusStop: None | (
        list[BusStop | BusStation | str] | BusStop | BusStation | str
    ) = Field(
        default=None,
        description="The stop or station from which the bus arrives.",
    )
    busNumber: list[str | Text] | str | Text | None = Field(
        default=None,
        description="The unique identifier for the bus.",
    )
    departureBusStop: None | (
        list[BusStop | BusStation | str] | BusStop | BusStation | str
    ) = Field(
        default=None,
        description="The stop or station from which the bus departs.",
    )
    busName: list[str | Text] | str | Text | None = Field(
        default=None,
        description="The name of the bus (e.g. Bolt Express).",
    )


if TYPE_CHECKING:
    from pydantic2_schemaorg.BusStop import BusStop
    from pydantic2_schemaorg.BusStation import BusStation
    from pydantic2_schemaorg.Text import Text
