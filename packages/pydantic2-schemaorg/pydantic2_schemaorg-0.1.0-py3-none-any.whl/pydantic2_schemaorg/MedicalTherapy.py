from __future__ import annotations

from typing import TYPE_CHECKING

from pydantic.v1 import Field

from pydantic2_schemaorg.TherapeuticProcedure import TherapeuticProcedure


class MedicalTherapy(TherapeuticProcedure):
    """Any medical intervention designed to prevent, treat, and cure human diseases and medical"
     "conditions, including both curative and palliative therapies. Medical therapies"
     "are typically processes of care relying upon pharmacotherapy, behavioral therapy,"
     "supportive therapy (with fluid or nutrition for example), or detoxification (e.g."
     "hemodialysis) aimed at improving or preventing a health condition.

    See: https://schema.org/MedicalTherapy
    Model depth: 5
    """

    type_: str = Field(default="MedicalTherapy", alias="@type", const=True)
    contraindication: None | (
        list[str | Text | MedicalContraindication]
        | str
        | Text
        | MedicalContraindication
    ) = Field(
        default=None,
        description="A contraindication for this therapy.",
    )
    duplicateTherapy: None | (
        list[MedicalTherapy | str] | MedicalTherapy | str
    ) = Field(
        default=None,
        description="A therapy that duplicates or overlaps this one.",
    )
    seriousAdverseOutcome: None | (
        list[MedicalEntity | str] | MedicalEntity | str
    ) = Field(
        default=None,
        description="A possible serious complication and/or serious side effect of this therapy. Serious"
        "adverse outcomes include those that are life-threatening; result in death, disability,"
        "or permanent damage; require hospitalization or prolong existing hospitalization;"
        "cause congenital anomalies or birth defects; or jeopardize the patient and may require"
        "medical or surgical intervention to prevent one of the outcomes in this definition.",
    )


if TYPE_CHECKING:
    from pydantic2_schemaorg.Text import Text
    from pydantic2_schemaorg.MedicalContraindication import MedicalContraindication
    from pydantic2_schemaorg.MedicalEntity import MedicalEntity
