from __future__ import annotations

from typing import TYPE_CHECKING

from pydantic.v1 import AnyUrl
from pydantic.v1 import Field
from pydantic.v1 import StrictBool
from pydantic.v1 import StrictFloat
from pydantic.v1 import StrictInt

from pydantic2_schemaorg.Residence import Residence


class ApartmentComplex(Residence):
    """Residence type: Apartment complex.

    See: https://schema.org/ApartmentComplex
    Model depth: 4
    """

    type_: str = Field(default="ApartmentComplex", alias="@type", const=True)
    numberOfAvailableAccommodationUnits: None | (
        list[QuantitativeValue | str] | QuantitativeValue | str
    ) = Field(
        default=None,
        description="Indicates the number of available accommodation units in an [[ApartmentComplex]],"
        "or the number of accommodation units for a specific [[FloorPlan]] (within its specific"
        "[[ApartmentComplex]]). See also [[numberOfAccommodationUnits]].",
    )
    petsAllowed: None | (
        list[str | Text | StrictBool | Boolean] | str | Text | StrictBool | Boolean
    ) = Field(
        default=None,
        description="Indicates whether pets are allowed to enter the accommodation or lodging business."
        "More detailed information can be put in a text value.",
    )
    tourBookingPage: None | (list[AnyUrl | URL | str] | AnyUrl | URL | str) = Field(
        default=None,
        description="A page providing information on how to book a tour of some [[Place]], such as an [[Accommodation]]"
        "or [[ApartmentComplex]] in a real estate setting, as well as other kinds of tours as appropriate.",
    )
    numberOfBedrooms: None | (
        list[StrictInt | StrictFloat | Number | QuantitativeValue | str]
        | StrictInt
        | StrictFloat
        | Number
        | QuantitativeValue
        | str
    ) = Field(
        default=None,
        description="The total integer number of bedrooms in a some [[Accommodation]], [[ApartmentComplex]]"
        "or [[FloorPlan]].",
    )
    numberOfAccommodationUnits: None | (
        list[QuantitativeValue | str] | QuantitativeValue | str
    ) = Field(
        default=None,
        description="Indicates the total (available plus unavailable) number of accommodation units in"
        "an [[ApartmentComplex]], or the number of accommodation units for a specific [[FloorPlan]]"
        "(within its specific [[ApartmentComplex]]). See also [[numberOfAvailableAccommodationUnits]].",
    )


if TYPE_CHECKING:
    from pydantic2_schemaorg.QuantitativeValue import QuantitativeValue
    from pydantic2_schemaorg.Text import Text
    from pydantic2_schemaorg.Boolean import Boolean
    from pydantic2_schemaorg.URL import URL
    from pydantic2_schemaorg.Number import Number
