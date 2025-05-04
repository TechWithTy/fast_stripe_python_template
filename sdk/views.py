# --- FastAPI Imports and Setup ---
import logging
from types import SimpleNamespace
from typing import Any

import stripe
from fastapi import APIRouter, Depends, HTTPException

from app.core.config import StripeSettings
from app.api.deps import get_current_user, get_db

# Import Pydantic schemas
from app.core.third_party_integrations.stripe_home._schemas import (
    CheckoutSessionRequest,
    CheckoutSessionResponse,
    ProductCreateRequest,
    ProductCreateResponse,
)

# Import Stripe client config
from .client import get_stripe_client

# Import Django ORM models
from .models import StripeCustomer, StripePlan

# Logger setup
logger = logging.getLogger(__name__)

router = APIRouter()


# --- FastAPI Endpoints ---


@router.post(
    "/checkout/{plan_id}", response_model=CheckoutSessionResponse, status_code=200
)
async def create_checkout_session(
    plan_id: int,
    payload: CheckoutSessionRequest,
    user: Any = Depends(get_current_user),
):
    """
    ```
    Create a Stripe Checkout Session for a specific plan.
    - Validates plan_id
    - Uses Pydantic for request/response
    - Handles Stripe and general errors
    ```
    """
    try:
        plan = StripePlan.objects.get(id=plan_id, active=True)
        # Extract URLs and customer_id
        success_url = payload.success_url
        cancel_url = payload.cancel_url
        customer_id = payload.customer_id
        # Create the checkout session
        checkout_url = await _create_checkout_session(
            plan, user, success_url, cancel_url, customer_id
        )
        return CheckoutSessionResponse(checkout_url=checkout_url)
    except StripePlan.DoesNotExist:
        raise HTTPException(status_code=404, detail="Plan not found")
    except stripe.error.StripeError as e:
        logger.error(f"Stripe error: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Error creating checkout session: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


async def _create_checkout_session(
    plan, user, success_url=None, cancel_url=None, customer_id=None
):
    # Use provided customer_id or get/create one
    if customer_id:
        customer_obj = StripeCustomer.objects.get(customer_id=customer_id)
        customer = SimpleNamespace(customer_id=customer_id)
    else:
        customer_obj, created = StripeCustomer.objects.get_or_create(
            user=user,
            defaults={
                "customer_id": _create_stripe_customer(user),
                "livemode": not StripeSettings.STRIPE_SECRET_KEY.startswith("sk_test_"),
            },
        )
        customer = SimpleNamespace(customer_id=customer_obj.customer_id)
    default_success_url = (
        f"{StripeSettings.BASE_URL}/subscription/success?session_id={{CHECKOUT_SESSION_ID}}"
    )
    default_cancel_url = f"{StripeSettings.BASE_URL}/subscription/cancel"
    stripe.api_key = (
        StripeSettings.STRIPE_SECRET_KEY_TEST
        if StripeSettings.TESTING
        else StripeSettings.STRIPE_SECRET_KEY
    )
    checkout_session = stripe.checkout.Session.create(
        customer=customer.customer_id,
        line_items=[{"price": plan.plan_id, "quantity": 1}],
        mode="subscription",
        success_url=success_url or default_success_url,
        cancel_url=cancel_url or default_cancel_url,
        allow_promotion_codes=True,
        billing_address_collection="required",
        customer_email=user.email if not customer.customer_id else None,
        client_reference_id=str(user.id),
        metadata={
            "plan_id": str(plan.id),
            "plan_name": plan.name,
            "user_id": str(user.id),
        },
    )
    return checkout_session.url


def _create_stripe_customer(user):
    try:
        stripe.api_key = (
            StripeSettings.STRIPE_SECRET_KEY_TEST
            if StripeSettings.TESTING
            else StripeSettings.STRIPE_SECRET_KEY
        )
        customer = stripe.Customer.create(
            email=user.email,
            name=getattr(user, "get_full_name", lambda: user.username)(),
            metadata={"user_id": str(user.id)},
        )
        return customer.id
    except Exception as e:
        logger.error(f"Error creating Stripe customer: {e}")
        raise


@router.post("/products", response_model=ProductCreateResponse, status_code=201)
async def create_product(
    payload: ProductCreateRequest,
    user: Any = Depends(get_current_user),
):
    """
    ```
    Create a new Stripe product with optional pricing plans.
    Handles metadata, images, tax codes, and creates local plan records.
    ```
    """
    try:
        stripe_client = get_stripe_client()
        product_data = payload.dict(exclude_unset=True)
        # Metadata handling
        if payload.metadata is not None:
            metadata = payload.metadata.copy()
            if payload.initial_credits is not None:
                metadata["initial_credits"] = payload.initial_credits
            if payload.monthly_credits is not None:
                metadata["monthly_credits"] = payload.monthly_credits
            if payload.subscription_tier is not None:
                metadata["subscription_tier"] = payload.subscription_tier
            product_data["metadata"] = metadata
        # Create the product
        stripe.api_key = (
            StripeSettings.STRIPE_SECRET_KEY_TEST
            if StripeSettings.TESTING
            else StripeSettings.STRIPE_SECRET_KEY
        )
        product = stripe_client.products.create(**product_data)
        created_prices = []
        if payload.pricing_plans:
            for plan_data in payload.pricing_plans:
                price_data = {
                    "product": product.id,
                    "unit_amount": int(plan_data.unit_amount * 100),
                    "currency": plan_data.currency.lower(),
                }
                if plan_data.recurring:
                    price_data["recurring"] = plan_data.recurring
                elif plan_data.interval:
                    price_data["recurring"] = {"interval": plan_data.interval}
                    if plan_data.interval_count:
                        price_data["recurring"]["interval_count"] = (
                            plan_data.interval_count
                        )
                    if plan_data.usage_type:
                        price_data["recurring"]["usage_type"] = plan_data.usage_type
                if plan_data.active is not None:
                    price_data["active"] = plan_data.active
                if plan_data.nickname:
                    price_data["nickname"] = plan_data.nickname
                if plan_data.metadata:
                    price_data["metadata"] = plan_data.metadata
                price = stripe_client.prices.create(**price_data)
                created_prices.append(price)
                if len(created_prices) == 1:
                    stripe_client.products.modify(product.id, default_price=price.id)
                if "recurring" in price_data:
                    StripePlan.objects.create(
                        plan_id=price.id,
                        name=f"{product.name} - {price_data.get('nickname', price.id)}",
                        amount=price_data["unit_amount"],
                        currency=price_data["currency"],
                        interval=price_data["recurring"]["interval"],
                        initial_credits=int(
                            product_data.get("metadata", {}).get("initial_credits", 0)
                        ),
                        monthly_credits=int(
                            product_data.get("metadata", {}).get("monthly_credits", 0)
                        ),
                        livemode=not StripeSettings.STRIPE_SECRET_KEY.startswith(
                            "sk_test_"
                        ),
                        active=price_data.get("active", True),
                    )
        return ProductCreateResponse(product=product, prices=created_prices)
    except stripe.error.StripeError as e:
        logger.error(f"Stripe error creating product: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Error creating product: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


# Add router to FastAPI app in your main.py or app entrypoint
# from .views import router as stripe_router
# app.include_router(stripe_router, prefix="/stripe", tags=["stripe"])
