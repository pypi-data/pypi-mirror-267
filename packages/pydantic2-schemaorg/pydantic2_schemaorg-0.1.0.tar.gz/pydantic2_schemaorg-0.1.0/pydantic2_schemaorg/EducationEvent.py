from __future__ import annotations

from typing import TYPE_CHECKING

from pydantic.v1 import AnyUrl
from pydantic.v1 import Field

from pydantic2_schemaorg.Event import Event


class EducationEvent(Event):
    """Event type: Education event.

    See: https://schema.org/EducationEvent
    Model depth: 3
    """

    type_: str = Field(default="EducationEvent", alias="@type", const=True)
    teaches: None | (list[str | Text | DefinedTerm] | str | Text | DefinedTerm) = Field(
        default=None,
        description="The item being described is intended to help a person learn the competency or learning"
        "outcome defined by the referenced term.",
    )
    assesses: None | (
        list[str | Text | DefinedTerm] | str | Text | DefinedTerm
    ) = Field(
        default=None,
        description="The item being described is intended to assess the competency or learning outcome defined"
        "by the referenced term.",
    )
    educationalLevel: None | (
        list[AnyUrl | URL | str | Text | DefinedTerm]
        | AnyUrl
        | URL
        | str
        | Text
        | DefinedTerm
    ) = Field(
        default=None,
        description="The level in terms of progression through an educational or training context. Examples"
        "of educational levels include 'beginner', 'intermediate' or 'advanced', and formal"
        "sets of level indicators.",
    )


if TYPE_CHECKING:
    from pydantic2_schemaorg.Text import Text
    from pydantic2_schemaorg.DefinedTerm import DefinedTerm
    from pydantic2_schemaorg.URL import URL
