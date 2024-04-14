from __future__ import annotations

from datetime import date
from datetime import datetime
from typing import TYPE_CHECKING

from pydantic.v1 import AnyUrl
from pydantic.v1 import Field
from pydantic.v1 import StrictBool
from pydantic.v1 import StrictFloat
from pydantic.v1 import StrictInt

from pydantic2_schemaorg.Intangible import Intangible


class Order(Intangible):
    """An order is a confirmation of a transaction (a receipt), which can contain multiple line"
     "items, each represented by an Offer that has been accepted by the customer.

    See: https://schema.org/Order
    Model depth: 3
    """

    type_: str = Field(default="Order", alias="@type", const=True)
    discountCurrency: list[str | Text] | str | Text | None = Field(
        default=None,
        description="The currency of the discount. Use standard formats: [ISO 4217 currency format](http://en.wikipedia.org/wiki/ISO_4217),"
        'e.g. "USD"; [Ticker symbol](https://en.wikipedia.org/wiki/List_of_cryptocurrencies)'
        'for cryptocurrencies, e.g. "BTC"; well known names for [Local Exchange Trading Systems](https://en.wikipedia.org/wiki/Local_exchange_trading_system)'
        '(LETS) and other currency types, e.g. "Ithaca HOUR".',
    )
    orderDelivery: None | (list[ParcelDelivery | str] | ParcelDelivery | str) = Field(
        default=None,
        description="The delivery of the parcel related to this order or order item.",
    )
    orderNumber: list[str | Text] | str | Text | None = Field(
        default=None,
        description="The identifier of the transaction.",
    )
    confirmationNumber: list[str | Text] | str | Text | None = Field(
        default=None,
        description="A number that confirms the given order or payment has been received.",
    )
    paymentUrl: None | (list[AnyUrl | URL | str] | AnyUrl | URL | str) = Field(
        default=None,
        description="The URL for sending a payment.",
    )
    paymentDueDate: None | (
        list[datetime | DateTime | date | Date | str]
        | datetime
        | DateTime
        | date
        | Date
        | str
    ) = Field(
        default=None,
        description="The date that payment is due.",
    )
    orderDate: None | (
        list[datetime | DateTime | date | Date | str]
        | datetime
        | DateTime
        | date
        | Date
        | str
    ) = Field(
        default=None,
        description="Date order was placed.",
    )
    seller: None | (
        list[Organization | Person | str] | Organization | Person | str
    ) = Field(
        default=None,
        description="An entity which offers (sells / leases / lends / loans) the services / goods. A seller may"
        "also be a provider.",
    )
    acceptedOffer: list[Offer | str] | Offer | str | None = Field(
        default=None,
        description="The offer(s) -- e.g., product, quantity and price combinations -- included in the order.",
    )
    paymentDue: None | (
        list[datetime | DateTime | str] | datetime | DateTime | str
    ) = Field(
        default=None,
        description="The date that payment is due.",
    )
    discount: None | (
        list[StrictInt | StrictFloat | Number | str | Text]
        | StrictInt
        | StrictFloat
        | Number
        | str
        | Text
    ) = Field(
        default=None,
        description="Any discount applied (to an Order).",
    )
    paymentMethodId: list[str | Text] | str | Text | None = Field(
        default=None,
        description="An identifier for the method of payment used (e.g. the last 4 digits of the credit card).",
    )
    orderedItem: None | (
        list[OrderItem | Product | Service | str] | OrderItem | Product | Service | str
    ) = Field(
        default=None,
        description="The item ordered.",
    )
    paymentMethod: None | (list[PaymentMethod | str] | PaymentMethod | str) = Field(
        default=None,
        description="The name of the credit card or other method of payment for the order.",
    )
    billingAddress: None | (list[PostalAddress | str] | PostalAddress | str) = Field(
        default=None,
        description="The billing address for the order.",
    )
    broker: None | (
        list[Organization | Person | str] | Organization | Person | str
    ) = Field(
        default=None,
        description="An entity that arranges for an exchange between a buyer and a seller. In most cases a broker"
        "never acquires or releases ownership of a product or service involved in an exchange."
        "If it is not clear whether an entity is a broker, seller, or buyer, the latter two terms"
        "are preferred.",
    )
    customer: None | (
        list[Organization | Person | str] | Organization | Person | str
    ) = Field(
        default=None,
        description="Party placing the order or paying the invoice.",
    )
    isGift: None | (
        list[StrictBool | Boolean | str] | StrictBool | Boolean | str
    ) = Field(
        default=None,
        description="Indicates whether the offer was accepted as a gift for someone other than the buyer.",
    )
    orderStatus: None | (list[OrderStatus | str] | OrderStatus | str) = Field(
        default=None,
        description="The current status of the order.",
    )
    partOfInvoice: list[Invoice | str] | Invoice | str | None = Field(
        default=None,
        description="The order is being paid as part of the referenced Invoice.",
    )
    discountCode: list[str | Text] | str | Text | None = Field(
        default=None,
        description="Code used to redeem a discount.",
    )
    merchant: None | (
        list[Organization | Person | str] | Organization | Person | str
    ) = Field(
        default=None,
        description="'merchant' is an out-dated term for 'seller'.",
    )


if TYPE_CHECKING:
    from pydantic2_schemaorg.Text import Text
    from pydantic2_schemaorg.ParcelDelivery import ParcelDelivery
    from pydantic2_schemaorg.URL import URL
    from pydantic2_schemaorg.DateTime import DateTime
    from pydantic2_schemaorg.Date import Date
    from pydantic2_schemaorg.Organization import Organization
    from pydantic2_schemaorg.Person import Person
    from pydantic2_schemaorg.Offer import Offer
    from pydantic2_schemaorg.Number import Number
    from pydantic2_schemaorg.OrderItem import OrderItem
    from pydantic2_schemaorg.Product import Product
    from pydantic2_schemaorg.Service import Service
    from pydantic2_schemaorg.PaymentMethod import PaymentMethod
    from pydantic2_schemaorg.PostalAddress import PostalAddress
    from pydantic2_schemaorg.Boolean import Boolean
    from pydantic2_schemaorg.OrderStatus import OrderStatus
    from pydantic2_schemaorg.Invoice import Invoice
