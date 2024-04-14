from __future__ import annotations

from typing import TYPE_CHECKING

from pydantic.v1 import Field
from pydantic.v1 import StrictFloat
from pydantic.v1 import StrictInt

from pydantic2_schemaorg.MedicalIntangible import MedicalIntangible


class DrugStrength(MedicalIntangible):
    """A specific strength in which a medical drug is available in a specific country.

    See: https://schema.org/DrugStrength
    Model depth: 4
    """

    type_: str = Field(default="DrugStrength", alias="@type", const=True)
    availableIn: None | (
        list[AdministrativeArea | str] | AdministrativeArea | str
    ) = Field(
        default=None,
        description="The location in which the strength is available.",
    )
    strengthUnit: list[str | Text] | str | Text | None = Field(
        default=None,
        description="The units of an active ingredient's strength, e.g. mg.",
    )
    activeIngredient: list[str | Text] | str | Text | None = Field(
        default=None,
        description="An active ingredient, typically chemical compounds and/or biologic substances.",
    )
    maximumIntake: None | (
        list[MaximumDoseSchedule | str] | MaximumDoseSchedule | str
    ) = Field(
        default=None,
        description="Recommended intake of this supplement for a given population as defined by a specific"
        "recommending authority.",
    )
    strengthValue: None | (
        list[StrictInt | StrictFloat | Number | str]
        | StrictInt
        | StrictFloat
        | Number
        | str
    ) = Field(
        default=None,
        description="The value of an active ingredient's strength, e.g. 325.",
    )


if TYPE_CHECKING:
    from pydantic2_schemaorg.AdministrativeArea import AdministrativeArea
    from pydantic2_schemaorg.Text import Text
    from pydantic2_schemaorg.MaximumDoseSchedule import MaximumDoseSchedule
    from pydantic2_schemaorg.Number import Number
