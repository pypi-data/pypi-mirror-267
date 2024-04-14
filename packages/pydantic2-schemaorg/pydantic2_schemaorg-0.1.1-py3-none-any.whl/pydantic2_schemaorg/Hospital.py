from __future__ import annotations
from typing import TYPE_CHECKING

from typing import List, Optional, Union


from pydantic.v1 import Field
from pydantic2_schemaorg.EmergencyService import EmergencyService
from pydantic2_schemaorg.MedicalOrganization import MedicalOrganization
from pydantic2_schemaorg.CivicStructure import CivicStructure


class Hospital(EmergencyService, MedicalOrganization, CivicStructure):
    """A hospital.

    See: https://schema.org/Hospital
    Model depth: 4
    """

    type_: str = Field(default="Hospital", alias="@type", const=True)
    medicalSpecialty: Optional[
        Union[List[Union["MedicalSpecialty", str]], "MedicalSpecialty", str]
    ] = Field(
        default=None,
        description="A medical specialty of the provider.",
    )
    healthcareReportingData: Optional[
        Union[
            List[Union["Dataset", "CDCPMDRecord", str]], "Dataset", "CDCPMDRecord", str
        ]
    ] = Field(
        default=None,
        description="Indicates data describing a hospital, e.g. a CDC [[CDCPMDRecord]] or as some kind of"
        "[[Dataset]].",
    )
    availableService: Optional[
        Union[
            List[Union["MedicalTest", "MedicalProcedure", "MedicalTherapy", str]],
            "MedicalTest",
            "MedicalProcedure",
            "MedicalTherapy",
            str,
        ]
    ] = Field(
        default=None,
        description="A medical service available from this provider.",
    )


if TYPE_CHECKING:
    from pydantic2_schemaorg.MedicalSpecialty import MedicalSpecialty
    from pydantic2_schemaorg.Dataset import Dataset
    from pydantic2_schemaorg.CDCPMDRecord import CDCPMDRecord
    from pydantic2_schemaorg.MedicalTest import MedicalTest
    from pydantic2_schemaorg.MedicalProcedure import MedicalProcedure
    from pydantic2_schemaorg.MedicalTherapy import MedicalTherapy
