from __future__ import annotations

from typing import TYPE_CHECKING

from pydantic.v1 import AnyUrl
from pydantic.v1 import Field

from pydantic2_schemaorg.CreativeWorkSeries import CreativeWorkSeries


class VideoGameSeries(CreativeWorkSeries):
    """A video game series.

    See: https://schema.org/VideoGameSeries
    Model depth: 4
    """

    type_: str = Field(default="VideoGameSeries", alias="@type", const=True)
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
    numberOfPlayers: None | (
        list[QuantitativeValue | str] | QuantitativeValue | str
    ) = Field(
        default=None,
        description="Indicate how many people can play this game (minimum, maximum, or range).",
    )
    quest: list[Thing | str] | Thing | str | None = Field(
        default=None,
        description="The task that a player-controlled character, or group of characters may complete in"
        "order to gain a reward.",
    )
    gamePlatform: None | (
        list[AnyUrl | URL | str | Text | Thing] | AnyUrl | URL | str | Text | Thing
    ) = Field(
        default=None,
        description='The electronic systems used to play <a href="http://en.wikipedia.org/wiki/Category:Video_game_platforms">video'
        "games</a>.",
    )
    trailer: None | (list[VideoObject | str] | VideoObject | str) = Field(
        default=None,
        description="The trailer of a movie or TV/radio series, season, episode, etc.",
    )
    numberOfEpisodes: None | (list[int | Integer | str] | int | Integer | str) = Field(
        default=None,
        description="The number of episodes in this season or series.",
    )
    gameItem: list[Thing | str] | Thing | str | None = Field(
        default=None,
        description="An item is an object within the game world that can be collected by a player or, occasionally,"
        "a non-player character.",
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
    characterAttribute: None | (list[Thing | str] | Thing | str) = Field(
        default=None,
        description="A piece of data that represents a particular aspect of a fictional character (skill,"
        "power, character points, advantage, disadvantage).",
    )
    directors: list[Person | str] | Person | str | None = Field(
        default=None,
        description="A director of e.g. TV, radio, movie, video games etc. content. Directors can be associated"
        "with individual items or with a series, episode, clip.",
    )
    gameLocation: None | (
        list[AnyUrl | URL | PostalAddress | Place | str]
        | AnyUrl
        | URL
        | PostalAddress
        | Place
        | str
    ) = Field(
        default=None,
        description="Real or fictional location of the game (or part of game).",
    )
    playMode: None | (list[GamePlayMode | str] | GamePlayMode | str) = Field(
        default=None,
        description="Indicates whether this game is multi-player, co-op or single-player. The game can be"
        "marked as multi-player, co-op and single-player at the same time.",
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
    cheatCode: None | (list[CreativeWork | str] | CreativeWork | str) = Field(
        default=None,
        description="Cheat codes to the game.",
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
    from pydantic2_schemaorg.QuantitativeValue import QuantitativeValue
    from pydantic2_schemaorg.Thing import Thing
    from pydantic2_schemaorg.URL import URL
    from pydantic2_schemaorg.Text import Text
    from pydantic2_schemaorg.VideoObject import VideoObject
    from pydantic2_schemaorg.Integer import Integer
    from pydantic2_schemaorg.Episode import Episode
    from pydantic2_schemaorg.PostalAddress import PostalAddress
    from pydantic2_schemaorg.Place import Place
    from pydantic2_schemaorg.GamePlayMode import GamePlayMode
    from pydantic2_schemaorg.CreativeWorkSeason import CreativeWorkSeason
    from pydantic2_schemaorg.Organization import Organization
    from pydantic2_schemaorg.CreativeWork import CreativeWork
