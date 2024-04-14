from __future__ import annotations

from typing import TYPE_CHECKING

from pydantic.v1 import Field
from pydantic.v1 import StrictBool

from pydantic2_schemaorg.Intangible import Intangible


class HealthPlanNetwork(Intangible):
    """A US-style health insurance plan network.

    See: https://schema.org/HealthPlanNetwork
    Model depth: 3
    """

    type_: str = Field(default="HealthPlanNetwork", alias="@type", const=True)
    healthPlanCostSharing: None | (
        list[StrictBool | Boolean | str] | StrictBool | Boolean | str
    ) = Field(
        default=None,
        description="The costs to the patient for services under this network or formulary.",
    )
    healthPlanNetworkId: list[str | Text] | str | Text | None = Field(
        default=None,
        description="Name or unique ID of network. (Networks are often reused across different insurance"
        "plans.)",
    )
    healthPlanNetworkTier: None | (list[str | Text] | str | Text) = Field(
        default=None,
        description="The tier(s) for this network.",
    )


if TYPE_CHECKING:
    from pydantic2_schemaorg.Boolean import Boolean
    from pydantic2_schemaorg.Text import Text
