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


def centroid_index_to_dataframe(centroid_index,
                                id_col = "aligned_fragment_id",
                                mz_col = "aligned_fragment_mz"):
    """
    Convert the internal centroid index into a report table.
    """

    centroid_df = pd.DataFrame({id_col: np.arange(len(centroid_index["centroid_mz"]),
                                                 dtype = int),
                                "centroid_original_id": centroid_index["centroid_original_id"],
                                mz_col: centroid_index["centroid_mz"],
                                "centroid_sigma": centroid_index["centroid_sigma"],
                                "centroid_edge": centroid_index["centroid_edge"],
                                "centroid_count": centroid_index["centroid_count"]})

    centroid_df["centroid_min_mz"] = centroid_df[mz_col] - centroid_df["centroid_edge"]
    centroid_df["centroid_max_mz"] = centroid_df[mz_col] + centroid_df["centroid_edge"]

    return centroid_df
