from __future__ import annotations

from typing import TYPE_CHECKING

from pydantic.v1 import AnyUrl
from pydantic.v1 import Field

from pydantic2_schemaorg.PerformingGroup import PerformingGroup


class MusicGroup(PerformingGroup):
    """A musical group, such as a band, an orchestra, or a choir. Can also be a solo musician.

    See: https://schema.org/MusicGroup
    Model depth: 4
    """

    type_: str = Field(default="MusicGroup", alias="@type", const=True)
    musicGroupMember: None | (list[Person | str] | Person | str) = Field(
        default=None,
        description="A member of a music group&#x2014;for example, John, Paul, George, or Ringo.",
    )
    album: list[MusicAlbum | str] | MusicAlbum | str | None = Field(
        default=None,
        description="A music album.",
    )
    tracks: None | (list[MusicRecording | str] | MusicRecording | str) = Field(
        default=None,
        description="A music recording (track)&#x2014;usually a single song.",
    )
    genre: None | (list[AnyUrl | URL | str | Text] | AnyUrl | URL | str | Text) = Field(
        default=None,
        description="Genre of the creative work, broadcast channel or group.",
    )
    track: None | (
        list[MusicRecording | ItemList | str] | MusicRecording | ItemList | str
    ) = Field(
        default=None,
        description="A music recording (track)&#x2014;usually a single song. If an ItemList is given, the"
        "list should contain items of type MusicRecording.",
    )
    albums: list[MusicAlbum | str] | MusicAlbum | str | None = Field(
        default=None,
        description="A collection of music albums.",
    )


if TYPE_CHECKING:
    from pydantic2_schemaorg.Person import Person
    from pydantic2_schemaorg.MusicAlbum import MusicAlbum
    from pydantic2_schemaorg.MusicRecording import MusicRecording
    from pydantic2_schemaorg.URL import URL
    from pydantic2_schemaorg.Text import Text
    from pydantic2_schemaorg.ItemList import ItemList
