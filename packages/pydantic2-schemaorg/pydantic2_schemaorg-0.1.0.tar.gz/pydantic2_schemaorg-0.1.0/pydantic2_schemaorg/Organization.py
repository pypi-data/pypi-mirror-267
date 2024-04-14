from __future__ import annotations

from datetime import date
from typing import TYPE_CHECKING

from pydantic.v1 import AnyUrl
from pydantic.v1 import Field

from pydantic2_schemaorg.Thing import Thing


class Organization(Thing):
    """An organization such as a school, NGO, corporation, club, etc.

    See: https://schema.org/Organization
    Model depth: 2
    """

    type_: str = Field(default="Organization", alias="@type", const=True)
    actionableFeedbackPolicy: None | (
        list[AnyUrl | URL | CreativeWork | str] | AnyUrl | URL | CreativeWork | str
    ) = Field(
        default=None,
        description="For a [[NewsMediaOrganization]] or other news-related [[Organization]], a statement"
        "about public engagement activities (for news media, the newsroom’s), including involving"
        "the public - digitally or otherwise -- in coverage decisions, reporting and activities"
        "after publication.",
    )
    dissolutionDate: None | (list[date | Date | str] | date | Date | str) = Field(
        default=None,
        description="The date that this organization was dissolved.",
    )
    funding: list[Grant | str] | Grant | str | None = Field(
        default=None,
        description="A [[Grant]] that directly or indirectly provide funding or sponsorship for this item."
        "See also [[ownershipFundingInfo]].",
    )
    reviews: list[Review | str] | Review | str | None = Field(
        default=None,
        description="Review of the item.",
    )
    memberOf: None | (
        list[ProgramMembership | Organization | str]
        | ProgramMembership
        | Organization
        | str
    ) = Field(
        default=None,
        description="An Organization (or ProgramMembership) to which this Person or Organization belongs.",
    )
    event: list[Event | str] | Event | str | None = Field(
        default=None,
        description="Upcoming or past event associated with this place, organization, or action.",
    )
    foundingDate: None | (list[date | Date | str] | date | Date | str) = Field(
        default=None,
        description="The date that this organization was founded.",
    )
    hasProductReturnPolicy: None | (
        list[ProductReturnPolicy | str] | ProductReturnPolicy | str
    ) = Field(
        default=None,
        description="Indicates a ProductReturnPolicy that may be applicable.",
    )
    foundingLocation: list[Place | str] | Place | str | None = Field(
        default=None,
        description="The place where the Organization was founded.",
    )
    founder: list[Person | str] | Person | str | None = Field(
        default=None,
        description="A person who founded this organization.",
    )
    employees: list[Person | str] | Person | str | None = Field(
        default=None,
        description="People working for this organization.",
    )
    makesOffer: list[Offer | str] | Offer | str | None = Field(
        default=None,
        description="A pointer to products or services offered by the organization or person.",
    )
    hasMerchantReturnPolicy: None | (
        list[MerchantReturnPolicy | str] | MerchantReturnPolicy | str
    ) = Field(
        default=None,
        description="Specifies a MerchantReturnPolicy that may be applicable.",
    )
    telephone: list[str | Text] | str | Text | None = Field(
        default=None,
        description="The telephone number.",
    )
    sponsor: None | (
        list[Organization | Person | str] | Organization | Person | str
    ) = Field(
        default=None,
        description="A person or organization that supports a thing through a pledge, promise, or financial"
        "contribution. E.g. a sponsor of a Medical Study or a corporate sponsor of an event.",
    )
    diversityStaffingReport: None | (
        list[AnyUrl | URL | Article | str] | AnyUrl | URL | Article | str
    ) = Field(
        default=None,
        description="For an [[Organization]] (often but not necessarily a [[NewsMediaOrganization]]),"
        "a report on staffing diversity issues. In a news context this might be for example ASNE"
        "or RTDNA (US) reports, or self-reported.",
    )
    numberOfEmployees: None | (
        list[QuantitativeValue | str] | QuantitativeValue | str
    ) = Field(
        default=None,
        description="The number of employees in an organization, e.g. business.",
    )
    owns: None | (
        list[OwnershipInfo | Product | str] | OwnershipInfo | Product | str
    ) = Field(
        default=None,
        description="Products owned by the organization or person.",
    )
    hasOfferCatalog: None | (list[OfferCatalog | str] | OfferCatalog | str) = Field(
        default=None,
        description="Indicates an OfferCatalog listing for this Organization, Person, or Service.",
    )
    diversityPolicy: None | (
        list[AnyUrl | URL | CreativeWork | str] | AnyUrl | URL | CreativeWork | str
    ) = Field(
        default=None,
        description="Statement on diversity policy by an [[Organization]] e.g. a [[NewsMediaOrganization]]."
        "For a [[NewsMediaOrganization]], a statement describing the newsroom’s diversity"
        "policy on both staffing and sources, typically providing staffing data.",
    )
    nonprofitStatus: None | (list[NonprofitType | str] | NonprofitType | str) = Field(
        default=None,
        description="nonprofitStatus indicates the legal status of a non-profit organization in its primary"
        "place of business.",
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
    legalName: list[str | Text] | str | Text | None = Field(
        default=None,
        description="The official name of the organization, e.g. the registered company name.",
    )
    founders: list[Person | str] | Person | str | None = Field(
        default=None,
        description="A person who founded this organization.",
    )
    globalLocationNumber: None | (list[str | Text] | str | Text) = Field(
        default=None,
        description="The [Global Location Number](http://www.gs1.org/gln) (GLN, sometimes also referred"
        "to as International Location Number or ILN) of the respective organization, person,"
        "or place. The GLN is a 13-digit number used to identify parties and physical locations.",
    )
    correctionsPolicy: None | (
        list[AnyUrl | URL | CreativeWork | str] | AnyUrl | URL | CreativeWork | str
    ) = Field(
        default=None,
        description="For an [[Organization]] (e.g. [[NewsMediaOrganization]]), a statement describing"
        "(in news media, the newsroom’s) disclosure and correction policy for errors.",
    )
    ethicsPolicy: None | (
        list[AnyUrl | URL | CreativeWork | str] | AnyUrl | URL | CreativeWork | str
    ) = Field(
        default=None,
        description="Statement about ethics policy, e.g. of a [[NewsMediaOrganization]] regarding journalistic"
        "and publishing practices, or of a [[Restaurant]], a page describing food source policies."
        "In the case of a [[NewsMediaOrganization]], an ethicsPolicy is typically a statement"
        "describing the personal, organizational, and corporate standards of behavior expected"
        "by the organization.",
    )
    naics: list[str | Text] | str | Text | None = Field(
        default=None,
        description="The North American Industry Classification System (NAICS) code for a particular organization"
        "or business person.",
    )
    email: list[str | Text] | str | Text | None = Field(
        default=None,
        description="Email address.",
    )
    unnamedSourcesPolicy: None | (
        list[AnyUrl | URL | CreativeWork | str] | AnyUrl | URL | CreativeWork | str
    ) = Field(
        default=None,
        description="For an [[Organization]] (typically a [[NewsMediaOrganization]]), a statement about"
        "policy on use of unnamed sources and the decision process required.",
    )
    department: None | (list[Organization | str] | Organization | str) = Field(
        default=None,
        description="A relationship between an organization and a department of that organization, also"
        "described as an organization (allowing different urls, logos, opening hours). For"
        "example: a store with a pharmacy, or a bakery with a cafe.",
    )
    vatID: list[str | Text] | str | Text | None = Field(
        default=None,
        description="The Value-added Tax ID of the organization or person.",
    )
    parentOrganization: None | (list[Organization | str] | Organization | str) = Field(
        default=None,
        description="The larger organization that this organization is a [[subOrganization]] of, if any.",
    )
    taxID: list[str | Text] | str | Text | None = Field(
        default=None,
        description="The Tax / Fiscal ID of the organization or person, e.g. the TIN in the US or the CIF/NIF in"
        "Spain.",
    )
    faxNumber: list[str | Text] | str | Text | None = Field(
        default=None,
        description="The fax number.",
    )
    knowsAbout: None | (
        list[AnyUrl | URL | str | Text | Thing] | AnyUrl | URL | str | Text | Thing
    ) = Field(
        default=None,
        description="Of a [[Person]], and less typically of an [[Organization]], to indicate a topic that"
        "is known about - suggesting possible expertise but not implying it. We do not distinguish"
        "skill levels here, or relate this to educational content, events, objectives or [[JobPosting]]"
        "descriptions.",
    )
    brand: None | (
        list[Brand | Organization | str] | Brand | Organization | str
    ) = Field(
        default=None,
        description="The brand(s) associated with a product or service, or the brand(s) maintained by an organization"
        "or business person.",
    )
    aggregateRating: None | (
        list[AggregateRating | str] | AggregateRating | str
    ) = Field(
        default=None,
        description="The overall rating, based on a collection of reviews or ratings, of the item.",
    )
    serviceArea: None | (
        list[AdministrativeArea | GeoShape | Place | str]
        | AdministrativeArea
        | GeoShape
        | Place
        | str
    ) = Field(
        default=None,
        description="The geographic area where the service is provided.",
    )
    interactionStatistic: None | (
        list[InteractionCounter | str] | InteractionCounter | str
    ) = Field(
        default=None,
        description="The number of interactions for the CreativeWork using the WebSite or SoftwareApplication."
        "The most specific child type of InteractionCounter should be used.",
    )
    ownershipFundingInfo: None | (
        list[AnyUrl | URL | str | Text | CreativeWork | AboutPage]
        | AnyUrl
        | URL
        | str
        | Text
        | CreativeWork
        | AboutPage
    ) = Field(
        default=None,
        description="For an [[Organization]] (often but not necessarily a [[NewsMediaOrganization]]),"
        "a description of organizational ownership structure; funding and grants. In a news/media"
        "setting, this is with particular reference to editorial independence. Note that the"
        "[[funder]] is also available and can be used to make basic funder information machine-readable.",
    )
    contactPoints: None | (list[ContactPoint | str] | ContactPoint | str) = Field(
        default=None,
        description="A contact point for a person or organization.",
    )
    awards: list[str | Text] | str | Text | None = Field(
        default=None,
        description="Awards won by or for this item.",
    )
    funder: None | (
        list[Organization | Person | str] | Organization | Person | str
    ) = Field(
        default=None,
        description="A person or organization that supports (sponsors) something through some kind of financial"
        "contribution.",
    )
    leiCode: list[str | Text] | str | Text | None = Field(
        default=None,
        description="An organization identifier that uniquely identifies a legal entity as defined in ISO"
        "17442.",
    )
    keywords: None | (
        list[AnyUrl | URL | str | Text | DefinedTerm]
        | AnyUrl
        | URL
        | str
        | Text
        | DefinedTerm
    ) = Field(
        default=None,
        description="Keywords or tags used to describe some item. Multiple textual entries in a keywords list"
        "are typically delimited by commas, or by repeating the property.",
    )
    location: None | (
        list[str | Text | VirtualLocation | PostalAddress | Place]
        | str
        | Text
        | VirtualLocation
        | PostalAddress
        | Place
    ) = Field(
        default=None,
        description="The location of, for example, where an event is happening, where an organization is located,"
        "or where an action takes place.",
    )
    review: list[Review | str] | Review | str | None = Field(
        default=None,
        description="A review of the item.",
    )
    agentInteractionStatistic: None | (
        list[InteractionCounter | str] | InteractionCounter | str
    ) = Field(
        default=None,
        description="The number of completed interactions for this entity, in a particular role (the 'agent'),"
        "in a particular action (indicated in the statistic), and in a particular context (i.e."
        "interactionService).",
    )
    subOrganization: None | (list[Organization | str] | Organization | str) = Field(
        default=None,
        description="A relationship between two organizations where the first includes the second, e.g.,"
        "as a subsidiary. See also: the more specific 'department' property.",
    )
    seeks: list[Demand | str] | Demand | str | None = Field(
        default=None,
        description="A pointer to products or services sought by the organization or person (demand).",
    )
    hasCredential: None | (
        list[EducationalOccupationalCredential | str]
        | EducationalOccupationalCredential
        | str
    ) = Field(
        default=None,
        description="A credential awarded to the Person or Organization.",
    )
    address: None | (
        list[str | Text | PostalAddress] | str | Text | PostalAddress
    ) = Field(
        default=None,
        description="Physical address of the item.",
    )
    contactPoint: None | (list[ContactPoint | str] | ContactPoint | str) = Field(
        default=None,
        description="A contact point for a person or organization.",
    )
    knowsLanguage: None | (list[str | Text | Language] | str | Text | Language) = Field(
        default=None,
        description="Of a [[Person]], and less typically of an [[Organization]], to indicate a known language."
        "We do not distinguish skill levels or reading/writing/speaking/signing here. Use"
        "language codes from the [IETF BCP 47 standard](http://tools.ietf.org/html/bcp47).",
    )
    alumni: list[Person | str] | Person | str | None = Field(
        default=None,
        description="Alumni of an organization.",
    )
    hasPOS: list[Place | str] | Place | str | None = Field(
        default=None,
        description="Points-of-Sales operated by the organization or person.",
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
    isicV4: list[str | Text] | str | Text | None = Field(
        default=None,
        description="The International Standard of Industrial Classification of All Economic Activities"
        "(ISIC), Revision 4 code for a particular organization, business person, or place.",
    )
    employee: list[Person | str] | Person | str | None = Field(
        default=None,
        description="Someone working for this organization.",
    )
    duns: list[str | Text] | str | Text | None = Field(
        default=None,
        description="The Dun & Bradstreet DUNS number for identifying an organization or business person.",
    )
    award: list[str | Text] | str | Text | None = Field(
        default=None,
        description="An award won by or for this item.",
    )
    publishingPrinciples: None | (
        list[AnyUrl | URL | CreativeWork | str] | AnyUrl | URL | CreativeWork | str
    ) = Field(
        default=None,
        description="The publishingPrinciples property indicates (typically via [[URL]]) a document describing"
        "the editorial principles of an [[Organization]] (or individual, e.g. a [[Person]]"
        "writing a blog) that relate to their activities as a publisher, e.g. ethics or diversity"
        "policies. When applied to a [[CreativeWork]] (e.g. [[NewsArticle]]) the principles"
        "are those of the party primarily responsible for the creation of the [[CreativeWork]]."
        "While such policies are most typically expressed in natural language, sometimes related"
        "information (e.g. indicating a [[funder]]) can be expressed using schema.org terminology.",
    )
    slogan: list[str | Text] | str | Text | None = Field(
        default=None,
        description="A slogan or motto associated with the item.",
    )
    iso6523Code: list[str | Text] | str | Text | None = Field(
        default=None,
        description="An organization identifier as defined in ISO 6523(-1). Note that many existing organization"
        "identifiers such as [leiCode](http://schema.org/leiCode), [duns](http://schema.org/duns)"
        "and [vatID](http://schema.org/vatID) can be expressed as an ISO 6523 identifier by"
        "setting the ICD part of the ISO 6523 identifier accordingly.",
    )
    logo: None | (
        list[AnyUrl | URL | ImageObject | str] | AnyUrl | URL | ImageObject | str
    ) = Field(
        default=None,
        description="An associated logo.",
    )
    events: list[Event | str] | Event | str | None = Field(
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
