from prometheus_client import Counter
from fastapi import HTTPException

# stripe_ERRORS Prometheus Counter for Stripe error types
stripe_ERRORS = Counter("stripe_errors", "Stripe errors by type", ["error_type"])

# --- Custom Exceptions for Stripe Operations ---

"""
Base exception for all Stripe-related errors.
"""
class StripeError(Exception):
    pass

"""
Raised when a user does not have permission to perform a Stripe operation.
"""
class StripePermissionError(StripeError):
    pass

"""
Raised when the Stripe service is unavailable or cannot be reached.
"""
class StripeServiceUnavailable(StripeError):
    pass

"""
Raised when a Stripe operation times out.
"""
class StripeTimeoutError(StripeError):
    pass

"""
Raised when a Stripe query fails due to syntax or execution error.
"""
class StripeQueryError(StripeError):
    pass

"""
Raised when authentication to Stripe fails.
"""
class StripeAuthenticationError(StripeError):
    pass

"""
Raised when a Stripe operation violates integrity constraints (e.g., duplicate charge).
"""
class StripeIntegrityError(StripeError):
    pass

"""
Raised when a requested Stripe resource is not found.
"""
class StripeNotFoundError(StripeError):
    pass

"""
Utility to wrap Stripe endpoint logic with robust exception-to-HTTP mapping and metrics/logging.
Usage (async):
    result = await handle_stripe_exceptions(
        lambda: some_async_func(...),
        stripe_calls=stripe_calls,
        endpoint="/stripe/payment",
        logger=logger,
        current_user=current_user,
        stripe_id=stripe_id,
        stripe_ERRORS=stripe_ERRORS
    )
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
    except StripePermissionError as e:
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
    except StripeAuthenticationError as e:
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
