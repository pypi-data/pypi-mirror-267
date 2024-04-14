from __future__ import annotations

from typing import TYPE_CHECKING

from pydantic.v1 import Field
from pydantic.v1 import StrictBool

from pydantic2_schemaorg.StructuredValue import StructuredValue


class DeliveryTimeSettings(StructuredValue):
    """A DeliveryTimeSettings represents re-usable pieces of shipping information, relating"
     "to timing. It is designed for publication on an URL that may be referenced via the [[shippingSettingsLink]]"
     "property of an [[OfferShippingDetails]]. Several occurrences can be published, distinguished"
     "(and identified/referenced) by their different values for [[transitTimeLabel]].

    See: https://schema.org/DeliveryTimeSettings
    Model depth: 4
    """

    type_: str = Field(default="DeliveryTimeSettings", alias="@type", const=True)
    shippingDestination: None | (
        list[DefinedRegion | str] | DefinedRegion | str
    ) = Field(
        default=None,
        description="indicates (possibly multiple) shipping destinations. These can be defined in several"
        "ways, e.g. postalCode ranges.",
    )
    transitTimeLabel: list[str | Text] | str | Text | None = Field(
        default=None,
        description="Label to match an [[OfferShippingDetails]] with a [[DeliveryTimeSettings]] (within"
        "the context of a [[shippingSettingsLink]] cross-reference).",
    )
    deliveryTime: None | (
        list[ShippingDeliveryTime | str] | ShippingDeliveryTime | str
    ) = Field(
        default=None,
        description="The total delay between the receipt of the order and the goods reaching the final customer.",
    )
    isUnlabelledFallback: None | (
        list[StrictBool | Boolean | str] | StrictBool | Boolean | str
    ) = Field(
        default=None,
        description="This can be marked 'true' to indicate that some published [[DeliveryTimeSettings]]"
        "or [[ShippingRateSettings]] are intended to apply to all [[OfferShippingDetails]]"
        "published by the same merchant, when referenced by a [[shippingSettingsLink]] in those"
        "settings. It is not meaningful to use a 'true' value for this property alongside a transitTimeLabel"
        "(for [[DeliveryTimeSettings]]) or shippingLabel (for [[ShippingRateSettings]]),"
        "since this property is for use with unlabelled settings.",
    )


if TYPE_CHECKING:
    from pydantic2_schemaorg.DefinedRegion import DefinedRegion
    from pydantic2_schemaorg.Text import Text
    from pydantic2_schemaorg.ShippingDeliveryTime import ShippingDeliveryTime
    from pydantic2_schemaorg.Boolean import Boolean
