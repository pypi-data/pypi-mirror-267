from __future__ import annotations

from typing import TYPE_CHECKING

from pydantic.v1 import Field

from pydantic2_schemaorg.WebPage import WebPage


class MedicalWebPage(WebPage):
    """A web page that provides medical information.

    See: https://schema.org/MedicalWebPage
    Model depth: 4
    """

    type_: str = Field(default="MedicalWebPage", alias="@type", const=True)
    aspect: list[str | Text] | str | Text | None = Field(
        default=None,
        description="An aspect of medical practice that is considered on the page, such as 'diagnosis', 'treatment',"
        "'causes', 'prognosis', 'etiology', 'epidemiology', etc.",
    )
    medicalAudience: None | (
        list[MedicalAudience | MedicalAudienceType | str]
        | MedicalAudience
        | MedicalAudienceType
        | str
    ) = Field(
        default=None,
        description="Medical audience for page.",
    )


if TYPE_CHECKING:
    from pydantic2_schemaorg.Text import Text
    from pydantic2_schemaorg.MedicalAudience import MedicalAudience
    from pydantic2_schemaorg.MedicalAudienceType import MedicalAudienceType
