from __future__ import annotations

from typing import TYPE_CHECKING

from pydantic.v1 import AnyUrl
from pydantic.v1 import Field

from pydantic2_schemaorg.Intangible import Intangible


class BroadcastChannel(Intangible):
    """A unique instance of a BroadcastService on a CableOrSatelliteService lineup.

    See: https://schema.org/BroadcastChannel
    Model depth: 3
    """

    type_: str = Field(default="BroadcastChannel", alias="@type", const=True)
    broadcastFrequency: None | (
        list[str | Text | BroadcastFrequencySpecification]
        | str
        | Text
        | BroadcastFrequencySpecification
    ) = Field(
        default=None,
        description="The frequency used for over-the-air broadcasts. Numeric values or simple ranges, e.g."
        "87-99. In addition a shortcut idiom is supported for frequences of AM and FM radio channels,"
        'e.g. "87 FM".',
    )
    broadcastChannelId: list[str | Text] | str | Text | None = Field(
        default=None,
        description="The unique address by which the BroadcastService can be identified in a provider lineup."
        "In US, this is typically a number.",
    )
    providesBroadcastService: None | (
        list[BroadcastService | str] | BroadcastService | str
    ) = Field(
        default=None,
        description="The BroadcastService offered on this channel.",
    )
    broadcastServiceTier: None | (list[str | Text] | str | Text) = Field(
        default=None,
        description="The type of service required to have access to the channel (e.g. Standard or Premium).",
    )
    inBroadcastLineup: None | (
        list[CableOrSatelliteService | str] | CableOrSatelliteService | str
    ) = Field(
        default=None,
        description="The CableOrSatelliteService offering the channel.",
    )
    genre: None | (list[AnyUrl | URL | str | Text] | AnyUrl | URL | str | Text) = Field(
        default=None,
        description="Genre of the creative work, broadcast channel or group.",
    )


if TYPE_CHECKING:
    from pydantic2_schemaorg.Text import Text
    from pydantic2_schemaorg.BroadcastFrequencySpecification import (
        BroadcastFrequencySpecification,
    )
    from pydantic2_schemaorg.BroadcastService import BroadcastService
    from pydantic2_schemaorg.CableOrSatelliteService import CableOrSatelliteService
    from pydantic2_schemaorg.URL import URL
