from __future__ import annotations

from typing import TYPE_CHECKING

from pydantic.v1 import AnyUrl
from pydantic.v1 import Field

from pydantic2_schemaorg.Thing import Thing


class BioChemEntity(Thing):
    """Any biological, chemical, or biochemical thing. For example: a protein; a gene; a chemical;"
     "a synthetic chemical.

    See: https://schema.org/BioChemEntity
    Model depth: 2
    """

    type_: str = Field(default="BioChemEntity", alias="@type", const=True)
    funding: list[Grant | str] | Grant | str | None = Field(
        default=None,
        description="A [[Grant]] that directly or indirectly provide funding or sponsorship for this item."
        "See also [[ownershipFundingInfo]].",
    )
    isLocatedInSubcellularLocation: None | (
        list[AnyUrl | URL | DefinedTerm | PropertyValue | str]
        | AnyUrl
        | URL
        | DefinedTerm
        | PropertyValue
        | str
    ) = Field(
        default=None,
        description="Subcellular location where this BioChemEntity is located; please use PropertyValue"
        "if you want to include any evidence.",
    )
    associatedDisease: None | (
        list[AnyUrl | URL | PropertyValue | MedicalCondition | str]
        | AnyUrl
        | URL
        | PropertyValue
        | MedicalCondition
        | str
    ) = Field(
        default=None,
        description="Disease associated to this BioChemEntity. Such disease can be a MedicalCondition or"
        "a URL. If you want to add an evidence supporting the association, please use PropertyValue.",
    )
    hasBioChemEntityPart: None | (
        list[BioChemEntity | str] | BioChemEntity | str
    ) = Field(
        default=None,
        description="Indicates a BioChemEntity that (in some sense) has this BioChemEntity as a part.",
    )
    hasRepresentation: None | (
        list[AnyUrl | URL | str | Text | PropertyValue]
        | AnyUrl
        | URL
        | str
        | Text
        | PropertyValue
    ) = Field(
        default=None,
        description="A common representation such as a protein sequence or chemical structure for this entity."
        "For images use schema.org/image.",
    )
    isInvolvedInBiologicalProcess: None | (
        list[AnyUrl | URL | DefinedTerm | PropertyValue | str]
        | AnyUrl
        | URL
        | DefinedTerm
        | PropertyValue
        | str
    ) = Field(
        default=None,
        description="Biological process this BioChemEntity is involved in; please use PropertyValue if"
        "you want to include any evidence.",
    )
    isPartOfBioChemEntity: None | (
        list[BioChemEntity | str] | BioChemEntity | str
    ) = Field(
        default=None,
        description="Indicates a BioChemEntity that is (in some sense) a part of this BioChemEntity.",
    )
    biologicalRole: None | (list[DefinedTerm | str] | DefinedTerm | str) = Field(
        default=None,
        description="A role played by the BioChemEntity within a biological context.",
    )
    hasMolecularFunction: None | (
        list[AnyUrl | URL | DefinedTerm | PropertyValue | str]
        | AnyUrl
        | URL
        | DefinedTerm
        | PropertyValue
        | str
    ) = Field(
        default=None,
        description="Molecular function performed by this BioChemEntity; please use PropertyValue if you"
        "want to include any evidence.",
    )
    bioChemSimilarity: None | (list[BioChemEntity | str] | BioChemEntity | str) = Field(
        default=None,
        description="A similar BioChemEntity, e.g., obtained by fingerprint similarity algorithms.",
    )
    isEncodedByBioChemEntity: None | (list[Gene | str] | Gene | str) = Field(
        default=None,
        description="Another BioChemEntity encoding by this one.",
    )
    taxonomicRange: None | (
        list[AnyUrl | URL | str | Text | Taxon | DefinedTerm]
        | AnyUrl
        | URL
        | str
        | Text
        | Taxon
        | DefinedTerm
    ) = Field(
        default=None,
        description="The taxonomic grouping of the organism that expresses, encodes, or in some way related"
        "to the BioChemEntity.",
    )
    bioChemInteraction: None | (
        list[BioChemEntity | str] | BioChemEntity | str
    ) = Field(
        default=None,
        description="A BioChemEntity that is known to interact with this item.",
    )


if TYPE_CHECKING:
    from pydantic2_schemaorg.Grant import Grant
    from pydantic2_schemaorg.URL import URL
    from pydantic2_schemaorg.DefinedTerm import DefinedTerm
    from pydantic2_schemaorg.PropertyValue import PropertyValue
    from pydantic2_schemaorg.MedicalCondition import MedicalCondition
    from pydantic2_schemaorg.Text import Text
    from pydantic2_schemaorg.Gene import Gene
    from pydantic2_schemaorg.Taxon import Taxon
