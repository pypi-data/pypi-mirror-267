from __future__ import annotations

from typing import TYPE_CHECKING

from pydantic.v1 import Field

from pydantic2_schemaorg.CreativeWork import CreativeWork


class ArchiveComponent(CreativeWork):
    """An intangible type to be applied to any archive content, carrying with it a set of properties"
     "required to describe archival items and collections.

    See: https://schema.org/ArchiveComponent
    Model depth: 3
    """

    type_: str = Field(default="ArchiveComponent", alias="@type", const=True)
    itemLocation: None | (
        list[str | Text | PostalAddress | Place] | str | Text | PostalAddress | Place
    ) = Field(
        default=None,
        description="Current location of the item.",
    )
    holdingArchive: None | (
        list[ArchiveOrganization | str] | ArchiveOrganization | str
    ) = Field(
        default=None,
        description="[[ArchiveOrganization]] that holds, keeps or maintains the [[ArchiveComponent]].",
    )


if TYPE_CHECKING:
    from pydantic2_schemaorg.Text import Text
    from pydantic2_schemaorg.PostalAddress import PostalAddress
    from pydantic2_schemaorg.Place import Place
    from pydantic2_schemaorg.ArchiveOrganization import ArchiveOrganization
