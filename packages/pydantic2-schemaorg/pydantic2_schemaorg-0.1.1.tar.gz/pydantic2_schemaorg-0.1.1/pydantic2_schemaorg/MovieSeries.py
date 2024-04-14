from __future__ import annotations
from typing import TYPE_CHECKING

from typing import List, Optional, Union


from pydantic.v1 import Field
from pydantic2_schemaorg.CreativeWorkSeries import CreativeWorkSeries


class MovieSeries(CreativeWorkSeries):
    """A series of movies. Included movies can be indicated with the hasPart property.

    See: https://schema.org/MovieSeries
    Model depth: 4
    """

    type_: str = Field(default="MovieSeries", alias="@type", const=True)
    musicBy: Optional[
        Union[List[Union["MusicGroup", "Person", str]], "MusicGroup", "Person", str]
    ] = Field(
        default=None,
        description="The composer of the soundtrack.",
    )
    director: Optional[Union[List[Union["Person", str]], "Person", str]] = Field(
        default=None,
        description="A director of e.g. TV, radio, movie, video gaming etc. content, or of an event. Directors"
        "can be associated with individual items or with a series, episode, clip.",
    )
    trailer: Optional[Union[List[Union["VideoObject", str]], "VideoObject", str]] = (
        Field(
            default=None,
            description="The trailer of a movie or TV/radio series, season, episode, etc.",
        )
    )
    actor: Optional[Union[List[Union["Person", str]], "Person", str]] = Field(
        default=None,
        description="An actor, e.g. in TV, radio, movie, video games etc., or in an event. Actors can be associated"
        "with individual items or with a series, episode, clip.",
    )
    directors: Optional[Union[List[Union["Person", str]], "Person", str]] = Field(
        default=None,
        description="A director of e.g. TV, radio, movie, video games etc. content. Directors can be associated"
        "with individual items or with a series, episode, clip.",
    )
    productionCompany: Optional[
        Union[List[Union["Organization", str]], "Organization", str]
    ] = Field(
        default=None,
        description="The production company or studio responsible for the item, e.g. series, video game,"
        "episode etc.",
    )
    actors: Optional[Union[List[Union["Person", str]], "Person", str]] = Field(
        default=None,
        description="An actor, e.g. in TV, radio, movie, video games etc. Actors can be associated with individual"
        "items or with a series, episode, clip.",
    )


if TYPE_CHECKING:
    from pydantic2_schemaorg.MusicGroup import MusicGroup
    from pydantic2_schemaorg.Person import Person
    from pydantic2_schemaorg.VideoObject import VideoObject
    from pydantic2_schemaorg.Organization import Organization
