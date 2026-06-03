from __future__ import annotations

import numpy as np

def weighted_quantile(values,
                      weights,
                      quantiles):
    """
    Calculate weighted quantiles.

    values    : mz values
    weights   : posterior probability / responsibility
    quantiles : [0.25, 0.5, 0.75], etc.
    """

    values = np.asarray(values, dtype=float)
    weights = np.asarray(weights, dtype=float)
    quantiles = np.asarray(quantiles, dtype=float)

    valid = np.isfinite(values) & np.isfinite(weights) & (weights > 0)

    values = values[valid]
    weights = weights[valid]

    if len(values) == 0:
        return np.repeat(np.nan, len(quantiles))

    sort_ids = np.argsort(values)

    values = values[sort_ids]
    weights = weights[sort_ids]

    cumulative_weights = np.cumsum(weights)
    cumulative_weights = cumulative_weights / cumulative_weights[-1]

    return np.interp(quantiles, cumulative_weights, values)
