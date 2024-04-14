from __future__ import annotations

from typing import TYPE_CHECKING

from pydantic.v1 import AnyUrl
from pydantic.v1 import Field

from pydantic2_schemaorg.Organization import Organization


class NewsMediaOrganization(Organization):
    """A News/Media organization such as a newspaper or TV station.

    See: https://schema.org/NewsMediaOrganization
    Model depth: 3
    """

    type_: str = Field(default="NewsMediaOrganization", alias="@type", const=True)
    actionableFeedbackPolicy: None | (
        list[AnyUrl | URL | CreativeWork | str] | AnyUrl | URL | CreativeWork | str
    ) = Field(
        default=None,
        description="For a [[NewsMediaOrganization]] or other news-related [[Organization]], a statement"
        "about public engagement activities (for news media, the newsroom’s), including involving"
        "the public - digitally or otherwise -- in coverage decisions, reporting and activities"
        "after publication.",
    )
    noBylinesPolicy: None | (
        list[AnyUrl | URL | CreativeWork | str] | AnyUrl | URL | CreativeWork | str
    ) = Field(
        default=None,
        description="For a [[NewsMediaOrganization]] or other news-related [[Organization]], a statement"
        "explaining when authors of articles are not named in bylines.",
    )
    diversityStaffingReport: None | (
        list[AnyUrl | URL | Article | str] | AnyUrl | URL | Article | str
    ) = Field(
        default=None,
        description="For an [[Organization]] (often but not necessarily a [[NewsMediaOrganization]]),"
        "a report on staffing diversity issues. In a news context this might be for example ASNE"
        "or RTDNA (US) reports, or self-reported.",
    )
    diversityPolicy: None | (
        list[AnyUrl | URL | CreativeWork | str] | AnyUrl | URL | CreativeWork | str
    ) = Field(
        default=None,
        description="Statement on diversity policy by an [[Organization]] e.g. a [[NewsMediaOrganization]]."
        "For a [[NewsMediaOrganization]], a statement describing the newsroom’s diversity"
        "policy on both staffing and sources, typically providing staffing data.",
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
    unnamedSourcesPolicy: None | (
        list[AnyUrl | URL | CreativeWork | str] | AnyUrl | URL | CreativeWork | str
    ) = Field(
        default=None,
        description="For an [[Organization]] (typically a [[NewsMediaOrganization]]), a statement about"
        "policy on use of unnamed sources and the decision process required.",
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
    verificationFactCheckingPolicy: None | (
        list[AnyUrl | URL | CreativeWork | str] | AnyUrl | URL | CreativeWork | str
    ) = Field(
        default=None,
        description="Disclosure about verification and fact-checking processes for a [[NewsMediaOrganization]]"
        "or other fact-checking [[Organization]].",
    )
    masthead: None | (
        list[AnyUrl | URL | CreativeWork | str] | AnyUrl | URL | CreativeWork | str
    ) = Field(
        default=None,
        description="For a [[NewsMediaOrganization]], a link to the masthead page or a page listing top editorial"
        "management.",
    )
    missionCoveragePrioritiesPolicy: None | (
        list[AnyUrl | URL | CreativeWork | str] | AnyUrl | URL | CreativeWork | str
    ) = Field(
        default=None,
        description="For a [[NewsMediaOrganization]], a statement on coverage priorities, including any"
        "public agenda or stance on issues.",
    )


if TYPE_CHECKING:
    from pydantic2_schemaorg.URL import URL
    from pydantic2_schemaorg.CreativeWork import CreativeWork
    from pydantic2_schemaorg.Article import Article
    from pydantic2_schemaorg.Text import Text
    from pydantic2_schemaorg.AboutPage import AboutPage
