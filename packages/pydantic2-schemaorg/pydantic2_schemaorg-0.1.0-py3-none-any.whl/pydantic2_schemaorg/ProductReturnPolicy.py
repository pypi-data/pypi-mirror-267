from __future__ import annotations

from typing import TYPE_CHECKING

from pydantic.v1 import AnyUrl
from pydantic.v1 import Field

from pydantic2_schemaorg.Intangible import Intangible


class ProductReturnPolicy(Intangible):
    """A ProductReturnPolicy provides information about product return policies associated"
     "with an [[Organization]] or [[Product]].

    See: https://schema.org/ProductReturnPolicy
    Model depth: 3
    """

    type_: str = Field(default="ProductReturnPolicy", alias="@type", const=True)
    productReturnLink: None | (list[AnyUrl | URL | str] | AnyUrl | URL | str) = Field(
        default=None,
        description="Indicates a Web page or service by URL, for product return.",
    )
    productReturnDays: None | (list[int | Integer | str] | int | Integer | str) = Field(
        default=None,
        description="The productReturnDays property indicates the number of days (from purchase) within"
        "which relevant product return policy is applicable.",
    )


if TYPE_CHECKING:
    from pydantic2_schemaorg.URL import URL
    from pydantic2_schemaorg.Integer import Integer
