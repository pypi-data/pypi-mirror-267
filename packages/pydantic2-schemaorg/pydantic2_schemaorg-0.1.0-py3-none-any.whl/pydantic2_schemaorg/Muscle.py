from __future__ import annotations

from typing import TYPE_CHECKING

from pydantic.v1 import Field

from pydantic2_schemaorg.AnatomicalStructure import AnatomicalStructure


class Muscle(AnatomicalStructure):
    """A muscle is an anatomical structure consisting of a contractile form of tissue that animals"
     "use to effect movement.

    See: https://schema.org/Muscle
    Model depth: 4
    """

    type_: str = Field(default="Muscle", alias="@type", const=True)
    antagonist: list[Muscle | str] | Muscle | str | None = Field(
        default=None,
        description="The muscle whose action counteracts the specified muscle.",
    )
    nerve: list[Nerve | str] | Nerve | str | None = Field(
        default=None,
        description="The underlying innervation associated with the muscle.",
    )
    muscleAction: list[str | Text] | str | Text | None = Field(
        default=None,
        description="The movement the muscle generates.",
    )
    bloodSupply: list[Vessel | str] | Vessel | str | None = Field(
        default=None,
        description="The blood vessel that carries blood from the heart to the muscle.",
    )
    insertion: None | (
        list[AnatomicalStructure | str] | AnatomicalStructure | str
    ) = Field(
        default=None,
        description="The place of attachment of a muscle, or what the muscle moves.",
    )


if TYPE_CHECKING:
    from pydantic2_schemaorg.Nerve import Nerve
    from pydantic2_schemaorg.Text import Text
    from pydantic2_schemaorg.Vessel import Vessel
    from pydantic2_schemaorg.AnatomicalStructure import AnatomicalStructure
