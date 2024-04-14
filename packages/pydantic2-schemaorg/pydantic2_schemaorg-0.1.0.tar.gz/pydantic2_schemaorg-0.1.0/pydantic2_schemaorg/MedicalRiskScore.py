from __future__ import annotations

from typing import TYPE_CHECKING

from pydantic.v1 import Field

from pydantic2_schemaorg.MedicalRiskEstimator import MedicalRiskEstimator


class MedicalRiskScore(MedicalRiskEstimator):
    """A simple system that adds up the number of risk factors to yield a score that is associated"
     "with prognosis, e.g. CHAD score, TIMI risk score.

    See: https://schema.org/MedicalRiskScore
    Model depth: 4
    """

    type_: str = Field(default="MedicalRiskScore", alias="@type", const=True)
    algorithm: list[str | Text] | str | Text | None = Field(
        default=None,
        description="The algorithm or rules to follow to compute the score.",
    )


if TYPE_CHECKING:
    from pydantic2_schemaorg.Text import Text
