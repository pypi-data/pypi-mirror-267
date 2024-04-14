from __future__ import annotations

from typing import TYPE_CHECKING

from pydantic.v1 import Field

from pydantic2_schemaorg.MedicalTest import MedicalTest


class PathologyTest(MedicalTest):
    """A medical test performed by a laboratory that typically involves examination of a tissue"
     "sample by a pathologist.

    See: https://schema.org/PathologyTest
    Model depth: 4
    """

    type_: str = Field(default="PathologyTest", alias="@type", const=True)
    tissueSample: list[str | Text] | str | Text | None = Field(
        default=None,
        description="The type of tissue sample required for the test.",
    )


if TYPE_CHECKING:
    from pydantic2_schemaorg.Text import Text
