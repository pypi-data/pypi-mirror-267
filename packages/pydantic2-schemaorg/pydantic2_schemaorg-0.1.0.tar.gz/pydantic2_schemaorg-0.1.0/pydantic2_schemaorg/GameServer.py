from __future__ import annotations

from typing import TYPE_CHECKING

from pydantic.v1 import Field

from pydantic2_schemaorg.Intangible import Intangible


class GameServer(Intangible):
    """Server that provides game interaction in a multiplayer game.

    See: https://schema.org/GameServer
    Model depth: 3
    """

    type_: str = Field(default="GameServer", alias="@type", const=True)
    serverStatus: None | (
        list[GameServerStatus | str] | GameServerStatus | str
    ) = Field(
        default=None,
        description="Status of a game server.",
    )
    game: list[VideoGame | str] | VideoGame | str | None = Field(
        default=None,
        description="Video game which is played on this server.",
    )
    playersOnline: None | (list[int | Integer | str] | int | Integer | str) = Field(
        default=None,
        description="Number of players on the server.",
    )


if TYPE_CHECKING:
    from pydantic2_schemaorg.GameServerStatus import GameServerStatus
    from pydantic2_schemaorg.VideoGame import VideoGame
    from pydantic2_schemaorg.Integer import Integer
