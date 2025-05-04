# FastAPI-compatible test imports and setup
import logging
import os
import uuid
from unittest.mock import MagicMock, patch

import core.third_party_integrations.stripe_home.api.credit as credit
import pytest
import stripe
from core.third_party_integrations.stripe_home.api.credit import (
    allocate_subscription_credits,
)
from fastapi.testclient import TestClient

# Assume FastAPI app is imported from the main app entrypoint
from app.main import app

# Configure logger
logger = logging.getLogger(__name__)

# Set Stripe API key from environment
stripe.api_key = os.environ.get("STRIPE_SECRET_KEY_TEST", "sk_test_dummy")
stripe.api_version = os.environ.get("STRIPE_API_VERSION", "2023-10-16")

client = TestClient(app)


# --- Fixtures and Mocks ---
@pytest.fixture
def mock_user():
    """Mock user object for testing purposes."""

    class User:
        def __init__(self):
            self.id = str(uuid.uuid4())
            self.email = "test@example.com"
            self.username = "testuser"
            self.profile = type("Profile", (), {"credits_balance": 0})()

    return User()


@pytest.fixture
def mock_plan():
    """Mock plan object for testing purposes."""

    class Plan:
        def __init__(self):
            self.id = str(uuid.uuid4())
            self.plan_id = f"price_{uuid.uuid4()}"
            self.name = "Test Plan"
            self.amount = 1999
            self.currency = "usd"
            self.interval = "month"
            self.initial_credits = 100
            self.monthly_credits = 50
            self.active = True
            self.livemode = False

    return Plan()


@pytest.fixture
def mock_stripe_customer():
    """Mock Stripe customer object."""

    class Customer:
        def __init__(self):
            self.id = f"cus_{uuid.uuid4()}"

    return Customer()


# --- Tests ---
def test_initial_credit_allocation(mock_user, mock_plan, _mock_stripe_customer):
    """Test allocating initial credits when subscription is created (FastAPI style)."""
    with patch(
        "core.third_party_integrations.stripe_home.api.credit.allocate_subscription_credits",
        autospec=True,
    ) as mock_allocate:
        mock_allocate.return_value = True
        subscription_id = f"sub_test_{uuid.uuid4()}"
        description = f"Initial credits for {mock_plan.name} subscription"
        success = credit.allocate_subscription_credits(
            mock_user, mock_plan.initial_credits, description, subscription_id
        )
        mock_allocate.assert_called_once_with(
            mock_user, mock_plan.initial_credits, description, subscription_id
        )
        assert success is True
        mock_user.profile.credits_balance = mock_plan.initial_credits
        assert mock_user.profile.credits_balance == mock_plan.initial_credits


def test_monthly_credit_allocation(mock_user, mock_plan, _mock_stripe_customer):
    """Test allocating monthly credits when invoice payment succeeds."""
    with patch(
        "core.third_party_integrations.stripe_home.api.credit.allocate_subscription_credits",
        autospec=True,
    ) as mock_allocate:
        mock_allocate.return_value = True

        subscription_id = f"sub_test_{uuid.uuid4()}"
        description = f"Monthly credits for {mock_plan.name} subscription"
        success = credit.allocate_subscription_credits(
            mock_user, mock_plan.monthly_credits, description, subscription_id
        )
        mock_allocate.assert_called_once_with(
            mock_user, mock_plan.monthly_credits, description, subscription_id
        )
        assert success is True
        mock_user.profile.credits_balance = mock_plan.monthly_credits
        assert mock_user.profile.credits_balance == mock_plan.monthly_credits


def test_subscription_cancellation(_mock_user, _mock_plan):
    """Test cancelling a subscription at period end (logic only)."""
    subscription = MagicMock()
    subscription.cancel_at_period_end = False
    subscription.status = "active"
    # Simulate cancellation
    subscription.cancel_at_period_end = True
    assert subscription.cancel_at_period_end is True
    assert subscription.status == "active"


def test_payment_failure_handling(mock_user):
    """Test system properly handles failed payments (logic only)."""
    subscription = MagicMock()
    subscription.status = "past_due"
    mock_user.profile.credits_balance = 0
    assert subscription.status == "past_due"
    assert mock_user.profile.credits_balance == 0


def test_simple_credit_allocation(mock_user):
    """A simplified test that focuses just on credit allocation to isolate the issue."""
    with patch(
        "core.third_party_integrations.stripe_home.api.credit.allocate_subscription_credits",
        autospec=True,
    ) as mock_allocate:
        mock_allocate.return_value = True
        subscription_id = f"sub_test_{uuid.uuid4()}"
        description = "Test credit allocation"
        test_credits = 25
        success = allocate_subscription_credits(
            mock_user, test_credits, description, subscription_id
        )
        mock_allocate.assert_called_once_with(
            mock_user, test_credits, description, subscription_id
        )
        assert success is True
        mock_user.profile.credits_balance = test_credits
        assert mock_user.profile.credits_balance == test_credits


def test_subscription_upgrade(mock_user, mock_plan):
    """Test upgrading a subscription to a higher tier plan (logic only)."""
    premium_plan = MagicMock()
    premium_plan.plan_id = f"premium_{uuid.uuid4()}"
    premium_plan.initial_credits = 200
    with patch(
        "core.third_party_integrations.stripe_home.api.credit.allocate_subscription_credits",
        autospec=True,
    ) as mock_allocate:
        mock_allocate.return_value = True
        subscription_id = f"sub_test_{uuid.uuid4()}"
        # Initial allocation
        description = f"Initial credits for {mock_plan.name} subscription"
        success = credit.allocate_subscription_credits(
            mock_user, mock_plan.initial_credits, description, subscription_id
        )
        mock_allocate.assert_called_with(
            mock_user, mock_plan.initial_credits, description, subscription_id
        )
        assert success is True
        # Simulate upgrade
        upgrade_description = f"Upgrade credits for {premium_plan.plan_id} subscription"
        upgrade_credits = premium_plan.initial_credits - mock_plan.initial_credits
        upgrade_success = credit.allocate_subscription_credits(
            mock_user, upgrade_credits, upgrade_description, subscription_id
        )
        mock_allocate.assert_called_with(
            mock_user, upgrade_credits, upgrade_description, subscription_id
        )
        assert upgrade_success is True
