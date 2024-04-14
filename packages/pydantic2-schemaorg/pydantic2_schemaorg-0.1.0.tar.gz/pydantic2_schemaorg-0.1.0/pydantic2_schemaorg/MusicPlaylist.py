from __future__ import annotations

from typing import TYPE_CHECKING

from pydantic.v1 import Field

from pydantic2_schemaorg.CreativeWork import CreativeWork


class MusicPlaylist(CreativeWork):
    """A collection of music tracks in playlist form.

    See: https://schema.org/MusicPlaylist
    Model depth: 3
    """

    type_: str = Field(default="MusicPlaylist", alias="@type", const=True)
    numTracks: None | (list[int | Integer | str] | int | Integer | str) = Field(
        default=None,
        description="The number of tracks in this album or playlist.",
    )
    tracks: None | (list[MusicRecording | str] | MusicRecording | str) = Field(
        default=None,
        description="A music recording (track)&#x2014;usually a single song.",
    )
    track: None | (
        list[MusicRecording | ItemList | str] | MusicRecording | ItemList | str
    ) = Field(
        default=None,
        description="A music recording (track)&#x2014;usually a single song. If an ItemList is given, the"
        "list should contain items of type MusicRecording.",
    )


if TYPE_CHECKING:
    from pydantic2_schemaorg.Integer import Integer
    from pydantic2_schemaorg.MusicRecording import MusicRecording
    from pydantic2_schemaorg.ItemList import ItemList
