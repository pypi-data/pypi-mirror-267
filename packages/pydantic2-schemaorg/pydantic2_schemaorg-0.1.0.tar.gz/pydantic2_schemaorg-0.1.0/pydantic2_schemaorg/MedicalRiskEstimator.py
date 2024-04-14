from __future__ import annotations

from typing import TYPE_CHECKING

from pydantic.v1 import Field

from pydantic2_schemaorg.MedicalEntity import MedicalEntity


class MedicalRiskEstimator(MedicalEntity):
    """Any rule set or interactive tool for estimating the risk of developing a complication"
     "or condition.

    See: https://schema.org/MedicalRiskEstimator
    Model depth: 3
    """

    type_: str = Field(default="MedicalRiskEstimator", alias="@type", const=True)
    includedRiskFactor: None | (
        list[MedicalRiskFactor | str] | MedicalRiskFactor | str
    ) = Field(
        default=None,
        description="A modifiable or non-modifiable risk factor included in the calculation, e.g. age, coexisting"
        "condition.",
    )
    estimatesRiskOf: None | (list[MedicalEntity | str] | MedicalEntity | str) = Field(
        default=None,
        description="The condition, complication, or symptom whose risk is being estimated.",
    )


if TYPE_CHECKING:
    from pydantic2_schemaorg.MedicalRiskFactor import MedicalRiskFactor
    from pydantic2_schemaorg.MedicalEntity import MedicalEntity
