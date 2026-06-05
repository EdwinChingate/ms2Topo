from __future__ import annotations

from pathlib import Path
import os
import re
import numpy as np
import pandas as pd
from scipy.sparse import coo_matrix, csr_matrix

def normalize_intensity_vector(spectrum_df,
                               intensity_col = "median_Int",
                               normalization = "l2"):
    """
    Normalize fragment intensities within one consensus spectrum.

    normalization options:
        None -> keep original intensities
        "l2" -> divide by vector norm
    """

    if normalization is None:
        return spectrum_df

    if normalization != "l2":
        raise ValueError("normalization must be None or 'l2'.")

    spectrum_df = spectrum_df.copy()

    intensity_vec = spectrum_df[intensity_col].to_numpy(dtype = float)
    norm_value = np.linalg.norm(intensity_vec)

    if norm_value > 0:
        spectrum_df[intensity_col] = spectrum_df[intensity_col] / norm_value

    return spectrum_df
