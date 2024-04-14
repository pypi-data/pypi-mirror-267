from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from pydantic.v1 import Field

from pydantic2_schemaorg.Event import Event


class DeliveryEvent(Event):
    """An event involving the delivery of an item.

    See: https://schema.org/DeliveryEvent
    Model depth: 3
    """

    type_: str = Field(default="DeliveryEvent", alias="@type", const=True)
    availableThrough: None | (
        list[datetime | DateTime | str] | datetime | DateTime | str
    ) = Field(
        default=None,
        description="After this date, the item will no longer be available for pickup.",
    )
    hasDeliveryMethod: None | (
        list[DeliveryMethod | str] | DeliveryMethod | str
    ) = Field(
        default=None,
        description="Method used for delivery or shipping.",
    )
    availableFrom: None | (
        list[datetime | DateTime | str] | datetime | DateTime | str
    ) = Field(
        default=None,
        description="When the item is available for pickup from the store, locker, etc.",
    )
    accessCode: list[str | Text] | str | Text | None = Field(
        default=None,
        description="Password, PIN, or access code needed for delivery (e.g. from a locker).",
    )


if TYPE_CHECKING:
    from pydantic2_schemaorg.DateTime import DateTime
    from pydantic2_schemaorg.DeliveryMethod import DeliveryMethod
    from pydantic2_schemaorg.Text import Text
