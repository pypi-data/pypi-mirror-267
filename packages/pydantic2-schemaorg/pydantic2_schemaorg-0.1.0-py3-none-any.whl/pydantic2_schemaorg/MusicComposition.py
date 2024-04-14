from __future__ import annotations

from typing import TYPE_CHECKING

from pydantic.v1 import Field

from pydantic2_schemaorg.CreativeWork import CreativeWork


class MusicComposition(CreativeWork):
    """A musical composition.

    See: https://schema.org/MusicComposition
    Model depth: 3
    """

    type_: str = Field(default="MusicComposition", alias="@type", const=True)
    lyricist: list[Person | str] | Person | str | None = Field(
        default=None,
        description="The person who wrote the words.",
    )
    recordedAs: None | (list[MusicRecording | str] | MusicRecording | str) = Field(
        default=None,
        description="An audio recording of the work.",
    )
    musicalKey: list[str | Text] | str | Text | None = Field(
        default=None,
        description="The key, mode, or scale this composition uses.",
    )
    firstPerformance: list[Event | str] | Event | str | None = Field(
        default=None,
        description="The date and place the work was first performed.",
    )
    musicArrangement: None | (
        list[MusicComposition | str] | MusicComposition | str
    ) = Field(
        default=None,
        description="An arrangement derived from the composition.",
    )
    iswcCode: list[str | Text] | str | Text | None = Field(
        default=None,
        description="The International Standard Musical Work Code for the composition.",
    )
    lyrics: None | (list[CreativeWork | str] | CreativeWork | str) = Field(
        default=None,
        description="The words in the song.",
    )
    composer: None | (
        list[Organization | Person | str] | Organization | Person | str
    ) = Field(
        default=None,
        description="The person or organization who wrote a composition, or who is the composer of a work performed"
        "at some event.",
    )
    musicCompositionForm: None | (list[str | Text] | str | Text) = Field(
        default=None,
        description="The type of composition (e.g. overture, sonata, symphony, etc.).",
    )
    includedComposition: None | (
        list[MusicComposition | str] | MusicComposition | str
    ) = Field(
        default=None,
        description="Smaller compositions included in this work (e.g. a movement in a symphony).",
    )


if TYPE_CHECKING:
    from pydantic2_schemaorg.Person import Person
    from pydantic2_schemaorg.MusicRecording import MusicRecording
    from pydantic2_schemaorg.Text import Text
    from pydantic2_schemaorg.Event import Event
    from pydantic2_schemaorg.CreativeWork import CreativeWork
    from pydantic2_schemaorg.Organization import Organization
