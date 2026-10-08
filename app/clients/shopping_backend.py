import os
import httpx
import logging

from app.models.shopping import AgentProduct, ShoppingIntent

SPRING_BOOT_URL = os.environ.get("SPRING_BOOT_URL", "http://localhost:8080")
logger = logging.getLogger(__name__)

class ShoppingBackendClient:
    """Minimal shopping backend client used by the local graph."""

    async def search_products(self, intent:ShoppingIntent) -> list[AgentProduct]:

        payload = {
            "category": intent.category,
            "keyword": intent.keyword,
            "brand": None,
            "maxPrice": (
                float(intent.max_price)
                if intent.max_price is not None
                else None
            ),
            "maxDeliveryDays": intent.max_delivery_days,
        }

        logger.info(
            "BACKEND_SEARCH_PRODUCTS_STARTED endpoint=/api/products/search keyword=%s max_price=%s",
            intent.keyword,
            intent.max_price
        )

        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{SPRING_BOOT_URL}/api/products/search",
                json=payload
            )

            response.raise_for_status()
            products_data = response.json()

            logger.info(
                "BACKEND_SEARCH_PRODUCTS_COMPLETED count=%d",
                len(products_data)
            )


            return [
                AgentProduct(
                    product_id=product["externalId"],
                    merchant_id=product["merchantCode"],
                    merchant_name=product["merchantName"],
                    name=product["name"],
                    brand=product.get("brand"),
                    category=product.get("category"),
                    price=product["price"],
                    shipping_cost=product["shippingCost"],
                    delivery_days=product.get("deliveryDays"),
                    rating=product.get("rating"),
                    stock_available=product["stockAvailable"],
                    product_url=product.get("productUrl"),
                )
                for product in products_data
            ]
