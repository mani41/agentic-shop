from app.agents.evaluation import evaluate_products
from app.agents.intent import understand_intent
import logging
import json
from app.clients.shopping_backend import (
    ShoppingBackendClient,
)
from app.graph.state import ShoppingState
from app.models.shopping import AgentProduct


backend_client = ShoppingBackendClient()
logger = logging.getLogger(__name__)


async def understand_intent_node(
        state: ShoppingState
) -> ShoppingState:

    intent = await understand_intent(
        state["user_request"]
    )

    return {
        "intent": intent
    }


async def search_products_node(
        state: ShoppingState
) -> ShoppingState:

    # get intent from state
    intent = state.get("intent")
    if not intent:
        return {
            "error": "No intent found in state."
        }

    # intent based search products using the backend client
    products = await backend_client.search_products(
        intent
    )

    # return products in the state
    return {
        "products": products
    }



async def evaluation_node(
    state: ShoppingState
) -> ShoppingState:

    trace_id = state["session_id"]

    logger.info(
        "EVALUATION_NODE_STARTED trace=%s",
        trace_id,
    )

    messages = state.get("messages", [])

    if not messages:
        raise ValueError("No messages available")

    tool_message = None

    for message in reversed(messages):

        if message.type == "tool":
            tool_message = message
            break

    if tool_message is None:
        raise ValueError(
            "No product search result found"
        )

    logger.info(
        "TOOL_MESSAGE_RESPONSE raw=%r",
        tool_message.content
    )

    products_data = json.loads(
        tool_message.content
    )

    products = [
        AgentProduct.model_validate(product)
        for product in products_data
    ]

    decision = await evaluate_products(
        state["user_request"],
        products,
    )

    logger.info(
        "EVALUATION_NODE_COMPLETED "
        "trace=%s selected=%s",
        trace_id,
        decision.selected_product.product_id,
    )

    return {
        "decision": decision
    }