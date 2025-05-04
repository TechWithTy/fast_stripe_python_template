import logging
from typing import Any

from _schemas import Credit
from stripe import StripeClient

from .credit import allocate_subscription_credits
from .models import StripeSubscription

# Utility function to handle subscription updates and credit allocations

def handle_subscription_update(
    instance: StripeSubscription,
    created: bool,
    stripe: StripeClient,
    **_kwargs: Any
) -> None:
    """
    Production-ready handler for subscription updates and credit allocations using the Stripe SDK.
    - Ensures idempotency and robust error handling.
    - Logs all actions for observability.
    - Allocates credits on creation and can be extended for plan changes.
    Args:
        instance (StripeSubscription): The subscription instance being created or updated.
        created (bool): True if the subscription was just created, False if updated.
        stripe (StripeClient): The Stripe SDK client instance.
        **kwargs: Additional keyword arguments.
    """
    logger = logging.getLogger(__name__)
    try:
        # Defensive: Ensure required fields are present
        if not instance.subscription_id or not instance.user_id:
            logger.error("Missing subscription_id or user_id in StripeSubscription instance.")
            raise ValueError("Missing required subscription fields.")
        # Idempotency: Optionally check if credits were already allocated (implement if needed)
        # Example: Use a Redis or DB check here for production
        if created:
            logger.info(f"[StripeWebhook] New subscription created: {instance.subscription_id} for user {instance.user_id}")
            # Add metadata to the Stripe subscription (for audit/tracking)
            stripe.subscriptions.modify(
                instance.subscription_id,
                metadata={"event": "created", "user_id": instance.user_id}
            )
            # Allocate initial credits for the new subscription
            initial_credits = getattr(instance, "initial_credits", 0)
            if initial_credits > 0:
                req = Credit.CreditAllocationRequest(
                    user_id=instance.user_id,
                    amount=initial_credits,
                    description="Initial credits for new subscription",
                    subscription_id=instance.subscription_id
                )
                import asyncio
                # In production, prefer a background task queue (e.g., Celery) for async ops
                asyncio.run(allocate_subscription_credits(req, stripe))
            else:
                logger.info(f"No initial credits to allocate for subscription {instance.subscription_id}")
        else:
            logger.info(f"[StripeWebhook] Subscription updated: {instance.subscription_id} for user {instance.user_id}")
            stripe.subscriptions.modify(
                instance.subscription_id,
                metadata={"event": "updated", "user_id": instance.user_id}
            )
            # Example: handle plan changes, monthly credits, or prorated adjustments
            # You should check for plan_id changes, and only allocate/deduct credits if needed
            # Example (pseudo):
            # if plan_changed:
            #     req = Credit.CreditAllocationRequest(...)
            #     asyncio.run(allocate_subscription_credits(req, stripe))
        logger.info(f"[StripeWebhook] Subscription processing completed for {instance.subscription_id}")
    except Exception as e:
        logger.error(f"[StripeWebhook] Error handling subscription update for {getattr(instance, 'subscription_id', 'unknown')}: {e}")
        # In production, consider alerting/metrics here
        raise RuntimeError(f"Stripe webhook handling failed: {e}") from e
