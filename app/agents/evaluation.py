import json
import logging

from langchain_core.messages import HumanMessage

from app.llm import llm
from app.models.shopping import (
    AgentDecision,
    AgentProduct,
)


logger = logging.getLogger(__name__)


async def evaluate_products(
    user_request: str,
    products: list[AgentProduct],
) -> AgentDecision:

    logger.info(
        "PRODUCT_EVALUATION_STARTED product_count=%d",
        len(products),
    )

    if not products:
        raise ValueError("No products available for evaluation")

    products_json = json.dumps(
        [
            product.model_dump(mode="json")
            for product in products
        ],
        indent=2,
    )

    prompt = f"""
You are a product evaluation agent.

The user asked:

{user_request}

You have received the following products:

{products_json}

Evaluate the products and select the best option.

Consider:

1. Total cost = product price + shipping cost
2. Delivery time
3. Rating
4. Stock availability
5. Match with the user's request
6. Brand preference if explicitly requested

Important rules:

- Do not invent product information.
- Do not change prices.
- Do not change delivery times.
- Do not recommend products that are out of stock.
- Do not perform any purchase.
- Do not make any payment.
- Do not approve any purchase.

Return ONLY valid JSON with exactly this structure:

{{
  "selected_product_id": "product_id",
  "alternative_product_ids": ["product_id"],
  "reasoning": "short explanation"
}}
"""
    # asking LLM to return selected_product_id as we dont want LLM to reproduce anything extra about the product
    # agent should just make a decision based on the product information provided and 
    # return the product_id of the selected product and alternative products

    response = await llm.ainvoke([
        HumanMessage(content=prompt)
    ])

    content = response.content.strip()

    if content.startswith("```"):
        content = (
            content
            .replace("```json", "")
            .replace("```", "")
            .strip()
        )

    decision_data = json.loads(content)

    selected_id = decision_data["selected_product_id"]

    selected_product = next(
        (
            product
            for product in products
            if product.product_id == selected_id
        ),
        None,
    )

    if selected_product is None:
        raise ValueError(
            f"LLM selected unknown product: {selected_id}"
        )

    alternative_ids = set(
        decision_data.get(
            "alternative_product_ids",
            []
        )
    )

    alternatives = [
        product
        for product in products
        if product.product_id in alternative_ids
        and product.product_id != selected_id
    ]

    decision = AgentDecision(
        selected_product=selected_product,
        alternatives=alternatives,
        reasoning=decision_data["reasoning"],
    )

    logger.info(
        "PRODUCT_EVALUATION_COMPLETED selected=%s alternatives=%d",
        decision.selected_product.product_id,
        len(decision.alternatives),
    )

    return decision