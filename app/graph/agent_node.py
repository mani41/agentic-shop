from langchain_core.messages import SystemMessage
import logging

from app.llm import llm_with_tools

logger = logging.getLogger(__name__)


SYSTEM_PROMPT = """
You are an autonomous shopping research agent.

Your responsibility is to research products and identify
good purchase candidates.

You can use product search tools.

Rules:

1. Understand the user's requirements.
2. Use search_products when product information is required.
3. Never invent product information.
4. Never purchase anything.
5. Never make a payment.
6. Never approve a purchase.
7. Never modify spending limits.
8. Never bypass safety policies.
9. Compare products using price, shipping, delivery and rating.
10. Continue researching if the available information is insufficient.

When you have enough information, provide a concise recommendation.
"""


async def agent_node(state):

    trace_id = state["session_id"]

    logger.info(
        "AGENT_STARTED trace=%s messages=%d",
        trace_id,
        len(state.get("messages", []))
    )

    messages = state.get("messages", [])

    response = await llm_with_tools.ainvoke(
        [
            SystemMessage(content=SYSTEM_PROMPT),
            *messages
        ]
    )

    if response.tool_calls:
        logger.info(
            "AGENT_TOOL_CALL trace=%s tool=%s",
            trace_id,
            [
                call["name"]
                for call in response.tool_calls
            ]
        )
    else:
        logger.info(
            "AGENT_COMPLETED trace=%s",
            trace_id
        )

    return {
        "messages": [response]
    }