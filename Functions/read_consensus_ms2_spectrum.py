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
from clean_feat_id import clean_feat_id
from normalize_intensity_vector import normalize_intensity_vector


def read_consensus_ms2_spectrum(consensus_spectrum_path,
                                feat_id,
                                spectrum_id,
                                mz_col = "median_mz(Da)",
                                intensity_col = "median_Int",
                                mz_std_col = "IQR_mz(Da)",
                                mz_iqr_ppm_col = "IQR_mz(ppm)",
                                drop_nonpositive_intensity = True,
                                min_fragment_intensity = 0.0,
                                normalization = "l2"):
    """
    Read one saved ms2Topo consensus spectrum and prepare it for centroid
    assignment.

    The first processing filter removes fragments with missing m/z, missing
    intensity, or intensity below the requested positive-intensity threshold.

    By default, only fragments with median_Int > 0 are kept. This means that
    downstream assignment statistics refer to the consensus fragments that have
    non-zero median intensity and were actually tested against the centroid
    vocabulary.

    The returned table is not an alignment result. It is one loaded consensus
    spectrum with provenance columns added. Per-file filtering statistics are
    also attached to the returned DataFrame through .attrs["filter_stats"].
    """

    consensus_spectrum_path = Path(consensus_spectrum_path)
    consensus_spectrum_df = pd.read_csv(consensus_spectrum_path)

    unnamed_cols = [col for col in consensus_spectrum_df.columns
                    if str(col).startswith("Unnamed")]

    if len(unnamed_cols) > 0:
        consensus_spectrum_df = consensus_spectrum_df.drop(columns = unnamed_cols)

    required_cols = [mz_col,
                     intensity_col]

    for col in required_cols:
        if col not in consensus_spectrum_df.columns:
            raise ValueError(f"Column '{col}' was not found in {consensus_spectrum_path}. "
                             f"Available columns: {list(consensus_spectrum_df.columns)}")

    consensus_spectrum_df = consensus_spectrum_df.copy()

    n_raw_fragment_rows = int(len(consensus_spectrum_df))

    consensus_spectrum_df[mz_col] = pd.to_numeric(consensus_spectrum_df[mz_col],
                                                  errors = "coerce")

    consensus_spectrum_df[intensity_col] = pd.to_numeric(consensus_spectrum_df[intensity_col],
                                                         errors = "coerce")

    mz_is_valid = np.isfinite(consensus_spectrum_df[mz_col].to_numpy(dtype = float))
    intensity_is_valid = np.isfinite(consensus_spectrum_df[intensity_col].to_numpy(dtype = float))
    numeric_filter = mz_is_valid & intensity_is_valid

    n_missing_mz_fragments = int((~mz_is_valid).sum())
    n_missing_intensity_fragments = int((~intensity_is_valid).sum())
    n_fragments_after_numeric_filter = int(numeric_filter.sum())

    consensus_spectrum_df = consensus_spectrum_df.loc[numeric_filter].copy()

    if min_fragment_intensity is None:
        if drop_nonpositive_intensity:
            intensity_threshold = 0.0
        else:
            intensity_threshold = None
    else:
        intensity_threshold = float(min_fragment_intensity)

    if intensity_threshold is not None:
        intensity_value_vec = consensus_spectrum_df[intensity_col].to_numpy(dtype = float)
        intensity_keep_filter = intensity_value_vec > intensity_threshold
        n_fragments_filtered_by_intensity = int((~intensity_keep_filter).sum())
        n_nonpositive_intensity_fragments = int((intensity_value_vec <= 0).sum())
        consensus_spectrum_df = consensus_spectrum_df.loc[intensity_keep_filter].copy()

    else:
        n_fragments_filtered_by_intensity = 0
        n_nonpositive_intensity_fragments = int((consensus_spectrum_df[intensity_col].to_numpy(dtype = float) <= 0).sum())

    n_fragments_after_intensity_filter = int(len(consensus_spectrum_df))

    filter_stats = {"feat_id": clean_feat_id(feat_id),
                    "spectrum_id": int(spectrum_id),
                    "n_raw_fragment_rows": n_raw_fragment_rows,
                    "n_missing_mz_fragments": n_missing_mz_fragments,
                    "n_missing_intensity_fragments": n_missing_intensity_fragments,
                    "n_fragments_after_numeric_filter": n_fragments_after_numeric_filter,
                    "intensity_threshold": intensity_threshold,
                    "n_nonpositive_intensity_fragments": n_nonpositive_intensity_fragments,
                    "n_fragments_filtered_by_intensity": n_fragments_filtered_by_intensity,
                    "n_fragments_after_intensity_filter": n_fragments_after_intensity_filter,
                    "n_loaded_positive_intensity_fragments": n_fragments_after_intensity_filter}

    if len(consensus_spectrum_df) == 0:
        consensus_spectrum_df.attrs["filter_stats"] = filter_stats
        return consensus_spectrum_df

    consensus_spectrum_df["raw_fragment_intensity"] = consensus_spectrum_df[intensity_col].to_numpy(dtype = float)

    consensus_spectrum_df = normalize_intensity_vector(spectrum_df = consensus_spectrum_df,
                                                       intensity_col = intensity_col,
                                                       normalization = normalization)

    if mz_std_col not in consensus_spectrum_df.columns:
        if mz_iqr_ppm_col not in consensus_spectrum_df.columns:
            raise ValueError(f"Neither '{mz_std_col}' nor '{mz_iqr_ppm_col}' was found in "
                             f"{consensus_spectrum_path}.")

        consensus_spectrum_df[mz_iqr_ppm_col] = pd.to_numeric(consensus_spectrum_df[mz_iqr_ppm_col],
                                                              errors = "coerce")

        consensus_spectrum_df[mz_std_col] = (consensus_spectrum_df[mz_iqr_ppm_col] / 1e6 *
                                             consensus_spectrum_df[mz_col])

    consensus_spectrum_df[mz_std_col] = pd.to_numeric(consensus_spectrum_df[mz_std_col],
                                                      errors = "coerce")

    n_before_mz_std_filter = len(consensus_spectrum_df)
    consensus_spectrum_df = consensus_spectrum_df.dropna(subset = [mz_std_col])
    n_fragments_filtered_by_mz_std = int(n_before_mz_std_filter - len(consensus_spectrum_df))

    filter_stats["n_fragments_filtered_by_mz_std"] = n_fragments_filtered_by_mz_std
    filter_stats["n_loaded_fragments"] = int(len(consensus_spectrum_df))
    filter_stats["n_loaded_positive_intensity_fragments"] = int(len(consensus_spectrum_df))

    consensus_spectrum_df = consensus_spectrum_df.sort_values(mz_col).reset_index(drop = True)

    consensus_spectrum_df["fragment_id_in_spectrum"] = np.arange(len(consensus_spectrum_df),
                                                                 dtype = int)
    consensus_spectrum_df["feat_id"] = clean_feat_id(feat_id)
    consensus_spectrum_df["spectrum_id"] = int(spectrum_id)
    consensus_spectrum_df["consensus_spectrum_file"] = str(consensus_spectrum_path)

    consensus_spectrum_df.attrs["filter_stats"] = filter_stats

    return consensus_spectrum_df
