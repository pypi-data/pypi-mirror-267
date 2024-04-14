from __future__ import annotations

from typing import TYPE_CHECKING

from pydantic.v1 import Field

from pydantic2_schemaorg.MedicalAudience import MedicalAudience
from pydantic2_schemaorg.Person import Person


class Patient(MedicalAudience, Person):
    """A patient is any person recipient of health care services.

    See: https://schema.org/Patient
    Model depth: 3
    """

    type_: str = Field(default="Patient", alias="@type", const=True)
    healthCondition: None | (
        list[MedicalCondition | str] | MedicalCondition | str
    ) = Field(
        default=None,
        description="Specifying the health condition(s) of a patient, medical study, or other target audience.",
    )
    drug: list[Drug | str] | Drug | str | None = Field(
        default=None,
        description="Specifying a drug or medicine used in a medication procedure.",
    )
    diagnosis: None | (list[MedicalCondition | str] | MedicalCondition | str) = Field(
        default=None,
        description="One or more alternative conditions considered in the differential diagnosis process"
        "as output of a diagnosis process.",
    )


if TYPE_CHECKING:
    from pydantic2_schemaorg.MedicalCondition import MedicalCondition
    from pydantic2_schemaorg.Drug import Drug
