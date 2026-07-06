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


def make_selected_aligned_spectra_wide_df(aligned_spectra_long_df):
    """
    Convert the long aligned spectra report into a wide table:

        aligned_fragment_id | aligned_fragment_mz | feat_3539 | feat_1171 | ...
    """

    if aligned_spectra_long_df is None or len(aligned_spectra_long_df) == 0:
        return pd.DataFrame()

    required_cols = ["feat_id",
                     "aligned_fragment_id",
                     "aligned_fragment_mz",
                     "aligned_intensity"]

    for col in required_cols:
        if col not in aligned_spectra_long_df.columns:
            raise ValueError("Missing required column: " + str(col))

    wide_df = aligned_spectra_long_df.pivot_table(
        index = ["aligned_fragment_id", "aligned_fragment_mz"],
        columns = "feat_id",
        values = "aligned_intensity",
        aggfunc = "max",
        fill_value = 0
    )

    wide_df = wide_df.reset_index()

    wide_df.columns.name = None

    feature_cols = [col for col in wide_df.columns
                    if col not in ["aligned_fragment_id", "aligned_fragment_mz"]]

    rename_dict = {col: "feat_" + str(col)
                   for col in feature_cols}

    wide_df = wide_df.rename(columns = rename_dict)

    wide_df = wide_df.sort_values("aligned_fragment_mz").reset_index(drop = True)

    return wide_df
