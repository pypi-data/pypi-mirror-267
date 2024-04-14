from __future__ import annotations

from typing import TYPE_CHECKING

from pydantic.v1 import Field
from pydantic.v1 import StrictFloat
from pydantic.v1 import StrictInt

from pydantic2_schemaorg.Intangible import Intangible


class HealthPlanCostSharingSpecification(Intangible):
    """A description of costs to the patient under a given network or formulary.

    See: https://schema.org/HealthPlanCostSharingSpecification
    Model depth: 3
    """

    type_: str = Field(
        default="HealthPlanCostSharingSpecification", alias="@type", const=True
    )
    healthPlanCoinsuranceOption: None | (list[str | Text] | str | Text) = Field(
        default=None,
        description="Whether the coinsurance applies before or after deductible, etc. TODO: Is this a closed"
        "set?",
    )
    healthPlanCopay: None | (
        list[PriceSpecification | str] | PriceSpecification | str
    ) = Field(
        default=None,
        description="The copay amount.",
    )
    healthPlanPharmacyCategory: None | (list[str | Text] | str | Text) = Field(
        default=None,
        description="The category or type of pharmacy associated with this cost sharing.",
    )
    healthPlanCopayOption: None | (list[str | Text] | str | Text) = Field(
        default=None,
        description="Whether the copay is before or after deductible, etc. TODO: Is this a closed set?",
    )
    healthPlanCoinsuranceRate: None | (
        list[StrictInt | StrictFloat | Number | str]
        | StrictInt
        | StrictFloat
        | Number
        | str
    ) = Field(
        default=None,
        description="The rate of coinsurance expressed as a number between 0.0 and 1.0.",
    )


if TYPE_CHECKING:
    from pydantic2_schemaorg.Text import Text
    from pydantic2_schemaorg.PriceSpecification import PriceSpecification
    from pydantic2_schemaorg.Number import Number
