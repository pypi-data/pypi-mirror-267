from __future__ import annotations

from typing import TYPE_CHECKING

from pydantic.v1 import AnyUrl
from pydantic.v1 import Field

from pydantic2_schemaorg.CreativeWork import CreativeWork


class SoftwareSourceCode(CreativeWork):
    """Computer programming source code. Example: Full (compile ready) solutions, code snippet"
     "samples, scripts, templates.

    See: https://schema.org/SoftwareSourceCode
    Model depth: 3
    """

    type_: str = Field(default="SoftwareSourceCode", alias="@type", const=True)
    codeSampleType: list[str | Text] | str | Text | None = Field(
        default=None,
        description="What type of code sample: full (compile ready) solution, code snippet, inline code,"
        "scripts, template.",
    )
    runtimePlatform: list[str | Text] | str | Text | None = Field(
        default=None,
        description="Runtime platform or script interpreter dependencies (example: Java v1, Python 2.3,"
        ".NET Framework 3.0).",
    )
    targetProduct: None | (
        list[SoftwareApplication | str] | SoftwareApplication | str
    ) = Field(
        default=None,
        description="Target Operating System / Product to which the code applies. If applies to several versions,"
        "just the product name can be used.",
    )
    runtime: list[str | Text] | str | Text | None = Field(
        default=None,
        description="Runtime platform or script interpreter dependencies (example: Java v1, Python 2.3,"
        ".NET Framework 3.0).",
    )
    programmingLanguage: None | (
        list[str | Text | ComputerLanguage] | str | Text | ComputerLanguage
    ) = Field(
        default=None,
        description="The computer programming language.",
    )
    codeRepository: None | (list[AnyUrl | URL | str] | AnyUrl | URL | str) = Field(
        default=None,
        description="Link to the repository where the un-compiled, human readable code and related code is"
        "located (SVN, GitHub, CodePlex).",
    )
    sampleType: list[str | Text] | str | Text | None = Field(
        default=None,
        description="What type of code sample: full (compile ready) solution, code snippet, inline code,"
        "scripts, template.",
    )


if TYPE_CHECKING:
    from pydantic2_schemaorg.Text import Text
    from pydantic2_schemaorg.SoftwareApplication import SoftwareApplication
    from pydantic2_schemaorg.ComputerLanguage import ComputerLanguage
    from pydantic2_schemaorg.URL import URL
