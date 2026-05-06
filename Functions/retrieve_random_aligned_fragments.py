from __future__ import annotations
from CosineMatrix import *
import numpy as np

# TODO: unresolved names: aligned_fragments_mat, current_sampling_size, n_fragments, n_spectra

def retrieve_random_aligned_fragments():

    rng = np.random.default_rng()
    sample_feature_module = rng.choice(np.arange(n_spectra),
                                       size = current_sampling_size,
                                       replace = False).tolist()
    current_sample_aligned_fragments_mat = np.full((n_fragments, current_sampling_size + 1),
                                                    np.nan)
    current_sample_aligned_fragments_mat[:, 0] = aligned_fragments_mat[:, 0]
    current_sample_aligned_fragments_mat[:, 1:] = aligned_fragments_mat[:, np.array(sample_feature_module) + 1].copy()

    cosine_matrix = CosineMatrix(AlignedFragmentsMat = current_sample_aligned_fragments_mat,
                                 N_features = current_sampling_size)

    return cosine_matrix