from __future__ import annotations

from typing import TYPE_CHECKING

from pydantic.v1 import Field

from pydantic2_schemaorg.AddAction import AddAction


class InsertAction(AddAction):
    """The act of adding at a specific location in an ordered collection.

    See: https://schema.org/InsertAction
    Model depth: 5
    """

    type_: str = Field(default="InsertAction", alias="@type", const=True)
    toLocation: list[Place | str] | Place | str | None = Field(
        default=None,
        description="A sub property of location. The final location of the object or the agent after the action.",
    )


if TYPE_CHECKING:
    from pydantic2_schemaorg.Place import Place
