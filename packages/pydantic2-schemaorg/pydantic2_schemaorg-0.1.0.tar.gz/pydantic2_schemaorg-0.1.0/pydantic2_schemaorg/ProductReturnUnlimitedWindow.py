from __future__ import annotations

from pydantic.v1 import Field

from pydantic2_schemaorg.ProductReturnEnumeration import ProductReturnEnumeration


class ProductReturnUnlimitedWindow(ProductReturnEnumeration):
    """ProductReturnUnlimitedWindow: there is an unlimited window for product returns.

    See: https://schema.org/ProductReturnUnlimitedWindow
    Model depth: 5
    """

    type_: str = Field(
        default="ProductReturnUnlimitedWindow", alias="@type", const=True
    )
