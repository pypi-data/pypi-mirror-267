from __future__ import annotations

from typing import TYPE_CHECKING

from pydantic.v1 import AnyUrl
from pydantic.v1 import Field

from pydantic2_schemaorg.Intangible import Intangible


class Brand(Intangible):
    """A brand is a name used by an organization or business person for labeling a product, product"
     "group, or similar.

    See: https://schema.org/Brand
    Model depth: 3
    """

    type_: str = Field(default="Brand", alias="@type", const=True)
    aggregateRating: None | (
        list[AggregateRating | str] | AggregateRating | str
    ) = Field(
        default=None,
        description="The overall rating, based on a collection of reviews or ratings, of the item.",
    )
    review: list[Review | str] | Review | str | None = Field(
        default=None,
        description="A review of the item.",
    )
    slogan: list[str | Text] | str | Text | None = Field(
        default=None,
        description="A slogan or motto associated with the item.",
    )
    logo: None | (
        list[AnyUrl | URL | ImageObject | str] | AnyUrl | URL | ImageObject | str
    ) = Field(
        default=None,
        description="An associated logo.",
    )


if TYPE_CHECKING:
    from pydantic2_schemaorg.AggregateRating import AggregateRating
    from pydantic2_schemaorg.Review import Review
    from pydantic2_schemaorg.Text import Text
    from pydantic2_schemaorg.URL import URL
    from pydantic2_schemaorg.ImageObject import ImageObject
