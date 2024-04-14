from __future__ import annotations

from typing import TYPE_CHECKING

from pydantic.v1 import Field
from pydantic.v1 import StrictFloat
from pydantic.v1 import StrictInt

from pydantic2_schemaorg.CreativeWork import CreativeWork
from pydantic2_schemaorg.PhysicalActivity import PhysicalActivity


class ExercisePlan(PhysicalActivity, CreativeWork):
    """Fitness-related activity designed for a specific health-related purpose, including"
     "defined exercise routines as well as activity prescribed by a clinician.

    See: https://schema.org/ExercisePlan
    Model depth: 3
    """

    type_: str = Field(default="ExercisePlan", alias="@type", const=True)
    workload: None | (
        list[QuantitativeValue | Energy | str] | QuantitativeValue | Energy | str
    ) = Field(
        default=None,
        description="Quantitative measure of the physiologic output of the exercise; also referred to as"
        "energy expenditure.",
    )
    exerciseType: list[str | Text] | str | Text | None = Field(
        default=None,
        description="Type(s) of exercise or activity, such as strength training, flexibility training,"
        "aerobics, cardiac rehabilitation, etc.",
    )
    activityDuration: None | (
        list[QuantitativeValue | Duration | str] | QuantitativeValue | Duration | str
    ) = Field(
        default=None,
        description="Length of time to engage in the activity.",
    )
    additionalVariable: list[str | Text] | str | Text | None = Field(
        default=None,
        description="Any additional component of the exercise prescription that may need to be articulated"
        "to the patient. This may include the order of exercises, the number of repetitions of"
        "movement, quantitative distance, progressions over time, etc.",
    )
    intensity: None | (
        list[str | Text | QuantitativeValue] | str | Text | QuantitativeValue
    ) = Field(
        default=None,
        description="Quantitative measure gauging the degree of force involved in the exercise, for example,"
        "heartbeats per minute. May include the velocity of the movement.",
    )
    restPeriods: None | (
        list[str | Text | QuantitativeValue] | str | Text | QuantitativeValue
    ) = Field(
        default=None,
        description="How often one should break from the activity.",
    )
    repetitions: None | (
        list[StrictInt | StrictFloat | Number | QuantitativeValue | str]
        | StrictInt
        | StrictFloat
        | Number
        | QuantitativeValue
        | str
    ) = Field(
        default=None,
        description="Number of times one should repeat the activity.",
    )
    activityFrequency: None | (
        list[str | Text | QuantitativeValue] | str | Text | QuantitativeValue
    ) = Field(
        default=None,
        description="How often one should engage in the activity.",
    )


if TYPE_CHECKING:
    from pydantic2_schemaorg.QuantitativeValue import QuantitativeValue
    from pydantic2_schemaorg.Energy import Energy
    from pydantic2_schemaorg.Text import Text
    from pydantic2_schemaorg.Duration import Duration
    from pydantic2_schemaorg.Number import Number
