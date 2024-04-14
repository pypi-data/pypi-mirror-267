from __future__ import annotations

from typing import TYPE_CHECKING

from pydantic.v1 import Field
from pydantic.v1 import StrictFloat
from pydantic.v1 import StrictInt

from pydantic2_schemaorg.CreativeWork import CreativeWork


class Clip(CreativeWork):
    """A short TV or radio program or a segment/part of a program.

    See: https://schema.org/Clip
    Model depth: 3
    """

    type_: str = Field(default="Clip", alias="@type", const=True)
    musicBy: None | (
        list[MusicGroup | Person | str] | MusicGroup | Person | str
    ) = Field(
        default=None,
        description="The composer of the soundtrack.",
    )
    partOfSeason: None | (
        list[CreativeWorkSeason | str] | CreativeWorkSeason | str
    ) = Field(
        default=None,
        description="The season to which this episode belongs.",
    )
    director: list[Person | str] | Person | str | None = Field(
        default=None,
        description="A director of e.g. TV, radio, movie, video gaming etc. content, or of an event. Directors"
        "can be associated with individual items or with a series, episode, clip.",
    )
    partOfEpisode: list[Episode | str] | Episode | str | None = Field(
        default=None,
        description="The episode to which this clip belongs.",
    )
    clipNumber: None | (
        list[int | Integer | str | Text] | int | Integer | str | Text
    ) = Field(
        default=None,
        description="Position of the clip within an ordered group of clips.",
    )
    endOffset: None | (
        list[StrictInt | StrictFloat | Number | HyperTocEntry | str]
        | StrictInt
        | StrictFloat
        | Number
        | HyperTocEntry
        | str
    ) = Field(
        default=None,
        description="The end time of the clip expressed as the number of seconds from the beginning of the work.",
    )
    actor: list[Person | str] | Person | str | None = Field(
        default=None,
        description="An actor, e.g. in TV, radio, movie, video games etc., or in an event. Actors can be associated"
        "with individual items or with a series, episode, clip.",
    )
    partOfSeries: None | (
        list[CreativeWorkSeries | str] | CreativeWorkSeries | str
    ) = Field(
        default=None,
        description="The series to which this episode or season belongs.",
    )
    directors: list[Person | str] | Person | str | None = Field(
        default=None,
        description="A director of e.g. TV, radio, movie, video games etc. content. Directors can be associated"
        "with individual items or with a series, episode, clip.",
    )
    actors: list[Person | str] | Person | str | None = Field(
        default=None,
        description="An actor, e.g. in TV, radio, movie, video games etc. Actors can be associated with individual"
        "items or with a series, episode, clip.",
    )
    startOffset: None | (
        list[StrictInt | StrictFloat | Number | HyperTocEntry | str]
        | StrictInt
        | StrictFloat
        | Number
        | HyperTocEntry
        | str
    ) = Field(
        default=None,
        description="The start time of the clip expressed as the number of seconds from the beginning of the"
        "work.",
    )


if TYPE_CHECKING:
    from pydantic2_schemaorg.MusicGroup import MusicGroup
    from pydantic2_schemaorg.Person import Person
    from pydantic2_schemaorg.CreativeWorkSeason import CreativeWorkSeason
    from pydantic2_schemaorg.Episode import Episode
    from pydantic2_schemaorg.Integer import Integer
    from pydantic2_schemaorg.Text import Text
    from pydantic2_schemaorg.Number import Number
    from pydantic2_schemaorg.HyperTocEntry import HyperTocEntry
    from pydantic2_schemaorg.CreativeWorkSeries import CreativeWorkSeries
