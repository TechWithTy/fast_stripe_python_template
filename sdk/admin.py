import logging
from typing import Any

from stripe import StripeClient

# Utility functions for Stripe admin operations using the Stripe SDK
# These are NOT FastAPI routes and do not depend on HTTP or FastAPI.
# All functions raise RuntimeError on failure and log errors.

def list_stripe_customers(stripe: StripeClient) -> list[dict[str, Any]]:
    """list Stripe customers using the Stripe SDK."""
    try:
        response = stripe.customers.list(limit=20)
        return list(response.auto_paging_iter())
    except Exception as e:
        logging.error(f"Error listing Stripe customers: {e}")
        raise RuntimeError("Stripe API error") from e


def list_stripe_subscriptions(stripe: StripeClient) -> list[dict[str, Any]]:
    """list Stripe subscriptions using the Stripe SDK."""
    try:
        response = stripe.subscriptions.list(limit=20)
        return list(response.auto_paging_iter())
    except Exception as e:
        logging.error(f"Error listing Stripe subscriptions: {e}")
        raise RuntimeError("Stripe API error") from e


def list_stripe_plans(stripe: StripeClient) -> list[dict[str, Any]]:
    """list Stripe plans using the Stripe SDK."""
    try:
        response = stripe.plans.list(limit=20)
        return list(response.auto_paging_iter())
    except Exception as e:
        logging.error(f"Error listing Stripe plans: {e}")
        raise RuntimeError("Stripe API error") from e


def list_stripe_invoices(stripe: StripeClient) -> list[dict[str, Any]]:
    """list Stripe invoices using the Stripe SDK."""
    try:
        response = stripe.invoices.list(limit=20)
        return list(response.auto_paging_iter())
    except Exception as e:
        logging.error(f"Error listing Stripe invoices: {e}")
        raise RuntimeError("Stripe API error") from e


def list_stripe_charges(stripe: StripeClient) -> list[dict[str, Any]]:
    """list Stripe charges using the Stripe SDK."""
    try:
        response = stripe.charges.list(limit=20)
        return list(response.auto_paging_iter())
    except Exception as e:
        logging.error(f"Error listing Stripe charges: {e}")
        raise RuntimeError("Stripe API error") from e


def list_stripe_products(stripe: StripeClient) -> list[dict[str, Any]]:
    """list Stripe products using the Stripe SDK."""
    try:
        response = stripe.products.list(limit=20)
        return list(response.auto_paging_iter())
    except Exception as e:
        logging.error(f"Error listing Stripe products: {e}")
        raise RuntimeError("Stripe API error") from e


def list_stripe_payment_intents(stripe: StripeClient) -> list[dict[str, Any]]:
    """list Stripe payment intents using the Stripe SDK."""
    try:
        response = stripe.payment_intents.list(limit=20)
        return list(response.auto_paging_iter())
    except Exception as e:
        logging.error(f"Error listing Stripe payment intents: {e}")
        raise RuntimeError("Stripe API error") from e


def list_stripe_refunds(stripe: StripeClient) -> list[dict[str, Any]]:
    """list Stripe refunds using the Stripe SDK."""
    try:
        response = stripe.refunds.list(limit=20)
        return list(response.auto_paging_iter())
    except Exception as e:
        logging.error(f"Error listing Stripe refunds: {e}")
        raise RuntimeError("Stripe API error") from e


def list_stripe_balance_transactions(stripe: StripeClient) -> list[dict[str, Any]]:
    """list Stripe balance transactions using the Stripe SDK."""
    try:
        response = stripe.balance_transactions.list(limit=20)
        return list(response.auto_paging_iter())
    except Exception as e:
        logging.error(f"Error listing Stripe balance transactions: {e}")
        raise RuntimeError("Stripe API error") from e


def list_stripe_payouts(stripe: StripeClient) -> list[dict[str, Any]]:
    """list Stripe payouts using the Stripe SDK."""
    try:
        response = stripe.payouts.list(limit=20)
        return list(response.auto_paging_iter())
    except Exception as e:
        logging.error(f"Error listing Stripe payouts: {e}")
        raise RuntimeError("Stripe API error") from e


def list_stripe_disputes(stripe: StripeClient) -> list[dict[str, Any]]:
    """list Stripe disputes using the Stripe SDK."""
    try:
        response = stripe.disputes.list(limit=20)
        return list(response.auto_paging_iter())
    except Exception as e:
        logging.error(f"Error listing Stripe disputes: {e}")
        raise RuntimeError("Stripe API error") from e


def list_stripe_events(stripe: StripeClient) -> list[dict[str, Any]]:
    """list Stripe events using the Stripe SDK."""
    try:
        response = stripe.events.list(limit=20)
        return list(response.auto_paging_iter())
    except Exception as e:
        logging.error(f"Error listing Stripe events: {e}")
        raise RuntimeError("Stripe API error") from e

# End of SDK utility functions for Stripe admin operations
