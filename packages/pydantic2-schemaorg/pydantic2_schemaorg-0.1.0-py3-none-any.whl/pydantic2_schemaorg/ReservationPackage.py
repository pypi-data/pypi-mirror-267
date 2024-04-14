from __future__ import annotations

from typing import TYPE_CHECKING

from pydantic.v1 import Field

from pydantic2_schemaorg.Reservation import Reservation


class ReservationPackage(Reservation):
    """A group of multiple reservations with common values for all sub-reservations.

    See: https://schema.org/ReservationPackage
    Model depth: 4
    """

    type_: str = Field(default="ReservationPackage", alias="@type", const=True)
    subReservation: None | (list[Reservation | str] | Reservation | str) = Field(
        default=None,
        description="The individual reservations included in the package. Typically a repeated property.",
    )


if TYPE_CHECKING:
    from pydantic2_schemaorg.Reservation import Reservation
