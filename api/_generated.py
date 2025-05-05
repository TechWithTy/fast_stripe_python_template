# Dynamically import all VAPI types as globals using TypesConfig
import importlib
import os
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from functools import lru_cache
from pathlib import Path
from threading import Lock

from ._types import TypesConfig

print(f"[DEBUG] sys.path before modification: {sys.path}")
print(
    f"[DEBUG] Attempting to import modules using library_name='{TypesConfig.library_name}'"
)

_imported_types = {}
_imported_types_lock = Lock()

# Circuit breaker config
CB_FAILURE_THRESHOLD = 3  # Number of failures before opening circuit
CB_RECOVERY_TIMEOUT = 10  # Seconds to wait before attempting recovery
CB_STATE = {}
CB_LAST_FAILURE = {}

NUM_THREADS = int(os.getenv("VAPI_IMPORT_THREADS", "8"))  # Configurable thread count


# Caching decorator for module/class import
@lru_cache(maxsize=128)
def cached_import(module_name, class_name):
    return getattr(importlib.import_module(module_name), class_name)


def import_type(filename):
    module_name = f"{TypesConfig.library_name}.{Path(filename).stem}"
    if TypesConfig.conversion_method == "camel_case":
        class_name = "".join(
            part.capitalize() for part in Path(filename).stem.split("_")
        )
    else:
        class_name = Path(filename).stem
    print(f"[DEBUG] Importing: module_name='{module_name}', class_name='{class_name}'")
    # Circuit breaker logic
    if CB_STATE.get(module_name, "closed") == "open":
        # Check if recovery timeout has passed
        if time.time() - CB_LAST_FAILURE.get(module_name, 0) < CB_RECOVERY_TIMEOUT:
            print(f"[CB] Circuit open for {module_name}, skipping import.")
            return None
        else:
            print(f"[CB] Recovery timeout passed for {module_name}, resetting circuit.")
            CB_STATE[module_name] = "closed"
            CB_LAST_FAILURE[module_name] = 0
    try:
        imported_class = cached_import(module_name, class_name)
        with _imported_types_lock:
            _imported_types[class_name] = imported_class
    except Exception as e:
        print(f"[ERROR] Failed to import {class_name} from {module_name}: {e}")
        # Circuit breaker failure tracking
        CB_LAST_FAILURE[module_name] = time.time()
        CB_STATE[module_name] = CB_STATE.get(module_name, "closed")
        failures = CB_STATE.get(f"{module_name}_failures", 0) + 1
        CB_STATE[f"{module_name}_failures"] = failures
        if failures >= CB_FAILURE_THRESHOLD:
            CB_STATE[module_name] = "open"
            print(f"[CB] Circuit opened for {module_name} after {failures} failures.")


# Use ThreadPoolExecutor to parallelize imports
with ThreadPoolExecutor(max_workers=NUM_THREADS) as executor:
    futures = [executor.submit(import_type, filename) for filename in TypesConfig.types]
    for future in as_completed(futures):
        future.result()

globals().update(_imported_types)

__all__ = list(_imported_types.keys())
