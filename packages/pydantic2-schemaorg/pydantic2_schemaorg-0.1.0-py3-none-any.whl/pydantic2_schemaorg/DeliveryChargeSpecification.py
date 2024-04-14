from __future__ import annotations

from typing import TYPE_CHECKING

from pydantic.v1 import Field

from pydantic2_schemaorg.PriceSpecification import PriceSpecification


class DeliveryChargeSpecification(PriceSpecification):
    """The price for the delivery of an offer using a particular delivery method.

    See: https://schema.org/DeliveryChargeSpecification
    Model depth: 5
    """

    type_: str = Field(default="DeliveryChargeSpecification", alias="@type", const=True)
    eligibleRegion: None | (
        list[str | Text | GeoShape | Place] | str | Text | GeoShape | Place
    ) = Field(
        default=None,
        description="The ISO 3166-1 (ISO 3166-1 alpha-2) or ISO 3166-2 code, the place, or the GeoShape for"
        "the geo-political region(s) for which the offer or delivery charge specification is"
        "valid. See also [[ineligibleRegion]].",
    )
    ineligibleRegion: None | (
        list[str | Text | GeoShape | Place] | str | Text | GeoShape | Place
    ) = Field(
        default=None,
        description="The ISO 3166-1 (ISO 3166-1 alpha-2) or ISO 3166-2 code, the place, or the GeoShape for"
        "the geo-political region(s) for which the offer or delivery charge specification is"
        "not valid, e.g. a region where the transaction is not allowed. See also [[eligibleRegion]].",
    )
    areaServed: None | (
        list[str | Text | AdministrativeArea | GeoShape | Place]
        | str
        | Text
        | AdministrativeArea
        | GeoShape
        | Place
    ) = Field(
        default=None,
        description="The geographic area where a service or offered item is provided.",
    )
    appliesToDeliveryMethod: None | (
        list[DeliveryMethod | str] | DeliveryMethod | str
    ) = Field(
        default=None,
        description="The delivery method(s) to which the delivery charge or payment charge specification"
        "applies.",
    )


if TYPE_CHECKING:
    from pydantic2_schemaorg.Text import Text
    from pydantic2_schemaorg.GeoShape import GeoShape
    from pydantic2_schemaorg.Place import Place
    from pydantic2_schemaorg.AdministrativeArea import AdministrativeArea
    from pydantic2_schemaorg.DeliveryMethod import DeliveryMethod
