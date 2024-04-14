from __future__ import annotations

from typing import TYPE_CHECKING

from pydantic.v1 import Field

from pydantic2_schemaorg.MedicalIntangible import MedicalIntangible


class DDxElement(MedicalIntangible):
    """An alternative, closely-related condition typically considered later in the differential"
     "diagnosis process along with the signs that are used to distinguish it.

    See: https://schema.org/DDxElement
    Model depth: 4
    """

    type_: str = Field(default="DDxElement", alias="@type", const=True)
    distinguishingSign: None | (
        list[MedicalSignOrSymptom | str] | MedicalSignOrSymptom | str
    ) = Field(
        default=None,
        description="One of a set of signs and symptoms that can be used to distinguish this diagnosis from others"
        "in the differential diagnosis.",
    )
    diagnosis: None | (list[MedicalCondition | str] | MedicalCondition | str) = Field(
        default=None,
        description="One or more alternative conditions considered in the differential diagnosis process"
        "as output of a diagnosis process.",
    )


if TYPE_CHECKING:
    from pydantic2_schemaorg.MedicalSignOrSymptom import MedicalSignOrSymptom
    from pydantic2_schemaorg.MedicalCondition import MedicalCondition
