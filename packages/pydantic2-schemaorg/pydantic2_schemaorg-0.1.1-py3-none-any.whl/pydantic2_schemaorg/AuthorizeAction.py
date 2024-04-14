from __future__ import annotations
from typing import TYPE_CHECKING

from typing import List, Optional, Union


from pydantic.v1 import Field
from pydantic2_schemaorg.AllocateAction import AllocateAction


class AuthorizeAction(AllocateAction):
    """The act of granting permission to an object.

    See: https://schema.org/AuthorizeAction
    Model depth: 5
    """

    type_: str = Field(default="AuthorizeAction", alias="@type", const=True)
    recipient: Optional[
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
        description="A sub property of participant. The participant who is at the receiving end of the action.",
    )


if TYPE_CHECKING:
    from pydantic2_schemaorg.Organization import Organization
    from pydantic2_schemaorg.Audience import Audience
    from pydantic2_schemaorg.ContactPoint import ContactPoint
    from pydantic2_schemaorg.Person import Person
