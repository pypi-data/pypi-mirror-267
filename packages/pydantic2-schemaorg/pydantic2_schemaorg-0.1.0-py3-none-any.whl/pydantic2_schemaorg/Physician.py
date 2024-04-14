from __future__ import annotations

from typing import TYPE_CHECKING

from pydantic.v1 import Field

from pydantic2_schemaorg.MedicalBusiness import MedicalBusiness
from pydantic2_schemaorg.MedicalOrganization import MedicalOrganization


class Physician(MedicalBusiness, MedicalOrganization):
    """A doctor's office.

    See: https://schema.org/Physician
    Model depth: 4
    """

    type_: str = Field(default="Physician", alias="@type", const=True)
    medicalSpecialty: None | (
        list[MedicalSpecialty | str] | MedicalSpecialty | str
    ) = Field(
        default=None,
        description="A medical specialty of the provider.",
    )
    hospitalAffiliation: None | (list[Hospital | str] | Hospital | str) = Field(
        default=None,
        description="A hospital with which the physician or office is affiliated.",
    )
    availableService: None | (
        list[MedicalTest | MedicalProcedure | MedicalTherapy | str]
        | MedicalTest
        | MedicalProcedure
        | MedicalTherapy
        | str
    ) = Field(
        default=None,
        description="A medical service available from this provider.",
    )


if TYPE_CHECKING:
    from pydantic2_schemaorg.MedicalSpecialty import MedicalSpecialty
    from pydantic2_schemaorg.Hospital import Hospital
    from pydantic2_schemaorg.MedicalTest import MedicalTest
    from pydantic2_schemaorg.MedicalProcedure import MedicalProcedure
    from pydantic2_schemaorg.MedicalTherapy import MedicalTherapy
