from __future__ import annotations

from typing import TYPE_CHECKING

from pydantic.v1 import Field
from pydantic.v1 import StrictBool
from pydantic.v1 import StrictFloat
from pydantic.v1 import StrictInt

from pydantic2_schemaorg.FinancialProduct import FinancialProduct
from pydantic2_schemaorg.PaymentMethod import PaymentMethod


class PaymentCard(PaymentMethod, FinancialProduct):
    """A payment method using a credit, debit, store or other card to associate the payment with"
     "an account.

    See: https://schema.org/PaymentCard
    Model depth: 5
    """

    type_: str = Field(default="PaymentCard", alias="@type", const=True)
    floorLimit: None | (list[MonetaryAmount | str] | MonetaryAmount | str) = Field(
        default=None,
        description="A floor limit is the amount of money above which credit card transactions must be authorized.",
    )
    monthlyMinimumRepaymentAmount: None | (
        list[StrictInt | StrictFloat | Number | MonetaryAmount | str]
        | StrictInt
        | StrictFloat
        | Number
        | MonetaryAmount
        | str
    ) = Field(
        default=None,
        description="The minimum payment is the lowest amount of money that one is required to pay on a credit"
        "card statement each month.",
    )
    cashBack: None | (
        list[StrictInt | StrictFloat | Number | StrictBool | Boolean | str]
        | StrictInt
        | StrictFloat
        | Number
        | StrictBool
        | Boolean
        | str
    ) = Field(
        default=None,
        description="A cardholder benefit that pays the cardholder a small percentage of their net expenditures.",
    )
    contactlessPayment: None | (
        list[StrictBool | Boolean | str] | StrictBool | Boolean | str
    ) = Field(
        default=None,
        description="A secure method for consumers to purchase products or services via debit, credit or smartcards"
        "by using RFID or NFC technology.",
    )


if TYPE_CHECKING:
    from pydantic2_schemaorg.MonetaryAmount import MonetaryAmount
    from pydantic2_schemaorg.Number import Number
    from pydantic2_schemaorg.Boolean import Boolean
