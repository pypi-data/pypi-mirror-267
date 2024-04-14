from __future__ import annotations

from typing import TYPE_CHECKING

from pydantic.v1 import Field

from pydantic2_schemaorg.Action import Action


class UpdateAction(Action):
    """The act of managing by changing/editing the state of the object.

    See: https://schema.org/UpdateAction
    Model depth: 3
    """

    type_: str = Field(default="UpdateAction", alias="@type", const=True)
    collection: list[Thing | str] | Thing | str | None = Field(
        default=None,
        description="A sub property of object. The collection target of the action.",
    )
    targetCollection: list[Thing | str] | Thing | str | None = Field(
        default=None,
        description="A sub property of object. The collection target of the action.",
    )


if TYPE_CHECKING:
    from pydantic2_schemaorg.Thing import Thing
