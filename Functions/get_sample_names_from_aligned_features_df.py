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

# Local function dependencies extracted from the same notebook.
from clean_feature_or_sample_id import clean_feature_or_sample_id


def get_sample_names_from_aligned_features_df(aligned_features_df,
                                              feat_id_col = "feat_id"):
    """
    Get real sample IDs from the aligned feature table.

    In ms2Topo, sample columns start immediately after feat_id.
    """

    aligned_features_df = aligned_features_df.copy()

    if feat_id_col not in aligned_features_df.columns:
        raise ValueError("feat_id_col was not found: " + str(feat_id_col))

    columns = list(aligned_features_df.columns)
    feat_id_col_id = columns.index(feat_id_col)

    sample_cols = columns[(feat_id_col_id + 1):]

    sample_names = [clean_feature_or_sample_id(sample_col)
                    for sample_col in sample_cols]

    return sample_names
