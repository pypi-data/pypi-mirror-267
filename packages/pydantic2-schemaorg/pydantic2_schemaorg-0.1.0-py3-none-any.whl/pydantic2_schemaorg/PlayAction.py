from __future__ import annotations

from typing import TYPE_CHECKING

from pydantic.v1 import Field

from pydantic2_schemaorg.Action import Action


class PlayAction(Action):
    """The act of playing/exercising/training/performing for enjoyment, leisure, recreation,"
     "competition or exercise. Related actions: * [[ListenAction]]: Unlike ListenAction"
     "(which is under ConsumeAction), PlayAction refers to performing for an audience or"
     "at an event, rather than consuming music. * [[WatchAction]]: Unlike WatchAction (which"
     "is under ConsumeAction), PlayAction refers to showing/displaying for an audience"
     "or at an event, rather than consuming visual content.

    See: https://schema.org/PlayAction
    Model depth: 3
    """

    type_: str = Field(default="PlayAction", alias="@type", const=True)
    event: list[Event | str] | Event | str | None = Field(
        default=None,
        description="Upcoming or past event associated with this place, organization, or action.",
    )
    audience: list[Audience | str] | Audience | str | None = Field(
        default=None,
        description="An intended audience, i.e. a group for whom something was created.",
    )


if TYPE_CHECKING:
    from pydantic2_schemaorg.Event import Event
    from pydantic2_schemaorg.Audience import Audience
