from __future__ import annotations

def deep_update(base, updates=None):
    """
    Recursively update a nested dictionary.

    This keeps configuration changes local: override only the values you want,
    while preserving the rest of the defaults.
    """
    if updates is None:
        return base

    for key, value in updates.items():
        if isinstance(value, dict) and isinstance(base.get(key), dict):
            deep_update(base[key], value)
        else:
            base[key] = value

    return base