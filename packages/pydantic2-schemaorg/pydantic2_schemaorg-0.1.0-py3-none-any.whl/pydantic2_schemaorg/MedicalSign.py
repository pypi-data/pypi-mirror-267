from __future__ import annotations

from typing import TYPE_CHECKING

from pydantic.v1 import Field

from pydantic2_schemaorg.MedicalSignOrSymptom import MedicalSignOrSymptom


class MedicalSign(MedicalSignOrSymptom):
    """Any physical manifestation of a person's medical condition discoverable by objective"
     "diagnostic tests or physical examination.

    See: https://schema.org/MedicalSign
    Model depth: 5
    """

    type_: str = Field(default="MedicalSign", alias="@type", const=True)
    identifyingTest: None | (list[MedicalTest | str] | MedicalTest | str) = Field(
        default=None,
        description="A diagnostic test that can identify this sign.",
    )
    identifyingExam: None | (list[PhysicalExam | str] | PhysicalExam | str) = Field(
        default=None,
        description="A physical examination that can identify this sign.",
    )


if TYPE_CHECKING:
    from pydantic2_schemaorg.MedicalTest import MedicalTest
    from pydantic2_schemaorg.PhysicalExam import PhysicalExam
