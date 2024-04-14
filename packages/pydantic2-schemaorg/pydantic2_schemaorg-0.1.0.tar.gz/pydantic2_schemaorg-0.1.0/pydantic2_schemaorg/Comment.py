from __future__ import annotations

from typing import TYPE_CHECKING

from pydantic.v1 import Field

from pydantic2_schemaorg.CreativeWork import CreativeWork


class Comment(CreativeWork):
    """A comment on an item - for example, a comment on a blog post. The comment's content is expressed"
     "via the [[text]] property, and its topic via [[about]], properties shared with all CreativeWorks.

    See: https://schema.org/Comment
    Model depth: 3
    """

    type_: str = Field(default="Comment", alias="@type", const=True)
    sharedContent: None | (list[CreativeWork | str] | CreativeWork | str) = Field(
        default=None,
        description="A CreativeWork such as an image, video, or audio clip shared as part of this posting.",
    )
    downvoteCount: None | (list[int | Integer | str] | int | Integer | str) = Field(
        default=None,
        description="The number of downvotes this question, answer or comment has received from the community.",
    )
    upvoteCount: None | (list[int | Integer | str] | int | Integer | str) = Field(
        default=None,
        description="The number of upvotes this question, answer or comment has received from the community.",
    )
    parentItem: None | (
        list[Comment | CreativeWork | str] | Comment | CreativeWork | str
    ) = Field(
        default=None,
        description="The parent of a question, answer or item in general. Typically used for Q/A discussion"
        "threads e.g. a chain of comments with the first comment being an [[Article]] or other"
        "[[CreativeWork]]. See also [[comment]] which points from something to a comment about"
        "it.",
    )


if TYPE_CHECKING:
    from pydantic2_schemaorg.CreativeWork import CreativeWork
    from pydantic2_schemaorg.Integer import Integer
