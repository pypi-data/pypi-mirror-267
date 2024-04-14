from __future__ import annotations
from typing import TYPE_CHECKING

from typing import List, Optional, Union


from pydantic.v1 import Field
from pydantic2_schemaorg.CreativeWork import CreativeWork


class MusicComposition(CreativeWork):
    """A musical composition.

    See: https://schema.org/MusicComposition
    Model depth: 3
    """

    type_: str = Field(default="MusicComposition", alias="@type", const=True)
    lyricist: Optional[Union[List[Union["Person", str]], "Person", str]] = Field(
        default=None,
        description="The person who wrote the words.",
    )
    recordedAs: Optional[
        Union[List[Union["MusicRecording", str]], "MusicRecording", str]
    ] = Field(
        default=None,
        description="An audio recording of the work.",
    )
    musicalKey: Optional[Union[List[Union[str, "Text"]], str, "Text"]] = Field(
        default=None,
        description="The key, mode, or scale this composition uses.",
    )
    firstPerformance: Optional[Union[List[Union["Event", str]], "Event", str]] = Field(
        default=None,
        description="The date and place the work was first performed.",
    )
    musicArrangement: Optional[
        Union[List[Union["MusicComposition", str]], "MusicComposition", str]
    ] = Field(
        default=None,
        description="An arrangement derived from the composition.",
    )
    iswcCode: Optional[Union[List[Union[str, "Text"]], str, "Text"]] = Field(
        default=None,
        description="The International Standard Musical Work Code for the composition.",
    )
    lyrics: Optional[Union[List[Union["CreativeWork", str]], "CreativeWork", str]] = (
        Field(
            default=None,
            description="The words in the song.",
        )
    )
    composer: Optional[
        Union[List[Union["Organization", "Person", str]], "Organization", "Person", str]
    ] = Field(
        default=None,
        description="The person or organization who wrote a composition, or who is the composer of a work performed"
        "at some event.",
    )
    musicCompositionForm: Optional[Union[List[Union[str, "Text"]], str, "Text"]] = (
        Field(
            default=None,
            description="The type of composition (e.g. overture, sonata, symphony, etc.).",
        )
    )
    includedComposition: Optional[
        Union[List[Union["MusicComposition", str]], "MusicComposition", str]
    ] = Field(
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
