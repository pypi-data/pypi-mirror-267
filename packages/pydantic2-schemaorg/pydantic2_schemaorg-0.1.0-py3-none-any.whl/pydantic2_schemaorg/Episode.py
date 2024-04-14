from __future__ import annotations

from typing import TYPE_CHECKING

from pydantic.v1 import Field

from pydantic2_schemaorg.CreativeWork import CreativeWork


class Episode(CreativeWork):
    """A media episode (e.g. TV, radio, video game) which can be part of a series or season.

    See: https://schema.org/Episode
    Model depth: 3
    """

    type_: str = Field(default="Episode", alias="@type", const=True)
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
    trailer: None | (list[VideoObject | str] | VideoObject | str) = Field(
        default=None,
        description="The trailer of a movie or TV/radio series, season, episode, etc.",
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
    duration: list[Duration | str] | Duration | str | None = Field(
        default=None,
        description="The duration of the item (movie, audio recording, event, etc.) in [ISO 8601 date format](http://en.wikipedia.org/wiki/ISO_8601).",
    )
    directors: list[Person | str] | Person | str | None = Field(
        default=None,
        description="A director of e.g. TV, radio, movie, video games etc. content. Directors can be associated"
        "with individual items or with a series, episode, clip.",
    )
    productionCompany: None | (list[Organization | str] | Organization | str) = Field(
        default=None,
        description="The production company or studio responsible for the item, e.g. series, video game,"
        "episode etc.",
    )
    episodeNumber: None | (
        list[int | Integer | str | Text] | int | Integer | str | Text
    ) = Field(
        default=None,
        description="Position of the episode within an ordered group of episodes.",
    )
    actors: list[Person | str] | Person | str | None = Field(
        default=None,
        description="An actor, e.g. in TV, radio, movie, video games etc. Actors can be associated with individual"
        "items or with a series, episode, clip.",
    )


if TYPE_CHECKING:
    from pydantic2_schemaorg.MusicGroup import MusicGroup
    from pydantic2_schemaorg.Person import Person
    from pydantic2_schemaorg.CreativeWorkSeason import CreativeWorkSeason
    from pydantic2_schemaorg.VideoObject import VideoObject
    from pydantic2_schemaorg.CreativeWorkSeries import CreativeWorkSeries
    from pydantic2_schemaorg.Duration import Duration
    from pydantic2_schemaorg.Organization import Organization
    from pydantic2_schemaorg.Integer import Integer
    from pydantic2_schemaorg.Text import Text
