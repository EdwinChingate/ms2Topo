from __future__ import annotations

from pathlib import Path
import os
import re
import numpy as np
import pandas as pd
from scipy.sparse import coo_matrix, csr_matrix

def neutral_loss_normalize_intensity_vector(intensity_vec,
                               normalization = "l2"):
    """
    Normalize one intensity vector.
    """

    intensity_vec = np.asarray(intensity_vec,
                               dtype = float)

    if normalization is None:
        return intensity_vec

    if normalization != "l2":
        raise ValueError("normalization must be None or 'l2'.")

    norm_value = np.linalg.norm(intensity_vec)

    if norm_value > 0:
        intensity_vec = intensity_vec / norm_value

    return intensity_vec
