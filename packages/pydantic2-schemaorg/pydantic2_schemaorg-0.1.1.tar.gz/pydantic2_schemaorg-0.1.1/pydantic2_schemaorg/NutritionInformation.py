from __future__ import annotations
from typing import TYPE_CHECKING

from typing import List, Optional, Union


from pydantic.v1 import Field
from pydantic2_schemaorg.StructuredValue import StructuredValue


class NutritionInformation(StructuredValue):
    """Nutritional information about the recipe.

    See: https://schema.org/NutritionInformation
    Model depth: 4
    """

    type_: str = Field(default="NutritionInformation", alias="@type", const=True)
    fiberContent: Optional[Union[List[Union["Mass", str]], "Mass", str]] = Field(
        default=None,
        description="The number of grams of fiber.",
    )
    servingSize: Optional[Union[List[Union[str, "Text"]], str, "Text"]] = Field(
        default=None,
        description="The serving size, in terms of the number of volume or mass.",
    )
    sodiumContent: Optional[Union[List[Union["Mass", str]], "Mass", str]] = Field(
        default=None,
        description="The number of milligrams of sodium.",
    )
    calories: Optional[Union[List[Union["Energy", str]], "Energy", str]] = Field(
        default=None,
        description="The number of calories.",
    )
    proteinContent: Optional[Union[List[Union["Mass", str]], "Mass", str]] = Field(
        default=None,
        description="The number of grams of protein.",
    )
    transFatContent: Optional[Union[List[Union["Mass", str]], "Mass", str]] = Field(
        default=None,
        description="The number of grams of trans fat.",
    )
    carbohydrateContent: Optional[Union[List[Union["Mass", str]], "Mass", str]] = Field(
        default=None,
        description="The number of grams of carbohydrates.",
    )
    sugarContent: Optional[Union[List[Union["Mass", str]], "Mass", str]] = Field(
        default=None,
        description="The number of grams of sugar.",
    )
    saturatedFatContent: Optional[Union[List[Union["Mass", str]], "Mass", str]] = Field(
        default=None,
        description="The number of grams of saturated fat.",
    )
    cholesterolContent: Optional[Union[List[Union["Mass", str]], "Mass", str]] = Field(
        default=None,
        description="The number of milligrams of cholesterol.",
    )
    fatContent: Optional[Union[List[Union["Mass", str]], "Mass", str]] = Field(
        default=None,
        description="The number of grams of fat.",
    )
    unsaturatedFatContent: Optional[Union[List[Union["Mass", str]], "Mass", str]] = (
        Field(
            default=None,
            description="The number of grams of unsaturated fat.",
        )
    )


if TYPE_CHECKING:
    from pydantic2_schemaorg.Mass import Mass
    from pydantic2_schemaorg.Text import Text
    from pydantic2_schemaorg.Energy import Energy
