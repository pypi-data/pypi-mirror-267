from __future__ import annotations
from typing import TYPE_CHECKING

from pydantic.v1 import AnyUrl
from typing import List, Optional, Union


from pydantic.v1 import Field
from pydantic2_schemaorg.CreativeWorkSeries import CreativeWorkSeries


class PodcastSeries(CreativeWorkSeries):
    """A podcast is an episodic series of digital audio or video files which a user can download"
     "and listen to.

    See: https://schema.org/PodcastSeries
    Model depth: 4
    """

    type_: str = Field(default="PodcastSeries", alias="@type", const=True)
    webFeed: Optional[
        Union[
            List[Union[AnyUrl, "URL", "DataFeed", str]], AnyUrl, "URL", "DataFeed", str
        ]
    ] = Field(
        default=None,
        description="The URL for a feed, e.g. associated with a podcast series, blog, or series of date-stamped"
        "updates. This is usually RSS or Atom.",
    )
    actor: Optional[Union[List[Union["Person", str]], "Person", str]] = Field(
        default=None,
        description="An actor, e.g. in TV, radio, movie, video games etc., or in an event. Actors can be associated"
        "with individual items or with a series, episode, clip.",
    )


if TYPE_CHECKING:
    from pydantic2_schemaorg.URL import URL
    from pydantic2_schemaorg.DataFeed import DataFeed
    from pydantic2_schemaorg.Person import Person
