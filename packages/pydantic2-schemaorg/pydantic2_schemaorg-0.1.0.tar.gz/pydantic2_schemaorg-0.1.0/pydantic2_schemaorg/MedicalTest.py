from __future__ import annotations

from typing import TYPE_CHECKING

from pydantic.v1 import Field

from pydantic2_schemaorg.MedicalEntity import MedicalEntity


class MedicalTest(MedicalEntity):
    """Any medical test, typically performed for diagnostic purposes.

    See: https://schema.org/MedicalTest
    Model depth: 3
    """

    type_: str = Field(default="MedicalTest", alias="@type", const=True)
    signDetected: None | (list[MedicalSign | str] | MedicalSign | str) = Field(
        default=None,
        description="A sign detected by the test.",
    )
    normalRange: None | (
        list[str | Text | MedicalEnumeration] | str | Text | MedicalEnumeration
    ) = Field(
        default=None,
        description="Range of acceptable values for a typical patient, when applicable.",
    )
    usesDevice: None | (list[MedicalDevice | str] | MedicalDevice | str) = Field(
        default=None,
        description="Device used to perform the test.",
    )
    usedToDiagnose: None | (
        list[MedicalCondition | str] | MedicalCondition | str
    ) = Field(
        default=None,
        description="A condition the test is used to diagnose.",
    )
    affectedBy: list[Drug | str] | Drug | str | None = Field(
        default=None,
        description="Drugs that affect the test's results.",
    )


if TYPE_CHECKING:
    from pydantic2_schemaorg.MedicalSign import MedicalSign
    from pydantic2_schemaorg.Text import Text
    from pydantic2_schemaorg.MedicalEnumeration import MedicalEnumeration
    from pydantic2_schemaorg.MedicalDevice import MedicalDevice
    from pydantic2_schemaorg.MedicalCondition import MedicalCondition
    from pydantic2_schemaorg.Drug import Drug
