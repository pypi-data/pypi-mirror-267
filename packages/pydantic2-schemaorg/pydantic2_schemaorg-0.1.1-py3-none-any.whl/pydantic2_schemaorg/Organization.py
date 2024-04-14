from __future__ import annotations
from typing import TYPE_CHECKING

from pydantic.v1 import AnyUrl
from typing import List, Optional, Union
from datetime import date


from pydantic.v1 import Field
from pydantic2_schemaorg.Thing import Thing


class Organization(Thing):
    """An organization such as a school, NGO, corporation, club, etc.

    See: https://schema.org/Organization
    Model depth: 2
    """

    type_: str = Field(default="Organization", alias="@type", const=True)
    actionableFeedbackPolicy: Optional[
        Union[
            List[Union[AnyUrl, "URL", "CreativeWork", str]],
            AnyUrl,
            "URL",
            "CreativeWork",
            str,
        ]
    ] = Field(
        default=None,
        description="For a [[NewsMediaOrganization]] or other news-related [[Organization]], a statement"
        "about public engagement activities (for news media, the newsroom’s), including involving"
        "the public - digitally or otherwise -- in coverage decisions, reporting and activities"
        "after publication.",
    )
    dissolutionDate: Optional[
        Union[List[Union[date, "Date", str]], date, "Date", str]
    ] = Field(
        default=None,
        description="The date that this organization was dissolved.",
    )
    funding: Optional[Union[List[Union["Grant", str]], "Grant", str]] = Field(
        default=None,
        description="A [[Grant]] that directly or indirectly provide funding or sponsorship for this item."
        "See also [[ownershipFundingInfo]].",
    )
    reviews: Optional[Union[List[Union["Review", str]], "Review", str]] = Field(
        default=None,
        description="Review of the item.",
    )
    memberOf: Optional[
        Union[
            List[Union["ProgramMembership", "Organization", str]],
            "ProgramMembership",
            "Organization",
            str,
        ]
    ] = Field(
        default=None,
        description="An Organization (or ProgramMembership) to which this Person or Organization belongs.",
    )
    event: Optional[Union[List[Union["Event", str]], "Event", str]] = Field(
        default=None,
        description="Upcoming or past event associated with this place, organization, or action.",
    )
    foundingDate: Optional[Union[List[Union[date, "Date", str]], date, "Date", str]] = (
        Field(
            default=None,
            description="The date that this organization was founded.",
        )
    )
    hasProductReturnPolicy: Optional[
        Union[List[Union["ProductReturnPolicy", str]], "ProductReturnPolicy", str]
    ] = Field(
        default=None,
        description="Indicates a ProductReturnPolicy that may be applicable.",
    )
    foundingLocation: Optional[Union[List[Union["Place", str]], "Place", str]] = Field(
        default=None,
        description="The place where the Organization was founded.",
    )
    founder: Optional[Union[List[Union["Person", str]], "Person", str]] = Field(
        default=None,
        description="A person who founded this organization.",
    )
    employees: Optional[Union[List[Union["Person", str]], "Person", str]] = Field(
        default=None,
        description="People working for this organization.",
    )
    makesOffer: Optional[Union[List[Union["Offer", str]], "Offer", str]] = Field(
        default=None,
        description="A pointer to products or services offered by the organization or person.",
    )
    hasMerchantReturnPolicy: Optional[
        Union[List[Union["MerchantReturnPolicy", str]], "MerchantReturnPolicy", str]
    ] = Field(
        default=None,
        description="Specifies a MerchantReturnPolicy that may be applicable.",
    )
    telephone: Optional[Union[List[Union[str, "Text"]], str, "Text"]] = Field(
        default=None,
        description="The telephone number.",
    )
    sponsor: Optional[
        Union[List[Union["Organization", "Person", str]], "Organization", "Person", str]
    ] = Field(
        default=None,
        description="A person or organization that supports a thing through a pledge, promise, or financial"
        "contribution. E.g. a sponsor of a Medical Study or a corporate sponsor of an event.",
    )
    diversityStaffingReport: Optional[
        Union[List[Union[AnyUrl, "URL", "Article", str]], AnyUrl, "URL", "Article", str]
    ] = Field(
        default=None,
        description="For an [[Organization]] (often but not necessarily a [[NewsMediaOrganization]]),"
        "a report on staffing diversity issues. In a news context this might be for example ASNE"
        "or RTDNA (US) reports, or self-reported.",
    )
    numberOfEmployees: Optional[
        Union[List[Union["QuantitativeValue", str]], "QuantitativeValue", str]
    ] = Field(
        default=None,
        description="The number of employees in an organization, e.g. business.",
    )
    owns: Optional[
        Union[
            List[Union["OwnershipInfo", "Product", str]],
            "OwnershipInfo",
            "Product",
            str,
        ]
    ] = Field(
        default=None,
        description="Products owned by the organization or person.",
    )
    hasOfferCatalog: Optional[
        Union[List[Union["OfferCatalog", str]], "OfferCatalog", str]
    ] = Field(
        default=None,
        description="Indicates an OfferCatalog listing for this Organization, Person, or Service.",
    )
    diversityPolicy: Optional[
        Union[
            List[Union[AnyUrl, "URL", "CreativeWork", str]],
            AnyUrl,
            "URL",
            "CreativeWork",
            str,
        ]
    ] = Field(
        default=None,
        description="Statement on diversity policy by an [[Organization]] e.g. a [[NewsMediaOrganization]]."
        "For a [[NewsMediaOrganization]], a statement describing the newsroom’s diversity"
        "policy on both staffing and sources, typically providing staffing data.",
    )
    nonprofitStatus: Optional[
        Union[List[Union["NonprofitType", str]], "NonprofitType", str]
    ] = Field(
        default=None,
        description="nonprofitStatus indicates the legal status of a non-profit organization in its primary"
        "place of business.",
    )
    members: Optional[
        Union[List[Union["Organization", "Person", str]], "Organization", "Person", str]
    ] = Field(
        default=None,
        description="A member of this organization.",
    )
    member: Optional[
        Union[List[Union["Organization", "Person", str]], "Organization", "Person", str]
    ] = Field(
        default=None,
        description="A member of an Organization or a ProgramMembership. Organizations can be members of"
        "organizations; ProgramMembership is typically for individuals.",
    )
    legalName: Optional[Union[List[Union[str, "Text"]], str, "Text"]] = Field(
        default=None,
        description="The official name of the organization, e.g. the registered company name.",
    )
    founders: Optional[Union[List[Union["Person", str]], "Person", str]] = Field(
        default=None,
        description="A person who founded this organization.",
    )
    globalLocationNumber: Optional[Union[List[Union[str, "Text"]], str, "Text"]] = (
        Field(
            default=None,
            description="The [Global Location Number](http://www.gs1.org/gln) (GLN, sometimes also referred"
            "to as International Location Number or ILN) of the respective organization, person,"
            "or place. The GLN is a 13-digit number used to identify parties and physical locations.",
        )
    )
    correctionsPolicy: Optional[
        Union[
            List[Union[AnyUrl, "URL", "CreativeWork", str]],
            AnyUrl,
            "URL",
            "CreativeWork",
            str,
        ]
    ] = Field(
        default=None,
        description="For an [[Organization]] (e.g. [[NewsMediaOrganization]]), a statement describing"
        "(in news media, the newsroom’s) disclosure and correction policy for errors.",
    )
    ethicsPolicy: Optional[
        Union[
            List[Union[AnyUrl, "URL", "CreativeWork", str]],
            AnyUrl,
            "URL",
            "CreativeWork",
            str,
        ]
    ] = Field(
        default=None,
        description="Statement about ethics policy, e.g. of a [[NewsMediaOrganization]] regarding journalistic"
        "and publishing practices, or of a [[Restaurant]], a page describing food source policies."
        "In the case of a [[NewsMediaOrganization]], an ethicsPolicy is typically a statement"
        "describing the personal, organizational, and corporate standards of behavior expected"
        "by the organization.",
    )
    naics: Optional[Union[List[Union[str, "Text"]], str, "Text"]] = Field(
        default=None,
        description="The North American Industry Classification System (NAICS) code for a particular organization"
        "or business person.",
    )
    email: Optional[Union[List[Union[str, "Text"]], str, "Text"]] = Field(
        default=None,
        description="Email address.",
    )
    unnamedSourcesPolicy: Optional[
        Union[
            List[Union[AnyUrl, "URL", "CreativeWork", str]],
            AnyUrl,
            "URL",
            "CreativeWork",
            str,
        ]
    ] = Field(
        default=None,
        description="For an [[Organization]] (typically a [[NewsMediaOrganization]]), a statement about"
        "policy on use of unnamed sources and the decision process required.",
    )
    department: Optional[
        Union[List[Union["Organization", str]], "Organization", str]
    ] = Field(
        default=None,
        description="A relationship between an organization and a department of that organization, also"
        "described as an organization (allowing different urls, logos, opening hours). For"
        "example: a store with a pharmacy, or a bakery with a cafe.",
    )
    vatID: Optional[Union[List[Union[str, "Text"]], str, "Text"]] = Field(
        default=None,
        description="The Value-added Tax ID of the organization or person.",
    )
    parentOrganization: Optional[
        Union[List[Union["Organization", str]], "Organization", str]
    ] = Field(
        default=None,
        description="The larger organization that this organization is a [[subOrganization]] of, if any.",
    )
    taxID: Optional[Union[List[Union[str, "Text"]], str, "Text"]] = Field(
        default=None,
        description="The Tax / Fiscal ID of the organization or person, e.g. the TIN in the US or the CIF/NIF in"
        "Spain.",
    )
    faxNumber: Optional[Union[List[Union[str, "Text"]], str, "Text"]] = Field(
        default=None,
        description="The fax number.",
    )
    knowsAbout: Optional[
        Union[
            List[Union[AnyUrl, "URL", str, "Text", "Thing"]],
            AnyUrl,
            "URL",
            str,
            "Text",
            "Thing",
        ]
    ] = Field(
        default=None,
        description="Of a [[Person]], and less typically of an [[Organization]], to indicate a topic that"
        "is known about - suggesting possible expertise but not implying it. We do not distinguish"
        "skill levels here, or relate this to educational content, events, objectives or [[JobPosting]]"
        "descriptions.",
    )
    brand: Optional[
        Union[List[Union["Brand", "Organization", str]], "Brand", "Organization", str]
    ] = Field(
        default=None,
        description="The brand(s) associated with a product or service, or the brand(s) maintained by an organization"
        "or business person.",
    )
    aggregateRating: Optional[
        Union[List[Union["AggregateRating", str]], "AggregateRating", str]
    ] = Field(
        default=None,
        description="The overall rating, based on a collection of reviews or ratings, of the item.",
    )
    serviceArea: Optional[
        Union[
            List[Union["AdministrativeArea", "GeoShape", "Place", str]],
            "AdministrativeArea",
            "GeoShape",
            "Place",
            str,
        ]
    ] = Field(
        default=None,
        description="The geographic area where the service is provided.",
    )
    interactionStatistic: Optional[
        Union[List[Union["InteractionCounter", str]], "InteractionCounter", str]
    ] = Field(
        default=None,
        description="The number of interactions for the CreativeWork using the WebSite or SoftwareApplication."
        "The most specific child type of InteractionCounter should be used.",
    )
    ownershipFundingInfo: Optional[
        Union[
            List[Union[AnyUrl, "URL", str, "Text", "CreativeWork", "AboutPage"]],
            AnyUrl,
            "URL",
            str,
            "Text",
            "CreativeWork",
            "AboutPage",
        ]
    ] = Field(
        default=None,
        description="For an [[Organization]] (often but not necessarily a [[NewsMediaOrganization]]),"
        "a description of organizational ownership structure; funding and grants. In a news/media"
        "setting, this is with particular reference to editorial independence. Note that the"
        "[[funder]] is also available and can be used to make basic funder information machine-readable.",
    )
    contactPoints: Optional[
        Union[List[Union["ContactPoint", str]], "ContactPoint", str]
    ] = Field(
        default=None,
        description="A contact point for a person or organization.",
    )
    awards: Optional[Union[List[Union[str, "Text"]], str, "Text"]] = Field(
        default=None,
        description="Awards won by or for this item.",
    )
    funder: Optional[
        Union[List[Union["Organization", "Person", str]], "Organization", "Person", str]
    ] = Field(
        default=None,
        description="A person or organization that supports (sponsors) something through some kind of financial"
        "contribution.",
    )
    leiCode: Optional[Union[List[Union[str, "Text"]], str, "Text"]] = Field(
        default=None,
        description="An organization identifier that uniquely identifies a legal entity as defined in ISO"
        "17442.",
    )
    keywords: Optional[
        Union[
            List[Union[AnyUrl, "URL", str, "Text", "DefinedTerm"]],
            AnyUrl,
            "URL",
            str,
            "Text",
            "DefinedTerm",
        ]
    ] = Field(
        default=None,
        description="Keywords or tags used to describe some item. Multiple textual entries in a keywords list"
        "are typically delimited by commas, or by repeating the property.",
    )
    location: Optional[
        Union[
            List[Union[str, "Text", "VirtualLocation", "PostalAddress", "Place"]],
            str,
            "Text",
            "VirtualLocation",
            "PostalAddress",
            "Place",
        ]
    ] = Field(
        default=None,
        description="The location of, for example, where an event is happening, where an organization is located,"
        "or where an action takes place.",
    )
    review: Optional[Union[List[Union["Review", str]], "Review", str]] = Field(
        default=None,
        description="A review of the item.",
    )
    agentInteractionStatistic: Optional[
        Union[List[Union["InteractionCounter", str]], "InteractionCounter", str]
    ] = Field(
        default=None,
        description="The number of completed interactions for this entity, in a particular role (the 'agent'),"
        "in a particular action (indicated in the statistic), and in a particular context (i.e."
        "interactionService).",
    )
    subOrganization: Optional[
        Union[List[Union["Organization", str]], "Organization", str]
    ] = Field(
        default=None,
        description="A relationship between two organizations where the first includes the second, e.g.,"
        "as a subsidiary. See also: the more specific 'department' property.",
    )
    seeks: Optional[Union[List[Union["Demand", str]], "Demand", str]] = Field(
        default=None,
        description="A pointer to products or services sought by the organization or person (demand).",
    )
    hasCredential: Optional[
        Union[
            List[Union["EducationalOccupationalCredential", str]],
            "EducationalOccupationalCredential",
            str,
        ]
    ] = Field(
        default=None,
        description="A credential awarded to the Person or Organization.",
    )
    address: Optional[
        Union[List[Union[str, "Text", "PostalAddress"]], str, "Text", "PostalAddress"]
    ] = Field(
        default=None,
        description="Physical address of the item.",
    )
    contactPoint: Optional[
        Union[List[Union["ContactPoint", str]], "ContactPoint", str]
    ] = Field(
        default=None,
        description="A contact point for a person or organization.",
    )
    knowsLanguage: Optional[
        Union[List[Union[str, "Text", "Language"]], str, "Text", "Language"]
    ] = Field(
        default=None,
        description="Of a [[Person]], and less typically of an [[Organization]], to indicate a known language."
        "We do not distinguish skill levels or reading/writing/speaking/signing here. Use"
        "language codes from the [IETF BCP 47 standard](http://tools.ietf.org/html/bcp47).",
    )
    alumni: Optional[Union[List[Union["Person", str]], "Person", str]] = Field(
        default=None,
        description="Alumni of an organization.",
    )
    hasPOS: Optional[Union[List[Union["Place", str]], "Place", str]] = Field(
        default=None,
        description="Points-of-Sales operated by the organization or person.",
    )
    areaServed: Optional[
        Union[
            List[Union[str, "Text", "AdministrativeArea", "GeoShape", "Place"]],
            str,
            "Text",
            "AdministrativeArea",
            "GeoShape",
            "Place",
        ]
    ] = Field(
        default=None,
        description="The geographic area where a service or offered item is provided.",
    )
    isicV4: Optional[Union[List[Union[str, "Text"]], str, "Text"]] = Field(
        default=None,
        description="The International Standard of Industrial Classification of All Economic Activities"
        "(ISIC), Revision 4 code for a particular organization, business person, or place.",
    )
    employee: Optional[Union[List[Union["Person", str]], "Person", str]] = Field(
        default=None,
        description="Someone working for this organization.",
    )
    duns: Optional[Union[List[Union[str, "Text"]], str, "Text"]] = Field(
        default=None,
        description="The Dun & Bradstreet DUNS number for identifying an organization or business person.",
    )
    award: Optional[Union[List[Union[str, "Text"]], str, "Text"]] = Field(
        default=None,
        description="An award won by or for this item.",
    )
    publishingPrinciples: Optional[
        Union[
            List[Union[AnyUrl, "URL", "CreativeWork", str]],
            AnyUrl,
            "URL",
            "CreativeWork",
            str,
        ]
    ] = Field(
        default=None,
        description="The publishingPrinciples property indicates (typically via [[URL]]) a document describing"
        "the editorial principles of an [[Organization]] (or individual, e.g. a [[Person]]"
        "writing a blog) that relate to their activities as a publisher, e.g. ethics or diversity"
        "policies. When applied to a [[CreativeWork]] (e.g. [[NewsArticle]]) the principles"
        "are those of the party primarily responsible for the creation of the [[CreativeWork]]."
        "While such policies are most typically expressed in natural language, sometimes related"
        "information (e.g. indicating a [[funder]]) can be expressed using schema.org terminology.",
    )
    slogan: Optional[Union[List[Union[str, "Text"]], str, "Text"]] = Field(
        default=None,
        description="A slogan or motto associated with the item.",
    )
    iso6523Code: Optional[Union[List[Union[str, "Text"]], str, "Text"]] = Field(
        default=None,
        description="An organization identifier as defined in ISO 6523(-1). Note that many existing organization"
        "identifiers such as [leiCode](http://schema.org/leiCode), [duns](http://schema.org/duns)"
        "and [vatID](http://schema.org/vatID) can be expressed as an ISO 6523 identifier by"
        "setting the ICD part of the ISO 6523 identifier accordingly.",
    )
    logo: Optional[
        Union[
            List[Union[AnyUrl, "URL", "ImageObject", str]],
            AnyUrl,
            "URL",
            "ImageObject",
            str,
        ]
    ] = Field(
        default=None,
        description="An associated logo.",
    )
    events: Optional[Union[List[Union["Event", str]], "Event", str]] = Field(
        default=None,
        description="Upcoming or past events associated with this place or organization.",
    )


if TYPE_CHECKING:
    from pydantic2_schemaorg.URL import URL
    from pydantic2_schemaorg.CreativeWork import CreativeWork
    from pydantic2_schemaorg.Date import Date
    from pydantic2_schemaorg.Grant import Grant
    from pydantic2_schemaorg.Review import Review
    from pydantic2_schemaorg.ProgramMembership import ProgramMembership
    from pydantic2_schemaorg.Event import Event
    from pydantic2_schemaorg.ProductReturnPolicy import ProductReturnPolicy
    from pydantic2_schemaorg.Place import Place
    from pydantic2_schemaorg.Person import Person
    from pydantic2_schemaorg.Offer import Offer
    from pydantic2_schemaorg.MerchantReturnPolicy import MerchantReturnPolicy
    from pydantic2_schemaorg.Text import Text
    from pydantic2_schemaorg.Article import Article
    from pydantic2_schemaorg.QuantitativeValue import QuantitativeValue
    from pydantic2_schemaorg.OwnershipInfo import OwnershipInfo
    from pydantic2_schemaorg.Product import Product
    from pydantic2_schemaorg.OfferCatalog import OfferCatalog
    from pydantic2_schemaorg.NonprofitType import NonprofitType
    from pydantic2_schemaorg.Thing import Thing
    from pydantic2_schemaorg.Brand import Brand
    from pydantic2_schemaorg.AggregateRating import AggregateRating
    from pydantic2_schemaorg.AdministrativeArea import AdministrativeArea
    from pydantic2_schemaorg.GeoShape import GeoShape
    from pydantic2_schemaorg.InteractionCounter import InteractionCounter
    from pydantic2_schemaorg.AboutPage import AboutPage
    from pydantic2_schemaorg.ContactPoint import ContactPoint
    from pydantic2_schemaorg.DefinedTerm import DefinedTerm
    from pydantic2_schemaorg.VirtualLocation import VirtualLocation
    from pydantic2_schemaorg.PostalAddress import PostalAddress
    from pydantic2_schemaorg.Demand import Demand
    from pydantic2_schemaorg.EducationalOccupationalCredential import (
        EducationalOccupationalCredential,
    )
    from pydantic2_schemaorg.Language import Language
    from pydantic2_schemaorg.ImageObject import ImageObject
