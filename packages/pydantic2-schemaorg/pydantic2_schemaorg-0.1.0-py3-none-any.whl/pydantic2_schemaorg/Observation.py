from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from pydantic.v1 import AnyUrl
from pydantic.v1 import Field

from pydantic2_schemaorg.Intangible import Intangible
from pydantic2_schemaorg.QuantitativeValue import QuantitativeValue


class Observation(QuantitativeValue, Intangible):
    """Instances of the class [[Observation]] are used to specify observations about an entity"
     "at a particular time. The principal properties of an [[Observation]] are [[observationAbout]],"
     "[[measuredProperty]], [[statType]], [[value] and [[observationDate]] and [[measuredProperty]]."
     "Some but not all Observations represent a [[QuantitativeValue]]. Quantitative observations"
     "can be about a [[StatisticalVariable]], which is an abstract specification about which"
     "we can make observations that are grounded at a particular location and time. Observations"
     "can also encode a subset of simple RDF-like statements (its observationAbout, a StatisticalVariable,"
     "defining the measuredPoperty; its observationAbout property indicating the entity"
     "the statement is about, and [[value]] ) In the context of a quantitative knowledge graph,"
     "typical properties could include [[measuredProperty]], [[observationAbout]],"
     "[[observationDate]], [[value]], [[unitCode]], [[unitText]], [[measurementMethod]].

    See: https://schema.org/Observation
    Model depth: 3
    """

    type_: str = Field(default="Observation", alias="@type", const=True)
    measurementQualifier: None | (list[Enumeration | str] | Enumeration | str) = Field(
        default=None,
        description="Provides additional qualification to an observation. For example, a GDP observation"
        "measures the Nominal value.",
    )
    measurementMethod: None | (
        list[(AnyUrl | URL | str | Text | DefinedTerm | MeasurementMethodEnum)]
        | AnyUrl
        | URL
        | str
        | Text
        | DefinedTerm
        | MeasurementMethodEnum
    ) = Field(
        default=None,
        description="A subproperty of [[measurementTechnique]] that can be used for specifying specific"
        "methods, in particular via [[MeasurementMethodEnum]].",
    )
    observationAbout: None | (list[Thing | Place | str] | Thing | Place | str) = Field(
        default=None,
        description="The [[observationAbout]] property identifies an entity, often a [[Place]], associated"
        "with an [[Observation]].",
    )
    observationPeriod: list[str | Text] | str | Text | None = Field(
        default=None,
        description="The length of time an Observation took place over. The format follows `P[0-9]*[Y|M|D|h|m|s]`."
        "For example, P1Y is Period 1 Year, P3M is Period 3 Months, P3h is Period 3 hours.",
    )
    variableMeasured: None | (
        list[str | Text | Property | PropertyValue | StatisticalVariable]
        | str
        | Text
        | Property
        | PropertyValue
        | StatisticalVariable
    ) = Field(
        default=None,
        description="The variableMeasured property can indicate (repeated as necessary) the variables"
        "that are measured in some dataset, either described as text or as pairs of identifier"
        "and description using PropertyValue, or more explicitly as a [[StatisticalVariable]].",
    )
    measurementTechnique: None | (
        list[(AnyUrl | URL | str | Text | DefinedTerm | MeasurementMethodEnum)]
        | AnyUrl
        | URL
        | str
        | Text
        | DefinedTerm
        | MeasurementMethodEnum
    ) = Field(
        default=None,
        description="A technique, method or technology used in an [[Observation]], [[StatisticalVariable]]"
        "or [[Dataset]] (or [[DataDownload]], [[DataCatalog]]), corresponding to the method"
        "used for measuring the corresponding variable(s) (for datasets, described using [[variableMeasured]];"
        "for [[Observation]], a [[StatisticalVariable]]). Often but not necessarily each"
        "[[variableMeasured]] will have an explicit representation as (or mapping to) an property"
        'such as those defined in Schema.org, or other RDF vocabularies and "knowledge graphs".'
        "In that case the subproperty of [[variableMeasured]] called [[measuredProperty]]"
        "is applicable. The [[measurementTechnique]] property helps when extra clarification"
        "is needed about how a [[measuredProperty]] was measured. This is oriented towards scientific"
        "and scholarly dataset publication but may have broader applicability; it is not intended"
        "as a full representation of measurement, but can often serve as a high level summary for"
        "dataset discovery. For example, if [[variableMeasured]] is: molecule concentration,"
        '[[measurementTechnique]] could be: "mass spectrometry" or "nmr spectroscopy"'
        'or "colorimetry" or "immunofluorescence". If the [[variableMeasured]] is "depression'
        'rating", the [[measurementTechnique]] could be "Zung Scale" or "HAM-D" or "Beck'
        'Depression Inventory". If there are several [[variableMeasured]] properties recorded'
        "for some given data object, use a [[PropertyValue]] for each [[variableMeasured]]"
        "and attach the corresponding [[measurementTechnique]]. The value can also be from"
        "an enumeration, organized as a [[MeasurementMetholdEnumeration]].",
    )
    observationDate: None | (
        list[datetime | DateTime | str] | datetime | DateTime | str
    ) = Field(
        default=None,
        description="The observationDate of an [[Observation]].",
    )
    measuredProperty: None | (list[Property | str] | Property | str) = Field(
        default=None,
        description="The measuredProperty of an [[Observation]], typically via its [[StatisticalVariable]]."
        "There are various kinds of applicable [[Property]]: a schema.org property, a property"
        "from other RDF-compatible systems, e.g. W3C RDF Data Cube, Data Commons, Wikidata,"
        "or schema.org extensions such as [GS1's](https://www.gs1.org/voc/?show=properties).",
    )
    measurementDenominator: None | (
        list[StatisticalVariable | str] | StatisticalVariable | str
    ) = Field(
        default=None,
        description="Identifies the denominator variable when an observation represents a ratio or percentage.",
    )
    marginOfError: None | (
        list[QuantitativeValue | str] | QuantitativeValue | str
    ) = Field(
        default=None,
        description="A [[marginOfError]] for an [[Observation]].",
    )


if TYPE_CHECKING:
    from pydantic2_schemaorg.Enumeration import Enumeration
    from pydantic2_schemaorg.URL import URL
    from pydantic2_schemaorg.Text import Text
    from pydantic2_schemaorg.DefinedTerm import DefinedTerm
    from pydantic2_schemaorg.MeasurementMethodEnum import MeasurementMethodEnum
    from pydantic2_schemaorg.Thing import Thing
    from pydantic2_schemaorg.Place import Place
    from pydantic2_schemaorg.Property import Property
    from pydantic2_schemaorg.PropertyValue import PropertyValue
    from pydantic2_schemaorg.StatisticalVariable import StatisticalVariable
    from pydantic2_schemaorg.DateTime import DateTime
    from pydantic2_schemaorg.QuantitativeValue import QuantitativeValue
