from __future__ import annotations

from datetime import date
from datetime import datetime
from typing import TYPE_CHECKING

from pydantic.v1 import Field

from pydantic2_schemaorg.Intangible import Intangible


class MerchantReturnPolicySeasonalOverride(Intangible):
    """A seasonal override of a return policy, for example used for holidays.

    See: https://schema.org/MerchantReturnPolicySeasonalOverride
    Model depth: 3
    """

    type_: str = Field(
        default="MerchantReturnPolicySeasonalOverride", alias="@type", const=True
    )
    merchantReturnDays: None | (
        list[datetime | DateTime | int | Integer | date | Date | str]
        | datetime
        | DateTime
        | int
        | Integer
        | date
        | Date
        | str
    ) = Field(
        default=None,
        description="Specifies either a fixed return date or the number of days (from the delivery date) that"
        "a product can be returned. Used when the [[returnPolicyCategory]] property is specified"
        "as [[MerchantReturnFiniteReturnWindow]].",
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
    returnPolicyCategory: None | (
        list[MerchantReturnEnumeration | str] | MerchantReturnEnumeration | str
    ) = Field(
        default=None,
        description="Specifies an applicable return policy (from an enumeration).",
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


if TYPE_CHECKING:
    from pydantic2_schemaorg.DateTime import DateTime
    from pydantic2_schemaorg.Integer import Integer
    from pydantic2_schemaorg.Date import Date
    from pydantic2_schemaorg.MerchantReturnEnumeration import MerchantReturnEnumeration
