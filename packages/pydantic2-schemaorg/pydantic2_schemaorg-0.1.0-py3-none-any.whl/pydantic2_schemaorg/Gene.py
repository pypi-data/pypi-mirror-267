from __future__ import annotations

from typing import TYPE_CHECKING

from pydantic.v1 import Field

from pydantic2_schemaorg.BioChemEntity import BioChemEntity


class Gene(BioChemEntity):
    """A discrete unit of inheritance which affects one or more biological traits (Source:"
     "[https://en.wikipedia.org/wiki/Gene](https://en.wikipedia.org/wiki/Gene))."
     "Examples include FOXP2 (Forkhead box protein P2), SCARNA21 (small Cajal body-specific"
     "RNA 21), A- (agouti genotype).

    See: https://schema.org/Gene
    Model depth: 3
    """

    type_: str = Field(default="Gene", alias="@type", const=True)
    encodesBioChemEntity: None | (
        list[BioChemEntity | str] | BioChemEntity | str
    ) = Field(
        default=None,
        description="Another BioChemEntity encoded by this one.",
    )
    alternativeOf: list[Gene | str] | Gene | str | None = Field(
        default=None,
        description="Another gene which is a variation of this one.",
    )
    hasBioPolymerSequence: None | (list[str | Text] | str | Text) = Field(
        default=None,
        description="A symbolic representation of a BioChemEntity. For example, a nucleotide sequence of"
        "a Gene or an amino acid sequence of a Protein.",
    )
    expressedIn: None | (
        list[
            (BioChemEntity | DefinedTerm | AnatomicalStructure | AnatomicalSystem | str)
        ]
        | BioChemEntity
        | DefinedTerm
        | AnatomicalStructure
        | AnatomicalSystem
        | str
    ) = Field(
        default=None,
        description="Tissue, organ, biological sample, etc in which activity of this gene has been observed"
        "experimentally. For example brain, digestive system.",
    )


if TYPE_CHECKING:
    from pydantic2_schemaorg.BioChemEntity import BioChemEntity
    from pydantic2_schemaorg.Text import Text
    from pydantic2_schemaorg.DefinedTerm import DefinedTerm
    from pydantic2_schemaorg.AnatomicalStructure import AnatomicalStructure
    from pydantic2_schemaorg.AnatomicalSystem import AnatomicalSystem
