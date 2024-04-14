from __future__ import annotations

from typing import TYPE_CHECKING

from pydantic.v1 import AnyUrl
from pydantic.v1 import Field
from pydantic.v1 import StrictFloat
from pydantic.v1 import StrictInt

from pydantic2_schemaorg.PriceSpecification import PriceSpecification


class UnitPriceSpecification(PriceSpecification):
    """The price asked for a given offer by the respective organization or person.

    See: https://schema.org/UnitPriceSpecification
    Model depth: 5
    """

    type_: str = Field(default="UnitPriceSpecification", alias="@type", const=True)
    unitText: list[str | Text] | str | Text | None = Field(
        default=None,
        description="A string or text indicating the unit of measurement. Useful if you cannot provide a standard"
        "unit code for <a href='unitCode'>unitCode</a>.",
    )
    unitCode: None | (
        list[AnyUrl | URL | str | Text] | AnyUrl | URL | str | Text
    ) = Field(
        default=None,
        description="The unit of measurement given using the UN/CEFACT Common Code (3 characters) or a URL."
        "Other codes than the UN/CEFACT Common Code may be used with a prefix followed by a colon.",
    )
    priceType: None | (
        list[str | Text | PriceTypeEnumeration] | str | Text | PriceTypeEnumeration
    ) = Field(
        default=None,
        description="Defines the type of a price specified for an offered product, for example a list price,"
        "a (temporary) sale price or a manufacturer suggested retail price. If multiple prices"
        "are specified for an offer the [[priceType]] property can be used to identify the type"
        "of each such specified price. The value of priceType can be specified as a value from enumeration"
        "PriceTypeEnumeration or as a free form text string for price types that are not already"
        "predefined in PriceTypeEnumeration.",
    )
    billingStart: None | (
        list[StrictInt | StrictFloat | Number | str]
        | StrictInt
        | StrictFloat
        | Number
        | str
    ) = Field(
        default=None,
        description="Specifies after how much time this price (or price component) becomes valid and billing"
        "starts. Can be used, for example, to model a price increase after the first year of a subscription."
        "The unit of measurement is specified by the unitCode property.",
    )
    billingDuration: None | (
        list[(StrictInt | StrictFloat | Number | QuantitativeValue | Duration | str)]
        | StrictInt
        | StrictFloat
        | Number
        | QuantitativeValue
        | Duration
        | str
    ) = Field(
        default=None,
        description="Specifies for how long this price (or price component) will be billed. Can be used, for"
        "example, to model the contractual duration of a subscription or payment plan. Type can"
        "be either a Duration or a Number (in which case the unit of measurement, for example month,"
        "is specified by the unitCode property).",
    )
    referenceQuantity: None | (
        list[QuantitativeValue | str] | QuantitativeValue | str
    ) = Field(
        default=None,
        description="The reference quantity for which a certain price applies, e.g. 1 EUR per 4 kWh of electricity."
        "This property is a replacement for unitOfMeasurement for the advanced cases where the"
        "price does not relate to a standard unit.",
    )
    priceComponentType: None | (
        list[PriceComponentTypeEnumeration | str] | PriceComponentTypeEnumeration | str
    ) = Field(
        default=None,
        description="Identifies a price component (for example, a line item on an invoice), part of the total"
        "price for an offer.",
    )
    billingIncrement: None | (
        list[StrictInt | StrictFloat | Number | str]
        | StrictInt
        | StrictFloat
        | Number
        | str
    ) = Field(
        default=None,
        description="This property specifies the minimal quantity and rounding increment that will be the"
        "basis for the billing. The unit of measurement is specified by the unitCode property.",
    )


if TYPE_CHECKING:
    from pydantic2_schemaorg.Text import Text
    from pydantic2_schemaorg.URL import URL
    from pydantic2_schemaorg.PriceTypeEnumeration import PriceTypeEnumeration
    from pydantic2_schemaorg.Number import Number
    from pydantic2_schemaorg.QuantitativeValue import QuantitativeValue
    from pydantic2_schemaorg.Duration import Duration
    from pydantic2_schemaorg.PriceComponentTypeEnumeration import (
        PriceComponentTypeEnumeration,
    )
