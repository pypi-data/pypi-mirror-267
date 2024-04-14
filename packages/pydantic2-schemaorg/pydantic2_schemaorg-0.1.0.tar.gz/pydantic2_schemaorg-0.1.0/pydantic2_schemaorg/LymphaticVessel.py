from __future__ import annotations

from typing import TYPE_CHECKING

from pydantic.v1 import Field

from pydantic2_schemaorg.Vessel import Vessel


class LymphaticVessel(Vessel):
    """A type of blood vessel that specifically carries lymph fluid unidirectionally toward"
     "the heart.

    See: https://schema.org/LymphaticVessel
    Model depth: 5
    """

    type_: str = Field(default="LymphaticVessel", alias="@type", const=True)
    runsTo: list[Vessel | str] | Vessel | str | None = Field(
        default=None,
        description="The vasculature the lymphatic structure runs, or efferents, to.",
    )
    regionDrained: None | (
        list[AnatomicalStructure | AnatomicalSystem | str]
        | AnatomicalStructure
        | AnatomicalSystem
        | str
    ) = Field(
        default=None,
        description="The anatomical or organ system drained by this vessel; generally refers to a specific"
        "part of an organ.",
    )
    originatesFrom: list[Vessel | str] | Vessel | str | None = Field(
        default=None,
        description="The vasculature the lymphatic structure originates, or afferents, from.",
    )


if TYPE_CHECKING:
    from pydantic2_schemaorg.Vessel import Vessel
    from pydantic2_schemaorg.AnatomicalStructure import AnatomicalStructure
    from pydantic2_schemaorg.AnatomicalSystem import AnatomicalSystem
