from __future__ import annotations

from datetime import date
from datetime import datetime
from typing import TYPE_CHECKING

from pydantic.v1 import Field
from pydantic.v1 import StrictFloat
from pydantic.v1 import StrictInt

from pydantic2_schemaorg.StructuredValue import StructuredValue


class DatedMoneySpecification(StructuredValue):
    """A DatedMoneySpecification represents monetary values with optional start and end"
     "dates. For example, this could represent an employee's salary over a specific period"
     "of time. __Note:__ This type has been superseded by [[MonetaryAmount]], use of that"
     "type is recommended.

    See: https://schema.org/DatedMoneySpecification
    Model depth: 4
    """

    type_: str = Field(default="DatedMoneySpecification", alias="@type", const=True)
    currency: list[str | Text] | str | Text | None = Field(
        default=None,
        description="The currency in which the monetary amount is expressed. Use standard formats: [ISO 4217"
        'currency format](http://en.wikipedia.org/wiki/ISO_4217), e.g. "USD"; [Ticker'
        "symbol](https://en.wikipedia.org/wiki/List_of_cryptocurrencies) for cryptocurrencies,"
        'e.g. "BTC"; well known names for [Local Exchange Trading Systems](https://en.wikipedia.org/wiki/Local_exchange_trading_system)'
        '(LETS) and other currency types, e.g. "Ithaca HOUR".',
    )
    startDate: None | (
        list[datetime | DateTime | date | Date | str]
        | datetime
        | DateTime
        | date
        | Date
        | str
    ) = Field(
        default=None,
        description="The start date and time of the item (in [ISO 8601 date format](http://en.wikipedia.org/wiki/ISO_8601)).",
    )
    endDate: None | (
        list[datetime | DateTime | date | Date | str]
        | datetime
        | DateTime
        | date
        | Date
        | str
    ) = Field(
        default=None,
        description="The end date and time of the item (in [ISO 8601 date format](http://en.wikipedia.org/wiki/ISO_8601)).",
    )
    amount: None | (
        list[StrictInt | StrictFloat | Number | MonetaryAmount | str]
        | StrictInt
        | StrictFloat
        | Number
        | MonetaryAmount
        | str
    ) = Field(
        default=None,
        description="The amount of money.",
    )


if TYPE_CHECKING:
    from pydantic2_schemaorg.Text import Text
    from pydantic2_schemaorg.DateTime import DateTime
    from pydantic2_schemaorg.Date import Date
    from pydantic2_schemaorg.Number import Number
    from pydantic2_schemaorg.MonetaryAmount import MonetaryAmount
