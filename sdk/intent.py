"""
Stripe PaymentIntent creation with asynchronous capture (automatic_async).
Implements production best practices: type safety, async, DRY, SOLID, and OpenAPI-ready models.
See _docs/best_practices/stripe_async_capture.md for rationale and webhook caveats.
"""

from typing import Literal

import stripe
from fastapi import HTTPException
from pydantic import BaseModel, ConfigDict, field_validator

from ..client import get_stripe_client


# --- Pydantic models ---
class PaymentIntentCreateRequest(BaseModel):
    amount: int  # Amount in the smallest currency unit (e.g., cents)
    currency: str
    payment_method: str
    payment_method_types: list[str] = ["card"]
    confirm: bool = True
    capture_method: Literal["automatic_async"] = "automatic_async"

    model_config = ConfigDict(extra="forbid")

    @field_validator("amount")
    @classmethod
    def amount_positive(cls, v):
        if v <= 0:
            raise ValueError("Amount must be positive")
        return v


class PaymentIntentCreateResponse(BaseModel):
    id: str
    status: str
    capture_method: Literal["automatic_async"]
    client_secret: str | None
    latest_charge: str | None

    model_config = ConfigDict(extra="ignore")


# --- Service function ---
async def create_payment_intent(
    payload: PaymentIntentCreateRequest,
    stripe_settings=None,  # Optionally inject settings for testing/multi-account
) -> PaymentIntentCreateResponse:
    """
    Create a Stripe PaymentIntent with asynchronous capture enabled.
    See Stripe docs for async capture webhook/response caveats:
    - balance_transaction, transfer, application_fee may be null initially
    - Downstream logic must handle delayed settlement
    """
    try:
        stripe_client = get_stripe_client(stripe_settings)
        pi = stripe_client.PaymentIntent.create(
            amount=payload.amount,
            currency=payload.currency,
            payment_method_types=payload.payment_method_types,
            payment_method=payload.payment_method,
            confirm=payload.confirm,
            capture_method=payload.capture_method,
        )
        return PaymentIntentCreateResponse(
            id=pi["id"],
            status=pi["status"],
            capture_method=pi["capture_method"],
            client_secret=pi.get("client_secret"),
            latest_charge=pi.get("latest_charge"),
        )
    except stripe.error.StripeError as e:
        # ! Secure logging only, do not expose internals
        raise HTTPException(status_code=400, detail=f"Stripe error: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")


# todo: Add FastAPI route and webhook handler for full async flow support.
# * See Stripe docs for required webhook event handling for async capture.
