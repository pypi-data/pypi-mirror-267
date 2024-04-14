from __future__ import annotations

from datetime import date
from datetime import datetime
from typing import TYPE_CHECKING

from pydantic.v1 import Field
from pydantic.v1 import StrictBool
from pydantic.v1 import StrictFloat
from pydantic.v1 import StrictInt

from pydantic2_schemaorg.StructuredValue import StructuredValue


class PriceSpecification(StructuredValue):
    """A structured value representing a price or price range. Typically, only the subclasses"
     "of this type are used for markup. It is recommended to use [[MonetaryAmount]] to describe"
     "independent amounts of money such as a salary, credit card limits, etc.

    See: https://schema.org/PriceSpecification
    Model depth: 4
    """

    type_: str = Field(default="PriceSpecification", alias="@type", const=True)
    eligibleTransactionVolume: None | (
        list[PriceSpecification | str] | PriceSpecification | str
    ) = Field(
        default=None,
        description="The transaction volume, in a monetary unit, for which the offer or price specification"
        "is valid, e.g. for indicating a minimal purchasing volume, to express free shipping"
        "above a certain order volume, or to limit the acceptance of credit cards to purchases"
        "to a certain minimal amount.",
    )
    validFrom: None | (
        list[datetime | DateTime | date | Date | str]
        | datetime
        | DateTime
        | date
        | Date
        | str
    ) = Field(
        default=None,
        description="The date when the item becomes valid.",
    )
    priceCurrency: list[str | Text] | str | Text | None = Field(
        default=None,
        description="The currency of the price, or a price component when attached to [[PriceSpecification]]"
        "and its subtypes. Use standard formats: [ISO 4217 currency format](http://en.wikipedia.org/wiki/ISO_4217),"
        'e.g. "USD"; [Ticker symbol](https://en.wikipedia.org/wiki/List_of_cryptocurrencies)'
        'for cryptocurrencies, e.g. "BTC"; well known names for [Local Exchange Trading Systems](https://en.wikipedia.org/wiki/Local_exchange_trading_system)'
        '(LETS) and other currency types, e.g. "Ithaca HOUR".',
    )
    price: None | (
        list[StrictInt | StrictFloat | Number | str | Text]
        | StrictInt
        | StrictFloat
        | Number
        | str
        | Text
    ) = Field(
        default=None,
        description="The offer price of a product, or of a price component when attached to PriceSpecification"
        "and its subtypes. Usage guidelines: * Use the [[priceCurrency]] property (with standard"
        "formats: [ISO 4217 currency format](http://en.wikipedia.org/wiki/ISO_4217),"
        'e.g. "USD"; [Ticker symbol](https://en.wikipedia.org/wiki/List_of_cryptocurrencies)'
        'for cryptocurrencies, e.g. "BTC"; well known names for [Local Exchange Trading Systems](https://en.wikipedia.org/wiki/Local_exchange_trading_system)'
        '(LETS) and other currency types, e.g. "Ithaca HOUR") instead of including [ambiguous'
        "symbols](http://en.wikipedia.org/wiki/Dollar_sign#Currencies_that_use_the_dollar_or_peso_sign)"
        "such as '$' in the value. * Use '.' (Unicode 'FULL STOP' (U+002E)) rather than ',' to indicate"
        "a decimal point. Avoid using these symbols as a readability separator. * Note that both"
        "[RDFa](http://www.w3.org/TR/xhtml-rdfa-primer/#using-the-content-attribute)"
        'and Microdata syntax allow the use of a "content=" attribute for publishing simple'
        "machine-readable values alongside more human-friendly formatting. * Use values from"
        "0123456789 (Unicode 'DIGIT ZERO' (U+0030) to 'DIGIT NINE' (U+0039)) rather than superficially"
        "similar Unicode symbols.",
    )
    eligibleQuantity: None | (
        list[QuantitativeValue | str] | QuantitativeValue | str
    ) = Field(
        default=None,
        description="The interval and unit of measurement of ordering quantities for which the offer or price"
        "specification is valid. This allows e.g. specifying that a certain freight charge is"
        "valid only for a certain quantity.",
    )
    maxPrice: None | (
        list[StrictInt | StrictFloat | Number | str]
        | StrictInt
        | StrictFloat
        | Number
        | str
    ) = Field(
        default=None,
        description="The highest price if the price is a range.",
    )
    minPrice: None | (
        list[StrictInt | StrictFloat | Number | str]
        | StrictInt
        | StrictFloat
        | Number
        | str
    ) = Field(
        default=None,
        description="The lowest price if the price is a range.",
    )
    valueAddedTaxIncluded: None | (
        list[StrictBool | Boolean | str] | StrictBool | Boolean | str
    ) = Field(
        default=None,
        description="Specifies whether the applicable value-added tax (VAT) is included in the price specification"
        "or not.",
    )
    validThrough: None | (
        list[datetime | DateTime | date | Date | str]
        | datetime
        | DateTime
        | date
        | Date
        | str
    ) = Field(
        default=None,
        description="The date after when the item is not valid. For example the end of an offer, salary period,"
        "or a period of opening hours.",
    )


if TYPE_CHECKING:
    from pydantic2_schemaorg.DateTime import DateTime
    from pydantic2_schemaorg.Date import Date
    from pydantic2_schemaorg.Text import Text
    from pydantic2_schemaorg.Number import Number
    from pydantic2_schemaorg.QuantitativeValue import QuantitativeValue
    from pydantic2_schemaorg.Boolean import Boolean
