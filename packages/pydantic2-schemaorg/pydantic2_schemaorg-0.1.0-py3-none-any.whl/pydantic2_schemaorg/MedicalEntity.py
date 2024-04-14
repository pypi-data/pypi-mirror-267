from __future__ import annotations

from typing import TYPE_CHECKING

from pydantic.v1 import Field

from pydantic2_schemaorg.Thing import Thing


class MedicalEntity(Thing):
    """The most generic type of entity related to health and the practice of medicine.

    See: https://schema.org/MedicalEntity
    Model depth: 2
    """

    type_: str = Field(default="MedicalEntity", alias="@type", const=True)
    funding: list[Grant | str] | Grant | str | None = Field(
        default=None,
        description="A [[Grant]] that directly or indirectly provide funding or sponsorship for this item."
        "See also [[ownershipFundingInfo]].",
    )
    code: list[MedicalCode | str] | MedicalCode | str | None = Field(
        default=None,
        description="A medical code for the entity, taken from a controlled vocabulary or ontology such as"
        "ICD-9, DiseasesDB, MeSH, SNOMED-CT, RxNorm, etc.",
    )
    guideline: None | (list[MedicalGuideline | str] | MedicalGuideline | str) = Field(
        default=None,
        description="A medical guideline related to this entity.",
    )
    recognizingAuthority: None | (
        list[Organization | str] | Organization | str
    ) = Field(
        default=None,
        description="If applicable, the organization that officially recognizes this entity as part of its"
        "endorsed system of medicine.",
    )
    study: None | (list[MedicalStudy | str] | MedicalStudy | str) = Field(
        default=None,
        description="A medical study or trial related to this entity.",
    )
    medicineSystem: None | (list[MedicineSystem | str] | MedicineSystem | str) = Field(
        default=None,
        description="The system of medicine that includes this MedicalEntity, for example 'evidence-based',"
        "'homeopathic', 'chiropractic', etc.",
    )
    relevantSpecialty: None | (
        list[MedicalSpecialty | str] | MedicalSpecialty | str
    ) = Field(
        default=None,
        description="If applicable, a medical specialty in which this entity is relevant.",
    )
    legalStatus: None | (
        list[str | Text | MedicalEnumeration | DrugLegalStatus]
        | str
        | Text
        | MedicalEnumeration
        | DrugLegalStatus
    ) = Field(
        default=None,
        description="The drug or supplement's legal status, including any controlled substance schedules"
        "that apply.",
    )


if TYPE_CHECKING:
    from pydantic2_schemaorg.Grant import Grant
    from pydantic2_schemaorg.MedicalCode import MedicalCode
    from pydantic2_schemaorg.MedicalGuideline import MedicalGuideline
    from pydantic2_schemaorg.Organization import Organization
    from pydantic2_schemaorg.MedicalStudy import MedicalStudy
    from pydantic2_schemaorg.MedicineSystem import MedicineSystem
    from pydantic2_schemaorg.MedicalSpecialty import MedicalSpecialty
    from pydantic2_schemaorg.Text import Text
    from pydantic2_schemaorg.MedicalEnumeration import MedicalEnumeration
    from pydantic2_schemaorg.DrugLegalStatus import DrugLegalStatus
