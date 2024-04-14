from __future__ import annotations

from typing import TYPE_CHECKING

from pydantic.v1 import Field

from pydantic2_schemaorg.MediaObject import MediaObject


class VideoObject(MediaObject):
    """A video file.

    See: https://schema.org/VideoObject
    Model depth: 4
    """

    type_: str = Field(default="VideoObject", alias="@type", const=True)
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
    transcript: list[str | Text] | str | Text | None = Field(
        default=None,
        description="If this MediaObject is an AudioObject or VideoObject, the transcript of that object.",
    )
    embeddedTextCaption: list[str | Text] | str | Text | None = Field(
        default=None,
        description="Represents textual captioning from a [[MediaObject]], e.g. text of a 'meme'.",
    )
    videoFrameSize: list[str | Text] | str | Text | None = Field(
        default=None,
        description="The frame size of the video.",
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
    caption: None | (list[str | Text | MediaObject] | str | Text | MediaObject) = Field(
        default=None,
        description="The caption for this object. For downloadable machine formats (closed caption, subtitles"
        "etc.) use MediaObject and indicate the [[encodingFormat]].",
    )
    actors: list[Person | str] | Person | str | None = Field(
        default=None,
        description="An actor, e.g. in TV, radio, movie, video games etc. Actors can be associated with individual"
        "items or with a series, episode, clip.",
    )
    videoQuality: list[str | Text] | str | Text | None = Field(
        default=None,
        description="The quality of the video.",
    )


if TYPE_CHECKING:
    from pydantic2_schemaorg.MusicGroup import MusicGroup
    from pydantic2_schemaorg.Person import Person
    from pydantic2_schemaorg.Text import Text
    from pydantic2_schemaorg.MediaObject import MediaObject
