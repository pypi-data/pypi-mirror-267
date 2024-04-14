from __future__ import annotations

from typing import TYPE_CHECKING

from pydantic.v1 import AnyUrl
from pydantic.v1 import Field

from pydantic2_schemaorg.CreativeWork import CreativeWork


class Movie(CreativeWork):
    """A movie.

    See: https://schema.org/Movie
    Model depth: 3
    """

    type_: str = Field(default="Movie", alias="@type", const=True)
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
    titleEIDR: None | (
        list[AnyUrl | URL | str | Text] | AnyUrl | URL | str | Text
    ) = Field(
        default=None,
        description="An [EIDR](https://eidr.org/) (Entertainment Identifier Registry) [[identifier]]"
        "representing at the most general/abstract level, a work of film or television. For example,"
        'the motion picture known as "Ghostbusters" has a titleEIDR of "10.5240/7EC7-228A-510A-053E-CBB8-J".'
        'This title (or work) may have several variants, which EIDR calls "edits". See [[editEIDR]].'
        "Since schema.org types like [[Movie]], [[TVEpisode]], [[TVSeason]], and [[TVSeries]]"
        "can be used for both works and their multiple expressions, it is possible to use [[titleEIDR]]"
        "alone (for a general description), or alongside [[editEIDR]] for a more edit-specific"
        "description.",
    )
    countryOfOrigin: None | (list[Country | str] | Country | str) = Field(
        default=None,
        description="The country of origin of something, including products as well as creative works such"
        "as movie and TV content. In the case of TV and movie, this would be the country of the principle"
        "offices of the production company or individual responsible for the movie. For other"
        "kinds of [[CreativeWork]] it is difficult to provide fully general guidance, and properties"
        "such as [[contentLocation]] and [[locationCreated]] may be more applicable. In the"
        "case of products, the country of origin of the product. The exact interpretation of this"
        "may vary by context and product type, and cannot be fully enumerated here.",
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
    duration: list[Duration | str] | Duration | str | None = Field(
        default=None,
        description="The duration of the item (movie, audio recording, event, etc.) in [ISO 8601 date format](http://en.wikipedia.org/wiki/ISO_8601).",
    )
    directors: list[Person | str] | Person | str | None = Field(
        default=None,
        description="A director of e.g. TV, radio, movie, video games etc. content. Directors can be associated"
        "with individual items or with a series, episode, clip.",
    )
    subtitleLanguage: None | (
        list[str | Text | Language] | str | Text | Language
    ) = Field(
        default=None,
        description="Languages in which subtitles/captions are available, in [IETF BCP 47 standard format](http://tools.ietf.org/html/bcp47).",
    )
    productionCompany: None | (list[Organization | str] | Organization | str) = Field(
        default=None,
        description="The production company or studio responsible for the item, e.g. series, video game,"
        "episode etc.",
    )
    actors: list[Person | str] | Person | str | None = Field(
        default=None,
        description="An actor, e.g. in TV, radio, movie, video games etc. Actors can be associated with individual"
        "items or with a series, episode, clip.",
    )


if TYPE_CHECKING:
    from pydantic2_schemaorg.MusicGroup import MusicGroup
    from pydantic2_schemaorg.Person import Person
    from pydantic2_schemaorg.URL import URL
    from pydantic2_schemaorg.Text import Text
    from pydantic2_schemaorg.Country import Country
    from pydantic2_schemaorg.VideoObject import VideoObject
    from pydantic2_schemaorg.Duration import Duration
    from pydantic2_schemaorg.Language import Language
    from pydantic2_schemaorg.Organization import Organization
