from __future__ import annotations

import numpy as np

def redistribute_sampling(context,
                          params):
    """
    Resample a chromatographic signal onto an evenly spaced axis.

    Expected context keys:
        peak_chromatogram, n_new

    Relevant params:
        params["columns"]["rt_col"]
        params["columns"]["int_col"]
        params["redistribution"]["auto_power_of_two"]
    """

    peak_chromatogram = context["peak_chromatogram"]
    n_new = context["n_new"]

    rt_col = params["columns"]["rt_col"]
    int_col = params["columns"]["int_col"]
    auto_power_of_two = params["redistribution"]["auto_power_of_two"]

    n_signals = len(peak_chromatogram[:, rt_col])

    if auto_power_of_two:
        n_new = 2 ** int(np.ceil(np.log(n_signals) / np.log(2)))

    redistributed_peak = np.zeros((n_new,
                                   2))

    rt = peak_chromatogram[:, rt_col]
    intensity = peak_chromatogram[:, int_col]

    min_rt = np.min(rt)
    max_rt = np.max(rt)
    rt_new = np.linspace(min_rt,
                         max_rt,
                         n_new)

    intensity_new = np.interp(rt_new,
                              rt,
                              intensity)

    redistributed_peak[:, 0] = rt_new
    redistributed_peak[:, 1] = intensity_new

    return redistributed_peak
