from __future__ import annotations

from typing import TYPE_CHECKING

from pydantic.v1 import Field

from pydantic2_schemaorg.MusicPlaylist import MusicPlaylist


class MusicAlbum(MusicPlaylist):
    """A collection of music tracks.

    See: https://schema.org/MusicAlbum
    Model depth: 4
    """

    type_: str = Field(default="MusicAlbum", alias="@type", const=True)
    albumRelease: None | (list[MusicRelease | str] | MusicRelease | str) = Field(
        default=None,
        description="A release of this album.",
    )
    albumReleaseType: None | (
        list[MusicAlbumReleaseType | str] | MusicAlbumReleaseType | str
    ) = Field(
        default=None,
        description="The kind of release which this album is: single, EP or album.",
    )
    byArtist: None | (
        list[MusicGroup | Person | str] | MusicGroup | Person | str
    ) = Field(
        default=None,
        description="The artist that performed this album or recording.",
    )
    albumProductionType: None | (
        list[MusicAlbumProductionType | str] | MusicAlbumProductionType | str
    ) = Field(
        default=None,
        description="Classification of the album by its type of content: soundtrack, live album, studio album,"
        "etc.",
    )


if TYPE_CHECKING:
    from pydantic2_schemaorg.MusicRelease import MusicRelease
    from pydantic2_schemaorg.MusicAlbumReleaseType import MusicAlbumReleaseType
    from pydantic2_schemaorg.MusicGroup import MusicGroup
    from pydantic2_schemaorg.Person import Person
    from pydantic2_schemaorg.MusicAlbumProductionType import MusicAlbumProductionType
