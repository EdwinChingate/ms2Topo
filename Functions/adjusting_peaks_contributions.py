from __future__ import annotations

import numpy as np

def adjusting_peaks_contributions(context,
                                  params):
    """
    Estimate linear contribution coefficients for overlapping Gaussian peaks.

    Expected context keys:
        smooth_peaks, chromatogram_matrix
    """

    smooth_peaks = context["smooth_peaks"]
    chromatogram_matrix = context["chromatogram_matrix"]

    int_vec = smooth_peaks[:, 1]
    n_peaks = len(chromatogram_matrix[0, :])
    chromatogram_matrix_transpose = chromatogram_matrix.T
    matrix_transpose_intensity = np.matmul(chromatogram_matrix_transpose,
                                           int_vec)

    matrix_transpose_chromatogram_matrix = np.matmul(chromatogram_matrix_transpose,
                                                     chromatogram_matrix)

    try:
        inverse_matrix = np.linalg.inv(matrix_transpose_chromatogram_matrix)
        contributions_vec = np.matmul(inverse_matrix,
                                      matrix_transpose_intensity)
    except np.linalg.LinAlgError:
        contributions_vec = np.ones(n_peaks)

    return contributions_vec
