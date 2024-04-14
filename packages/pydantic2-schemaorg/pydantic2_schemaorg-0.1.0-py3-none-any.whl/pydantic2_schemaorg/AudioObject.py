from __future__ import annotations

from typing import TYPE_CHECKING

from pydantic.v1 import Field

from pydantic2_schemaorg.MediaObject import MediaObject


class AudioObject(MediaObject):
    """An audio file.

    See: https://schema.org/AudioObject
    Model depth: 4
    """

    type_: str = Field(default="AudioObject", alias="@type", const=True)
    transcript: list[str | Text] | str | Text | None = Field(
        default=None,
        description="If this MediaObject is an AudioObject or VideoObject, the transcript of that object.",
    )
    embeddedTextCaption: list[str | Text] | str | Text | None = Field(
        default=None,
        description="Represents textual captioning from a [[MediaObject]], e.g. text of a 'meme'.",
    )
    caption: None | (list[str | Text | MediaObject] | str | Text | MediaObject) = Field(
        default=None,
        description="The caption for this object. For downloadable machine formats (closed caption, subtitles"
        "etc.) use MediaObject and indicate the [[encodingFormat]].",
    )


if TYPE_CHECKING:
    from pydantic2_schemaorg.Text import Text
    from pydantic2_schemaorg.MediaObject import MediaObject
