from __future__ import annotations

from typing import TYPE_CHECKING

from pydantic.v1 import Field

from pydantic2_schemaorg.MedicalEntity import MedicalEntity


class MedicalCondition(MedicalEntity):
    """Any condition of the human body that affects the normal functioning of a person, whether"
     "physically or mentally. Includes diseases, injuries, disabilities, disorders, syndromes,"
     "etc.

    See: https://schema.org/MedicalCondition
    Model depth: 3
    """

    type_: str = Field(default="MedicalCondition", alias="@type", const=True)
    typicalTest: None | (list[MedicalTest | str] | MedicalTest | str) = Field(
        default=None,
        description="A medical test typically performed given this condition.",
    )
    differentialDiagnosis: None | (list[DDxElement | str] | DDxElement | str) = Field(
        default=None,
        description="One of a set of differential diagnoses for the condition. Specifically, a closely-related"
        "or competing diagnosis typically considered later in the cognitive process whereby"
        "this medical condition is distinguished from others most likely responsible for a similar"
        "collection of signs and symptoms to reach the most parsimonious diagnosis or diagnoses"
        "in a patient.",
    )
    secondaryPrevention: None | (
        list[MedicalTherapy | str] | MedicalTherapy | str
    ) = Field(
        default=None,
        description="A preventative therapy used to prevent reoccurrence of the medical condition after"
        "an initial episode of the condition.",
    )
    expectedPrognosis: list[str | Text] | str | Text | None = Field(
        default=None,
        description="The likely outcome in either the short term or long term of the medical condition.",
    )
    stage: None | (
        list[MedicalConditionStage | str] | MedicalConditionStage | str
    ) = Field(
        default=None,
        description="The stage of the condition, if applicable.",
    )
    possibleTreatment: None | (
        list[MedicalTherapy | str] | MedicalTherapy | str
    ) = Field(
        default=None,
        description="A possible treatment to address this condition, sign or symptom.",
    )
    primaryPrevention: None | (
        list[MedicalTherapy | str] | MedicalTherapy | str
    ) = Field(
        default=None,
        description="A preventative therapy used to prevent an initial occurrence of the medical condition,"
        "such as vaccination.",
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
    drug: list[Drug | str] | Drug | str | None = Field(
        default=None,
        description="Specifying a drug or medicine used in a medication procedure.",
    )
    associatedAnatomy: None | (
        list[(AnatomicalStructure | SuperficialAnatomy | AnatomicalSystem | str)]
        | AnatomicalStructure
        | SuperficialAnatomy
        | AnatomicalSystem
        | str
    ) = Field(
        default=None,
        description="The anatomy of the underlying organ system or structures associated with this entity.",
    )
    possibleComplication: None | (list[str | Text] | str | Text) = Field(
        default=None,
        description="A possible unexpected and unfavorable evolution of a medical condition. Complications"
        "may include worsening of the signs or symptoms of the disease, extension of the condition"
        "to other organ systems, etc.",
    )
    riskFactor: None | (
        list[MedicalRiskFactor | str] | MedicalRiskFactor | str
    ) = Field(
        default=None,
        description="A modifiable or non-modifiable factor that increases the risk of a patient contracting"
        "this condition, e.g. age, coexisting condition.",
    )
    signOrSymptom: None | (
        list[MedicalSignOrSymptom | str] | MedicalSignOrSymptom | str
    ) = Field(
        default=None,
        description="A sign or symptom of this condition. Signs are objective or physically observable manifestations"
        "of the medical condition while symptoms are the subjective experience of the medical"
        "condition.",
    )
    pathophysiology: list[str | Text] | str | Text | None = Field(
        default=None,
        description="Changes in the normal mechanical, physical, and biochemical functions that are associated"
        "with this activity or condition.",
    )
    naturalProgression: list[str | Text] | str | Text | None = Field(
        default=None,
        description="The expected progression of the condition if it is not treated and allowed to progress"
        "naturally.",
    )
    epidemiology: list[str | Text] | str | Text | None = Field(
        default=None,
        description="The characteristics of associated patients, such as age, gender, race etc.",
    )


if TYPE_CHECKING:
    from pydantic2_schemaorg.MedicalTest import MedicalTest
    from pydantic2_schemaorg.DDxElement import DDxElement
    from pydantic2_schemaorg.MedicalTherapy import MedicalTherapy
    from pydantic2_schemaorg.Text import Text
    from pydantic2_schemaorg.MedicalConditionStage import MedicalConditionStage
    from pydantic2_schemaorg.MedicalStudyStatus import MedicalStudyStatus
    from pydantic2_schemaorg.EventStatusType import EventStatusType
    from pydantic2_schemaorg.Drug import Drug
    from pydantic2_schemaorg.AnatomicalStructure import AnatomicalStructure
    from pydantic2_schemaorg.SuperficialAnatomy import SuperficialAnatomy
    from pydantic2_schemaorg.AnatomicalSystem import AnatomicalSystem
    from pydantic2_schemaorg.MedicalRiskFactor import MedicalRiskFactor
    from pydantic2_schemaorg.MedicalSignOrSymptom import MedicalSignOrSymptom
