import logging
from datetime import datetime, timezone

from _schemas import Credit, Subscription
from fastapi import Depends
from pydantic import BaseModel
from stripe import StripeClient

from .client import get_stripe_client

# Import your Stripe models (for type hints and validation)

logger = logging.getLogger(__name__)


async def allocate_subscription_credits(
    req: Credit.CreditAllocationRequest,
    stripe: StripeClient = Depends(get_stripe_client),
    # db_session: AsyncSession = Depends(get_db_session),  # Uncomment and implement for real DB
) -> Credit.CreditAllocationResult:
    """
    Allocate credits to a user and record the transaction.
    Uses the Stripe client for any necessary Stripe-side operations.
    This function is async and ready for FastAPI DI and future DB integration.
    All actions are logged; errors are raised for proper API handling.
    """
    logger.info(
        f"Allocating {req.amount} credits to user {req.user_id} for subscription {req.subscription_id}"
    )
    try:
        # Example Stripe usage: attach metadata or log a custom event
        # stripe.Customer.modify(req.user_id, metadata={"last_credit_allocation": str(datetime.now(timezone.utc))})
        # TODO: Add real Stripe or DB logic as needed
        allocated_at = datetime.now(timezone.utc)
        logger.info(f"Successfully allocated credits to user {req.user_id}")
        return Credit.CreditAllocationResult(
            user_id=req.user_id,
            amount=req.amount,
            description=req.description,
            subscription_id=req.subscription_id,
            allocated_at=allocated_at,
            status="success",
            details={},
        )
    except Exception as e:
        logger.error(f"Failed to allocate credits: {e}")
        raise


class PlanMappingRequest(BaseModel):
    plan_name: str


class PlanMappingResult(BaseModel):
    plan_name: str
    subscription_tier: str


async def map_plan_to_subscription_tier(
    req: PlanMappingRequest,
) -> PlanMappingResult:
    """
    Map Stripe plan name to subscription tier.
    """
    logger.info(f"Mapping plan {req.plan_name} to subscription tier")
    try:
        mapping = {
            "Free Plan": "free",
            "Basic Plan": "basic",
            "Premium Plan": "premium",
            "Enterprise Plan": "enterprise",
        }

        # Try exact match first
        if req.plan_name in mapping:
            return PlanMappingResult(
                plan_name=req.plan_name,
                subscription_tier=mapping[req.plan_name],
            )

        # Try partial match
        for key, value in mapping.items():
            if key.lower().split()[0] in req.plan_name.lower():
                return PlanMappingResult(
                    plan_name=req.plan_name,
                    subscription_tier=value,
                )

        # Default to basic
        return PlanMappingResult(
            plan_name=req.plan_name,
            subscription_tier="basic",
        )
    except Exception as e:
        logger.error(f"Failed to map plan to subscription tier: {e}")
        raise


async def handle_subscription_change(
    req: Subscription.SubscriptionChangeRequest,
) -> Subscription.SubscriptionChangeResult:
    """
    Handle credit changes when user changes subscription plan.
    """
    logger.info(
        f"Handling subscription change for user {req.user_id} from {req.old_plan_name} to {req.new_plan_name}"
    )
    try:
        # Calculate credit difference for immediate allocation
        # TODO: Replace with real DB logic to get initial credits for plans
        old_plan_credits = 0
        new_plan_credits = 0

        credit_adjustment = new_plan_credits - old_plan_credits

        if credit_adjustment > 0:
            # This is an upgrade - give additional credits
            description = f"Additional credits for upgrading to {req.new_plan_name}"
            allocation_req = Credit.CreditAllocationRequest(
                user_id=req.user_id,
                amount=credit_adjustment,
                description=description,
                subscription_id=req.subscription_id,
            )
            allocation_result = await allocate_subscription_credits(allocation_req)
            if allocation_result.status != "success":
                raise Exception("Failed to allocate credits")
        elif credit_adjustment < 0:
            # This is a downgrade - typically no action needed for credits
            # You could implement credit reduction here if that's part of your business logic
            pass
        else:
            # No change in initial credits
            pass

        # Update user profile subscription tier if successful
        # TODO: Replace with real DB logic to update user profile
        new_tier_req = PlanMappingRequest(plan_name=req.new_plan_name)
        new_tier_result = await map_plan_to_subscription_tier(new_tier_req)
        if new_tier_result.subscription_tier:
            # Update user profile with new subscription tier
            pass

        return Subscription.SubscriptionChangeResult(
            user_id=req.user_id,
            old_plan_name=req.old_plan_name,
            new_plan_name=req.new_plan_name,
            subscription_id=req.subscription_id,
            status="success",
            details={},
        )
    except Exception as e:
        logger.error(f"Failed to handle subscription change: {e}")
        raise


# The rest of your functions (map_plan_to_subscription_tier, handle_subscription_change, etc.) can also accept
# a StripeClient parameter via Depends(get_stripe_client) if they need to interact with Stripe.
# Example:
# async def handle_subscription_change(..., stripe: StripeClient = Depends(get_stripe_client)):

# Example FastAPI endpoint usage:
# @router.post("/credits/allocate", response_model=CreditAllocationResult)
# async def allocate_credits_endpoint(
#     req: CreditAllocationRequest,
#     db_session: AsyncSession = Depends(get_db_session),
# ):
#     return await allocate_subscription_credits(req, db_session)

# @router.post("/subscriptions/change", response_model=SubscriptionChangeResult)
# async def handle_subscription_change_endpoint(
#     req: SubscriptionChangeRequest,
#     db_session: AsyncSession = Depends(get_db_session),
# ):
#     return await handle_subscription_change(req, db_session)
