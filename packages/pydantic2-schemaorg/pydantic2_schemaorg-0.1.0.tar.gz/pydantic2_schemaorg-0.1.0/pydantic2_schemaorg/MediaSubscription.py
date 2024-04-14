from __future__ import annotations

from typing import TYPE_CHECKING

from pydantic.v1 import Field

from pydantic2_schemaorg.Intangible import Intangible


class MediaSubscription(Intangible):
    """A subscription which allows a user to access media including audio, video, books, etc.

    See: https://schema.org/MediaSubscription
    Model depth: 3
    """

    type_: str = Field(default="MediaSubscription", alias="@type", const=True)
    expectsAcceptanceOf: None | (list[Offer | str] | Offer | str) = Field(
        default=None,
        description="An Offer which must be accepted before the user can perform the Action. For example, the"
        "user may need to buy a movie before being able to watch it.",
    )
    authenticator: None | (list[Organization | str] | Organization | str) = Field(
        default=None,
        description="The Organization responsible for authenticating the user's subscription. For example,"
        "many media apps require a cable/satellite provider to authenticate your subscription"
        "before playing media.",
    )


if TYPE_CHECKING:
    from pydantic2_schemaorg.Offer import Offer
    from pydantic2_schemaorg.Organization import Organization
