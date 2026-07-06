# Extracted from notebook: 904937b2-026f-4f59-b3c0-21112b1589f8.ipynb
# One function per file. Auto-generated from top-level function definitions.
from __future__ import annotations

from pathlib import Path
import os
import re
import glob
import sys

import numpy as np
import pandas as pd
from scipy.sparse import coo_matrix, csr_matrix

try:
    import matplotlib.pyplot as plt
except Exception:
    plt = None

try:
    import networkx as nx
except Exception:
    nx = None

try:
    from sklearn.mixture import GaussianMixture
except Exception:
    GaussianMixture = None


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
