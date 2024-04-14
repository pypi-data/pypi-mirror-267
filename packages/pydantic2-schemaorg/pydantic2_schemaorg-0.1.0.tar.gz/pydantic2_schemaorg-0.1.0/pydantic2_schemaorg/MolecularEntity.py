from __future__ import annotations

from typing import TYPE_CHECKING

from pydantic.v1 import Field

from pydantic2_schemaorg.BioChemEntity import BioChemEntity


class MolecularEntity(BioChemEntity):
    """Any constitutionally or isotopically distinct atom, molecule, ion, ion pair, radical,"
     "radical ion, complex, conformer etc., identifiable as a separately distinguishable"
     "entity.

    See: https://schema.org/MolecularEntity
    Model depth: 3
    """

    type_: str = Field(default="MolecularEntity", alias="@type", const=True)
    potentialUse: None | (list[DefinedTerm | str] | DefinedTerm | str) = Field(
        default=None,
        description="Intended use of the BioChemEntity by humans.",
    )
    chemicalRole: None | (list[DefinedTerm | str] | DefinedTerm | str) = Field(
        default=None,
        description="A role played by the BioChemEntity within a chemical context.",
    )
    smiles: list[str | Text] | str | Text | None = Field(
        default=None,
        description="A specification in form of a line notation for describing the structure of chemical species"
        r"using short ASCII strings. Double bond stereochemistry \ indicators may need to be escaped"
        "in the string in formats where the backslash is an escape character.",
    )
    iupacName: list[str | Text] | str | Text | None = Field(
        default=None,
        description="Systematic method of naming chemical compounds as recommended by the International"
        "Union of Pure and Applied Chemistry (IUPAC).",
    )
    inChI: list[str | Text] | str | Text | None = Field(
        default=None,
        description="Non-proprietary identifier for molecular entity that can be used in printed and electronic"
        "data sources thus enabling easier linking of diverse data compilations.",
    )
    monoisotopicMolecularWeight: None | (
        list[str | Text | QuantitativeValue] | str | Text | QuantitativeValue
    ) = Field(
        default=None,
        description="The monoisotopic mass is the sum of the masses of the atoms in a molecule using the unbound,"
        "ground-state, rest mass of the principal (most abundant) isotope for each element instead"
        "of the isotopic average mass. Please include the units in the form '&lt;Number&gt; &lt;unit&gt;',"
        "for example '770.230488 g/mol' or as '&lt;QuantitativeValue&gt;.",
    )
    molecularWeight: None | (
        list[str | Text | QuantitativeValue] | str | Text | QuantitativeValue
    ) = Field(
        default=None,
        description="This is the molecular weight of the entity being described, not of the parent. Units should"
        "be included in the form '&lt;Number&gt; &lt;unit&gt;', for example '12 amu' or as '&lt;QuantitativeValue&gt;.",
    )
    inChIKey: list[str | Text] | str | Text | None = Field(
        default=None,
        description="InChIKey is a hashed version of the full InChI (using the SHA-256 algorithm).",
    )
    molecularFormula: list[str | Text] | str | Text | None = Field(
        default=None,
        description="The empirical formula is the simplest whole number ratio of all the atoms in a molecule.",
    )


if TYPE_CHECKING:
    from pydantic2_schemaorg.DefinedTerm import DefinedTerm
    from pydantic2_schemaorg.Text import Text
    from pydantic2_schemaorg.QuantitativeValue import QuantitativeValue
