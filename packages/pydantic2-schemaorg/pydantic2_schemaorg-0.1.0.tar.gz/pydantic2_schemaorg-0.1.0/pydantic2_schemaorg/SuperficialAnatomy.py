from __future__ import annotations

from typing import TYPE_CHECKING

from pydantic.v1 import Field

from pydantic2_schemaorg.MedicalEntity import MedicalEntity


class SuperficialAnatomy(MedicalEntity):
    """Anatomical features that can be observed by sight (without dissection), including"
     "the form and proportions of the human body as well as surface landmarks that correspond"
     "to deeper subcutaneous structures. Superficial anatomy plays an important role in"
     "sports medicine, phlebotomy, and other medical specialties as underlying anatomical"
     "structures can be identified through surface palpation. For example, during back surgery,"
     "superficial anatomy can be used to palpate and count vertebrae to find the site of incision."
     "Or in phlebotomy, superficial anatomy can be used to locate an underlying vein; for example,"
     "the median cubital vein can be located by palpating the borders of the cubital fossa (such"
     "as the epicondyles of the humerus) and then looking for the superficial signs of the vein,"
     "such as size, prominence, ability to refill after depression, and feel of surrounding"
     "tissue support. As another example, in a subluxation (dislocation) of the glenohumeral"
     "joint, the bony structure becomes pronounced with the deltoid muscle failing to cover"
     "the glenohumeral joint allowing the edges of the scapula to be superficially visible."
     "Here, the superficial anatomy is the visible edges of the scapula, implying the underlying"
     "dislocation of the joint (the related anatomical structure).

    See: https://schema.org/SuperficialAnatomy
    Model depth: 3
    """

    type_: str = Field(default="SuperficialAnatomy", alias="@type", const=True)
    significance: list[str | Text] | str | Text | None = Field(
        default=None,
        description="The significance associated with the superficial anatomy; as an example, how characteristics"
        "of the superficial anatomy can suggest underlying medical conditions or courses of"
        "treatment.",
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
    relatedAnatomy: None | (
        list[AnatomicalStructure | AnatomicalSystem | str]
        | AnatomicalStructure
        | AnatomicalSystem
        | str
    ) = Field(
        default=None,
        description="Anatomical systems or structures that relate to the superficial anatomy.",
    )
    associatedPathophysiology: None | (list[str | Text] | str | Text) = Field(
        default=None,
        description="If applicable, a description of the pathophysiology associated with the anatomical"
        "system, including potential abnormal changes in the mechanical, physical, and biochemical"
        "functions of the system.",
    )


if TYPE_CHECKING:
    from pydantic2_schemaorg.Text import Text
    from pydantic2_schemaorg.MedicalTherapy import MedicalTherapy
    from pydantic2_schemaorg.MedicalCondition import MedicalCondition
    from pydantic2_schemaorg.AnatomicalStructure import AnatomicalStructure
    from pydantic2_schemaorg.AnatomicalSystem import AnatomicalSystem
