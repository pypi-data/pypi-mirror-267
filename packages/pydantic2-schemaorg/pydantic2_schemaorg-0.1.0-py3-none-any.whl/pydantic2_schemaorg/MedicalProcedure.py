from __future__ import annotations

from typing import TYPE_CHECKING

from pydantic.v1 import Field

from pydantic2_schemaorg.MedicalEntity import MedicalEntity


class MedicalProcedure(MedicalEntity):
    """A process of care used in either a diagnostic, therapeutic, preventive or palliative"
     "capacity that relies on invasive (surgical), non-invasive, or other techniques.

    See: https://schema.org/MedicalProcedure
    Model depth: 3
    """

    type_: str = Field(default="MedicalProcedure", alias="@type", const=True)
    bodyLocation: list[str | Text] | str | Text | None = Field(
        default=None,
        description="Location in the body of the anatomical structure.",
    )
    howPerformed: list[str | Text] | str | Text | None = Field(
        default=None,
        description="How the procedure is performed.",
    )
    procedureType: None | (
        list[MedicalProcedureType | str] | MedicalProcedureType | str
    ) = Field(
        default=None,
        description="The type of procedure, for example Surgical, Noninvasive, or Percutaneous.",
    )
    status: None | (
        list[str | Text | MedicalStudyStatus | EventStatusType]
        | str
        | Text
        | MedicalStudyStatus
        | EventStatusType
    ) = Field(
        default=None,
        description="The status of the study (enumerated).",
    )
    followup: list[str | Text] | str | Text | None = Field(
        default=None,
        description="Typical or recommended followup care after the procedure is performed.",
    )
    preparation: None | (
        list[str | Text | MedicalEntity] | str | Text | MedicalEntity
    ) = Field(
        default=None,
        description="Typical preparation that a patient must undergo before having the procedure performed.",
    )


if TYPE_CHECKING:
    from pydantic2_schemaorg.Text import Text
    from pydantic2_schemaorg.MedicalProcedureType import MedicalProcedureType
    from pydantic2_schemaorg.MedicalStudyStatus import MedicalStudyStatus
    from pydantic2_schemaorg.EventStatusType import EventStatusType
    from pydantic2_schemaorg.MedicalEntity import MedicalEntity
