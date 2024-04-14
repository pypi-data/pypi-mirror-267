from __future__ import annotations

from typing import TYPE_CHECKING

from pydantic.v1 import Field

from pydantic2_schemaorg.Intangible import Intangible


class Enumeration(Intangible):
    """Lists or enumerations—for example, a list of cuisines or music genres, etc.

    See: https://schema.org/Enumeration
    Model depth: 3
    """

    type_: str = Field(default="Enumeration", alias="@type", const=True)
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
    from pydantic2_schemaorg.Class import Class
    from pydantic2_schemaorg.Property import Property
