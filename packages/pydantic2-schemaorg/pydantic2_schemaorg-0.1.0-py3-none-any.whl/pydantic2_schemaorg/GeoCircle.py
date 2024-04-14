from __future__ import annotations

from typing import TYPE_CHECKING

from pydantic.v1 import Field
from pydantic.v1 import StrictFloat
from pydantic.v1 import StrictInt

from pydantic2_schemaorg.GeoShape import GeoShape


class GeoCircle(GeoShape):
    """A GeoCircle is a GeoShape representing a circular geographic area. As it is a GeoShape"
     "it provides the simple textual property 'circle', but also allows the combination of"
     "postalCode alongside geoRadius. The center of the circle can be indicated via the 'geoMidpoint'"
     "property, or more approximately using 'address', 'postalCode'.

    See: https://schema.org/GeoCircle
    Model depth: 5
    """

    type_: str = Field(default="GeoCircle", alias="@type", const=True)
    geoRadius: None | (
        list[StrictInt | StrictFloat | Number | str | Text | Distance]
        | StrictInt
        | StrictFloat
        | Number
        | str
        | Text
        | Distance
    ) = Field(
        default=None,
        description="Indicates the approximate radius of a GeoCircle (metres unless indicated otherwise"
        "via Distance notation).",
    )
    geoMidpoint: None | (list[GeoCoordinates | str] | GeoCoordinates | str) = Field(
        default=None,
        description="Indicates the GeoCoordinates at the centre of a GeoShape, e.g. GeoCircle.",
    )


if TYPE_CHECKING:
    from pydantic2_schemaorg.Number import Number
    from pydantic2_schemaorg.Text import Text
    from pydantic2_schemaorg.Distance import Distance
    from pydantic2_schemaorg.GeoCoordinates import GeoCoordinates
