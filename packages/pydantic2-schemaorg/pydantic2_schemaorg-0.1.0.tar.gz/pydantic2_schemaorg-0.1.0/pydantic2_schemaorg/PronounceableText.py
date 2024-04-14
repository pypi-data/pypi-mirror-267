from __future__ import annotations

from typing import TYPE_CHECKING

from pydantic.v1 import Field

from pydantic2_schemaorg.Text import Text


class PronounceableText(Text):
    """Data type: PronounceableText.

    See: https://schema.org/PronounceableText
    Model depth: 6
    """

    type_: str = Field(default="PronounceableText", alias="@type", const=True)
    inLanguage: None | (list[str | Text | Language] | str | Text | Language) = Field(
        default=None,
        description="The language of the content or performance or used in an action. Please use one of the language"
        "codes from the [IETF BCP 47 standard](http://tools.ietf.org/html/bcp47). See also"
        "[[availableLanguage]].",
    )
    phoneticText: list[str | Text] | str | Text | None = Field(
        default=None,
        description="Representation of a text [[textValue]] using the specified [[speechToTextMarkup]]."
        "For example the city name of Houston in IPA: /ˈhjuːstən/.",
    )
    speechToTextMarkup: list[str | Text] | str | Text | None = Field(
        default=None,
        description="Form of markup used. eg. [SSML](https://www.w3.org/TR/speech-synthesis11) or [IPA](https://www.wikidata.org/wiki/Property:P898).",
    )
    textValue: list[str | Text] | str | Text | None = Field(
        default=None,
        description="Text value being annotated.",
    )


if TYPE_CHECKING:
    from pydantic2_schemaorg.Text import Text
    from pydantic2_schemaorg.Language import Language
