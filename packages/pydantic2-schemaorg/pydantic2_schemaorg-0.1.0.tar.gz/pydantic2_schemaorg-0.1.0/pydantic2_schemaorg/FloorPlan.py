from __future__ import annotations

from typing import TYPE_CHECKING

from pydantic.v1 import AnyUrl
from pydantic.v1 import Field
from pydantic.v1 import StrictBool
from pydantic.v1 import StrictFloat
from pydantic.v1 import StrictInt

from pydantic2_schemaorg.Intangible import Intangible


class FloorPlan(Intangible):
    """A FloorPlan is an explicit representation of a collection of similar accommodations,"
     "allowing the provision of common information (room counts, sizes, layout diagrams)"
     "and offers for rental or sale. In typical use, some [[ApartmentComplex]] has an [[accommodationFloorPlan]]"
     "which is a [[FloorPlan]]. A FloorPlan is always in the context of a particular place,"
     "either a larger [[ApartmentComplex]] or a single [[Apartment]]. The visual/spatial"
     "aspects of a floor plan (i.e. room layout, [see wikipedia](https://en.wikipedia.org/wiki/Floor_plan))"
     "can be indicated using [[image]].

    See: https://schema.org/FloorPlan
    Model depth: 3
    """

    type_: str = Field(default="FloorPlan", alias="@type", const=True)
    layoutImage: None | (
        list[AnyUrl | URL | ImageObject | str] | AnyUrl | URL | ImageObject | str
    ) = Field(
        default=None,
        description="A schematic image showing the floorplan layout.",
    )
    floorSize: None | (list[QuantitativeValue | str] | QuantitativeValue | str) = Field(
        default=None,
        description="The size of the accommodation, e.g. in square meter or squarefoot. Typical unit code(s):"
        "MTK for square meter, FTK for square foot, or YDK for square yard.",
    )
    numberOfAvailableAccommodationUnits: None | (
        list[QuantitativeValue | str] | QuantitativeValue | str
    ) = Field(
        default=None,
        description="Indicates the number of available accommodation units in an [[ApartmentComplex]],"
        "or the number of accommodation units for a specific [[FloorPlan]] (within its specific"
        "[[ApartmentComplex]]). See also [[numberOfAccommodationUnits]].",
    )
    isPlanForApartment: None | (
        list[Accommodation | str] | Accommodation | str
    ) = Field(
        default=None,
        description="Indicates some accommodation that this floor plan describes.",
    )
    numberOfBathroomsTotal: None | (
        list[int | Integer | str] | int | Integer | str
    ) = Field(
        default=None,
        description="The total integer number of bathrooms in some [[Accommodation]], following real estate"
        "conventions as [documented in RESO](https://ddwiki.reso.org/display/DDW17/BathroomsTotalInteger+Field):"
        '"The simple sum of the number of bathrooms. For example for a property with two Full Bathrooms'
        'and one Half Bathroom, the Bathrooms Total Integer will be 3.". See also [[numberOfRooms]].',
    )
    petsAllowed: None | (
        list[str | Text | StrictBool | Boolean] | str | Text | StrictBool | Boolean
    ) = Field(
        default=None,
        description="Indicates whether pets are allowed to enter the accommodation or lodging business."
        "More detailed information can be put in a text value.",
    )
    amenityFeature: None | (
        list[LocationFeatureSpecification | str] | LocationFeatureSpecification | str
    ) = Field(
        default=None,
        description="An amenity feature (e.g. a characteristic or service) of the Accommodation. This generic"
        "property does not make a statement about whether the feature is included in an offer for"
        "the main accommodation or available at extra costs.",
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
    numberOfPartialBathrooms: None | (
        list[StrictInt | StrictFloat | Number | str]
        | StrictInt
        | StrictFloat
        | Number
        | str
    ) = Field(
        default=None,
        description="Number of partial bathrooms - The total number of half and ¼ bathrooms in an [[Accommodation]]."
        "This corresponds to the [BathroomsPartial field in RESO](https://ddwiki.reso.org/display/DDW17/BathroomsPartial+Field).",
    )
    numberOfFullBathrooms: None | (
        list[StrictInt | StrictFloat | Number | str]
        | StrictInt
        | StrictFloat
        | Number
        | str
    ) = Field(
        default=None,
        description="Number of full bathrooms - The total number of full and ¾ bathrooms in an [[Accommodation]]."
        "This corresponds to the [BathroomsFull field in RESO](https://ddwiki.reso.org/display/DDW17/BathroomsFull+Field).",
    )
    numberOfAccommodationUnits: None | (
        list[QuantitativeValue | str] | QuantitativeValue | str
    ) = Field(
        default=None,
        description="Indicates the total (available plus unavailable) number of accommodation units in"
        "an [[ApartmentComplex]], or the number of accommodation units for a specific [[FloorPlan]]"
        "(within its specific [[ApartmentComplex]]). See also [[numberOfAvailableAccommodationUnits]].",
    )
    numberOfRooms: None | (
        list[StrictInt | StrictFloat | Number | QuantitativeValue | str]
        | StrictInt
        | StrictFloat
        | Number
        | QuantitativeValue
        | str
    ) = Field(
        default=None,
        description="The number of rooms (excluding bathrooms and closets) of the accommodation or lodging"
        "business. Typical unit code(s): ROM for room or C62 for no unit. The type of room can be"
        "put in the unitText property of the QuantitativeValue.",
    )


if TYPE_CHECKING:
    from pydantic2_schemaorg.URL import URL
    from pydantic2_schemaorg.ImageObject import ImageObject
    from pydantic2_schemaorg.QuantitativeValue import QuantitativeValue
    from pydantic2_schemaorg.Accommodation import Accommodation
    from pydantic2_schemaorg.Integer import Integer
    from pydantic2_schemaorg.Text import Text
    from pydantic2_schemaorg.Boolean import Boolean
    from pydantic2_schemaorg.LocationFeatureSpecification import (
        LocationFeatureSpecification,
    )
    from pydantic2_schemaorg.Number import Number
