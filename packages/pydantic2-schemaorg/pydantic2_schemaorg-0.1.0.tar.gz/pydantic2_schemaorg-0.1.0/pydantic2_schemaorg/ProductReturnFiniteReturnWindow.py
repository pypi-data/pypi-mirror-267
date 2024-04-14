from __future__ import annotations

from pydantic.v1 import Field

from pydantic2_schemaorg.ProductReturnEnumeration import ProductReturnEnumeration


class ProductReturnFiniteReturnWindow(ProductReturnEnumeration):
    """ProductReturnFiniteReturnWindow: there is a finite window for product returns.

    See: https://schema.org/ProductReturnFiniteReturnWindow
    Model depth: 5
    """

    type_: str = Field(
        default="ProductReturnFiniteReturnWindow", alias="@type", const=True
    )
