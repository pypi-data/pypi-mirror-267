from __future__ import annotations

from typing import TYPE_CHECKING

from pydantic.v1 import Field

from pydantic2_schemaorg.MedicalEntity import MedicalEntity


class AnatomicalStructure(MedicalEntity):
    """Any part of the human body, typically a component of an anatomical system. Organs, tissues,"
     "and cells are all anatomical structures.

    See: https://schema.org/AnatomicalStructure
    Model depth: 3
    """

    type_: str = Field(default="AnatomicalStructure", alias="@type", const=True)
    connectedTo: None | (
        list[AnatomicalStructure | str] | AnatomicalStructure | str
    ) = Field(
        default=None,
        description="Other anatomical structures to which this structure is connected.",
    )
    bodyLocation: list[str | Text] | str | Text | None = Field(
        default=None,
        description="Location in the body of the anatomical structure.",
    )
    diagram: None | (list[ImageObject | str] | ImageObject | str) = Field(
        default=None,
        description="An image containing a diagram that illustrates the structure and/or its component substructures"
        "and/or connections with other structures.",
    )
    relatedTherapy: None | (list[MedicalTherapy | str] | MedicalTherapy | str) = Field(
        default=None,
        description="A medical therapy related to this anatomy.",
    )
    relatedCondition: None | (
        list[MedicalCondition | str] | MedicalCondition | str
    ) = Field(
        default=None,
        description="A medical condition associated with this anatomy.",
    )
    subStructure: None | (
        list[AnatomicalStructure | str] | AnatomicalStructure | str
    ) = Field(
        default=None,
        description="Component (sub-)structure(s) that comprise this anatomical structure.",
    )
    associatedPathophysiology: None | (list[str | Text] | str | Text) = Field(
        default=None,
        description="If applicable, a description of the pathophysiology associated with the anatomical"
        "system, including potential abnormal changes in the mechanical, physical, and biochemical"
        "functions of the system.",
    )
    partOfSystem: None | (
        list[AnatomicalSystem | str] | AnatomicalSystem | str
    ) = Field(
        default=None,
        description="The anatomical or organ system that this structure is part of.",
    )


if TYPE_CHECKING:
    from pydantic2_schemaorg.Text import Text
    from pydantic2_schemaorg.ImageObject import ImageObject
    from pydantic2_schemaorg.MedicalTherapy import MedicalTherapy
    from pydantic2_schemaorg.MedicalCondition import MedicalCondition
    from pydantic2_schemaorg.AnatomicalSystem import AnatomicalSystem
