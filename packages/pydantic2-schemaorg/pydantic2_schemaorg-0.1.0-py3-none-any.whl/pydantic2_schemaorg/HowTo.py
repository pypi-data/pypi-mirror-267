from __future__ import annotations

from typing import TYPE_CHECKING

from pydantic.v1 import Field

from pydantic2_schemaorg.CreativeWork import CreativeWork


class HowTo(CreativeWork):
    """Instructions that explain how to achieve a result by performing a sequence of steps.

    See: https://schema.org/HowTo
    Model depth: 3
    """

    type_: str = Field(default="HowTo", alias="@type", const=True)
    supply: None | (list[str | Text | HowToSupply] | str | Text | HowToSupply) = Field(
        default=None,
        description="A sub-property of instrument. A supply consumed when performing instructions or a direction.",
    )
    steps: None | (
        list[str | Text | CreativeWork | ItemList]
        | str
        | Text
        | CreativeWork
        | ItemList
    ) = Field(
        default=None,
        description="A single step item (as HowToStep, text, document, video, etc.) or a HowToSection (originally"
        "misnamed 'steps'; 'step' is preferred).",
    )
    totalTime: list[Duration | str] | Duration | str | None = Field(
        default=None,
        description="The total time required to perform instructions or a direction (including time to prepare"
        "the supplies), in [ISO 8601 duration format](http://en.wikipedia.org/wiki/ISO_8601).",
    )
    tool: None | (list[str | Text | HowToTool] | str | Text | HowToTool) = Field(
        default=None,
        description="A sub property of instrument. An object used (but not consumed) when performing instructions"
        "or a direction.",
    )
    yield_: None | (
        list[str | Text | QuantitativeValue] | str | Text | QuantitativeValue
    ) = Field(
        default=None,
        alias="yield",
        description="The quantity that results by performing instructions. For example, a paper airplane,"
        "10 personalized candles.",
    )
    performTime: list[Duration | str] | Duration | str | None = Field(
        default=None,
        description="The length of time it takes to perform instructions or a direction (not including time"
        "to prepare the supplies), in [ISO 8601 duration format](http://en.wikipedia.org/wiki/ISO_8601).",
    )
    step: None | (
        list[str | Text | CreativeWork | HowToSection | HowToStep]
        | str
        | Text
        | CreativeWork
        | HowToSection
        | HowToStep
    ) = Field(
        default=None,
        description="A single step item (as HowToStep, text, document, video, etc.) or a HowToSection.",
    )
    estimatedCost: None | (
        list[str | Text | MonetaryAmount] | str | Text | MonetaryAmount
    ) = Field(
        default=None,
        description="The estimated cost of the supply or supplies consumed when performing instructions.",
    )
    prepTime: list[Duration | str] | Duration | str | None = Field(
        default=None,
        description="The length of time it takes to prepare the items to be used in instructions or a direction,"
        "in [ISO 8601 duration format](http://en.wikipedia.org/wiki/ISO_8601).",
    )


if TYPE_CHECKING:
    from pydantic2_schemaorg.Text import Text
    from pydantic2_schemaorg.HowToSupply import HowToSupply
    from pydantic2_schemaorg.CreativeWork import CreativeWork
    from pydantic2_schemaorg.ItemList import ItemList
    from pydantic2_schemaorg.Duration import Duration
    from pydantic2_schemaorg.HowToTool import HowToTool
    from pydantic2_schemaorg.QuantitativeValue import QuantitativeValue
    from pydantic2_schemaorg.HowToSection import HowToSection
    from pydantic2_schemaorg.HowToStep import HowToStep
    from pydantic2_schemaorg.MonetaryAmount import MonetaryAmount
