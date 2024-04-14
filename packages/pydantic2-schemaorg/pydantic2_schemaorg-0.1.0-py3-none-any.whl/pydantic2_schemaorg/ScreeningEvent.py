from __future__ import annotations

from typing import TYPE_CHECKING

from pydantic.v1 import Field

from pydantic2_schemaorg.Event import Event


class ScreeningEvent(Event):
    """A screening of a movie or other video.

    See: https://schema.org/ScreeningEvent
    Model depth: 3
    """

    type_: str = Field(default="ScreeningEvent", alias="@type", const=True)
    videoFormat: list[str | Text] | str | Text | None = Field(
        default=None,
        description="The type of screening or video broadcast used (e.g. IMAX, 3D, SD, HD, etc.).",
    )
    subtitleLanguage: None | (
        list[str | Text | Language] | str | Text | Language
    ) = Field(
        default=None,
        description="Languages in which subtitles/captions are available, in [IETF BCP 47 standard format](http://tools.ietf.org/html/bcp47).",
    )
    workPresented: list[Movie | str] | Movie | str | None = Field(
        default=None,
        description="The movie presented during this event.",
    )


if TYPE_CHECKING:
    from pydantic2_schemaorg.Text import Text
    from pydantic2_schemaorg.Language import Language
    from pydantic2_schemaorg.Movie import Movie
