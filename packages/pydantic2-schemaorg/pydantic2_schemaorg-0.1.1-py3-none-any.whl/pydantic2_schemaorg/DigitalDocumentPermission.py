from __future__ import annotations
from typing import TYPE_CHECKING

from typing import List, Optional, Union


from pydantic.v1 import Field
from pydantic2_schemaorg.Intangible import Intangible


class DigitalDocumentPermission(Intangible):
    """A permission for a particular person or group to access a particular file.

    See: https://schema.org/DigitalDocumentPermission
    Model depth: 3
    """

    type_: str = Field(default="DigitalDocumentPermission", alias="@type", const=True)
    grantee: Optional[
        Union[
            List[Union["Organization", "Audience", "ContactPoint", "Person", str]],
            "Organization",
            "Audience",
            "ContactPoint",
            "Person",
            str,
        ]
    ] = Field(
        default=None,
        description="The person, organization, contact point, or audience that has been granted this permission.",
    )
    permissionType: Optional[
        Union[
            List[Union["DigitalDocumentPermissionType", str]],
            "DigitalDocumentPermissionType",
            str,
        ]
    ] = Field(
        default=None,
        description="The type of permission granted the person, organization, or audience.",
    )


if TYPE_CHECKING:
    from pydantic2_schemaorg.Organization import Organization
    from pydantic2_schemaorg.Audience import Audience
    from pydantic2_schemaorg.ContactPoint import ContactPoint
    from pydantic2_schemaorg.Person import Person
    from pydantic2_schemaorg.DigitalDocumentPermissionType import (
        DigitalDocumentPermissionType,
    )
