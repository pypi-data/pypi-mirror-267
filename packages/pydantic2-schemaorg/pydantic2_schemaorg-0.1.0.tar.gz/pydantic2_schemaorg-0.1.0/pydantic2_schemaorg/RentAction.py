from __future__ import annotations

from typing import TYPE_CHECKING

from pydantic.v1 import Field

from pydantic2_schemaorg.TradeAction import TradeAction


class RentAction(TradeAction):
    """The act of giving money in return for temporary use, but not ownership, of an object such"
     "as a vehicle or property. For example, an agent rents a property from a landlord in exchange"
     "for a periodic payment.

    See: https://schema.org/RentAction
    Model depth: 4
    """

    type_: str = Field(default="RentAction", alias="@type", const=True)
    landlord: None | (
        list[Organization | Person | str] | Organization | Person | str
    ) = Field(
        default=None,
        description="A sub property of participant. The owner of the real estate property.",
    )
    realEstateAgent: None | (
        list[RealEstateAgent | str] | RealEstateAgent | str
    ) = Field(
        default=None,
        description="A sub property of participant. The real estate agent involved in the action.",
    )


if TYPE_CHECKING:
    from pydantic2_schemaorg.Organization import Organization
    from pydantic2_schemaorg.Person import Person
    from pydantic2_schemaorg.RealEstateAgent import RealEstateAgent
