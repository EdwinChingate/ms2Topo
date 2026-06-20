from __future__ import annotations

import numpy as np

def fragments_from_features(aligned_intensity_df):
    aligned_intensity_mat = aligned_intensity_df.to_numpy()
    fragments_count_vec = np.sum(aligned_intensity_mat,
                                 axis = 1)
    fragments_count_loc = np.where(fragments_count_vec > 0)[0]
    return fragments_count_loc
