from __future__ import annotations

from typing import TYPE_CHECKING

from pydantic.v1 import Field

from pydantic2_schemaorg.Intangible import Intangible


class Property(Intangible):
    """A property, used to indicate attributes and relationships of some Thing; equivalent"
     "to rdf:Property.

    See: https://schema.org/Property
    Model depth: 3
    """

    type_: str = Field(default="Property", alias="@type", const=True)
    inverseOf: list[Property | str] | Property | str | None = Field(
        default=None,
        description="Relates a property to a property that is its inverse. Inverse properties relate the same"
        "pairs of items to each other, but in reversed direction. For example, the 'alumni' and"
        "'alumniOf' properties are inverseOf each other. Some properties don't have explicit"
        "inverses; in these situations RDFa and JSON-LD syntax for reverse properties can be"
        "used.",
    )
    domainIncludes: list[Class | str] | Class | str | None = Field(
        default=None,
        description="Relates a property to a class that is (one of) the type(s) the property is expected to be"
        "used on.",
    )
    rangeIncludes: list[Class | str] | Class | str | None = Field(
        default=None,
        description="Relates a property to a class that constitutes (one of) the expected type(s) for values"
        "of the property.",
    )
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
    from pydantic2_schemaorg.Enumeration import Enumeration
