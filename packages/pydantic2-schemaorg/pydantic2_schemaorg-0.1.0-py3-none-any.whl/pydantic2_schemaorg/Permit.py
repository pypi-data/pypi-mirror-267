from __future__ import annotations

from datetime import date
from datetime import datetime
from typing import TYPE_CHECKING

from pydantic.v1 import Field

from pydantic2_schemaorg.Intangible import Intangible


class Permit(Intangible):
    """A permit issued by an organization, e.g. a parking pass.

    See: https://schema.org/Permit
    Model depth: 3
    """

    type_: str = Field(default="Permit", alias="@type", const=True)
    validUntil: None | (list[date | Date | str] | date | Date | str) = Field(
        default=None,
        description="The date when the item is no longer valid.",
    )
    validFrom: None | (
        list[datetime | DateTime | date | Date | str]
        | datetime
        | DateTime
        | date
        | Date
        | str
    ) = Field(
        default=None,
        description="The date when the item becomes valid.",
    )
    validFor: list[Duration | str] | Duration | str | None = Field(
        default=None,
        description="The duration of validity of a permit or similar thing.",
    )
    permitAudience: None | (list[Audience | str] | Audience | str) = Field(
        default=None,
        description="The target audience for this permit.",
    )
    issuedBy: None | (list[Organization | str] | Organization | str) = Field(
        default=None,
        description="The organization issuing the ticket or permit.",
    )
    validIn: None | (list[AdministrativeArea | str] | AdministrativeArea | str) = Field(
        default=None,
        description="The geographic area where a permit or similar thing is valid.",
    )
    issuedThrough: list[Service | str] | Service | str | None = Field(
        default=None,
        description="The service through which the permit was granted.",
    )


if TYPE_CHECKING:
    from pydantic2_schemaorg.Date import Date
    from pydantic2_schemaorg.DateTime import DateTime
    from pydantic2_schemaorg.Duration import Duration
    from pydantic2_schemaorg.Audience import Audience
    from pydantic2_schemaorg.Organization import Organization
    from pydantic2_schemaorg.AdministrativeArea import AdministrativeArea
    from pydantic2_schemaorg.Service import Service
