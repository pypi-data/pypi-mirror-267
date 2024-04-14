from __future__ import annotations

from typing import TYPE_CHECKING

from pydantic.v1 import Field
from pydantic.v1 import StrictBool

from pydantic2_schemaorg.LoanOrCredit import LoanOrCredit


class MortgageLoan(LoanOrCredit):
    """A loan in which property or real estate is used as collateral. (A loan securitized against"
     "some real estate.)

    See: https://schema.org/MortgageLoan
    Model depth: 6
    """

    type_: str = Field(default="MortgageLoan", alias="@type", const=True)
    domiciledMortgage: None | (
        list[StrictBool | Boolean | str] | StrictBool | Boolean | str
    ) = Field(
        default=None,
        description="Whether borrower is a resident of the jurisdiction where the property is located.",
    )
    loanMortgageMandateAmount: None | (
        list[MonetaryAmount | str] | MonetaryAmount | str
    ) = Field(
        default=None,
        description="Amount of mortgage mandate that can be converted into a proper mortgage at a later stage.",
    )


if TYPE_CHECKING:
    from pydantic2_schemaorg.Boolean import Boolean
    from pydantic2_schemaorg.MonetaryAmount import MonetaryAmount
