import logging

import stripe
from fastapi import Depends, FastAPI

from app.core.config import StripeSettings

# --- Singleton StripeClient Management ---
_stripe_client = None


def register_stripe_startup(app: FastAPI) -> None:
    """
    Register startup logic to initialize the StripeClient singleton.
    """

    @app.lifespan
    async def lifespan(_app: FastAPI):
        global _stripe_client
        try:
            _stripe_client = get_stripe_client(StripeSettings.STRIPE_SECRET_KEY)
            logging.info("StripeClient initialized successfully.")
        except Exception as e:
            logging.error(f"Failed to initialize StripeClient: {e}")
            raise
        yield


def get_stripe_client(settings: StripeSettings = Depends(StripeSettings)):
    """
    Returns the configured Stripe client/module for API calls.
    Sets the API key based on environment (test or production).
    Extend here for multi-account or advanced scenarios.
    """
    stripe.api_key = settings.STRIPE_SECRET_KEY or "sk_test_default"
    return stripe


# --- Optional: StripeConfig Utilities (Test helpers) ---
class StripeConfig:
    """
    Configuration utilities for Stripe integration (test mode, test cards, etc.)
    """

    @classmethod
    def is_test_mode(cls, settings: StripeSettings) -> bool:
        """Check if Stripe is in test mode."""
        return settings.STRIPE_SECRET_KEY.startswith("sk_test_")

    @staticmethod
    def get_test_card_numbers() -> dict[str, str]:
        """Return test card numbers for different scenarios."""
        return {
            "success": "4242424242424242",
            "requires_auth": "4000002500003155",
            "declined": "4000000000000002",
            "insufficient_funds": "4000000000009995",
            "processing_error": "4000000000000119",
        }

    @staticmethod
    def get_test_dashboard_url(object_id: str, object_type: str) -> str:
        """Generate Stripe dashboard URL for test objects."""
        base_url = "https://dashboard.stripe.com/test/"
        paths = {
            "customer": f"customers/{object_id}",
            "subscription": f"subscriptions/{object_id}",
            "payment": f"payments/{object_id}",
            "invoice": f"invoices/{object_id}",
        }
        return base_url + paths.get(object_type, "")


# Usage in your main app:
# from .config import register_stripe_startup, get_stripe_client
# register_stripe_startup(app)
# Use Depends(get_stripe_client) in your endpoints/services
