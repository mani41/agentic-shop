import json

from langchain_core.tools import tool
import logging

from app.clients.shopping_backend import ShoppingBackendClient
from app.models.shopping import ShoppingIntent


backend_client = ShoppingBackendClient()
logger = logging.getLogger(__name__)

@tool
async def search_products_tool(
    keyword: str,
    category: str,
    max_price: float | None = None,
    max_delivery_days: int | None = None,
) -> list[dict]:
    """
    Search available products across supported merchants.

    Use this tool when the user wants to find products.
    The tool searches merchants through the Spring Boot shopping backend.
    """

    logger.info(
        "TOOL_SEARCH_PRODUCTS_STARTED trace=search_products_tool keyword=%s category=%s max_price=%s max_delivery_days=%s",
        keyword,
        category,
        max_price,
        max_delivery_days
    )

    intent = ShoppingIntent(
        category=category,
        keyword=keyword,
        max_price=max_price,
        max_delivery_days=max_delivery_days,
        preferred_brands=[],
        quantity=1
    )

    products = await backend_client.search_products(intent)

    logger.info(
        "TOOL_SEARCH_PRODUCTS_COMPLETED trace=search_products_tool keyword=%s category=%s max_price=%s max_delivery_days=%s products_found=%d",
        keyword,
        category,
        max_price,
        max_delivery_days,
        len(products)
    )

    return json.dumps([
        product.model_dump(mode="json") 
        for product in products
    ])