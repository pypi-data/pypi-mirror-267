from __future__ import annotations

from typing import TYPE_CHECKING

from pydantic.v1 import Field

from pydantic2_schemaorg.MedicalEntity import MedicalEntity


class DrugClass(MedicalEntity):
    """A class of medical drugs, e.g., statins. Classes can represent general pharmacological"
     "class, common mechanisms of action, common physiological effects, etc.

    See: https://schema.org/DrugClass
    Model depth: 3
    """

    type_: str = Field(default="DrugClass", alias="@type", const=True)
    drug: list[Drug | str] | Drug | str | None = Field(
        default=None,
        description="Specifying a drug or medicine used in a medication procedure.",
    )


if TYPE_CHECKING:
    from pydantic2_schemaorg.Drug import Drug
