from __future__ import annotations

import numpy as np

def neutral_losses_full_distance_matrix(neutral_losses_array):
    """
    Full pairwise distance matrix for neutral-loss m/z values.

    DistanceMat[i, j] = abs(neutral_losses_array[i] - neutral_losses_array[j])
    """

    neutral_losses_array = np.asarray(neutral_losses_array,
                                      dtype = float)

    DistanceMat = np.abs(neutral_losses_array[:, None] -
                         neutral_losses_array[None, :])

    return DistanceMat
