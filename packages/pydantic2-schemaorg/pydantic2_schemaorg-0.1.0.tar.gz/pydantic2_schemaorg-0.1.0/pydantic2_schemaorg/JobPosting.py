from __future__ import annotations

from datetime import date
from datetime import datetime
from typing import TYPE_CHECKING

from pydantic.v1 import AnyUrl
from pydantic.v1 import Field
from pydantic.v1 import StrictBool
from pydantic.v1 import StrictFloat
from pydantic.v1 import StrictInt

from pydantic2_schemaorg.Intangible import Intangible


class JobPosting(Intangible):
    """A listing that describes a job opening in a certain organization.

    See: https://schema.org/JobPosting
    Model depth: 3
    """

    type_: str = Field(default="JobPosting", alias="@type", const=True)
    employmentUnit: None | (list[Organization | str] | Organization | str) = Field(
        default=None,
        description="Indicates the department, unit and/or facility where the employee reports and/or in"
        "which the job is to be performed.",
    )
    occupationalCategory: None | (
        list[str | Text | CategoryCode] | str | Text | CategoryCode
    ) = Field(
        default=None,
        description="A category describing the job, preferably using a term from a taxonomy such as [BLS O*NET-SOC](http://www.onetcenter.org/taxonomy.html),"
        "[ISCO-08](https://www.ilo.org/public/english/bureau/stat/isco/isco08/) or"
        "similar, with the property repeated for each applicable value. Ideally the taxonomy"
        "should be identified, and both the textual label and formal code for the category should"
        "be provided. Note: for historical reasons, any textual label and formal code provided"
        "as a literal may be assumed to be from O*NET-SOC.",
    )
    physicalRequirement: None | (
        list[AnyUrl | URL | str | Text | DefinedTerm]
        | AnyUrl
        | URL
        | str
        | Text
        | DefinedTerm
    ) = Field(
        default=None,
        description="A description of the types of physical activity associated with the job. Defined terms"
        "such as those in O*net may be used, but note that there is no way to specify the level of ability"
        "as well as its nature when using a defined term.",
    )
    experienceInPlaceOfEducation: None | (
        list[StrictBool | Boolean | str] | StrictBool | Boolean | str
    ) = Field(
        default=None,
        description="Indicates whether a [[JobPosting]] will accept experience (as indicated by [[OccupationalExperienceRequirements]])"
        "in place of its formal educational qualifications (as indicated by [[educationRequirements]])."
        "If true, indicates that satisfying one of these requirements is sufficient.",
    )
    jobImmediateStart: None | (
        list[StrictBool | Boolean | str] | StrictBool | Boolean | str
    ) = Field(
        default=None,
        description="An indicator as to whether a position is available for an immediate start.",
    )
    qualifications: None | (
        list[str | Text | EducationalOccupationalCredential]
        | str
        | Text
        | EducationalOccupationalCredential
    ) = Field(
        default=None,
        description="Specific qualifications required for this role or Occupation.",
    )
    sensoryRequirement: None | (
        list[AnyUrl | URL | str | Text | DefinedTerm]
        | AnyUrl
        | URL
        | str
        | Text
        | DefinedTerm
    ) = Field(
        default=None,
        description="A description of any sensory requirements and levels necessary to function on the job,"
        "including hearing and vision. Defined terms such as those in O*net may be used, but note"
        "that there is no way to specify the level of ability as well as its nature when using a defined"
        "term.",
    )
    title: list[str | Text] | str | Text | None = Field(
        default=None,
        description="The title of the job.",
    )
    baseSalary: None | (
        list[
            (
                StrictInt
                | StrictFloat
                | Number
                | PriceSpecification
                | MonetaryAmount
                | str
            )
        ]
        | StrictInt
        | StrictFloat
        | Number
        | PriceSpecification
        | MonetaryAmount
        | str
    ) = Field(
        default=None,
        description="The base salary of the job or of an employee in an EmployeeRole.",
    )
    salaryCurrency: list[str | Text] | str | Text | None = Field(
        default=None,
        description="The currency (coded using [ISO 4217](http://en.wikipedia.org/wiki/ISO_4217))"
        "used for the main salary information in this job posting or for this employee.",
    )
    securityClearanceRequirement: None | (
        list[AnyUrl | URL | str | Text] | AnyUrl | URL | str | Text
    ) = Field(
        default=None,
        description="A description of any security clearance requirements of the job.",
    )
    skills: None | (list[str | Text | DefinedTerm] | str | Text | DefinedTerm) = Field(
        default=None,
        description="A statement of knowledge, skill, ability, task or any other assertion expressing a competency"
        "that is desired or required to fulfill this role or to work in this occupation.",
    )
    employmentType: list[str | Text] | str | Text | None = Field(
        default=None,
        description="Type of employment (e.g. full-time, part-time, contract, temporary, seasonal, internship).",
    )
    hiringOrganization: None | (
        list[Organization | Person | str] | Organization | Person | str
    ) = Field(
        default=None,
        description="Organization or Person offering the job position.",
    )
    totalJobOpenings: None | (list[int | Integer | str] | int | Integer | str) = Field(
        default=None,
        description="The number of positions open for this job posting. Use a positive integer. Do not use if"
        "the number of positions is unclear or not known.",
    )
    jobLocation: list[Place | str] | Place | str | None = Field(
        default=None,
        description="A (typically single) geographic location associated with the job position.",
    )
    applicationContact: None | (list[ContactPoint | str] | ContactPoint | str) = Field(
        default=None,
        description="Contact details for further information relevant to this job posting.",
    )
    incentives: list[str | Text] | str | Text | None = Field(
        default=None,
        description="Description of bonus and commission compensation aspects of the job.",
    )
    educationRequirements: None | (
        list[str | Text | EducationalOccupationalCredential]
        | str
        | Text
        | EducationalOccupationalCredential
    ) = Field(
        default=None,
        description="Educational background needed for the position or Occupation.",
    )
    workHours: list[str | Text] | str | Text | None = Field(
        default=None,
        description="The typical working hours for this job (e.g. 1st shift, night shift, 8am-5pm).",
    )
    benefits: list[str | Text] | str | Text | None = Field(
        default=None,
        description="Description of benefits associated with the job.",
    )
    applicantLocationRequirements: None | (
        list[AdministrativeArea | str] | AdministrativeArea | str
    ) = Field(
        default=None,
        description="The location(s) applicants can apply from. This is usually used for telecommuting jobs"
        "where the applicant does not need to be in a physical office. Note: This should not be used"
        "for citizenship or work visa requirements.",
    )
    directApply: None | (
        list[StrictBool | Boolean | str] | StrictBool | Boolean | str
    ) = Field(
        default=None,
        description="Indicates whether an [[url]] that is associated with a [[JobPosting]] enables direct"
        "application for the job, via the posting website. A job posting is considered to have"
        "directApply of [[True]] if an application process for the specified job can be directly"
        "initiated via the url(s) given (noting that e.g. multiple internet domains might nevertheless"
        "be involved at an implementation level). A value of [[False]] is appropriate if there"
        "is no clear path to applying directly online for the specified job, navigating directly"
        "from the JobPosting url(s) supplied.",
    )
    jobLocationType: list[str | Text] | str | Text | None = Field(
        default=None,
        description="A description of the job location (e.g. TELECOMMUTE for telecommute jobs).",
    )
    employerOverview: list[str | Text] | str | Text | None = Field(
        default=None,
        description="A description of the employer, career opportunities and work environment for this position.",
    )
    industry: None | (
        list[str | Text | DefinedTerm] | str | Text | DefinedTerm
    ) = Field(
        default=None,
        description="The industry associated with the job position.",
    )
    jobStartDate: None | (
        list[date | Date | str | Text] | date | Date | str | Text
    ) = Field(
        default=None,
        description="The date on which a successful applicant for this job would be expected to start work."
        "Choose a specific date in the future or use the jobImmediateStart property to indicate"
        "the position is to be filled as soon as possible.",
    )
    incentiveCompensation: None | (list[str | Text] | str | Text) = Field(
        default=None,
        description="Description of bonus and commission compensation aspects of the job.",
    )
    responsibilities: list[str | Text] | str | Text | None = Field(
        default=None,
        description="Responsibilities associated with this role or Occupation.",
    )
    datePosted: None | (
        list[datetime | DateTime | date | Date | str]
        | datetime
        | DateTime
        | date
        | Date
        | str
    ) = Field(
        default=None,
        description="Publication date of an online listing.",
    )
    specialCommitments: list[str | Text] | str | Text | None = Field(
        default=None,
        description="Any special commitments associated with this job posting. Valid entries include VeteranCommit,"
        "MilitarySpouseCommit, etc.",
    )
    estimatedSalary: None | (
        list[
            (
                StrictInt
                | StrictFloat
                | Number
                | MonetaryAmount
                | MonetaryAmountDistribution
                | str
            )
        ]
        | StrictInt
        | StrictFloat
        | Number
        | MonetaryAmount
        | MonetaryAmountDistribution
        | str
    ) = Field(
        default=None,
        description="An estimated salary for a job posting or occupation, based on a variety of variables including,"
        "but not limited to industry, job title, and location. Estimated salaries are often computed"
        "by outside organizations rather than the hiring organization, who may not have committed"
        "to the estimated value.",
    )
    relevantOccupation: None | (list[Occupation | str] | Occupation | str) = Field(
        default=None,
        description="The Occupation for the JobPosting.",
    )
    experienceRequirements: None | (
        list[str | Text | OccupationalExperienceRequirements]
        | str
        | Text
        | OccupationalExperienceRequirements
    ) = Field(
        default=None,
        description="Description of skills and experience needed for the position or Occupation.",
    )
    eligibilityToWorkRequirement: None | (list[str | Text] | str | Text) = Field(
        default=None,
        description="The legal requirements such as citizenship, visa and other documentation required"
        "for an applicant to this job.",
    )
    jobBenefits: list[str | Text] | str | Text | None = Field(
        default=None,
        description="Description of benefits associated with the job.",
    )
    validThrough: None | (
        list[datetime | DateTime | date | Date | str]
        | datetime
        | DateTime
        | date
        | Date
        | str
    ) = Field(
        default=None,
        description="The date after when the item is not valid. For example the end of an offer, salary period,"
        "or a period of opening hours.",
    )


if TYPE_CHECKING:
    from pydantic2_schemaorg.Organization import Organization
    from pydantic2_schemaorg.Text import Text
    from pydantic2_schemaorg.CategoryCode import CategoryCode
    from pydantic2_schemaorg.URL import URL
    from pydantic2_schemaorg.DefinedTerm import DefinedTerm
    from pydantic2_schemaorg.Boolean import Boolean
    from pydantic2_schemaorg.EducationalOccupationalCredential import (
        EducationalOccupationalCredential,
    )
    from pydantic2_schemaorg.Number import Number
    from pydantic2_schemaorg.PriceSpecification import PriceSpecification
    from pydantic2_schemaorg.MonetaryAmount import MonetaryAmount
    from pydantic2_schemaorg.Person import Person
    from pydantic2_schemaorg.Integer import Integer
    from pydantic2_schemaorg.Place import Place
    from pydantic2_schemaorg.ContactPoint import ContactPoint
    from pydantic2_schemaorg.AdministrativeArea import AdministrativeArea
    from pydantic2_schemaorg.Date import Date
    from pydantic2_schemaorg.DateTime import DateTime
    from pydantic2_schemaorg.MonetaryAmountDistribution import (
        MonetaryAmountDistribution,
    )
    from pydantic2_schemaorg.Occupation import Occupation
    from pydantic2_schemaorg.OccupationalExperienceRequirements import (
        OccupationalExperienceRequirements,
    )
