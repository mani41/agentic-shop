import json

from langchain_core.messages import HumanMessage

from app.llm import llm
from app.models.shopping import ShoppingRequest, ShoppingIntent

async def understand_intent(
        user_request: str
) -> ShoppingIntent:

    prompt = f"""
You are a shopping requirements extraction agent.

Extract the user's shopping requirements.

Return ONLY valid JSON.

The JSON must have exactly these fields:

{{
  "category": "string",
  "keyword": "string",
  "preferred_brands": ["string"],
  "max_price": number or null,
  "max_delivery_days": number or null,
  "quantity": number
}}

Rules:

1. Do not invent requirements.
2. If the user does not specify a maximum price,
   use null.
3. If the user does not specify preferred brands,
   return an empty array.
4. If quantity is not specified, use 1.
5. max_price must be the maximum total product price
   the user requested.
6. Return JSON only.

User request:

{user_request}
"""

    response = await llm.ainvoke(
        [
            HumanMessage(content=prompt)
        ]
    )

    content = response.content

    # Remove markdown fences if the model adds them.
    content = content.strip()

    if content.startswith("```"):
        content = content.replace(
            "```json",
            ""
        ).replace(
            "```",
            ""
        ).strip()

    data = json.loads(content)

    return ShoppingIntent.model_validate(data)