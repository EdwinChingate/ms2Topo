from __future__ import annotations

import numpy as np

def CosineMatrix(AlignedFragmentsMat,
                 N_features,
                 dtype = np.float32):
    """
    Fast vectorized cosine matrix.

    Rows of AlignedFragmentsMat are aligned fragments.
    Column 0 is fragment m/z.
    Columns 1..N_features are spectra.
    """

    spectra_mat = np.asarray(AlignedFragmentsMat[:, 1:N_features + 1],
                             dtype=dtype)

    dot_mat = spectra_mat.T @ spectra_mat

    norms = np.sqrt(np.sum(spectra_mat * spectra_mat,
                           axis=0))

    denom = np.outer(norms,
                     norms)

    CosineMat = np.zeros_like(dot_mat,
                              dtype=dtype) 

    valid = denom > 0

    CosineMat[valid] = dot_mat[valid] / denom[valid] 


    return CosineMat
