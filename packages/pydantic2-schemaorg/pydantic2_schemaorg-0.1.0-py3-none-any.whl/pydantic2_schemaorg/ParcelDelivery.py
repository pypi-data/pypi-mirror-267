from __future__ import annotations

from datetime import date
from datetime import datetime
from typing import TYPE_CHECKING

from pydantic.v1 import AnyUrl
from pydantic.v1 import Field

from pydantic2_schemaorg.Intangible import Intangible


class ParcelDelivery(Intangible):
    """The delivery of a parcel either via the postal service or a commercial service.

    See: https://schema.org/ParcelDelivery
    Model depth: 3
    """

    type_: str = Field(default="ParcelDelivery", alias="@type", const=True)
    trackingUrl: None | (list[AnyUrl | URL | str] | AnyUrl | URL | str) = Field(
        default=None,
        description="Tracking url for the parcel delivery.",
    )
    deliveryStatus: None | (list[DeliveryEvent | str] | DeliveryEvent | str) = Field(
        default=None,
        description="New entry added as the package passes through each leg of its journey (from shipment to"
        "final delivery).",
    )
    trackingNumber: list[str | Text] | str | Text | None = Field(
        default=None,
        description="Shipper tracking number.",
    )
    hasDeliveryMethod: None | (
        list[DeliveryMethod | str] | DeliveryMethod | str
    ) = Field(
        default=None,
        description="Method used for delivery or shipping.",
    )
    provider: None | (
        list[Organization | Person | str] | Organization | Person | str
    ) = Field(
        default=None,
        description="The service provider, service operator, or service performer; the goods producer."
        "Another party (a seller) may offer those services or goods on behalf of the provider."
        "A provider may also serve as the seller.",
    )
    carrier: None | (list[Organization | str] | Organization | str) = Field(
        default=None,
        description="'carrier' is an out-dated term indicating the 'provider' for parcel delivery and flights.",
    )
    originAddress: None | (list[PostalAddress | str] | PostalAddress | str) = Field(
        default=None,
        description="Shipper's address.",
    )
    itemShipped: list[Product | str] | Product | str | None = Field(
        default=None,
        description="Item(s) being shipped.",
    )
    deliveryAddress: None | (list[PostalAddress | str] | PostalAddress | str) = Field(
        default=None,
        description="Destination address.",
    )
    expectedArrivalUntil: None | (
        list[datetime | DateTime | date | Date | str]
        | datetime
        | DateTime
        | date
        | Date
        | str
    ) = Field(
        default=None,
        description="The latest date the package may arrive.",
    )
    expectedArrivalFrom: None | (
        list[datetime | DateTime | date | Date | str]
        | datetime
        | DateTime
        | date
        | Date
        | str
    ) = Field(
        default=None,
        description="The earliest date the package may arrive.",
    )
    partOfOrder: list[Order | str] | Order | str | None = Field(
        default=None,
        description="The overall order the items in this delivery were included in.",
    )


if TYPE_CHECKING:
    from pydantic2_schemaorg.URL import URL
    from pydantic2_schemaorg.DeliveryEvent import DeliveryEvent
    from pydantic2_schemaorg.Text import Text
    from pydantic2_schemaorg.DeliveryMethod import DeliveryMethod
    from pydantic2_schemaorg.Organization import Organization
    from pydantic2_schemaorg.Person import Person
    from pydantic2_schemaorg.PostalAddress import PostalAddress
    from pydantic2_schemaorg.Product import Product
    from pydantic2_schemaorg.DateTime import DateTime
    from pydantic2_schemaorg.Date import Date
    from pydantic2_schemaorg.Order import Order
