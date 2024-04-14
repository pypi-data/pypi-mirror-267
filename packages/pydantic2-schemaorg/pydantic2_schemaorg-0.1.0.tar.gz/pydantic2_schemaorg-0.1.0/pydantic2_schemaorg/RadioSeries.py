from __future__ import annotations

from typing import TYPE_CHECKING

from pydantic.v1 import AnyUrl
from pydantic.v1 import Field

from pydantic2_schemaorg.CreativeWorkSeries import CreativeWorkSeries


class RadioSeries(CreativeWorkSeries):
    """CreativeWorkSeries dedicated to radio broadcast and associated online delivery.

    See: https://schema.org/RadioSeries
    Model depth: 4
    """

    type_: str = Field(default="RadioSeries", alias="@type", const=True)
    musicBy: None | (
        list[MusicGroup | Person | str] | MusicGroup | Person | str
    ) = Field(
        default=None,
        description="The composer of the soundtrack.",
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
    numberOfEpisodes: None | (list[int | Integer | str] | int | Integer | str) = Field(
        default=None,
        description="The number of episodes in this season or series.",
    )
    episodes: list[Episode | str] | Episode | str | None = Field(
        default=None,
        description="An episode of a TV/radio series or season.",
    )
    actor: list[Person | str] | Person | str | None = Field(
        default=None,
        description="An actor, e.g. in TV, radio, movie, video games etc., or in an event. Actors can be associated"
        "with individual items or with a series, episode, clip.",
    )
    directors: list[Person | str] | Person | str | None = Field(
        default=None,
        description="A director of e.g. TV, radio, movie, video games etc. content. Directors can be associated"
        "with individual items or with a series, episode, clip.",
    )
    season: None | (
        list[AnyUrl | URL | CreativeWorkSeason | str]
        | AnyUrl
        | URL
        | CreativeWorkSeason
        | str
    ) = Field(
        default=None,
        description="A season in a media series.",
    )
    productionCompany: None | (list[Organization | str] | Organization | str) = Field(
        default=None,
        description="The production company or studio responsible for the item, e.g. series, video game,"
        "episode etc.",
    )
    episode: list[Episode | str] | Episode | str | None = Field(
        default=None,
        description="An episode of a TV, radio or game media within a series or season.",
    )
    numberOfSeasons: None | (list[int | Integer | str] | int | Integer | str) = Field(
        default=None,
        description="The number of seasons in this series.",
    )
    containsSeason: None | (
        list[CreativeWorkSeason | str] | CreativeWorkSeason | str
    ) = Field(
        default=None,
        description="A season that is part of the media series.",
    )
    actors: list[Person | str] | Person | str | None = Field(
        default=None,
        description="An actor, e.g. in TV, radio, movie, video games etc. Actors can be associated with individual"
        "items or with a series, episode, clip.",
    )
    seasons: None | (list[CreativeWorkSeason | str] | CreativeWorkSeason | str) = Field(
        default=None,
        description="A season in a media series.",
    )


if TYPE_CHECKING:
    from pydantic2_schemaorg.MusicGroup import MusicGroup
    from pydantic2_schemaorg.Person import Person
    from pydantic2_schemaorg.VideoObject import VideoObject
    from pydantic2_schemaorg.Integer import Integer
    from pydantic2_schemaorg.Episode import Episode
    from pydantic2_schemaorg.URL import URL
    from pydantic2_schemaorg.CreativeWorkSeason import CreativeWorkSeason
    from pydantic2_schemaorg.Organization import Organization
