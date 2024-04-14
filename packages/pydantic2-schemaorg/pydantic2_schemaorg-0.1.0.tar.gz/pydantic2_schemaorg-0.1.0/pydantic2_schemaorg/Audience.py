from __future__ import annotations

from typing import TYPE_CHECKING

from pydantic.v1 import Field

from pydantic2_schemaorg.Intangible import Intangible


class Audience(Intangible):
    """Intended audience for an item, i.e. the group for whom the item was created.

    See: https://schema.org/Audience
    Model depth: 3
    """

    type_: str = Field(default="Audience", alias="@type", const=True)
    audienceType: list[str | Text] | str | Text | None = Field(
        default=None,
        description="The target group associated with a given audience (e.g. veterans, car owners, musicians,"
        "etc.).",
    )
    geographicArea: None | (
        list[AdministrativeArea | str] | AdministrativeArea | str
    ) = Field(
        default=None,
        description="The geographic area associated with the audience.",
    )


if TYPE_CHECKING:
    from pydantic2_schemaorg.Text import Text
    from pydantic2_schemaorg.AdministrativeArea import AdministrativeArea
