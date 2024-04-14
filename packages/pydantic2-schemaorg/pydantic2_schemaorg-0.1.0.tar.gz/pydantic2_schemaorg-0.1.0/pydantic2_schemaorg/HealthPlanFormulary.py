from __future__ import annotations

from typing import TYPE_CHECKING

from pydantic.v1 import Field
from pydantic.v1 import StrictBool

from pydantic2_schemaorg.Intangible import Intangible


class HealthPlanFormulary(Intangible):
    """For a given health insurance plan, the specification for costs and coverage of prescription"
     "drugs.

    See: https://schema.org/HealthPlanFormulary
    Model depth: 3
    """

    type_: str = Field(default="HealthPlanFormulary", alias="@type", const=True)
    healthPlanCostSharing: None | (
        list[StrictBool | Boolean | str] | StrictBool | Boolean | str
    ) = Field(
        default=None,
        description="The costs to the patient for services under this network or formulary.",
    )
    healthPlanDrugTier: list[str | Text] | str | Text | None = Field(
        default=None,
        description="The tier(s) of drugs offered by this formulary or insurance plan.",
    )
    offersPrescriptionByMail: None | (
        list[StrictBool | Boolean | str] | StrictBool | Boolean | str
    ) = Field(
        default=None,
        description="Whether prescriptions can be delivered by mail.",
    )


if TYPE_CHECKING:
    from pydantic2_schemaorg.Boolean import Boolean
    from pydantic2_schemaorg.Text import Text
