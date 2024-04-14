from __future__ import annotations

from typing import TYPE_CHECKING

from pydantic.v1 import Field

from pydantic2_schemaorg.Trip import Trip


class TrainTrip(Trip):
    """A trip on a commercial train line.

    See: https://schema.org/TrainTrip
    Model depth: 4
    """

    type_: str = Field(default="TrainTrip", alias="@type", const=True)
    departurePlatform: list[str | Text] | str | Text | None = Field(
        default=None,
        description="The platform from which the train departs.",
    )
    trainNumber: list[str | Text] | str | Text | None = Field(
        default=None,
        description="The unique identifier for the train.",
    )
    trainName: list[str | Text] | str | Text | None = Field(
        default=None,
        description="The name of the train (e.g. The Orient Express).",
    )
    arrivalStation: None | (list[TrainStation | str] | TrainStation | str) = Field(
        default=None,
        description="The station where the train trip ends.",
    )
    arrivalPlatform: list[str | Text] | str | Text | None = Field(
        default=None,
        description="The platform where the train arrives.",
    )
    departureStation: None | (list[TrainStation | str] | TrainStation | str) = Field(
        default=None,
        description="The station from which the train departs.",
    )


if TYPE_CHECKING:
    from pydantic2_schemaorg.Text import Text
    from pydantic2_schemaorg.TrainStation import TrainStation
