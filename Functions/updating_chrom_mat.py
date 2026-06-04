from __future__ import annotations

import numpy as np

def updating_chrom_mat(context,
                       params):
    """
    Scale each Gaussian contribution by its fitted contribution coefficient.

    Expected context keys:
        chromatogram_matrix, contributions_vec
    """

    chromatogram_matrix = context["chromatogram_matrix"]
    contributions_vec = context["contributions_vec"]

    updated_chromatogram_matrix = chromatogram_matrix.copy()
    n_contributions = len(contributions_vec)

    for peak_id in np.arange(n_contributions,
                             dtype = int):
        updated_chromatogram_matrix[:, peak_id] = chromatogram_matrix[:, peak_id] * contributions_vec[peak_id]

    return updated_chromatogram_matrix
