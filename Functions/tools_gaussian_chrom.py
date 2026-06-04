from __future__ import annotations

import numpy as np
from gauss_boundaries import *
from raw_gauss_seed import *
from redistribute_sampling import *
from smooth_data_and_find_peaks import *

def tools_gaussian_chrom(context,
                         params):
    """
    Generate smoothed chromatogram, parameter seeds, and bounds for curve fitting.

    Expected context keys:
        chromatogram
    """

    chromatogram = context["chromatogram"]

    smooth_context = {"chromatogram": chromatogram}

    smooth_peaks, peaks_max = smooth_data_and_find_peaks(context = smooth_context,
                                                         params = params)

    if len(peaks_max) == 0:
        return [[], [], []]

    n_smooth_points = len(smooth_peaks[:, 1])

    redistribution_context = {"peak_chromatogram": chromatogram,
                              "n_new": n_smooth_points}

    s_chrom = redistribute_sampling(context = redistribution_context,
                                    params = params)

    boundaries_context = {"smooth_peaks": smooth_peaks}
    bounds_mat = gauss_boundaries(context = boundaries_context,
                                  params = params)

    seed_context = {"smooth_peaks": smooth_peaks,
                    "peaks_max": peaks_max,
                    "bounds_mat": bounds_mat}

    parameters_mat = raw_gauss_seed(context = seed_context,
                                    params = params)

    n_peaks = len(parameters_mat[:, 0])

    min_vec = np.array([bounds_mat[:, 0]] * n_peaks)
    max_vec = np.array([bounds_mat[:, 1]] * n_peaks)

    min_list = min_vec.flatten()
    max_list = max_vec.flatten()

    bounds = (min_list,
              max_list)

    parameters_list = parameters_mat.flatten()

    return [s_chrom,
            parameters_list,
            bounds]
