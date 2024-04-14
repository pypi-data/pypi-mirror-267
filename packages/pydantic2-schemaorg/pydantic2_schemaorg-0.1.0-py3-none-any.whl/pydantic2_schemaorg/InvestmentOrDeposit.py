from __future__ import annotations

from typing import TYPE_CHECKING

from pydantic.v1 import Field
from pydantic.v1 import StrictFloat
from pydantic.v1 import StrictInt

from pydantic2_schemaorg.FinancialProduct import FinancialProduct


class InvestmentOrDeposit(FinancialProduct):
    """A type of financial product that typically requires the client to transfer funds to a"
     "financial service in return for potential beneficial financial return.

    See: https://schema.org/InvestmentOrDeposit
    Model depth: 5
    """

    type_: str = Field(default="InvestmentOrDeposit", alias="@type", const=True)
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
    from pydantic2_schemaorg.Number import Number
    from pydantic2_schemaorg.MonetaryAmount import MonetaryAmount
