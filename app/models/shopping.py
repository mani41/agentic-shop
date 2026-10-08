from decimal import Decimal
from pydantic import BaseModel, Field


class ShoppingRequest(BaseModel):
    session_id: str
    request: str


class ShoppingIntent(BaseModel):

    category: str

    keyword: str

    preferred_brands: list[str] = Field(
        default_factory=list
    )

    max_price: Decimal | None = None

    max_delivery_days: int | None = None

    quantity: int = 1


class AgentProduct(BaseModel):

    product_id: str

    merchant_id: str

    merchant_name: str

    name: str

    brand: str | None = None

    category: str | None = None

    price: Decimal

    shipping_cost: Decimal

    delivery_days: int | None = None

    rating: Decimal | None = None

    stock_available: bool

    product_url: str | None = None


class AgentDecision(BaseModel):
    # AgentDecision represents the agent's research conclusion, not an approved purchase.

    selected_product: AgentProduct
    alternatives: list[AgentProduct] = Field(
        default_factory=list
    )
    reasoning: str | None = None