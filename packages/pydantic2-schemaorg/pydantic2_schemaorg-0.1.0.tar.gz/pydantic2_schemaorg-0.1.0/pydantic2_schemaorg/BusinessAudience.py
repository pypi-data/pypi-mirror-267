from __future__ import annotations

from typing import TYPE_CHECKING

from pydantic.v1 import Field

from pydantic2_schemaorg.Audience import Audience


class BusinessAudience(Audience):
    """A set of characteristics belonging to businesses, e.g. who compose an item's target"
     "audience.

    See: https://schema.org/BusinessAudience
    Model depth: 4
    """

    type_: str = Field(default="BusinessAudience", alias="@type", const=True)
    yearsInOperation: None | (
        list[QuantitativeValue | str] | QuantitativeValue | str
    ) = Field(
        default=None,
        description="The age of the business.",
    )
    numberOfEmployees: None | (
        list[QuantitativeValue | str] | QuantitativeValue | str
    ) = Field(
        default=None,
        description="The number of employees in an organization, e.g. business.",
    )
    yearlyRevenue: None | (
        list[QuantitativeValue | str] | QuantitativeValue | str
    ) = Field(
        default=None,
        description="The size of the business in annual revenue.",
    )


if TYPE_CHECKING:
    from pydantic2_schemaorg.QuantitativeValue import QuantitativeValue
