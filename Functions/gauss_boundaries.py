from __future__ import annotations

import numpy as np
from scipy import integrate

def gauss_boundaries(context,
                     params):
    """
    Build curve-fit bounds for Gaussian parameters.

    Expected context keys:
        smooth_peaks

    Relevant params:
        params["gaussian"]["min_value"]
    """

    smooth_peaks = context["smooth_peaks"]
    min_value = params["gaussian"]["min_value"]

    rt_vec = smooth_peaks[:, 0]
    int_vec = smooth_peaks[:, 1]

    rt_max = np.max(rt_vec)
    rt_min = np.min(rt_vec)
    rt_max_difference = rt_max - rt_min

    integral = integrate.simpson(y = int_vec,
                                 x = rt_vec)

    bounds_list = [[rt_min, rt_max, rt_max_difference],
                   [min_value, rt_max_difference, rt_max_difference / 6],
                   [min_value, integral, integral / 2]]

    bounds_mat = np.array(bounds_list)

    return bounds_mat
