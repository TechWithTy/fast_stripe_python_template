from pydantic import BaseModel, Field


class StripeCustomer(BaseModel):
    """Link between Django user and Stripe customer"""

    user_id: str
    customer_id: str
    created_at: str
    updated_at: str
    livemode: bool = False

    def get_dashboard_url(self) -> str:
        """Get URL to view this customer in Stripe dashboard"""
        if self.livemode:
            return f"https://dashboard.stripe.com/customers/{self.customer_id}"
        return f"https://dashboard.stripe.com/test/customers/{self.customer_id}"


class StripePlan(BaseModel):
    """Store plan information from Stripe"""

    plan_id: str
    name: str
    amount: int  # in cents
    currency: str = "usd"
    interval: str  # month, year, etc.
    initial_credits: int = 0  # Credits given upon subscription
    monthly_credits: int = 0  # Credits given monthly
    features: dict = {}  # Store plan features as JSON
    active: bool = True
    livemode: bool = False
    created_at: str
    updated_at: str


class StripeSubscription(BaseModel):
    """Store subscription information"""

    class StatusEnum(str):
        ACTIVE = "active"
        PAST_DUE = "past_due"
        UNPAID = "unpaid"
        CANCELED = "canceled"
        INCOMPLETE = "incomplete"
        INCOMPLETE_EXPIRED = "incomplete_expired"
        TRIALING = "trialing"

    user_id: str
    subscription_id: str
    status: StatusEnum
    plan_id: str
    current_period_start: str
    current_period_end: str
    cancel_at_period_end: bool = False
    livemode: bool = False
    created_at: str
    updated_at: str

    def get_dashboard_url(self) -> str:
        """Get URL to view this subscription in Stripe dashboard"""
        if self.livemode:
            return f"https://dashboard.stripe.com/subscriptions/{self.subscription_id}"
        return f"https://dashboard.stripe.com/test/subscriptions/{self.subscription_id}"


class ProgrammableCheckoutPayload(BaseModel):
    mode: str = Field(..., description="Checkout mode: subscription, payment, or setup")
    line_items: list[dict] = Field(
        ..., description="List of line items for the checkout session"
    )
    success_url: str = Field(..., description="URL to redirect after success")
    cancel_url: str = Field(..., description="URL to redirect after cancellation")
    customer: str | None = Field(
        default=None, description="Stripe customer ID (optional)"
    )
    payment_intent_data: dict | None = Field(
        default=None, description="Additional payment intent data (optional)"
    )
    subscription_data: dict | None = Field(
        default=None, description="Additional subscription data (optional)"
    )
    client_reference_id: str | None = Field(
        default=None, description="Reference for client (optional)"
    )
    metadata: dict | None = Field(
        default=None, description="Additional metadata (optional)"
    )
    allow_promotion_codes: bool | None = Field(default=None)
    billing_address_collection: str | None = Field(default=None)
    customer_email: str | None = Field(default=None)
