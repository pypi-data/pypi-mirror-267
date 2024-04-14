from __future__ import annotations

from pydantic.v1 import Field

from pydantic2_schemaorg.Enumeration import Enumeration


class ProductReturnEnumeration(Enumeration):
    """ProductReturnEnumeration enumerates several kinds of product return policy. Note"
     "that this structure may not capture all aspects of the policy.

    See: https://schema.org/ProductReturnEnumeration
    Model depth: 4
    """

    type_: str = Field(default="ProductReturnEnumeration", alias="@type", const=True)
