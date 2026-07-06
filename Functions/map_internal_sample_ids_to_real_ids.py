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


def map_internal_sample_ids_to_real_ids(feature_samples_df,
                                        sample_names,
                                        internal_sample_id_col = "Sample_id"):
    """
    Add real sample IDs to a {feat_id}.csv table.

    The original Sample_id column is an internal integer index.
    """

    if internal_sample_id_col not in feature_samples_df.columns:
        raise ValueError("internal_sample_id_col was not found: "
                         + str(internal_sample_id_col))

    feature_samples_df = feature_samples_df.copy()

    internal_sample_id_vec = pd.to_numeric(feature_samples_df[internal_sample_id_col],
                                           errors = "coerce")

    feature_samples_df["internal_sample_id"] = internal_sample_id_vec.astype("Int64")

    sample_id_map = {sample_id: sample_name
                     for sample_id, sample_name in enumerate(sample_names)}

    feature_samples_df["actual_sample_id"] = feature_samples_df["internal_sample_id"].map(sample_id_map)

    missing_map_filter = feature_samples_df["actual_sample_id"].isna()

    if missing_map_filter.any():
        missing_ids = feature_samples_df.loc[missing_map_filter,
                                             "internal_sample_id"].dropna().unique()

        raise ValueError("Some internal Sample_id values were not found in the sample map: "
                         + str(list(missing_ids))
                         + "\nNumber of sample names available: "
                         + str(len(sample_names)))

    return feature_samples_df
