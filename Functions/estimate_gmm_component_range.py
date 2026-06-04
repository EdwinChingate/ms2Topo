from __future__ import annotations

import numpy as np
def estimate_gmm_component_range(n_points,
                                 iqr_mz_da,
                                 target_component_iqr_da,
                                 min_points_per_component = 5,
                                 max_components_cap = 20):
    """
    Estimate local GMM component range from support and mz spread.
    """

    if n_points < min_points_per_component:
        return 0, 0

    if target_component_iqr_da <= 0:
        raise ValueError("target_component_iqr_da must be > 0")

    max_by_points = n_points // min_points_per_component

    if iqr_mz_da <= 0:
        max_by_iqr = 1
    else:
        max_by_iqr = int(np.ceil(iqr_mz_da / target_component_iqr_da))

    max_components = min(max_by_points,
                         max_by_iqr,
                         max_components_cap)

    max_components = max(max_components,
                         1)

    min_components = 1

    return min_components, max_components
