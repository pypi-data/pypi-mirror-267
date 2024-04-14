from __future__ import annotations

from typing import TYPE_CHECKING

from pydantic.v1 import Field
from pydantic.v1 import StrictBool

from pydantic2_schemaorg.Product import Product
from pydantic2_schemaorg.Substance import Substance


class DietarySupplement(Substance, Product):
    """A product taken by mouth that contains a dietary ingredient intended to supplement the"
     "diet. Dietary ingredients may include vitamins, minerals, herbs or other botanicals,"
     "amino acids, and substances such as enzymes, organ tissues, glandulars and metabolites.

    See: https://schema.org/DietarySupplement
    Model depth: 3
    """

    type_: str = Field(default="DietarySupplement", alias="@type", const=True)
    recommendedIntake: None | (
        list[RecommendedDoseSchedule | str] | RecommendedDoseSchedule | str
    ) = Field(
        default=None,
        description="Recommended intake of this supplement for a given population as defined by a specific"
        "recommending authority.",
    )
    proprietaryName: list[str | Text] | str | Text | None = Field(
        default=None,
        description="Proprietary name given to the diet plan, typically by its originator or creator.",
    )
    safetyConsideration: list[str | Text] | str | Text | None = Field(
        default=None,
        description="Any potential safety concern associated with the supplement. May include interactions"
        "with other drugs and foods, pregnancy, breastfeeding, known adverse reactions, and"
        "documented efficacy of the supplement.",
    )
    isProprietary: None | (
        list[StrictBool | Boolean | str] | StrictBool | Boolean | str
    ) = Field(
        default=None,
        description="True if this item's name is a proprietary/brand name (vs. generic name).",
    )
    activeIngredient: list[str | Text] | str | Text | None = Field(
        default=None,
        description="An active ingredient, typically chemical compounds and/or biologic substances.",
    )
    nonProprietaryName: list[str | Text] | str | Text | None = Field(
        default=None,
        description="The generic name of this drug or supplement.",
    )
    maximumIntake: None | (
        list[MaximumDoseSchedule | str] | MaximumDoseSchedule | str
    ) = Field(
        default=None,
        description="Recommended intake of this supplement for a given population as defined by a specific"
        "recommending authority.",
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
    mechanismOfAction: list[str | Text] | str | Text | None = Field(
        default=None,
        description="The specific biochemical interaction through which this drug or supplement produces"
        "its pharmacological effect.",
    )
    targetPopulation: list[str | Text] | str | Text | None = Field(
        default=None,
        description="Characteristics of the population for which this is intended, or which typically uses"
        "it, e.g. 'adults'.",
    )


if TYPE_CHECKING:
    from pydantic2_schemaorg.RecommendedDoseSchedule import RecommendedDoseSchedule
    from pydantic2_schemaorg.Text import Text
    from pydantic2_schemaorg.Boolean import Boolean
    from pydantic2_schemaorg.MaximumDoseSchedule import MaximumDoseSchedule
    from pydantic2_schemaorg.MedicalEnumeration import MedicalEnumeration
    from pydantic2_schemaorg.DrugLegalStatus import DrugLegalStatus
