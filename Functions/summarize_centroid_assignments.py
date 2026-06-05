from __future__ import annotations

from pathlib import Path
import os
import re
import numpy as np
import pandas as pd
from scipy.sparse import coo_matrix, csr_matrix

def summarize_centroid_assignments(fragment_assignment_df,
                                   centroid_df):
    """
    Summarize how the learned GMM centroids behave after assignment.

    This is the centroid-level diagnostic table. It is useful for checking
    whether a GMM centroid behaves as a tight recurrent motif, an ambiguous
    overlap region, or a mostly unused component.
    """

    centroid_diagnostic_df = centroid_df.copy()

    default_cols = {"n_assigned_fragments": 0,
                    "n_confident_fragments": 0,
                    "n_ambiguous_fragments": 0,
                    "n_spectra_present": 0,
                    "assigned_intensity_sum": 0.0,
                    "observed_mz_mean": np.nan,
                    "observed_mz_std": np.nan,
                    "residual_mean": np.nan,
                    "residual_std": np.nan,
                    "residual_abs_median": np.nan,
                    "posterior_mean": np.nan,
                    "posterior_min": np.nan,
                    "posterior_median": np.nan}

    if fragment_assignment_df is None or len(fragment_assignment_df) == 0:
        for col, value in default_cols.items():
            centroid_diagnostic_df[col] = value

        centroid_diagnostic_df["empirical_residual_std_to_centroid_sigma"] = np.nan
        return centroid_diagnostic_df

    assigned_df = fragment_assignment_df[fragment_assignment_df["assignment_status"] > 0].copy()

    if len(assigned_df) == 0:
        for col, value in default_cols.items():
            centroid_diagnostic_df[col] = value

        centroid_diagnostic_df["empirical_residual_std_to_centroid_sigma"] = np.nan
        return centroid_diagnostic_df

    grouped = assigned_df.groupby("assigned_fragment_id")

    n_assigned = grouped.size().rename("n_assigned_fragments")
    n_confident = grouped.apply(lambda df: int((df["assignment_status"] == 2).sum())).rename("n_confident_fragments")
    n_ambiguous = grouped.apply(lambda df: int((df["assignment_status"] == 1).sum())).rename("n_ambiguous_fragments")
    n_spectra = grouped["spectrum_id"].nunique().rename("n_spectra_present")
    intensity_sum = grouped["fragment_intensity"].sum().rename("assigned_intensity_sum")
    observed_mz_mean = grouped["fragment_mz"].mean().rename("observed_mz_mean")
    observed_mz_std = grouped["fragment_mz"].std().rename("observed_mz_std")
    residual_mean = grouped["mz_residual"].mean().rename("residual_mean")
    residual_std = grouped["mz_residual"].std().rename("residual_std")
    residual_abs_median = grouped["mz_residual"].apply(lambda values: np.nanmedian(np.abs(values))).rename("residual_abs_median")
    posterior_mean = grouped["assignment_posterior"].mean().rename("posterior_mean")
    posterior_min = grouped["assignment_posterior"].min().rename("posterior_min")
    posterior_median = grouped["assignment_posterior"].median().rename("posterior_median")

    summary_df = pd.concat([n_assigned,
                            n_confident,
                            n_ambiguous,
                            n_spectra,
                            intensity_sum,
                            observed_mz_mean,
                            observed_mz_std,
                            residual_mean,
                            residual_std,
                            residual_abs_median,
                            posterior_mean,
                            posterior_min,
                            posterior_median],
                           axis = 1).reset_index()

    summary_df = summary_df.rename(columns = {"assigned_fragment_id": "aligned_fragment_id"})

    centroid_diagnostic_df = centroid_diagnostic_df.merge(summary_df,
                                                          on = "aligned_fragment_id",
                                                          how = "left")

    fill_zero_cols = ["n_assigned_fragments",
                      "n_confident_fragments",
                      "n_ambiguous_fragments",
                      "n_spectra_present",
                      "assigned_intensity_sum"]

    for col in fill_zero_cols:
        centroid_diagnostic_df[col] = centroid_diagnostic_df[col].fillna(0)

    centroid_diagnostic_df["empirical_residual_std_to_centroid_sigma"] = (centroid_diagnostic_df["residual_std"] /
                                                                          centroid_diagnostic_df["centroid_sigma"])

    return centroid_diagnostic_df
