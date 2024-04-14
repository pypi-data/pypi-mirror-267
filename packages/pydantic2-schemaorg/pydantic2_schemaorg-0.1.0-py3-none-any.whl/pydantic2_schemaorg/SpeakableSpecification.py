from __future__ import annotations

from typing import TYPE_CHECKING

from pydantic.v1 import Field

from pydantic2_schemaorg.Intangible import Intangible


class SpeakableSpecification(Intangible):
    """A SpeakableSpecification indicates (typically via [[xpath]] or [[cssSelector]])"
     "sections of a document that are highlighted as particularly [[speakable]]. Instances"
     "of this type are expected to be used primarily as values of the [[speakable]] property.

    See: https://schema.org/SpeakableSpecification
    Model depth: 3
    """

    type_: str = Field(default="SpeakableSpecification", alias="@type", const=True)
    xpath: list[str | XPathType] | str | XPathType | None = Field(
        default=None,
        description="An XPath, e.g. of a [[SpeakableSpecification]] or [[WebPageElement]]. In the latter"
        'case, multiple matches within a page can constitute a single conceptual "Web page element".',
    )
    cssSelector: None | (list[str | CssSelectorType] | str | CssSelectorType) = Field(
        default=None,
        description="A CSS selector, e.g. of a [[SpeakableSpecification]] or [[WebPageElement]]. In the"
        'latter case, multiple matches within a page can constitute a single conceptual "Web'
        'page element".',
    )


if TYPE_CHECKING:
    from pydantic2_schemaorg.XPathType import XPathType
    from pydantic2_schemaorg.CssSelectorType import CssSelectorType
