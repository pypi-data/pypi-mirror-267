from __future__ import annotations

from typing import TYPE_CHECKING

from pydantic.v1 import Field
from pydantic.v1 import StrictFloat
from pydantic.v1 import StrictInt

from pydantic2_schemaorg.StructuredValue import StructuredValue


class GeoCoordinates(StructuredValue):
    """The geographic coordinates of a place or event.

    See: https://schema.org/GeoCoordinates
    Model depth: 4
    """

    type_: str = Field(default="GeoCoordinates", alias="@type", const=True)
    addressCountry: None | (list[str | Text | Country] | str | Text | Country) = Field(
        default=None,
        description="The country. For example, USA. You can also provide the two-letter [ISO 3166-1 alpha-2"
        "country code](http://en.wikipedia.org/wiki/ISO_3166-1).",
    )
    elevation: None | (
        list[StrictInt | StrictFloat | Number | str | Text]
        | StrictInt
        | StrictFloat
        | Number
        | str
        | Text
    ) = Field(
        default=None,
        description="The elevation of a location ([WGS 84](https://en.wikipedia.org/wiki/World_Geodetic_System))."
        r"Values may be of the form 'NUMBER UNIT\_OF\_MEASUREMENT' (e.g., '1,000 m', '3,200 ft')"
        "while numbers alone should be assumed to be a value in meters.",
    )
    latitude: None | (
        list[StrictInt | StrictFloat | Number | str | Text]
        | StrictInt
        | StrictFloat
        | Number
        | str
        | Text
    ) = Field(
        default=None,
        description="The latitude of a location. For example ```37.42242``` ([WGS 84](https://en.wikipedia.org/wiki/World_Geodetic_System)).",
    )
    longitude: None | (
        list[StrictInt | StrictFloat | Number | str | Text]
        | StrictInt
        | StrictFloat
        | Number
        | str
        | Text
    ) = Field(
        default=None,
        description="The longitude of a location. For example ```-122.08585``` ([WGS 84](https://en.wikipedia.org/wiki/World_Geodetic_System)).",
    )
    address: None | (
        list[str | Text | PostalAddress] | str | Text | PostalAddress
    ) = Field(
        default=None,
        description="Physical address of the item.",
    )
    postalCode: list[str | Text] | str | Text | None = Field(
        default=None,
        description="The postal code. For example, 94043.",
    )


if TYPE_CHECKING:
    from pydantic2_schemaorg.Text import Text
    from pydantic2_schemaorg.Country import Country
    from pydantic2_schemaorg.Number import Number
    from pydantic2_schemaorg.PostalAddress import PostalAddress
