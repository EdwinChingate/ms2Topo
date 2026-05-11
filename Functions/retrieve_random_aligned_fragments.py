from __future__ import annotations
from CosineMatrix import *
import numpy as np

def retrieve_random_aligned_fragments(aligned_fragments_mat,
                                      current_sampling_size,
                                      rng = None):
    """
    Sample spectra from an aligned-fragment matrix and compute their cosine matrix.
    """

    if rng is None:
        rng = np.random.default_rng()

    n_fragments = aligned_fragments_mat.shape[0]
    n_spectra = aligned_fragments_mat.shape[1] - 1

    if n_spectra < 1:
        raise ValueError("aligned_fragments_mat must contain at least one spectrum column after the m/z column.")

    current_sampling_size = min(int(current_sampling_size),
                                n_spectra)

    current_sampling_size = max(current_sampling_size,
                                1)

    sampled_spectrum_ids = rng.choice(np.arange(n_spectra),
                                      size = current_sampling_size,
                                      replace = False).tolist()

    current_sample_aligned_fragments_mat = np.full((n_fragments, current_sampling_size + 1),
                                                   np.nan)

    current_sample_aligned_fragments_mat[:, 0] = aligned_fragments_mat[:, 0]
    current_sample_aligned_fragments_mat[:, 1:] = aligned_fragments_mat[:, np.array(sampled_spectrum_ids) + 1].copy()

    cosine_matrix = CosineMatrix(AlignedFragmentsMat = current_sample_aligned_fragments_mat,
                                 N_features = current_sampling_size)

    return [cosine_matrix,
            current_sample_aligned_fragments_mat,
            sampled_spectrum_ids]