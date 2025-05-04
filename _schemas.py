from datetime import datetime
from typing import Any

from pydantic import BaseModel


class Credit:
    class CreditAllocationRequest(BaseModel):
        user_id: str
        amount: int
        description: str
        subscription_id: str

    class CreditAllocationResult(BaseModel):
        user_id: str
        amount: int
        description: str
        subscription_id: str
        allocated_at: datetime
        status: str
        details: dict[str, Any] = {}


class Subscription:
    class SubscriptionChangeRequest(BaseModel):
        user_id: str
        old_plan_name: str
        new_plan_name: str
        subscription_id: str

    class SubscriptionChangeResult(BaseModel):
        user_id: str
        old_plan_name: str
        new_plan_name: str
        subscription_id: str
        status: str
        details: dict[str, Any] = {}


# --- Pydantic Models ---
class CheckoutSessionRequest(BaseModel):
    success_url: str | None = None
    cancel_url: str | None = None
    customer_id: str | None = None


class CheckoutSessionResponse(BaseModel):
    checkout_url: str


class ProductPricePlan(BaseModel):
    unit_amount: float
    currency: str
    recurring: dict | None = None
    interval: str | None = None
    interval_count: int | None = None
    usage_type: str | None = None
    active: bool | None = True
    nickname: str | None = None
    metadata: dict | None = None


class ProductCreateRequest(BaseModel):
    name: str
    active: bool = True
    description: str | None = None
    id: str | None = None
    statement_descriptor: str | None = None
    unit_label: str | None = None
    url: str | None = None
    metadata: dict | None = None
    initial_credits: int | None = None
    monthly_credits: int | None = None
    subscription_tier: str | None = None
    images: list[str] | None = None
    tax_code: str | None = None
    pricing_plans: list[ProductPricePlan] | None = None


class ProductCreateResponse(BaseModel):
    product: dict
    prices: list[dict]
