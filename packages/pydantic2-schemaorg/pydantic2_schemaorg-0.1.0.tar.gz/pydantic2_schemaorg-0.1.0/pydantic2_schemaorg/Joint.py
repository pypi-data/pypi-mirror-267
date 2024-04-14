from __future__ import annotations

from typing import TYPE_CHECKING

from pydantic.v1 import Field

from pydantic2_schemaorg.AnatomicalStructure import AnatomicalStructure


class Joint(AnatomicalStructure):
    """The anatomical location at which two or more bones make contact.

    See: https://schema.org/Joint
    Model depth: 4
    """

    type_: str = Field(default="Joint", alias="@type", const=True)
    structuralClass: list[str | Text] | str | Text | None = Field(
        default=None,
        description="The name given to how bone physically connects to each other.",
    )
    functionalClass: None | (
        list[str | Text | MedicalEntity] | str | Text | MedicalEntity
    ) = Field(
        default=None,
        description="The degree of mobility the joint allows.",
    )
    biomechnicalClass: list[str | Text] | str | Text | None = Field(
        default=None,
        description="The biomechanical properties of the bone.",
    )


if TYPE_CHECKING:
    from pydantic2_schemaorg.Text import Text
    from pydantic2_schemaorg.MedicalEntity import MedicalEntity
