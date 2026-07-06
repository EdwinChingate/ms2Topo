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


def summarize_fragment_assignments(fragment_assignment_df,
                                   feature_id_map_df):
    """
    Summarize assignment coverage per consensus spectrum.

    assigned_fraction_int is the fraction of loaded positive-intensity
    consensus-fragment intensity that was assigned to any learned centroid.
    """

    if fragment_assignment_df is None or len(fragment_assignment_df) == 0:
        return pd.DataFrame()

    summary_rows = []

    score_col = "assignment_score" if "assignment_score" in fragment_assignment_df.columns else "assignment_posterior"

    for spectrum_id, spectrum_df in fragment_assignment_df.groupby("spectrum_id"):

        total_intensity = spectrum_df["fragment_intensity"].sum()

        assigned_filter = spectrum_df["assignment_status"] > 0
        confident_filter = spectrum_df["assignment_status"] == 2
        ambiguous_filter = spectrum_df["assignment_status"] == 1
        unassigned_filter = spectrum_df["assignment_status"] == 0
        no_candidate_filter = spectrum_df["n_candidate_fragments"] == 0

        assigned_intensity = spectrum_df.loc[assigned_filter, "fragment_intensity"].sum()
        confident_intensity = spectrum_df.loc[confident_filter, "fragment_intensity"].sum()
        ambiguous_intensity = spectrum_df.loc[ambiguous_filter, "fragment_intensity"].sum()
        unassigned_intensity = spectrum_df.loc[unassigned_filter, "fragment_intensity"].sum()

        if total_intensity > 0:
            assigned_fraction_int = assigned_intensity / total_intensity
            confident_fraction_int = confident_intensity / total_intensity
            ambiguous_fraction_int = ambiguous_intensity / total_intensity
            unassigned_fraction_int = unassigned_intensity / total_intensity

        else:
            assigned_fraction_int = np.nan
            confident_fraction_int = np.nan
            ambiguous_fraction_int = np.nan
            unassigned_fraction_int = np.nan

        assigned_scores = spectrum_df.loc[assigned_filter, score_col]

        feat_id = feature_id_map_df.loc[feature_id_map_df["spectrum_id"] == spectrum_id,
                                        "feat_id"]

        if len(feat_id) > 0:
            feat_id = feat_id.iloc[0]

        else:
            feat_id = np.nan

        summary_rows.append({"spectrum_id": int(spectrum_id),
                             "feat_id": feat_id,
                             "n_loaded_positive_intensity_fragments": int(len(spectrum_df)),
                             "n_fragments": int(len(spectrum_df)),
                             "n_assigned_fragments": int(assigned_filter.sum()),
                             "n_confident_fragments": int(confident_filter.sum()),
                             "n_ambiguous_fragments": int(ambiguous_filter.sum()),
                             "n_unassigned_fragments": int(unassigned_filter.sum()),
                             "n_no_candidate_fragments": int(no_candidate_filter.sum()),
                             "all_positive_intensity_fragments_assigned": bool(unassigned_filter.sum() == 0),
                             "total_intensity": float(total_intensity),
                             "assigned_intensity": float(assigned_intensity),
                             "confident_intensity": float(confident_intensity),
                             "ambiguous_intensity": float(ambiguous_intensity),
                             "unassigned_intensity": float(unassigned_intensity),
                             "assigned_fraction_int": float(assigned_fraction_int),
                             "confident_fraction_int": float(confident_fraction_int),
                             "ambiguous_fraction_int": float(ambiguous_fraction_int),
                             "unassigned_fraction_int": float(unassigned_fraction_int),
                             "mean_assignment_score": float(assigned_scores.mean()) if len(assigned_scores) > 0 else np.nan,
                             "median_assignment_score": float(assigned_scores.median()) if len(assigned_scores) > 0 else np.nan,
                             "mean_assignment_posterior": float(assigned_scores.mean()) if len(assigned_scores) > 0 else np.nan,
                             "median_assignment_posterior": float(assigned_scores.median()) if len(assigned_scores) > 0 else np.nan,
                             "mean_n_candidate_fragments": float(spectrum_df["n_candidate_fragments"].mean())})

    assignment_summary_df = pd.DataFrame(summary_rows)
    assignment_summary_df = assignment_summary_df.sort_values("spectrum_id").reset_index(drop = True)

    return assignment_summary_df
