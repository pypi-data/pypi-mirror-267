from __future__ import annotations

from typing import TYPE_CHECKING

from pydantic.v1 import Field

from pydantic2_schemaorg.Dataset import Dataset


class DataFeed(Dataset):
    """A single feed providing structured information about one or more entities or topics.

    See: https://schema.org/DataFeed
    Model depth: 4
    """

    type_: str = Field(default="DataFeed", alias="@type", const=True)
    dataFeedElement: None | (
        list[str | Text | DataFeedItem | Thing] | str | Text | DataFeedItem | Thing
    ) = Field(
        default=None,
        description="An item within a data feed. Data feeds may have many elements.",
    )


if TYPE_CHECKING:
    from pydantic2_schemaorg.Text import Text
    from pydantic2_schemaorg.DataFeedItem import DataFeedItem
    from pydantic2_schemaorg.Thing import Thing
