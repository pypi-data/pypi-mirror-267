from __future__ import annotations

from typing import TYPE_CHECKING

from pydantic.v1 import AnyUrl
from pydantic.v1 import Field

from pydantic2_schemaorg.Intangible import Intangible


class HealthInsurancePlan(Intangible):
    """A US-style health insurance plan, including PPOs, EPOs, and HMOs.

    See: https://schema.org/HealthInsurancePlan
    Model depth: 3
    """

    type_: str = Field(default="HealthInsurancePlan", alias="@type", const=True)
    healthPlanDrugTier: list[str | Text] | str | Text | None = Field(
        default=None,
        description="The tier(s) of drugs offered by this formulary or insurance plan.",
    )
    includesHealthPlanNetwork: None | (
        list[HealthPlanNetwork | str] | HealthPlanNetwork | str
    ) = Field(
        default=None,
        description="Networks covered by this plan.",
    )
    healthPlanId: list[str | Text] | str | Text | None = Field(
        default=None,
        description="The 14-character, HIOS-generated Plan ID number. (Plan IDs must be unique, even across"
        "different markets.)",
    )
    usesHealthPlanIdStandard: None | (
        list[AnyUrl | URL | str | Text] | AnyUrl | URL | str | Text
    ) = Field(
        default=None,
        description='The standard for interpreting the Plan ID. The preferred is "HIOS". See the Centers'
        "for Medicare & Medicaid Services for more details.",
    )
    contactPoint: None | (list[ContactPoint | str] | ContactPoint | str) = Field(
        default=None,
        description="A contact point for a person or organization.",
    )
    includesHealthPlanFormulary: None | (
        list[HealthPlanFormulary | str] | HealthPlanFormulary | str
    ) = Field(
        default=None,
        description="Formularies covered by this plan.",
    )
    healthPlanMarketingUrl: None | (
        list[AnyUrl | URL | str] | AnyUrl | URL | str
    ) = Field(
        default=None,
        description="The URL that goes directly to the plan brochure for the specific standard plan or plan"
        "variation.",
    )
    healthPlanDrugOption: None | (list[str | Text] | str | Text) = Field(
        default=None,
        description="TODO.",
    )
    benefitsSummaryUrl: None | (list[AnyUrl | URL | str] | AnyUrl | URL | str) = Field(
        default=None,
        description="The URL that goes directly to the summary of benefits and coverage for the specific standard"
        "plan or plan variation.",
    )


if TYPE_CHECKING:
    from pydantic2_schemaorg.Text import Text
    from pydantic2_schemaorg.HealthPlanNetwork import HealthPlanNetwork
    from pydantic2_schemaorg.URL import URL
    from pydantic2_schemaorg.ContactPoint import ContactPoint
    from pydantic2_schemaorg.HealthPlanFormulary import HealthPlanFormulary
