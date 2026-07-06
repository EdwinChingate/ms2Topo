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
from find_feature_column import find_feature_column


def reconstruct_consensus_spectrum_from_aligned_df(aligned_intensity_df,
                                                   feat_id,
                                                   aligned_mz_df = None,
                                                   mz_col = "aligned_fragment_mz",
                                                   drop_zero_intensity = True,
                                                   sort_by_mz = True):
    """
    Reconstruct one aligned consensus spectrum from the wide aligned table.

    If aligned_mz_df is provided, the returned table also includes the
    representative observed m/z stored during alignment.
    """

    if mz_col not in aligned_intensity_df.columns:
        raise ValueError("mz_col was not found in aligned_intensity_df: "
                         + str(mz_col))

    feature_col = find_feature_column(aligned_df = aligned_intensity_df,
                                      feat_id = feat_id)

    aligned_spectrum_df = pd.DataFrame({
        "aligned_fragment_id": aligned_intensity_df.index,
        "aligned_fragment_mz": pd.to_numeric(aligned_intensity_df[mz_col],
                                             errors = "coerce"),
        "aligned_intensity": pd.to_numeric(aligned_intensity_df[feature_col],
                                           errors = "coerce")
    })

    if aligned_mz_df is not None:

        if mz_col not in aligned_mz_df.columns:
            raise ValueError("mz_col was not found in aligned_mz_df: "
                             + str(mz_col))

        aligned_mz_feature_col = find_feature_column(aligned_df = aligned_mz_df,
                                                     feat_id = feat_id)

        aligned_spectrum_df["representative_observed_mz"] = pd.to_numeric(
            aligned_mz_df[aligned_mz_feature_col],
            errors = "coerce"
        )

    aligned_spectrum_df = aligned_spectrum_df.dropna(subset = ["aligned_fragment_mz",
                                                               "aligned_intensity"])

    if drop_zero_intensity:
        aligned_spectrum_df = aligned_spectrum_df[aligned_spectrum_df["aligned_intensity"] > 0].copy()

    if sort_by_mz:
        aligned_spectrum_df = aligned_spectrum_df.sort_values("aligned_fragment_mz").reset_index(drop = True)

    return aligned_spectrum_df
