from __future__ import annotations

from typing import TYPE_CHECKING

from pydantic.v1 import Field

from pydantic2_schemaorg.MusicPlaylist import MusicPlaylist


class MusicRelease(MusicPlaylist):
    """A MusicRelease is a specific release of a music album.

    See: https://schema.org/MusicRelease
    Model depth: 4
    """

    type_: str = Field(default="MusicRelease", alias="@type", const=True)
    releaseOf: None | (list[MusicAlbum | str] | MusicAlbum | str) = Field(
        default=None,
        description="The album this is a release of.",
    )
    creditedTo: None | (
        list[Organization | Person | str] | Organization | Person | str
    ) = Field(
        default=None,
        description="The group the release is credited to if different than the byArtist. For example, Red"
        'and Blue is credited to "Stefani Germanotta Band", but by Lady Gaga.',
    )
    recordLabel: None | (list[Organization | str] | Organization | str) = Field(
        default=None,
        description="The label that issued the release.",
    )
    catalogNumber: list[str | Text] | str | Text | None = Field(
        default=None,
        description="The catalog number for the release.",
    )
    duration: list[Duration | str] | Duration | str | None = Field(
        default=None,
        description="The duration of the item (movie, audio recording, event, etc.) in [ISO 8601 date format](http://en.wikipedia.org/wiki/ISO_8601).",
    )
    musicReleaseFormat: None | (
        list[MusicReleaseFormatType | str] | MusicReleaseFormatType | str
    ) = Field(
        default=None,
        description="Format of this release (the type of recording media used, i.e. compact disc, digital"
        "media, LP, etc.).",
    )


if TYPE_CHECKING:
    from pydantic2_schemaorg.MusicAlbum import MusicAlbum
    from pydantic2_schemaorg.Organization import Organization
    from pydantic2_schemaorg.Person import Person
    from pydantic2_schemaorg.Text import Text
    from pydantic2_schemaorg.Duration import Duration
    from pydantic2_schemaorg.MusicReleaseFormatType import MusicReleaseFormatType
