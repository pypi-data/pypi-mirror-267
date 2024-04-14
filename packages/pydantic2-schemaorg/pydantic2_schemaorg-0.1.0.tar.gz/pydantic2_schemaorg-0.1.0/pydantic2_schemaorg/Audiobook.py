from __future__ import annotations

from typing import TYPE_CHECKING

from pydantic.v1 import Field

from pydantic2_schemaorg.AudioObject import AudioObject
from pydantic2_schemaorg.Book import Book


class Audiobook(AudioObject, Book):
    """An audiobook.

    See: https://schema.org/Audiobook
    Model depth: 4
    """

    type_: str = Field(default="Audiobook", alias="@type", const=True)
    readBy: list[Person | str] | Person | str | None = Field(
        default=None,
        description="A person who reads (performs) the audiobook.",
    )
    duration: list[Duration | str] | Duration | str | None = Field(
        default=None,
        description="The duration of the item (movie, audio recording, event, etc.) in [ISO 8601 date format](http://en.wikipedia.org/wiki/ISO_8601).",
    )


if TYPE_CHECKING:
    from pydantic2_schemaorg.Person import Person
    from pydantic2_schemaorg.Duration import Duration
