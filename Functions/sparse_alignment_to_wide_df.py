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


def sparse_alignment_to_wide_df(aligned_sparse_mat,
                                aligned_mz_vec,
                                feature_id_map_df,
                                id_col = "aligned_fragment_id",
                                mz_col = "aligned_fragment_mz"):

    """
    Convert a sparse aligned matrix into a wide DataFrame.

    Use this only when the dense table is small enough to fit in memory.
    """

    feature_id_map_df = feature_id_map_df.sort_values("spectrum_id").reset_index(drop = True)

    aligned_df = pd.DataFrame(aligned_sparse_mat.toarray())
    aligned_df.columns = [str(feat_id) for feat_id in feature_id_map_df["feat_id"].tolist()]

    aligned_df.insert(0,
                      mz_col,
                      aligned_mz_vec)

    aligned_df.insert(0,
                      id_col,
                      np.arange(len(aligned_mz_vec),
                                dtype = int))

    return aligned_df
