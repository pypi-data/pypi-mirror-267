from __future__ import annotations

from typing import TYPE_CHECKING

from pydantic.v1 import Field

from pydantic2_schemaorg.CreateAction import CreateAction


class WriteAction(CreateAction):
    """The act of authoring written creative content.

    See: https://schema.org/WriteAction
    Model depth: 4
    """

    type_: str = Field(default="WriteAction", alias="@type", const=True)
    inLanguage: None | (list[str | Text | Language] | str | Text | Language) = Field(
        default=None,
        description="The language of the content or performance or used in an action. Please use one of the language"
        "codes from the [IETF BCP 47 standard](http://tools.ietf.org/html/bcp47). See also"
        "[[availableLanguage]].",
    )
    language: list[Language | str] | Language | str | None = Field(
        default=None,
        description="A sub property of instrument. The language used on this action.",
    )


if TYPE_CHECKING:
    from pydantic2_schemaorg.Text import Text
    from pydantic2_schemaorg.Language import Language
