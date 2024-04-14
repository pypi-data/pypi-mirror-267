from __future__ import annotations

from typing import TYPE_CHECKING

from pydantic.v1 import Field

from pydantic2_schemaorg.CreativeWork import CreativeWork


class Review(CreativeWork):
    """A review of an item - for example, of a restaurant, movie, or store.

    See: https://schema.org/Review
    Model depth: 3
    """

    type_: str = Field(default="Review", alias="@type", const=True)
    itemReviewed: list[Thing | str] | Thing | str | None = Field(
        default=None,
        description="The item that is being reviewed/rated.",
    )
    associatedClaimReview: None | (list[Review | str] | Review | str) = Field(
        default=None,
        description="An associated [[ClaimReview]], related by specific common content, topic or claim."
        "The expectation is that this property would be most typically used in cases where a single"
        "activity is conducting both claim reviews and media reviews, in which case [[relatedMediaReview]]"
        "would commonly be used on a [[ClaimReview]], while [[relatedClaimReview]] would be"
        "used on [[MediaReview]].",
    )
    positiveNotes: None | (
        list[str | Text | ListItem | WebContent | ItemList]
        | str
        | Text
        | ListItem
        | WebContent
        | ItemList
    ) = Field(
        default=None,
        description="Provides positive considerations regarding something, for example product highlights"
        "or (alongside [[negativeNotes]]) pro/con lists for reviews. In the case of a [[Review]],"
        "the property describes the [[itemReviewed]] from the perspective of the review; in"
        "the case of a [[Product]], the product itself is being described. The property values"
        "can be expressed either as unstructured text (repeated as necessary), or if ordered,"
        "as a list (in which case the most positive is at the beginning of the list).",
    )
    reviewAspect: list[str | Text] | str | Text | None = Field(
        default=None,
        description="This Review or Rating is relevant to this part or facet of the itemReviewed.",
    )
    associatedReview: None | (list[Review | str] | Review | str) = Field(
        default=None,
        description="An associated [[Review]].",
    )
    reviewRating: list[Rating | str] | Rating | str | None = Field(
        default=None,
        description="The rating given in this review. Note that reviews can themselves be rated. The ```reviewRating```"
        "applies to rating given by the review. The [[aggregateRating]] property applies to"
        "the review itself, as a creative work.",
    )
    associatedMediaReview: None | (list[Review | str] | Review | str) = Field(
        default=None,
        description="An associated [[MediaReview]], related by specific common content, topic or claim."
        "The expectation is that this property would be most typically used in cases where a single"
        "activity is conducting both claim reviews and media reviews, in which case [[relatedMediaReview]]"
        "would commonly be used on a [[ClaimReview]], while [[relatedClaimReview]] would be"
        "used on [[MediaReview]].",
    )
    reviewBody: list[str | Text] | str | Text | None = Field(
        default=None,
        description="The actual body of the review.",
    )
    negativeNotes: None | (
        list[str | Text | ListItem | WebContent | ItemList]
        | str
        | Text
        | ListItem
        | WebContent
        | ItemList
    ) = Field(
        default=None,
        description="Provides negative considerations regarding something, most typically in pro/con"
        "lists for reviews (alongside [[positiveNotes]]). For symmetry In the case of a [[Review]],"
        "the property describes the [[itemReviewed]] from the perspective of the review; in"
        "the case of a [[Product]], the product itself is being described. Since product descriptions"
        "tend to emphasise positive claims, it may be relatively unusual to find [[negativeNotes]]"
        "used in this way. Nevertheless for the sake of symmetry, [[negativeNotes]] can be used"
        "on [[Product]]. The property values can be expressed either as unstructured text (repeated"
        "as necessary), or if ordered, as a list (in which case the most negative is at the beginning"
        "of the list).",
    )


if TYPE_CHECKING:
    from pydantic2_schemaorg.Thing import Thing
    from pydantic2_schemaorg.Text import Text
    from pydantic2_schemaorg.ListItem import ListItem
    from pydantic2_schemaorg.WebContent import WebContent
    from pydantic2_schemaorg.ItemList import ItemList
    from pydantic2_schemaorg.Rating import Rating
