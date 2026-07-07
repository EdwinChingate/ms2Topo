# Extracted from notebook: 713031fb-407a-42c5-b338-3c1aba9bdf96.ipynb
# One unique top-level function per file. Auto-generated from top-level function definitions.
from __future__ import annotations
import numpy as np
from estimate_min_component_separation_da import estimate_min_component_separation_da


def estimate_max_gmm_components_from_mz_interval(mz_vec,
                                                 min_component_separation_da = 1e-3,
                                                 max_components_per_da = None,
                                                 min_component_separation_ppm = 3,
                                                 max_components_cap = 10,
                                                 min_points_per_component = None):
    """
    Estimate the maximum interpretable GMM components from the m/z interval.

    The primary constraint is component density along the m/z axis:

        max_components_by_interval =
            floor(window_width_da / minimum_separation_da) + 1

    where minimum_separation_da is the largest active constraint among:
        min_component_separation_da
        1 / max_components_per_da
        min_component_separation_ppm converted to Da

    min_points_per_component can still be used as a safety cap, but it is not
    the main source of model complexity.
    """

    mz_vec = np.asarray(mz_vec,
                        dtype = float)

    mz_vec = mz_vec[np.isfinite(mz_vec)]

    n_points = len(mz_vec)

    if n_points == 0:
        return {"max_components": 0,
                "window_width_da": np.nan,
                "minimum_separation_da": np.nan,
                "max_components_by_interval": 0,
                "max_components_by_points": np.nan}

    if n_points == 1:
        return {"max_components": 1,
                "window_width_da": 0.0,
                "minimum_separation_da": np.nan,
                "max_components_by_interval": 1,
                "max_components_by_points": 1}

    median_mz = float(np.median(mz_vec))
    min_mz = float(np.min(mz_vec))
    max_mz = float(np.max(mz_vec))

    window_width_da = max_mz - min_mz

    minimum_separation_da = estimate_min_component_separation_da(
        median_mz = median_mz,
        min_component_separation_da = min_component_separation_da,
        max_components_per_da = max_components_per_da,
        min_component_separation_ppm = min_component_separation_ppm)

    if minimum_separation_da <= 0:

        max_components_by_interval = 1

    else:

        max_components_by_interval = int(np.floor(window_width_da /
                                                  minimum_separation_da)) + 1

    max_components = min(int(max_components_by_interval),
                         int(max_components_cap),
                         int(n_points))

    max_components_by_points = np.nan

    if min_points_per_component is not None:

        min_points_per_component = max(int(min_points_per_component),
                                       1)

        max_components_by_points = int(n_points) // min_points_per_component

        max_components_by_points = max(max_components_by_points,
                                       1)

        max_components = min(max_components,
                             max_components_by_points)

    max_components = max(int(max_components),
                         1)

    return {"max_components": max_components,
            "window_width_da": float(window_width_da),
            "minimum_separation_da": float(minimum_separation_da),
            "max_components_by_interval": int(max_components_by_interval),
            "max_components_by_points": max_components_by_points}
