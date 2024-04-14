from __future__ import annotations

from typing import TYPE_CHECKING

from pydantic.v1 import Field

from pydantic2_schemaorg.MedicalBusiness import MedicalBusiness
from pydantic2_schemaorg.MedicalOrganization import MedicalOrganization


class MedicalClinic(MedicalBusiness, MedicalOrganization):
    """A facility, often associated with a hospital or medical school, that is devoted to the"
     "specific diagnosis and/or healthcare. Previously limited to outpatients but with"
     "evolution it may be open to inpatients as well.

    See: https://schema.org/MedicalClinic
    Model depth: 4
    """

    type_: str = Field(default="MedicalClinic", alias="@type", const=True)
    medicalSpecialty: None | (
        list[MedicalSpecialty | str] | MedicalSpecialty | str
    ) = Field(
        default=None,
        description="A medical specialty of the provider.",
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
    from pydantic2_schemaorg.MedicalTest import MedicalTest
    from pydantic2_schemaorg.MedicalProcedure import MedicalProcedure
    from pydantic2_schemaorg.MedicalTherapy import MedicalTherapy
