"""
Redis configuration settings with timeout and performance parameters.
"""

# Import settings
from app.core.config import settings


class ValkeyConfig:
    """
    Production-grade configuration for Valkey (Redis) client.
    Follows best practices for distributed caching, sharding, locking, retry/backoff, SSL, and monitoring.
    See _docs/best_practices for rationale and advanced usage.

    Shared config values (sourced from REDIS_*) are compatible with both legacy Redis and Valkey clients.
    Valkey-only features use VAPI_* environment variables for advanced configuration.
    """

    # --- Sharding/Cluster (Valkey-only, VAPI_*) ---
    VALKEY_SHARD_SIZE = getattr(
        settings, "VAPI_SHARD_SIZE", 25 * 1024 * 1024 * 1024
    )  # 25GB per shard
    VALKEY_SHARD_OPS_LIMIT = getattr(
        settings, "VAPI_SHARD_OPS_LIMIT", 25000
    )  # ops/second per shard
    VALKEY_SHARD_NODES = getattr(
        settings,
        "VAPI_SHARD_NODES",
        [
            {"host": "shard1", "port": 6379},
            {"host": "shard2", "port": 6379},
        ],
    )
    VALKEY_CLUSTER_MODE = getattr(settings, "VAPI_CLUSTER_MODE", False)

    # --- Connection (shared, REDIS_*) ---
    VALKEY_HOST = getattr(settings, "REDIS_HOST", "localhost")
    VALKEY_PORT = getattr(settings, "REDIS_PORT", 6379)
    VALKEY_DB = getattr(settings, "REDIS_DB", 0)
    VALKEY_POOL_SIZE = getattr(settings, "REDIS_POOL_SIZE", 20)
    VALKEY_MAX_CONNECTIONS = getattr(settings, "REDIS_MAX_CONNECTIONS", 100)
    VALKEY_SOCKET_TIMEOUT = getattr(settings, "REDIS_SOCKET_TIMEOUT", 5)
    VALKEY_SOCKET_CONNECT_TIMEOUT = getattr(settings, "REDIS_SOCKET_CONNECT_TIMEOUT", 5)

    # --- Cluster Mode (Valkey-only, VAPI_*) ---
    VALKEY_CLUSTER = getattr(settings, "VAPI_CLUSTER", False)

    # --- Authentication (shared, REDIS_*) ---
    VALKEY_PASSWORD = getattr(settings, "REDIS_PASSWORD", None)
    VALKEY_USERNAME = getattr(settings, "REDIS_USERNAME", None)

    # --- Retry/Backoff (Valkey-only, VAPI_*) ---
    VALKEY_RETRY_ATTEMPTS = getattr(settings, "VAPI_RETRY_ATTEMPTS", 3)
    # Supported backoff types: exponential, jitter, constant
    VALKEY_RETRY_BACKOFF_TYPE = getattr(
        settings, "VAPI_RETRY_BACKOFF_TYPE", "exponential"
    )
    VALKEY_RETRY_BACKOFF_BASE = getattr(settings, "VAPI_RETRY_BACKOFF_BASE", 0.01)
    VALKEY_RETRY_BACKOFF_CAP = getattr(settings, "VAPI_RETRY_BACKOFF_CAP", 0.5)

    # --- Stripe Configuration ---
    STRIPE_SECRET_KEY = getattr(settings, "STRIPE_SECRET_KEY", "sk_live_your_key")
    STRIPE_WEBHOOK_SECRET = getattr(settings, "STRIPE_WEBHOOK_SECRET", "whsec_your_secret")
    STRIPE_PUBLISHABLE_KEY = getattr(settings, "STRIPE_PUBLISHABLE_KEY", "pk_live_your_key")
    STRIPE_SUCCESS_URL = getattr(settings, "STRIPE_SUCCESS_URL", "http://localhost:8000/success")
    STRIPE_CANCEL_URL = getattr(settings, "STRIPE_CANCEL_URL", "http://localhost:8000/cancel")
    STRIPE_PORTAL_RETURN_URL = getattr(settings, "STRIPE_PORTAL_RETURN_URL", "http://localhost:8000/portal")

    # --- Locking (Valkey-only, VAPI_*) ---
    VALKEY_LOCK_TIMEOUT = getattr(settings, "VAPI_LOCK_TIMEOUT", 10)
    VALKEY_LOCK_BLOCKING = getattr(settings, "VAPI_LOCK_BLOCKING", True)
    VALKEY_LOCK_BLOCKING_TIMEOUT = getattr(settings, "VAPI_LOCK_BLOCKING_TIMEOUT", 5)

    # --- Command Timeout (Valkey-only, VAPI_*) ---
    VALKEY_COMMAND_TIMEOUT = getattr(settings, "VAPI_COMMAND_TIMEOUT", 5)

    # --- SSL/TLS (shared, REDIS_*) ---
    VALKEY_SSL = getattr(settings, "REDIS_SSL", False)
    VALKEY_SSL_CERT_REQS = getattr(settings, "REDIS_SSL_CERT_REQS", None)
    VALKEY_SSL_CA_CERTS = getattr(settings, "REDIS_SSL_CA_CERTS", None)
    VALKEY_SSL_KEYFILE = getattr(settings, "REDIS_SSL_KEYFILE", None)
    VALKEY_SSL_CERTFILE = getattr(settings, "REDIS_SSL_CERTFILE", None)

    # --- Monitoring (Valkey-only, VAPI_*) ---
    VALKEY_METRICS_ENABLED = getattr(settings, "VAPI_METRICS_ENABLED", True)
    VALKEY_METRICS_NAMESPACE = getattr(settings, "VAPI_METRICS_NAMESPACE", "valkey")

    # --- Docs ---
    # See _docs/best_practices for advanced usage, rationale, and tuning recommendations.
