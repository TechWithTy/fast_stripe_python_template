"""
Test suite for Stripe async PaymentIntent creation (automatic_async).
- Mocks Stripe API to avoid real charges.
- Validates Pydantic models, error handling, and async logic.
- Follows DRY, SOLID, and CI/CD best practices.
"""

import pytest

from app.core.third_party_integrations.stripe_home.sdk.intent import (
    PaymentIntentCreateRequest,
    PaymentIntentCreateResponse,
    create_payment_intent,
)


class MockStripeClient:
    class PaymentIntent:
        @staticmethod
        def create(**kwargs):
            if kwargs["amount"] <= 0:
                raise ValueError("Amount must be positive")
            # Simulate Stripe response
            return {
                "id": "pi_test_123",
                "status": "succeeded",
                "capture_method": "automatic_async",
                "client_secret": "secret_123",
                "latest_charge": "ch_test_123",
            }

def mock_get_stripe_client(settings=None):
    return MockStripeClient

@pytest.mark.asyncio
async def test_create_payment_intent_success(monkeypatch):
    # Patch get_stripe_client
    from app.core.third_party_integrations.stripe_home import sdk
    monkeypatch.setattr(sdk.intent, "get_stripe_client", mock_get_stripe_client)

    payload = PaymentIntentCreateRequest(
        amount=2000,
        currency="usd",
        payment_method="pm_card_visa"
    )
    response = await create_payment_intent(payload)
    assert isinstance(response, PaymentIntentCreateResponse)
    assert response.status == "succeeded"
    assert response.capture_method == "automatic_async"
    assert response.id.startswith("pi_")
    assert response.latest_charge.startswith("ch_")

@pytest.mark.asyncio
async def test_create_payment_intent_invalid_amount(monkeypatch):
    from app.core.third_party_integrations.stripe_home import sdk
    monkeypatch.setattr(sdk.intent, "get_stripe_client", mock_get_stripe_client)

    with pytest.raises(ValueError):
        PaymentIntentCreateRequest(
            amount=0,
            currency="usd",
            payment_method="pm_card_visa"
        )
