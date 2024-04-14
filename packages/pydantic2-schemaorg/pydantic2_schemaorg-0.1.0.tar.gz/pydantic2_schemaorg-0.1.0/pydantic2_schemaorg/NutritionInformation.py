from __future__ import annotations

from typing import TYPE_CHECKING

from pydantic.v1 import Field

from pydantic2_schemaorg.StructuredValue import StructuredValue


class NutritionInformation(StructuredValue):
    """Nutritional information about the recipe.

    See: https://schema.org/NutritionInformation
    Model depth: 4
    """

    type_: str = Field(default="NutritionInformation", alias="@type", const=True)
    fiberContent: list[Mass | str] | Mass | str | None = Field(
        default=None,
        description="The number of grams of fiber.",
    )
    servingSize: list[str | Text] | str | Text | None = Field(
        default=None,
        description="The serving size, in terms of the number of volume or mass.",
    )
    sodiumContent: list[Mass | str] | Mass | str | None = Field(
        default=None,
        description="The number of milligrams of sodium.",
    )
    calories: list[Energy | str] | Energy | str | None = Field(
        default=None,
        description="The number of calories.",
    )
    proteinContent: list[Mass | str] | Mass | str | None = Field(
        default=None,
        description="The number of grams of protein.",
    )
    transFatContent: list[Mass | str] | Mass | str | None = Field(
        default=None,
        description="The number of grams of trans fat.",
    )
    carbohydrateContent: list[Mass | str] | Mass | str | None = Field(
        default=None,
        description="The number of grams of carbohydrates.",
    )
    sugarContent: list[Mass | str] | Mass | str | None = Field(
        default=None,
        description="The number of grams of sugar.",
    )
    saturatedFatContent: list[Mass | str] | Mass | str | None = Field(
        default=None,
        description="The number of grams of saturated fat.",
    )
    cholesterolContent: list[Mass | str] | Mass | str | None = Field(
        default=None,
        description="The number of milligrams of cholesterol.",
    )
    fatContent: list[Mass | str] | Mass | str | None = Field(
        default=None,
        description="The number of grams of fat.",
    )
    unsaturatedFatContent: None | (list[Mass | str] | Mass | str) = Field(
        default=None,
        description="The number of grams of unsaturated fat.",
    )


if TYPE_CHECKING:
    from pydantic2_schemaorg.Mass import Mass
    from pydantic2_schemaorg.Text import Text
    from pydantic2_schemaorg.Energy import Energy
