from __future__ import annotations

from typing import TYPE_CHECKING

from pydantic.v1 import Field

from pydantic2_schemaorg.Legislation import Legislation
from pydantic2_schemaorg.MediaObject import MediaObject


class LegislationObject(MediaObject, Legislation):
    """A specific object or file containing a Legislation. Note that the same Legislation can"
     "be published in multiple files. For example, a digitally signed PDF, a plain PDF and an"
     "HTML version.

    See: https://schema.org/LegislationObject
    Model depth: 4
    """

    type_: str = Field(default="LegislationObject", alias="@type", const=True)
    legislationLegalValue: None | (
        list[LegalValueLevel | str] | LegalValueLevel | str
    ) = Field(
        default=None,
        description="The legal value of this legislation file. The same legislation can be written in multiple"
        'files with different legal values. Typically a digitally signed PDF have a "stronger"'
        "legal value than the HTML file of the same act.",
    )


if TYPE_CHECKING:
    from pydantic2_schemaorg.LegalValueLevel import LegalValueLevel
