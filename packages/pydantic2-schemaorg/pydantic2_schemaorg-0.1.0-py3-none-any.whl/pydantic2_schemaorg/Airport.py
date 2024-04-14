from __future__ import annotations

from typing import TYPE_CHECKING

from pydantic.v1 import Field

from pydantic2_schemaorg.CivicStructure import CivicStructure


class Airport(CivicStructure):
    """An airport.

    See: https://schema.org/Airport
    Model depth: 4
    """

    type_: str = Field(default="Airport", alias="@type", const=True)
    iataCode: list[str | Text] | str | Text | None = Field(
        default=None,
        description="IATA identifier for an airline or airport.",
    )
    icaoCode: list[str | Text] | str | Text | None = Field(
        default=None,
        description="ICAO identifier for an airport.",
    )


if TYPE_CHECKING:
    from pydantic2_schemaorg.Text import Text
