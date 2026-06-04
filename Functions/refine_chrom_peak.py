from __future__ import annotations

from adjusting_peaks_contributions import *
from overlapping_gauss_peaks import *
from parameters_fit_gauss_parallel_peaks import *
from refine_chrom_mat import *
from updating_chrom_mat import *

def refine_chrom_peak(context,
                      params):
    """
    Refine one Gaussian parameter matrix against a smoothed chromatogram.

    Expected context keys:
        parameters_mat, smooth_peaks, bounds_mat
    """

    parameters_mat = context["parameters_mat"]
    smooth_peaks = context["smooth_peaks"]
    bounds_mat = context["bounds_mat"]

    rt_vec = smooth_peaks[:, 0]

    overlap_context = {"rt_vec": rt_vec,
                       "parameters_mat": parameters_mat}

    chromatogram_matrix = overlapping_gauss_peaks(context = overlap_context,
                                                  params = params)

    contribution_context = {"smooth_peaks": smooth_peaks,
                            "chromatogram_matrix": chromatogram_matrix}

    contributions_vec = adjusting_peaks_contributions(context = contribution_context,
                                                      params = params)

    update_context = {"chromatogram_matrix": chromatogram_matrix,
                      "contributions_vec": contributions_vec}

    chromatogram_matrix = updating_chrom_mat(context = update_context,
                                             params = params)

    refine_context = {"chromatogram_matrix": chromatogram_matrix,
                      "chromatogram": smooth_peaks,
                      "parameters_mat": parameters_mat}

    chromatogram_matrix = refine_chrom_mat(context = refine_context,
                                           params = params)

    fit_context = {"rt_vec": rt_vec,
                   "chromatogram_matrix": chromatogram_matrix,
                   "bounds_mat": bounds_mat,
                   "parameters_mat": parameters_mat}

    gaussian_population = parameters_fit_gauss_parallel_peaks(context = fit_context,
                                                              params = params)

    return gaussian_population
