from typing import Annotated, TypedDict

from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages

from app.models.shopping import AgentDecision


class ShoppingState(TypedDict, total=False):

    session_id: str

    user_request: str

    messages: Annotated[
        list[BaseMessage],
        add_messages
    ]

    decision: AgentDecision