from __future__ import annotations

from typing import TYPE_CHECKING

from pydantic.v1 import AnyUrl
from pydantic.v1 import Field
from pydantic.v1 import StrictFloat
from pydantic.v1 import StrictInt

from pydantic2_schemaorg.Service import Service


class FinancialProduct(Service):
    """A product provided to consumers and businesses by financial institutions such as banks,"
     "insurance companies, brokerage firms, consumer finance companies, and investment"
     "companies which comprise the financial services industry.

    See: https://schema.org/FinancialProduct
    Model depth: 4
    """

    type_: str = Field(default="FinancialProduct", alias="@type", const=True)
    annualPercentageRate: None | (
        list[StrictInt | StrictFloat | Number | QuantitativeValue | str]
        | StrictInt
        | StrictFloat
        | Number
        | QuantitativeValue
        | str
    ) = Field(
        default=None,
        description="The annual rate that is charged for borrowing (or made by investing), expressed as a single"
        "percentage number that represents the actual yearly cost of funds over the term of a loan."
        "This includes any fees or additional costs associated with the transaction.",
    )
    feesAndCommissionsSpecification: None | (
        list[AnyUrl | URL | str | Text] | AnyUrl | URL | str | Text
    ) = Field(
        default=None,
        description="Description of fees, commissions, and other terms applied either to a class of financial"
        "product, or by a financial service organization.",
    )
    interestRate: None | (
        list[StrictInt | StrictFloat | Number | QuantitativeValue | str]
        | StrictInt
        | StrictFloat
        | Number
        | QuantitativeValue
        | str
    ) = Field(
        default=None,
        description="The interest rate, charged or paid, applicable to the financial product. Note: This"
        "is different from the calculated annualPercentageRate.",
    )


if TYPE_CHECKING:
    from pydantic2_schemaorg.Number import Number
    from pydantic2_schemaorg.QuantitativeValue import QuantitativeValue
    from pydantic2_schemaorg.URL import URL
    from pydantic2_schemaorg.Text import Text
