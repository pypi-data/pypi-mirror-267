from __future__ import annotations

from typing import TYPE_CHECKING

from pydantic.v1 import Field

from pydantic2_schemaorg.CommunicateAction import CommunicateAction


class AskAction(CommunicateAction):
    """The act of posing a question / favor to someone. Related actions: * [[ReplyAction]]:"
     "Appears generally as a response to AskAction.

    See: https://schema.org/AskAction
    Model depth: 5
    """

    type_: str = Field(default="AskAction", alias="@type", const=True)
    question: list[Question | str] | Question | str | None = Field(
        default=None,
        description="A sub property of object. A question.",
    )


if TYPE_CHECKING:
    from pydantic2_schemaorg.Question import Question
