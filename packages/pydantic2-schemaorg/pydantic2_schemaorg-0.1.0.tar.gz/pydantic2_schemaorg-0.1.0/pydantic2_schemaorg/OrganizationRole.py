from __future__ import annotations

from typing import TYPE_CHECKING

from pydantic.v1 import Field
from pydantic.v1 import StrictFloat
from pydantic.v1 import StrictInt

from pydantic2_schemaorg.Role import Role


class OrganizationRole(Role):
    """A subclass of Role used to describe roles within organizations.

    See: https://schema.org/OrganizationRole
    Model depth: 4
    """

    type_: str = Field(default="OrganizationRole", alias="@type", const=True)
    numberedPosition: None | (
        list[StrictInt | StrictFloat | Number | str]
        | StrictInt
        | StrictFloat
        | Number
        | str
    ) = Field(
        default=None,
        description="A number associated with a role in an organization, for example, the number on an athlete's"
        "jersey.",
    )


if TYPE_CHECKING:
    from pydantic2_schemaorg.Number import Number
