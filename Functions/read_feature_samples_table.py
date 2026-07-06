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
from get_sample_names_from_aligned_features_df import get_sample_names_from_aligned_features_df
from map_internal_sample_ids_to_real_ids import map_internal_sample_ids_to_real_ids


def read_feature_samples_table(consensus_spectra_folder,
                               feat_id,
                               aligned_features_df = None,
                               sample_names = None,
                               sample_id_col = "Sample_id",
                               feat_id_col = "feat_id"):
    """
    Read {feat_id}.csv and add actual sample IDs.

    Provide either:
        aligned_features_df
    or:
        sample_names

    aligned_features_df is preferred because it uses the same sample columns
    shown in your ms2Topo feature table.
    """

    feat_id_clean = clean_feature_or_sample_id(feat_id)

    feature_table_path = Path(consensus_spectra_folder) / (feat_id_clean + ".csv")

    if not feature_table_path.exists():
        raise FileNotFoundError("Feature sample table was not found: "
                                + str(feature_table_path))

    feature_samples_df = pd.read_csv(feature_table_path)

    unnamed_cols = [col for col in feature_samples_df.columns
                    if str(col).startswith("Unnamed")]

    if len(unnamed_cols) > 0:
        feature_samples_df = feature_samples_df.drop(columns = unnamed_cols)

    if sample_names is None:
        if aligned_features_df is None:
            raise ValueError("Provide either aligned_features_df or sample_names "
                             "to translate internal Sample_id values.")

        sample_names = get_sample_names_from_aligned_features_df(aligned_features_df = aligned_features_df,
                                                                 feat_id_col = feat_id_col)

    feature_samples_df = map_internal_sample_ids_to_real_ids(feature_samples_df = feature_samples_df,
                                                             sample_names = sample_names,
                                                             internal_sample_id_col = sample_id_col)

    return feature_samples_df
