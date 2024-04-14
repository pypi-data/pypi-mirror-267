from __future__ import annotations

from typing import TYPE_CHECKING

from pydantic.v1 import Field

from pydantic2_schemaorg.Intangible import Intangible


class Seat(Intangible):
    """Used to describe a seat, such as a reserved seat in an event reservation.

    See: https://schema.org/Seat
    Model depth: 3
    """

    type_: str = Field(default="Seat", alias="@type", const=True)
    seatingType: None | (
        list[str | Text | QualitativeValue] | str | Text | QualitativeValue
    ) = Field(
        default=None,
        description="The type/class of the seat.",
    )
    seatNumber: list[str | Text] | str | Text | None = Field(
        default=None,
        description="The location of the reserved seat (e.g., 27).",
    )
    seatSection: list[str | Text] | str | Text | None = Field(
        default=None,
        description="The section location of the reserved seat (e.g. Orchestra).",
    )
    seatRow: list[str | Text] | str | Text | None = Field(
        default=None,
        description="The row location of the reserved seat (e.g., B).",
    )


if TYPE_CHECKING:
    from pydantic2_schemaorg.Text import Text
    from pydantic2_schemaorg.QualitativeValue import QualitativeValue
