from __future__ import annotations

from typing import TYPE_CHECKING

from pydantic.v1 import Field

from pydantic2_schemaorg.Intangible import Intangible


class Class(Intangible):
    """A class, also often called a 'Type'; equivalent to rdfs:Class.

    See: https://schema.org/Class
    Model depth: 3
    """

    type_: str = Field(default="Class", alias="@type", const=True)
    supersededBy: None | (
        list[Class | Property | Enumeration | str]
        | Class
        | Property
        | Enumeration
        | str
    ) = Field(
        default=None,
        description="Relates a term (i.e. a property, class or enumeration) to one that supersedes it.",
    )


if TYPE_CHECKING:
    from pydantic2_schemaorg.Property import Property
    from pydantic2_schemaorg.Enumeration import Enumeration
