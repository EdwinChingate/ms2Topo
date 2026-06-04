from __future__ import annotations

import numpy as np

def weight_gauss(context,
                 params):
    """
    Estimate Gaussian parameters by intensity-weighted moments.

    Expected context keys:
        rt_vec, int_vec, rt

    Relevant params:
        params["gaussian"]["estimate_rt_from_weights"]
    """

    rt_vec = context["rt_vec"]
    int_vec = context["int_vec"].copy()
    rt = context["rt"]

    min_intensity = np.min(int_vec)

    if min_intensity < 0:
        int_vec = int_vec - min_intensity

    max_intensity = np.max(int_vec)
    n_signals = len(int_vec)
    sum_intensity = np.sum(int_vec)
    relative_intensity = int_vec / sum_intensity

    if params["gaussian"]["estimate_rt_from_weights"]:
        rt = np.sum(rt_vec * relative_intensity)

    rt_difference = rt_vec - rt
    variance = np.sum(relative_intensity * rt_difference ** 2) * n_signals / (n_signals - 1)
    rt_std = np.sqrt(variance)
    integral = max_intensity * rt_std * np.sqrt(2 * np.pi)

    gaussian_parameters = [rt,
                           rt_std,
                           integral]

    return gaussian_parameters
