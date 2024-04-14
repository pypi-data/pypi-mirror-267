from __future__ import annotations

from typing import TYPE_CHECKING

from pydantic.v1 import Field

from pydantic2_schemaorg.CreativeWork import CreativeWork
from pydantic2_schemaorg.LifestyleModification import LifestyleModification


class Diet(LifestyleModification, CreativeWork):
    """A strategy of regulating the intake of food to achieve or maintain a specific health-related"
     "goal.

    See: https://schema.org/Diet
    Model depth: 3
    """

    type_: str = Field(default="Diet", alias="@type", const=True)
    expertConsiderations: None | (list[str | Text] | str | Text) = Field(
        default=None,
        description="Medical expert advice related to the plan.",
    )
    risks: list[str | Text] | str | Text | None = Field(
        default=None,
        description="Specific physiologic risks associated to the diet plan.",
    )
    dietFeatures: list[str | Text] | str | Text | None = Field(
        default=None,
        description="Nutritional information specific to the dietary plan. May include dietary recommendations"
        "on what foods to avoid, what foods to consume, and specific alterations/deviations"
        "from the USDA or other regulatory body's approved dietary guidelines.",
    )
    endorsers: None | (
        list[Organization | Person | str] | Organization | Person | str
    ) = Field(
        default=None,
        description="People or organizations that endorse the plan.",
    )
    physiologicalBenefits: None | (list[str | Text] | str | Text) = Field(
        default=None,
        description="Specific physiologic benefits associated to the plan.",
    )


if TYPE_CHECKING:
    from pydantic2_schemaorg.Text import Text
    from pydantic2_schemaorg.Organization import Organization
    from pydantic2_schemaorg.Person import Person
