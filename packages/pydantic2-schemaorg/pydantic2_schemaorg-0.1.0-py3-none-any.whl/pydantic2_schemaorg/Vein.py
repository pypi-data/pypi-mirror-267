from __future__ import annotations

from typing import TYPE_CHECKING

from pydantic.v1 import Field

from pydantic2_schemaorg.Vessel import Vessel


class Vein(Vessel):
    """A type of blood vessel that specifically carries blood to the heart.

    See: https://schema.org/Vein
    Model depth: 5
    """

    type_: str = Field(default="Vein", alias="@type", const=True)
    drainsTo: list[Vessel | str] | Vessel | str | None = Field(
        default=None,
        description="The vasculature that the vein drains into.",
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
    tributary: None | (
        list[AnatomicalStructure | str] | AnatomicalStructure | str
    ) = Field(
        default=None,
        description="The anatomical or organ system that the vein flows into; a larger structure that the vein"
        "connects to.",
    )


if TYPE_CHECKING:
    from pydantic2_schemaorg.Vessel import Vessel
    from pydantic2_schemaorg.AnatomicalStructure import AnatomicalStructure
    from pydantic2_schemaorg.AnatomicalSystem import AnatomicalSystem
