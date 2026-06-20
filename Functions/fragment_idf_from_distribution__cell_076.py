from __future__ import annotations

import numpy as np
import pandas as pd

def fragment_idf_from_distribution(DF_vector,
                                   n_features,
                                   smooth_idf = False):
    """
    Calculate the inverse feature frequency for each aligned fragment.
    """

    IDF = np.zeros(len(DF_vector),
                   dtype = float)

    valid_fragments = DF_vector > 0

    if smooth_idf:
        IDF[valid_fragments] = np.log((1 + n_features) / (1 + DF_vector[valid_fragments])) + 1

    else:
        IDF[valid_fragments] = np.log(n_features / DF_vector[valid_fragments])

    return IDF
