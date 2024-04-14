from __future__ import annotations

from typing import TYPE_CHECKING

from pydantic.v1 import Field
from pydantic.v1 import StrictFloat
from pydantic.v1 import StrictInt

from pydantic2_schemaorg.Intangible import Intangible


class ProgramMembership(Intangible):
    """Used to describe membership in a loyalty programs (e.g. \"StarAliance\"), traveler"
     "clubs (e.g. \"AAA\"), purchase clubs (\"Safeway Club\"), etc.

    See: https://schema.org/ProgramMembership
    Model depth: 3
    """

    type_: str = Field(default="ProgramMembership", alias="@type", const=True)
    membershipPointsEarned: None | (
        list[StrictInt | StrictFloat | Number | QuantitativeValue | str]
        | StrictInt
        | StrictFloat
        | Number
        | QuantitativeValue
        | str
    ) = Field(
        default=None,
        description="The number of membership points earned by the member. If necessary, the unitText can"
        "be used to express the units the points are issued in. (E.g. stars, miles, etc.)",
    )
    hostingOrganization: None | (list[Organization | str] | Organization | str) = Field(
        default=None,
        description="The organization (airline, travelers' club, etc.) the membership is made with.",
    )
    members: None | (
        list[Organization | Person | str] | Organization | Person | str
    ) = Field(
        default=None,
        description="A member of this organization.",
    )
    member: None | (
        list[Organization | Person | str] | Organization | Person | str
    ) = Field(
        default=None,
        description="A member of an Organization or a ProgramMembership. Organizations can be members of"
        "organizations; ProgramMembership is typically for individuals.",
    )
    membershipNumber: list[str | Text] | str | Text | None = Field(
        default=None,
        description="A unique identifier for the membership.",
    )
    programName: list[str | Text] | str | Text | None = Field(
        default=None,
        description="The program providing the membership.",
    )


if TYPE_CHECKING:
    from pydantic2_schemaorg.Number import Number
    from pydantic2_schemaorg.QuantitativeValue import QuantitativeValue
    from pydantic2_schemaorg.Organization import Organization
    from pydantic2_schemaorg.Person import Person
    from pydantic2_schemaorg.Text import Text
