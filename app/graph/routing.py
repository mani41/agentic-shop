from langchain_core.messages import AIMessage
import logging

logger = logging.getLogger(__name__)


def should_continue(state):

    messages = state.get("messages", [])
    trace_id = state["session_id"]

    if not messages:
        logger.info(
            "GRAPH_ROUTE trace=%s route=end  reason=no_messages",
            trace_id
        )
        return "evaluate"

    last_message = messages[-1]

    if isinstance(last_message, AIMessage):
        if last_message.tool_calls:
            logger.info(
                "GRAPH_ROUTE trace=%s route=tools",
                trace_id
            )
            return "tools"

    return "evaluate"