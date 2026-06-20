from __future__ import annotations

import numpy as np
import pandas as pd

def aligned_fragments_to_binary_matrix(aligned_intensity_df,
                                       feature_cols):
    """
    Convert an aligned fragments-by-features table into a binary matrix.

    Rows:
        aligned fragments

    Columns:
        features

    Values:
        1 if the feature contains the aligned fragment, else 0.
    """

    binary_fragment_mat = (aligned_intensity_df[feature_cols].to_numpy(dtype = float) > 0).astype(int)

    return binary_fragment_mat
