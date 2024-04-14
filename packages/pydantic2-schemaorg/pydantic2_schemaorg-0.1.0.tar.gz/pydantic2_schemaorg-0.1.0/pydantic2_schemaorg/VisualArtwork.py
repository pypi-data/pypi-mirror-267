from __future__ import annotations

from typing import TYPE_CHECKING

from pydantic.v1 import AnyUrl
from pydantic.v1 import Field

from pydantic2_schemaorg.CreativeWork import CreativeWork


class VisualArtwork(CreativeWork):
    """A work of art that is primarily visual in character.

    See: https://schema.org/VisualArtwork
    Model depth: 3
    """

    type_: str = Field(default="VisualArtwork", alias="@type", const=True)
    letterer: list[Person | str] | Person | str | None = Field(
        default=None,
        description="The individual who adds lettering, including speech balloons and sound effects, to"
        "artwork.",
    )
    colorist: list[Person | str] | Person | str | None = Field(
        default=None,
        description="The individual who adds color to inked drawings.",
    )
    artEdition: None | (
        list[int | Integer | str | Text] | int | Integer | str | Text
    ) = Field(
        default=None,
        description="The number of copies when multiple copies of a piece of artwork are produced - e.g. for"
        "a limited edition of 20 prints, 'artEdition' refers to the total number of copies (in"
        'this example "20").',
    )
    artist: list[Person | str] | Person | str | None = Field(
        default=None,
        description="The primary artist for a work in a medium other than pencils or digital line art--for example,"
        "if the primary artwork is done in watercolors or digital paints.",
    )
    height: None | (
        list[QuantitativeValue | Distance | str] | QuantitativeValue | Distance | str
    ) = Field(
        default=None,
        description="The height of the item.",
    )
    artform: None | (
        list[AnyUrl | URL | str | Text] | AnyUrl | URL | str | Text
    ) = Field(
        default=None,
        description="e.g. Painting, Drawing, Sculpture, Print, Photograph, Assemblage, Collage, etc.",
    )
    width: None | (
        list[QuantitativeValue | Distance | str] | QuantitativeValue | Distance | str
    ) = Field(
        default=None,
        description="The width of the item.",
    )
    penciler: list[Person | str] | Person | str | None = Field(
        default=None,
        description="The individual who draws the primary narrative artwork.",
    )
    surface: None | (
        list[AnyUrl | URL | str | Text] | AnyUrl | URL | str | Text
    ) = Field(
        default=None,
        description="A material used as a surface in some artwork, e.g. Canvas, Paper, Wood, Board, etc.",
    )
    inker: list[Person | str] | Person | str | None = Field(
        default=None,
        description="The individual who traces over the pencil drawings in ink after pencils are complete.",
    )
    artMedium: None | (
        list[AnyUrl | URL | str | Text] | AnyUrl | URL | str | Text
    ) = Field(
        default=None,
        description="The material used. (E.g. Oil, Watercolour, Acrylic, Linoprint, Marble, Cyanotype,"
        "Digital, Lithograph, DryPoint, Intaglio, Pastel, Woodcut, Pencil, Mixed Media, etc.)",
    )
    depth: None | (
        list[QuantitativeValue | Distance | str] | QuantitativeValue | Distance | str
    ) = Field(
        default=None,
        description="The depth of the item.",
    )
    artworkSurface: None | (
        list[AnyUrl | URL | str | Text] | AnyUrl | URL | str | Text
    ) = Field(
        default=None,
        description="The supporting materials for the artwork, e.g. Canvas, Paper, Wood, Board, etc.",
    )


if TYPE_CHECKING:
    from pydantic2_schemaorg.Person import Person
    from pydantic2_schemaorg.Integer import Integer
    from pydantic2_schemaorg.Text import Text
    from pydantic2_schemaorg.QuantitativeValue import QuantitativeValue
    from pydantic2_schemaorg.Distance import Distance
    from pydantic2_schemaorg.URL import URL
