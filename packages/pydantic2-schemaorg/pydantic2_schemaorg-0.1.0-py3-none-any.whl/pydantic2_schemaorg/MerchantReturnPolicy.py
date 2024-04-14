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


class MerchantReturnPolicy(Intangible):
    """A MerchantReturnPolicy provides information about product return policies associated"
     "with an [[Organization]], [[Product]], or [[Offer]].

    See: https://schema.org/MerchantReturnPolicy
    Model depth: 3
    """

    type_: str = Field(default="MerchantReturnPolicy", alias="@type", const=True)
    customerRemorseReturnLabelSource: None | (
        list[ReturnLabelSourceEnumeration | str] | ReturnLabelSourceEnumeration | str
    ) = Field(
        default=None,
        description="The method (from an enumeration) by which the customer obtains a return shipping label"
        "for a product returned due to customer remorse.",
    )
    inStoreReturnsOffered: None | (
        list[StrictBool | Boolean | str] | StrictBool | Boolean | str
    ) = Field(
        default=None,
        description="Are in-store returns offered? (For more advanced return methods use the [[returnMethod]]"
        "property.)",
    )
    restockingFee: None | (
        list[StrictInt | StrictFloat | Number | MonetaryAmount | str]
        | StrictInt
        | StrictFloat
        | Number
        | MonetaryAmount
        | str
    ) = Field(
        default=None,
        description="Use [[MonetaryAmount]] to specify a fixed restocking fee for product returns, or use"
        "[[Number]] to specify a percentage of the product price paid by the customer.",
    )
    refundType: None | (
        list[RefundTypeEnumeration | str] | RefundTypeEnumeration | str
    ) = Field(
        default=None,
        description="A refund type, from an enumerated list.",
    )
    returnMethod: None | (
        list[ReturnMethodEnumeration | str] | ReturnMethodEnumeration | str
    ) = Field(
        default=None,
        description="The type of return method offered, specified from an enumeration.",
    )
    applicableCountry: None | (
        list[str | Text | Country] | str | Text | Country
    ) = Field(
        default=None,
        description="A country where a particular merchant return policy applies to, for example the two-letter"
        "ISO 3166-1 alpha-2 country code.",
    )
    itemDefectReturnLabelSource: None | (
        list[ReturnLabelSourceEnumeration | str] | ReturnLabelSourceEnumeration | str
    ) = Field(
        default=None,
        description="The method (from an enumeration) by which the customer obtains a return shipping label"
        "for a defect product.",
    )
    merchantReturnDays: None | (
        list[datetime | DateTime | int | Integer | date | Date | str]
        | datetime
        | DateTime
        | int
        | Integer
        | date
        | Date
        | str
    ) = Field(
        default=None,
        description="Specifies either a fixed return date or the number of days (from the delivery date) that"
        "a product can be returned. Used when the [[returnPolicyCategory]] property is specified"
        "as [[MerchantReturnFiniteReturnWindow]].",
    )
    customerRemorseReturnFees: None | (
        list[ReturnFeesEnumeration | str] | ReturnFeesEnumeration | str
    ) = Field(
        default=None,
        description="The type of return fees if the product is returned due to customer remorse.",
    )
    returnFees: None | (
        list[ReturnFeesEnumeration | str] | ReturnFeesEnumeration | str
    ) = Field(
        default=None,
        description="The type of return fees for purchased products (for any return reason).",
    )
    additionalProperty: None | (
        list[PropertyValue | str] | PropertyValue | str
    ) = Field(
        default=None,
        description="A property-value pair representing an additional characteristic of the entity, e.g."
        "a product feature or another characteristic for which there is no matching property"
        "in schema.org. Note: Publishers should be aware that applications designed to use specific"
        "schema.org properties (e.g. http://schema.org/width, http://schema.org/color,"
        "http://schema.org/gtin13, ...) will typically expect such data to be provided using"
        "those properties, rather than using the generic property/value mechanism.",
    )
    itemCondition: None | (
        list[OfferItemCondition | str] | OfferItemCondition | str
    ) = Field(
        default=None,
        description="A predefined value from OfferItemCondition specifying the condition of the product"
        "or service, or the products or services included in the offer. Also used for product return"
        "policies to specify the condition of products accepted for returns.",
    )
    customerRemorseReturnShippingFeesAmount: None | (
        list[MonetaryAmount | str] | MonetaryAmount | str
    ) = Field(
        default=None,
        description="The amount of shipping costs if a product is returned due to customer remorse. Applicable"
        "when property [[customerRemorseReturnFees]] equals [[ReturnShippingFees]].",
    )
    returnPolicyCategory: None | (
        list[MerchantReturnEnumeration | str] | MerchantReturnEnumeration | str
    ) = Field(
        default=None,
        description="Specifies an applicable return policy (from an enumeration).",
    )
    returnLabelSource: None | (
        list[ReturnLabelSourceEnumeration | str] | ReturnLabelSourceEnumeration | str
    ) = Field(
        default=None,
        description="The method (from an enumeration) by which the customer obtains a return shipping label"
        "for a product returned for any reason.",
    )
    merchantReturnLink: None | (list[AnyUrl | URL | str] | AnyUrl | URL | str) = Field(
        default=None,
        description="Specifies a Web page or service by URL, for product returns.",
    )
    itemDefectReturnFees: None | (
        list[ReturnFeesEnumeration | str] | ReturnFeesEnumeration | str
    ) = Field(
        default=None,
        description="The type of return fees for returns of defect products.",
    )
    itemDefectReturnShippingFeesAmount: None | (
        list[MonetaryAmount | str] | MonetaryAmount | str
    ) = Field(
        default=None,
        description="Amount of shipping costs for defect product returns. Applicable when property [[itemDefectReturnFees]]"
        "equals [[ReturnShippingFees]].",
    )
    returnPolicySeasonalOverride: None | (
        list[MerchantReturnPolicySeasonalOverride | str]
        | MerchantReturnPolicySeasonalOverride
        | str
    ) = Field(
        default=None,
        description="Seasonal override of a return policy.",
    )
    returnShippingFeesAmount: None | (
        list[MonetaryAmount | str] | MonetaryAmount | str
    ) = Field(
        default=None,
        description="Amount of shipping costs for product returns (for any reason). Applicable when property"
        "[[returnFees]] equals [[ReturnShippingFees]].",
    )
    returnPolicyCountry: None | (
        list[str | Text | Country] | str | Text | Country
    ) = Field(
        default=None,
        description='The country where the product has to be sent to for returns, for example "Ireland" using'
        "the [[name]] property of [[Country]]. You can also provide the two-letter [ISO 3166-1"
        "alpha-2 country code](http://en.wikipedia.org/wiki/ISO_3166-1). Note that this"
        "can be different from the country where the product was originally shipped from or sent"
        "to.",
    )


if TYPE_CHECKING:
    from pydantic2_schemaorg.ReturnLabelSourceEnumeration import (
        ReturnLabelSourceEnumeration,
    )
    from pydantic2_schemaorg.Boolean import Boolean
    from pydantic2_schemaorg.Number import Number
    from pydantic2_schemaorg.MonetaryAmount import MonetaryAmount
    from pydantic2_schemaorg.RefundTypeEnumeration import RefundTypeEnumeration
    from pydantic2_schemaorg.ReturnMethodEnumeration import ReturnMethodEnumeration
    from pydantic2_schemaorg.Text import Text
    from pydantic2_schemaorg.Country import Country
    from pydantic2_schemaorg.DateTime import DateTime
    from pydantic2_schemaorg.Integer import Integer
    from pydantic2_schemaorg.Date import Date
    from pydantic2_schemaorg.ReturnFeesEnumeration import ReturnFeesEnumeration
    from pydantic2_schemaorg.PropertyValue import PropertyValue
    from pydantic2_schemaorg.OfferItemCondition import OfferItemCondition
    from pydantic2_schemaorg.MerchantReturnEnumeration import MerchantReturnEnumeration
    from pydantic2_schemaorg.URL import URL
    from pydantic2_schemaorg.MerchantReturnPolicySeasonalOverride import (
        MerchantReturnPolicySeasonalOverride,
    )
