from __future__ import annotations

from typing import TYPE_CHECKING

from pydantic.v1 import Field

from pydantic2_schemaorg.AnatomicalStructure import AnatomicalStructure


class Nerve(AnatomicalStructure):
    """A common pathway for the electrochemical nerve impulses that are transmitted along"
     "each of the axons.

    See: https://schema.org/Nerve
    Model depth: 4
    """

    type_: str = Field(default="Nerve", alias="@type", const=True)
    sensoryUnit: None | (
        list[AnatomicalStructure | SuperficialAnatomy | str]
        | AnatomicalStructure
        | SuperficialAnatomy
        | str
    ) = Field(
        default=None,
        description="The neurological pathway extension that inputs and sends information to the brain or"
        "spinal cord.",
    )
    sourcedFrom: None | (list[BrainStructure | str] | BrainStructure | str) = Field(
        default=None,
        description="The neurological pathway that originates the neurons.",
    )
    branch: None | (
        list[AnatomicalStructure | str] | AnatomicalStructure | str
    ) = Field(
        default=None,
        description="The branches that delineate from the nerve bundle. Not to be confused with [[branchOf]].",
    )
    nerveMotor: list[Muscle | str] | Muscle | str | None = Field(
        default=None,
        description="The neurological pathway extension that involves muscle control.",
    )


if TYPE_CHECKING:
    from pydantic2_schemaorg.AnatomicalStructure import AnatomicalStructure
    from pydantic2_schemaorg.SuperficialAnatomy import SuperficialAnatomy
    from pydantic2_schemaorg.BrainStructure import BrainStructure
    from pydantic2_schemaorg.Muscle import Muscle
