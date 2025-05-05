from fastapi import HTTPException
from prometheus_client import Counter
from stripe import (
    APIConnectionError,
    APIError,
    AuthenticationError,
    CardError,
    IdempotencyError,
    InvalidRequestError,
    PermissionError,
    RateLimitError,
    SignatureVerificationError,
    StripeError,
)

# stripe_ERRORS Prometheus Counter for Stripe error types
stripe_ERRORS = Counter("stripe_errors", "Stripe errors by type", ["error_type"])

# --- Custom Exceptions for Stripe Operations (subclassing Stripe's) ---


class StripeServiceUnavailable(StripeError):
    """Raised when the Stripe service is unavailable or cannot be reached."""

    pass


class StripeTimeoutError(StripeError):
    """Raised when a Stripe operation times out."""

    pass


class StripeQueryError(StripeError):
    """Raised when a Stripe query fails due to syntax or execution error."""

    pass


class StripeIntegrityError(StripeError):
    """Raised when a Stripe operation violates integrity constraints (e.g., duplicate charge)."""

    pass


class StripeNotFoundError(StripeError):
    """Raised when a requested Stripe resource is not found."""

    pass


"""
Base exception for all Stripe-related errors.
"""


async def handle_stripe_exceptions(
    func,
    *,
    stripe_calls=None,
    endpoint: str | None = None,
    logger=None,
    current_user: dict | None = None,
    stripe_id: str | None = None,
    stripe_ERRORS=None,
):
    try:
        return await func() if hasattr(func, "__await__") else func()
    except APIConnectionError as e:
        if stripe_calls and endpoint:
            stripe_calls.labels(endpoint=endpoint, status="connection_error").inc()
        if stripe_ERRORS:
            stripe_ERRORS.labels(error_type="connection_error").inc()
        if logger:
            logger.error(
                "Stripe connection error",
                user_id=current_user.get("id") if current_user else None,
                error=str(e),
                stripe_id=stripe_id,
            )
        raise HTTPException(status_code=503, detail="Stripe connection error.")
    except APIError as e:
        # ! Stripe APIError: generic API error (e.g. 5xx, Stripe internal failure)
        if stripe_calls and endpoint:
            stripe_calls.labels(endpoint=endpoint, status="api_error").inc()
        if stripe_ERRORS:
            stripe_ERRORS.labels(error_type="api_error").inc()
        if logger:
            logger.error(
                "Stripe API error",
                user_id=current_user.get("id") if current_user else None,
                error=str(e),
                stripe_id=stripe_id,
            )
        raise HTTPException(status_code=502, detail="Stripe API error.")
    except AuthenticationError as e:
        if stripe_calls and endpoint:
            stripe_calls.labels(endpoint=endpoint, status="auth_error").inc()
        if stripe_ERRORS:
            stripe_ERRORS.labels(error_type="auth").inc()
        if logger:
            logger.error(
                "Stripe authentication error",
                user_id=current_user.get("id") if current_user else None,
                error=str(e),
                stripe_id=stripe_id,
            )
        raise HTTPException(status_code=401, detail="Stripe authentication error.")
    except PermissionError as e:
        if stripe_calls and endpoint:
            stripe_calls.labels(endpoint=endpoint, status="permission_error").inc()
        if stripe_ERRORS:
            stripe_ERRORS.labels(error_type="permission").inc()
        if logger:
            logger.warning(
                "Stripe permission error",
                user_id=current_user.get("id") if current_user else None,
                error=str(e),
                stripe_id=stripe_id,
            )
        raise HTTPException(status_code=403, detail="Insufficient Stripe permissions.")
    except RateLimitError as e:
        if stripe_calls and endpoint:
            stripe_calls.labels(endpoint=endpoint, status="rate_limit_error").inc()
        if stripe_ERRORS:
            stripe_ERRORS.labels(error_type="rate_limit").inc()
        if logger:
            logger.warning(
                "Stripe rate limit error",
                user_id=current_user.get("id") if current_user else None,
                error=str(e),
                stripe_id=stripe_id,
            )
        raise HTTPException(status_code=429, detail="Stripe rate limit exceeded.")
    except InvalidRequestError as e:
        if stripe_calls and endpoint:
            stripe_calls.labels(endpoint=endpoint, status="invalid_request").inc()
        if stripe_ERRORS:
            stripe_ERRORS.labels(error_type="invalid_request").inc()
        if logger:
            logger.error(
                "Stripe invalid request",
                user_id=current_user.get("id") if current_user else None,
                error=str(e),
                stripe_id=stripe_id,
            )
        raise HTTPException(status_code=400, detail="Stripe invalid request.")
    except CardError as e:
        if stripe_calls and endpoint:
            stripe_calls.labels(endpoint=endpoint, status="card_error").inc()
        if stripe_ERRORS:
            stripe_ERRORS.labels(error_type="card").inc()
        if logger:
            logger.error(
                "Stripe card error",
                user_id=current_user.get("id") if current_user else None,
                error=str(e),
                stripe_id=stripe_id,
            )
        raise HTTPException(status_code=402, detail="Stripe card error.")
    except IdempotencyError as e:
        if stripe_calls and endpoint:
            stripe_calls.labels(endpoint=endpoint, status="idempotency_error").inc()
        if stripe_ERRORS:
            stripe_ERRORS.labels(error_type="idempotency").inc()
        if logger:
            logger.error(
                "Stripe idempotency error",
                user_id=current_user.get("id") if current_user else None,
                error=str(e),
                stripe_id=stripe_id,
            )
        raise HTTPException(status_code=409, detail="Stripe idempotency error.")
    except SignatureVerificationError as e:
        if stripe_calls and endpoint:
            stripe_calls.labels(
                endpoint=endpoint, status="signature_verification_error"
            ).inc()
        if stripe_ERRORS:
            stripe_ERRORS.labels(error_type="signature_verification").inc()
        if logger:
            logger.error(
                "Stripe signature verification error",
                user_id=current_user.get("id") if current_user else None,
                error=str(e),
                stripe_id=stripe_id,
            )
        raise HTTPException(
            status_code=400, detail="Stripe signature verification error."
        )
    except StripeTimeoutError as e:
        if stripe_calls and endpoint:
            stripe_calls.labels(endpoint=endpoint, status="timeout").inc()
        if stripe_ERRORS:
            stripe_ERRORS.labels(error_type="timeout").inc()
        if logger:
            logger.error(
                "Stripe timeout",
                user_id=current_user.get("id") if current_user else None,
                error=str(e),
                stripe_id=stripe_id,
            )
        raise HTTPException(status_code=504, detail="Stripe timeout error.")
    except StripeQueryError as e:
        if stripe_calls and endpoint:
            stripe_calls.labels(endpoint=endpoint, status="query_error").inc()
        if stripe_ERRORS:
            stripe_ERRORS.labels(error_type="query").inc()
        if logger:
            logger.error(
                "Stripe query error",
                user_id=current_user.get("id") if current_user else None,
                error=str(e),
                stripe_id=stripe_id,
            )
        raise HTTPException(status_code=400, detail="Stripe query error.")
    except StripeIntegrityError as e:
        if stripe_calls and endpoint:
            stripe_calls.labels(endpoint=endpoint, status="integrity_error").inc()
        if stripe_ERRORS:
            stripe_ERRORS.labels(error_type="integrity").inc()
        if logger:
            logger.warning(
                "Stripe integrity error",
                user_id=current_user.get("id") if current_user else None,
                error=str(e),
                stripe_id=stripe_id,
            )
        raise HTTPException(status_code=409, detail="Stripe integrity error.")
    except StripeNotFoundError as e:
        if stripe_calls and endpoint:
            stripe_calls.labels(endpoint=endpoint, status="not_found").inc()
        if stripe_ERRORS:
            stripe_ERRORS.labels(error_type="not_found").inc()
        if logger:
            logger.warning(
                "Stripe resource not found",
                user_id=current_user.get("id") if current_user else None,
                error=str(e),
                stripe_id=stripe_id,
            )
        raise HTTPException(status_code=404, detail="Stripe resource not found.")
    except StripeServiceUnavailable as e:
        if stripe_calls and endpoint:
            stripe_calls.labels(endpoint=endpoint, status="service_unavailable").inc()
        if stripe_ERRORS:
            stripe_ERRORS.labels(error_type="service_unavailable").inc()
        if logger:
            logger.error(
                "Stripe service unavailable",
                user_id=current_user.get("id") if current_user else None,
                error=str(e),
                stripe_id=stripe_id,
            )
        raise HTTPException(status_code=503, detail="Stripe service unavailable.")
    except StripeError as e:
        if stripe_calls and endpoint:
            stripe_calls.labels(endpoint=endpoint, status="stripe_error").inc()
        if stripe_ERRORS:
            stripe_ERRORS.labels(error_type="stripe").inc()
        if logger:
            logger.error(
                "Stripe error",
                user_id=current_user.get("id") if current_user else None,
                error=str(e),
                stripe_id=stripe_id,
            )
        raise HTTPException(status_code=500, detail="A Stripe error occurred.")
    except HTTPException as e:
        if stripe_calls and endpoint:
            stripe_calls.labels(endpoint=endpoint, status="error").inc()
        if stripe_ERRORS:
            stripe_ERRORS.labels(error_type="client").inc()
        if logger:
            logger.warning(
                "Client error",
                user_id=current_user.get("id") if current_user else None,
                error=str(e),
                stripe_id=stripe_id,
            )
        raise
    except Exception as e:
        if stripe_calls and endpoint:
            stripe_calls.labels(endpoint=endpoint, status="error").inc()
        if stripe_ERRORS:
            stripe_ERRORS.labels(error_type="server").inc()
        if logger:
            logger.error(
                "Server error",
                user_id=current_user.get("id") if current_user else None,
                error=str(e),
                stripe_id=stripe_id,
            )
        raise HTTPException(status_code=500, detail="A Stripe storage error occurred.")
