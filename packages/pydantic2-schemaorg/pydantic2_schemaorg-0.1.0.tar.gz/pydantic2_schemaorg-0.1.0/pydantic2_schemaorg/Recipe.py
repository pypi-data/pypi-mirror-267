from __future__ import annotations

from typing import TYPE_CHECKING

from pydantic.v1 import Field

from pydantic2_schemaorg.HowTo import HowTo


class Recipe(HowTo):
    """A recipe. For dietary restrictions covered by the recipe, a few common restrictions"
     "are enumerated via [[suitableForDiet]]. The [[keywords]] property can also be used"
     "to add more detail.

    See: https://schema.org/Recipe
    Model depth: 4
    """

    type_: str = Field(default="Recipe", alias="@type", const=True)
    suitableForDiet: None | (list[RestrictedDiet | str] | RestrictedDiet | str) = Field(
        default=None,
        description="Indicates a dietary restriction or guideline for which this recipe or menu item is suitable,"
        "e.g. diabetic, halal etc.",
    )
    cookTime: list[Duration | str] | Duration | str | None = Field(
        default=None,
        description="The time it takes to actually cook the dish, in [ISO 8601 duration format](http://en.wikipedia.org/wiki/ISO_8601).",
    )
    recipeInstructions: None | (
        list[str | Text | CreativeWork | ItemList]
        | str
        | Text
        | CreativeWork
        | ItemList
    ) = Field(
        default=None,
        description="A step in making the recipe, in the form of a single item (document, video, etc.) or an ordered"
        "list with HowToStep and/or HowToSection items.",
    )
    recipeIngredient: list[str | Text] | str | Text | None = Field(
        default=None,
        description="A single ingredient used in the recipe, e.g. sugar, flour or garlic.",
    )
    recipeCategory: list[str | Text] | str | Text | None = Field(
        default=None,
        description="The category of the recipe—for example, appetizer, entree, etc.",
    )
    nutrition: None | (
        list[NutritionInformation | str] | NutritionInformation | str
    ) = Field(
        default=None,
        description="Nutrition information about the recipe or menu item.",
    )
    recipeYield: None | (
        list[str | Text | QuantitativeValue] | str | Text | QuantitativeValue
    ) = Field(
        default=None,
        description="The quantity produced by the recipe (for example, number of people served, number of"
        "servings, etc).",
    )
    recipeCuisine: list[str | Text] | str | Text | None = Field(
        default=None,
        description="The cuisine of the recipe (for example, French or Ethiopian).",
    )
    cookingMethod: list[str | Text] | str | Text | None = Field(
        default=None,
        description="The method of cooking, such as Frying, Steaming, ...",
    )
    ingredients: list[str | Text] | str | Text | None = Field(
        default=None,
        description="A single ingredient used in the recipe, e.g. sugar, flour or garlic.",
    )


if TYPE_CHECKING:
    from pydantic2_schemaorg.RestrictedDiet import RestrictedDiet
    from pydantic2_schemaorg.Duration import Duration
    from pydantic2_schemaorg.Text import Text
    from pydantic2_schemaorg.CreativeWork import CreativeWork
    from pydantic2_schemaorg.ItemList import ItemList
    from pydantic2_schemaorg.NutritionInformation import NutritionInformation
    from pydantic2_schemaorg.QuantitativeValue import QuantitativeValue
