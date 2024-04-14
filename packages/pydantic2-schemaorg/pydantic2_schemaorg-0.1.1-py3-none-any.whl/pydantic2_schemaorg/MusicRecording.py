from __future__ import annotations
from typing import TYPE_CHECKING

from typing import List, Optional, Union


from pydantic.v1 import Field
from pydantic2_schemaorg.CreativeWork import CreativeWork


class MusicRecording(CreativeWork):
    """A music recording (track), usually a single song.

    See: https://schema.org/MusicRecording
    Model depth: 3
    """

    type_: str = Field(default="MusicRecording", alias="@type", const=True)
    recordingOf: Optional[
        Union[List[Union["MusicComposition", str]], "MusicComposition", str]
    ] = Field(
        default=None,
        description="The composition this track is a recording of.",
    )
    inPlaylist: Optional[
        Union[List[Union["MusicPlaylist", str]], "MusicPlaylist", str]
    ] = Field(
        default=None,
        description="The playlist to which this recording belongs.",
    )
    inAlbum: Optional[Union[List[Union["MusicAlbum", str]], "MusicAlbum", str]] = Field(
        default=None,
        description="The album to which this recording belongs.",
    )
    duration: Optional[Union[List[Union["Duration", str]], "Duration", str]] = Field(
        default=None,
        description="The duration of the item (movie, audio recording, event, etc.) in [ISO 8601 date format](http://en.wikipedia.org/wiki/ISO_8601).",
    )
    isrcCode: Optional[Union[List[Union[str, "Text"]], str, "Text"]] = Field(
        default=None,
        description="The International Standard Recording Code for the recording.",
    )
    byArtist: Optional[
        Union[List[Union["MusicGroup", "Person", str]], "MusicGroup", "Person", str]
    ] = Field(
        default=None,
        description="The artist that performed this album or recording.",
    )


if TYPE_CHECKING:
    from pydantic2_schemaorg.MusicComposition import MusicComposition
    from pydantic2_schemaorg.MusicPlaylist import MusicPlaylist
    from pydantic2_schemaorg.MusicAlbum import MusicAlbum
    from pydantic2_schemaorg.Duration import Duration
    from pydantic2_schemaorg.Text import Text
    from pydantic2_schemaorg.MusicGroup import MusicGroup
    from pydantic2_schemaorg.Person import Person
