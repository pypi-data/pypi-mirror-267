from __future__ import annotations

from pydantic.v1 import Field

from pydantic2_schemaorg.AutomotiveBusiness import AutomotiveBusiness
from pydantic2_schemaorg.Store import Store


class AutoPartsStore(AutomotiveBusiness, Store):
    """An auto parts store.

    See: https://schema.org/AutoPartsStore
    Model depth: 5
    """

    type_: str = Field(default="AutoPartsStore", alias="@type", const=True)
