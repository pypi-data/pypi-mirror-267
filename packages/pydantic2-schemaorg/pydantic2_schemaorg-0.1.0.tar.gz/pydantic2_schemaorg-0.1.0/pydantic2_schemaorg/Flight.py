from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from pydantic.v1 import Field

from pydantic2_schemaorg.Trip import Trip


class Flight(Trip):
    """An airline flight.

    See: https://schema.org/Flight
    Model depth: 4
    """

    type_: str = Field(default="Flight", alias="@type", const=True)
    departureGate: list[str | Text] | str | Text | None = Field(
        default=None,
        description="Identifier of the flight's departure gate.",
    )
    mealService: list[str | Text] | str | Text | None = Field(
        default=None,
        description="Description of the meals that will be provided or available for purchase.",
    )
    estimatedFlightDuration: None | (
        list[str | Text | Duration] | str | Text | Duration
    ) = Field(
        default=None,
        description="The estimated time the flight will take.",
    )
    seller: None | (
        list[Organization | Person | str] | Organization | Person | str
    ) = Field(
        default=None,
        description="An entity which offers (sells / leases / lends / loans) the services / goods. A seller may"
        "also be a provider.",
    )
    arrivalAirport: None | (list[Airport | str] | Airport | str) = Field(
        default=None,
        description="The airport where the flight terminates.",
    )
    carrier: None | (list[Organization | str] | Organization | str) = Field(
        default=None,
        description="'carrier' is an out-dated term indicating the 'provider' for parcel delivery and flights.",
    )
    boardingPolicy: None | (
        list[BoardingPolicyType | str] | BoardingPolicyType | str
    ) = Field(
        default=None,
        description="The type of boarding policy used by the airline (e.g. zone-based or group-based).",
    )
    departureAirport: None | (list[Airport | str] | Airport | str) = Field(
        default=None,
        description="The airport where the flight originates.",
    )
    webCheckinTime: None | (
        list[datetime | DateTime | str] | datetime | DateTime | str
    ) = Field(
        default=None,
        description="The time when a passenger can check into the flight online.",
    )
    flightDistance: None | (
        list[str | Text | Distance] | str | Text | Distance
    ) = Field(
        default=None,
        description="The distance of the flight.",
    )
    departureTerminal: list[str | Text] | str | Text | None = Field(
        default=None,
        description="Identifier of the flight's departure terminal.",
    )
    flightNumber: list[str | Text] | str | Text | None = Field(
        default=None,
        description="The unique identifier for a flight including the airline IATA code. For example, if describing"
        "United flight 110, where the IATA code for United is 'UA', the flightNumber is 'UA110'.",
    )
    arrivalTerminal: list[str | Text] | str | Text | None = Field(
        default=None,
        description="Identifier of the flight's arrival terminal.",
    )
    aircraft: None | (list[str | Text | Vehicle] | str | Text | Vehicle) = Field(
        default=None,
        description='The kind of aircraft (e.g., "Boeing 747").',
    )
    arrivalGate: list[str | Text] | str | Text | None = Field(
        default=None,
        description="Identifier of the flight's arrival gate.",
    )


if TYPE_CHECKING:
    from pydantic2_schemaorg.Text import Text
    from pydantic2_schemaorg.Duration import Duration
    from pydantic2_schemaorg.Organization import Organization
    from pydantic2_schemaorg.Person import Person
    from pydantic2_schemaorg.Airport import Airport
    from pydantic2_schemaorg.BoardingPolicyType import BoardingPolicyType
    from pydantic2_schemaorg.DateTime import DateTime
    from pydantic2_schemaorg.Distance import Distance
    from pydantic2_schemaorg.Vehicle import Vehicle
