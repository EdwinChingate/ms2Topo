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


def contrast_original_and_aligned_mz(original_consensus_spectrum_df,
                                     aligned_spectrum_df,
                                     original_mz_col = "median_mz(Da)",
                                     original_intensity_col = "median_Int",
                                     mz_match_tolerance_da = 0.01):
    """
    Contrast original consensus m/z values with aligned centroid m/z values.

    If representative_observed_mz exists, matching is done against that column.
    Otherwise matching is done against aligned_fragment_mz.
    """

    original_df = original_consensus_spectrum_df.copy()
    aligned_df = aligned_spectrum_df.copy()

    if "representative_observed_mz" in aligned_df.columns:
        aligned_match_col = "representative_observed_mz"
    else:
        aligned_match_col = "aligned_fragment_mz"

    original_df = original_df.sort_values(original_mz_col).reset_index(drop = True)
    aligned_df = aligned_df.sort_values(aligned_match_col).reset_index(drop = True)

    contrast_df = pd.merge_asof(left = original_df,
                                right = aligned_df,
                                left_on = original_mz_col,
                                right_on = aligned_match_col,
                                direction = "nearest",
                                tolerance = mz_match_tolerance_da)

    contrast_df = contrast_df.rename(columns = {original_mz_col: "original_consensus_mz",
                                                original_intensity_col: "original_consensus_intensity"})

    contrast_df["delta_original_to_aligned_centroid_da"] = (
        contrast_df["original_consensus_mz"] -
        contrast_df["aligned_fragment_mz"]
    )

    if "representative_observed_mz" in contrast_df.columns:
        contrast_df["delta_original_to_representative_observed_da"] = (
            contrast_df["original_consensus_mz"] -
            contrast_df["representative_observed_mz"]
        )

    selected_cols = ["original_fragment_id",
                     "original_consensus_mz",
                     "original_consensus_intensity",
                     "aligned_fragment_id",
                     "aligned_fragment_mz",
                     "aligned_intensity"]

    if "representative_observed_mz" in contrast_df.columns:
        selected_cols.append("representative_observed_mz")

    selected_cols += ["delta_original_to_aligned_centroid_da"]

    if "delta_original_to_representative_observed_da" in contrast_df.columns:
        selected_cols.append("delta_original_to_representative_observed_da")

    selected_cols = [col for col in selected_cols
                     if col in contrast_df.columns]

    return contrast_df[selected_cols]
