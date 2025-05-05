# ! Stripe Types Registry for type checking and runtime reflection
# Uses types-stripe stubs for static analysis, and real stripe package for runtime

import stripe
from typing import Any

# * Dynamically build an exhaustive registry of all Stripe classes/types
STRIPE_TYPE_REGISTRY: dict[str, Any] = {}

for name in dir(stripe):
    obj = getattr(stripe, name)
    if isinstance(obj, type):
        # Exclude builtins and private classes
        if obj.__module__.startswith("stripe") and not name.startswith("_"):
            STRIPE_TYPE_REGISTRY[name] = obj

# * Generate an exhaustive list of all valid Stripe types for export
# This will create individual exports for every public Stripe type

# // BEGIN AUTO-GENERATED STRIPE TYPES EXPORTS
# * Each type is individually exported for type checking and import convenience
for _type_name, _type in STRIPE_TYPE_REGISTRY.items():
    globals()[_type_name] = _type
# // END AUTO-GENERATED STRIPE TYPES EXPORTS

__all__ = list(STRIPE_TYPE_REGISTRY.keys())

# // STRIPE_TYPE_REGISTRY and all Stripe types are now available as direct imports
# // Type checkers (mypy, pyright) will use types-stripe stubs automatically if installed