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


def read_original_consensus_spectrum(consensus_spectra_folder,
                                     feat_id,
                                     mz_col = "median_mz(Da)",
                                     intensity_col = "median_Int",
                                     min_fragment_intensity = 0.0):
    """
    Read the original Consensus_ms2-spectra_{feat_id}.csv table.
    """

    feat_id_clean = clean_feature_or_sample_id(feat_id)

    consensus_spectrum_path = (
        Path(consensus_spectra_folder) /
        ("Consensus_ms2-spectra_" + feat_id_clean + ".csv")
    )

    if not consensus_spectrum_path.exists():
        raise FileNotFoundError("Consensus spectrum was not found: "
                                + str(consensus_spectrum_path))

    consensus_df = pd.read_csv(consensus_spectrum_path)

    unnamed_cols = [col for col in consensus_df.columns
                    if str(col).startswith("Unnamed")]

    if len(unnamed_cols) > 0:
        consensus_df = consensus_df.drop(columns = unnamed_cols)

    if mz_col not in consensus_df.columns:
        raise ValueError("mz_col was not found: " + str(mz_col))

    if intensity_col not in consensus_df.columns:
        raise ValueError("intensity_col was not found: " + str(intensity_col))

    consensus_df = consensus_df.copy()

    consensus_df[mz_col] = pd.to_numeric(consensus_df[mz_col],
                                         errors = "coerce")

    consensus_df[intensity_col] = pd.to_numeric(consensus_df[intensity_col],
                                                errors = "coerce")

    consensus_df = consensus_df.dropna(subset = [mz_col,
                                                 intensity_col])

    if min_fragment_intensity is not None:
        consensus_df = consensus_df[consensus_df[intensity_col] > min_fragment_intensity].copy()

    consensus_df = consensus_df.sort_values(mz_col).reset_index(drop = True)

    consensus_df.insert(0,
                        "original_fragment_id",
                        np.arange(len(consensus_df),
                                  dtype = int))

    return consensus_df
