from __future__ import annotations

from typing import TYPE_CHECKING

from pydantic.v1 import Field
from pydantic.v1 import StrictFloat
from pydantic.v1 import StrictInt

from pydantic2_schemaorg.MedicalIntangible import MedicalIntangible


class DoseSchedule(MedicalIntangible):
    """A specific dosing schedule for a drug or supplement.

    See: https://schema.org/DoseSchedule
    Model depth: 4
    """

    type_: str = Field(default="DoseSchedule", alias="@type", const=True)
    frequency: list[str | Text] | str | Text | None = Field(
        default=None,
        description="How often the dose is taken, e.g. 'daily'.",
    )
    doseValue: None | (
        list[StrictInt | StrictFloat | Number | QualitativeValue | str]
        | StrictInt
        | StrictFloat
        | Number
        | QualitativeValue
        | str
    ) = Field(
        default=None,
        description="The value of the dose, e.g. 500.",
    )
    doseUnit: list[str | Text] | str | Text | None = Field(
        default=None,
        description="The unit of the dose, e.g. 'mg'.",
    )
    targetPopulation: list[str | Text] | str | Text | None = Field(
        default=None,
        description="Characteristics of the population for which this is intended, or which typically uses"
        "it, e.g. 'adults'.",
    )


if TYPE_CHECKING:
    from pydantic2_schemaorg.Text import Text
    from pydantic2_schemaorg.Number import Number
    from pydantic2_schemaorg.QualitativeValue import QualitativeValue
