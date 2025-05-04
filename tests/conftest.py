import uuid
import pytest

@pytest.fixture
def mock_stripe_customer():
    """Mock Stripe customer object for use in tests."""
    class Customer:
        def __init__(self):
            self.id = f"cus_{uuid.uuid4()}"
            self.user_id = str(uuid.uuid4())
    return Customer()
