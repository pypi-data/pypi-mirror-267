from __future__ import annotations

from pydantic.v1 import Field

from pydantic2_schemaorg.CivicStructure import CivicStructure
from pydantic2_schemaorg.EmergencyService import EmergencyService


class FireStation(EmergencyService, CivicStructure):
    """A fire station. With firemen.

    See: https://schema.org/FireStation
    Model depth: 4
    """

    type_: str = Field(default="FireStation", alias="@type", const=True)
