from __future__ import annotations

from typing import TYPE_CHECKING

from pydantic.v1 import Field

from pydantic2_schemaorg.PlayAction import PlayAction


class ExerciseAction(PlayAction):
    """The act of participating in exertive activity for the purposes of improving health and"
     "fitness.

    See: https://schema.org/ExerciseAction
    Model depth: 4
    """

    type_: str = Field(default="ExerciseAction", alias="@type", const=True)
    sportsTeam: None | (list[SportsTeam | str] | SportsTeam | str) = Field(
        default=None,
        description="A sub property of participant. The sports team that participated on this action.",
    )
    toLocation: list[Place | str] | Place | str | None = Field(
        default=None,
        description="A sub property of location. The final location of the object or the agent after the action.",
    )
    opponent: list[Person | str] | Person | str | None = Field(
        default=None,
        description="A sub property of participant. The opponent on this action.",
    )
    sportsActivityLocation: None | (
        list[SportsActivityLocation | str] | SportsActivityLocation | str
    ) = Field(
        default=None,
        description="A sub property of location. The sports activity location where this action occurred.",
    )
    fromLocation: list[Place | str] | Place | str | None = Field(
        default=None,
        description="A sub property of location. The original location of the object or the agent before the"
        "action.",
    )
    exerciseType: list[str | Text] | str | Text | None = Field(
        default=None,
        description="Type(s) of exercise or activity, such as strength training, flexibility training,"
        "aerobics, cardiac rehabilitation, etc.",
    )
    exerciseRelatedDiet: list[Diet | str] | Diet | str | None = Field(
        default=None,
        description="A sub property of instrument. The diet used in this action.",
    )
    exerciseCourse: list[Place | str] | Place | str | None = Field(
        default=None,
        description="A sub property of location. The course where this action was taken.",
    )
    course: list[Place | str] | Place | str | None = Field(
        default=None,
        description="A sub property of location. The course where this action was taken.",
    )
    exercisePlan: None | (list[ExercisePlan | str] | ExercisePlan | str) = Field(
        default=None,
        description="A sub property of instrument. The exercise plan used on this action.",
    )
    distance: list[Distance | str] | Distance | str | None = Field(
        default=None,
        description="The distance travelled, e.g. exercising or travelling.",
    )
    diet: list[Diet | str] | Diet | str | None = Field(
        default=None,
        description="A sub property of instrument. The diet used in this action.",
    )
    sportsEvent: None | (list[SportsEvent | str] | SportsEvent | str) = Field(
        default=None,
        description="A sub property of location. The sports event where this action occurred.",
    )


if TYPE_CHECKING:
    from pydantic2_schemaorg.SportsTeam import SportsTeam
    from pydantic2_schemaorg.Place import Place
    from pydantic2_schemaorg.Person import Person
    from pydantic2_schemaorg.SportsActivityLocation import SportsActivityLocation
    from pydantic2_schemaorg.Text import Text
    from pydantic2_schemaorg.Diet import Diet
    from pydantic2_schemaorg.ExercisePlan import ExercisePlan
    from pydantic2_schemaorg.Distance import Distance
    from pydantic2_schemaorg.SportsEvent import SportsEvent
