from __future__ import annotations

from typing import TYPE_CHECKING

from pydantic.v1 import Field

from pydantic2_schemaorg.TechArticle import TechArticle


class APIReference(TechArticle):
    """Reference documentation for application programming interfaces (APIs).

    See: https://schema.org/APIReference
    Model depth: 5
    """

    type_: str = Field(default="APIReference", alias="@type", const=True)
    targetPlatform: list[str | Text] | str | Text | None = Field(
        default=None,
        description="Type of app development: phone, Metro style, desktop, XBox, etc.",
    )
    programmingModel: list[str | Text] | str | Text | None = Field(
        default=None,
        description="Indicates whether API is managed or unmanaged.",
    )
    assemblyVersion: list[str | Text] | str | Text | None = Field(
        default=None,
        description="Associated product/technology version. E.g., .NET Framework 4.5.",
    )
    assembly: list[str | Text] | str | Text | None = Field(
        default=None,
        description="Library file name, e.g., mscorlib.dll, system.web.dll.",
    )
    executableLibraryName: None | (list[str | Text] | str | Text) = Field(
        default=None,
        description="Library file name, e.g., mscorlib.dll, system.web.dll.",
    )


if TYPE_CHECKING:
    from pydantic2_schemaorg.Text import Text
