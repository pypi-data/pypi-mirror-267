from __future__ import annotations

from datetime import date
from typing import TYPE_CHECKING

from pydantic.v1 import Field

from pydantic2_schemaorg.MedicalEntity import MedicalEntity


class MedicalGuideline(MedicalEntity):
    """Any recommendation made by a standard society (e.g. ACC/AHA) or consensus statement"
     "that denotes how to diagnose and treat a particular condition. Note: this type should"
     "be used to tag the actual guideline recommendation; if the guideline recommendation"
     "occurs in a larger scholarly article, use MedicalScholarlyArticle to tag the overall"
     "article, not this type. Note also: the organization making the recommendation should"
     "be captured in the recognizingAuthority base property of MedicalEntity.

    See: https://schema.org/MedicalGuideline
    Model depth: 3
    """

    type_: str = Field(default="MedicalGuideline", alias="@type", const=True)
    evidenceLevel: None | (
        list[MedicalEvidenceLevel | str] | MedicalEvidenceLevel | str
    ) = Field(
        default=None,
        description="Strength of evidence of the data used to formulate the guideline (enumerated).",
    )
    guidelineSubject: None | (list[MedicalEntity | str] | MedicalEntity | str) = Field(
        default=None,
        description="The medical conditions, treatments, etc. that are the subject of the guideline.",
    )
    guidelineDate: None | (list[date | Date | str] | date | Date | str) = Field(
        default=None,
        description="Date on which this guideline's recommendation was made.",
    )
    evidenceOrigin: list[str | Text] | str | Text | None = Field(
        default=None,
        description="Source of the data used to formulate the guidance, e.g. RCT, consensus opinion, etc.",
    )


if TYPE_CHECKING:
    from pydantic2_schemaorg.MedicalEvidenceLevel import MedicalEvidenceLevel
    from pydantic2_schemaorg.MedicalEntity import MedicalEntity
    from pydantic2_schemaorg.Date import Date
    from pydantic2_schemaorg.Text import Text
