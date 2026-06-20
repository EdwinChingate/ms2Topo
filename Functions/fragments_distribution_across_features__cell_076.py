from __future__ import annotations

import numpy as np
import pandas as pd

def fragments_distribution_across_features(binary_fragment_mat):
    """
    Count how many features contain each aligned fragment.

    Rows:
        aligned fragments

    Columns:
        features
    """

    DF_vector = np.sum(binary_fragment_mat,
                       axis = 1)

    return DF_vector
