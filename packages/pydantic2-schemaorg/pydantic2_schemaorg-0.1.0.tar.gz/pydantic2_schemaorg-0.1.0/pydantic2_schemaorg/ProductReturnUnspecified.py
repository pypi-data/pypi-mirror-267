from __future__ import annotations

from pydantic.v1 import Field

from pydantic2_schemaorg.ProductReturnEnumeration import ProductReturnEnumeration


class ProductReturnUnspecified(ProductReturnEnumeration):
    """ProductReturnUnspecified: a product return policy is not specified here.

    See: https://schema.org/ProductReturnUnspecified
    Model depth: 5
    """

    type_: str = Field(default="ProductReturnUnspecified", alias="@type", const=True)
