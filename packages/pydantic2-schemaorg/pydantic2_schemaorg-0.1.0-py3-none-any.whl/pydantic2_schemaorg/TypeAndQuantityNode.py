from __future__ import annotations

from typing import TYPE_CHECKING

from pydantic.v1 import AnyUrl
from pydantic.v1 import Field
from pydantic.v1 import StrictFloat
from pydantic.v1 import StrictInt

from pydantic2_schemaorg.StructuredValue import StructuredValue


class TypeAndQuantityNode(StructuredValue):
    """A structured value indicating the quantity, unit of measurement, and business function"
     "of goods included in a bundle offer.

    See: https://schema.org/TypeAndQuantityNode
    Model depth: 4
    """

    type_: str = Field(default="TypeAndQuantityNode", alias="@type", const=True)
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
    amountOfThisGood: None | (
        list[StrictInt | StrictFloat | Number | str]
        | StrictInt
        | StrictFloat
        | Number
        | str
    ) = Field(
        default=None,
        description="The quantity of the goods included in the offer.",
    )
    businessFunction: None | (
        list[BusinessFunction | str] | BusinessFunction | str
    ) = Field(
        default=None,
        description="The business function (e.g. sell, lease, repair, dispose) of the offer or component"
        "of a bundle (TypeAndQuantityNode). The default is http://purl.org/goodrelations/v1#Sell.",
    )
    typeOfGood: None | (
        list[Product | Service | str] | Product | Service | str
    ) = Field(
        default=None,
        description="The product that this structured value is referring to.",
    )


if TYPE_CHECKING:
    from pydantic2_schemaorg.Text import Text
    from pydantic2_schemaorg.URL import URL
    from pydantic2_schemaorg.Number import Number
    from pydantic2_schemaorg.BusinessFunction import BusinessFunction
    from pydantic2_schemaorg.Product import Product
    from pydantic2_schemaorg.Service import Service
