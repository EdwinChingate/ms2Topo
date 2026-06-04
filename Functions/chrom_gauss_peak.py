from __future__ import annotations

import numpy as np

def chrom_gauss_peak(context,
                     params):
    """
    Calculate one Gaussian chromatographic peak.

    Expected context keys:
        rt_vec, rt, rt_std, integral

    Relevant params:
        params["gaussian"]["std_distance"]
    """

    rt_vec = context["rt_vec"]
    rt = context["rt"]
    rt_std = context["rt_std"]
    integral = context["integral"]

    std_distance = params["gaussian"]["std_distance"]

    n_signals = len(rt_vec)
    gaussian_intensity = np.zeros(n_signals)

    min_rt = rt - std_distance * rt_std
    max_rt = rt + std_distance * rt_std
    rt_filter = (rt_vec > min_rt) & (rt_vec < max_rt)

    log_vec = -((rt_vec[rt_filter] - rt) / rt_std) ** 2 / 2
    gaussian_intensity[rt_filter] = np.exp(log_vec) * integral / (rt_std * np.sqrt(2 * np.pi))

    return gaussian_intensity
