from __future__ import annotations

from typing import TYPE_CHECKING

from pydantic.v1 import Field

from pydantic2_schemaorg.Organization import Organization


class Airline(Organization):
    """An organization that provides flights for passengers.

    See: https://schema.org/Airline
    Model depth: 3
    """

    type_: str = Field(default="Airline", alias="@type", const=True)
    iataCode: list[str | Text] | str | Text | None = Field(
        default=None,
        description="IATA identifier for an airline or airport.",
    )
    boardingPolicy: None | (
        list[BoardingPolicyType | str] | BoardingPolicyType | str
    ) = Field(
        default=None,
        description="The type of boarding policy used by the airline (e.g. zone-based or group-based).",
    )


if TYPE_CHECKING:
    from pydantic2_schemaorg.Text import Text
    from pydantic2_schemaorg.BoardingPolicyType import BoardingPolicyType
