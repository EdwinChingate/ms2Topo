from __future__ import annotations

from pathlib import Path
import os
import re
import numpy as np
import pandas as pd
from scipy.sparse import coo_matrix, csr_matrix

def build_centroid_diagnostic_df(loss_assignment_df,
                                 centroid_df):
    """
    Summarize how each neutral-loss centroid behaved after assignment.
    """

    if loss_assignment_df is None or len(loss_assignment_df) == 0:
        centroid_diagnostic_df = centroid_df.copy()
        centroid_diagnostic_df["n_assigned_losses"] = 0
        centroid_diagnostic_df["n_spectra_present"] = 0
        return centroid_diagnostic_df

    assigned_df = loss_assignment_df[loss_assignment_df["assigned_loss_id"] >= 0].copy()

    if len(assigned_df) == 0:
        centroid_diagnostic_df = centroid_df.copy()
        centroid_diagnostic_df["n_assigned_losses"] = 0
        centroid_diagnostic_df["n_spectra_present"] = 0
        return centroid_diagnostic_df

    grouped = assigned_df.groupby("assigned_loss_id")

    diagnostic_df = grouped.agg(n_assigned_losses = ("neutral_loss_mz", "size"),
                                n_confident_losses = ("assignment_status", lambda x: int(np.sum(np.asarray(x) == 2))),
                                n_ambiguous_losses = ("assignment_status", lambda x: int(np.sum(np.asarray(x) == 1))),
                                n_spectra_present = ("spectrum_id", "nunique"),
                                assigned_intensity_sum = ("neutral_loss_intensity", "sum"),
                                observed_loss_mz_mean = ("neutral_loss_mz", "mean"),
                                observed_loss_mz_std = ("neutral_loss_mz", "std"),
                                residual_mean = ("mz_residual", "mean"),
                                residual_std = ("mz_residual", "std"),
                                residual_abs_median = ("mz_residual", lambda x: float(np.nanmedian(np.abs(x)))),
                                posterior_mean = ("assignment_posterior", "mean"),
                                posterior_min = ("assignment_posterior", "min")).reset_index()

    centroid_diagnostic_df = centroid_df.merge(diagnostic_df,
                                               left_on = "aligned_loss_id",
                                               right_on = "assigned_loss_id",
                                               how = "left")

    fill_zero_cols = ["n_assigned_losses", "n_confident_losses", "n_ambiguous_losses",
                      "n_spectra_present", "assigned_intensity_sum"]

    for col in fill_zero_cols:
        if col in centroid_diagnostic_df.columns:
            centroid_diagnostic_df[col] = centroid_diagnostic_df[col].fillna(0)

    centroid_diagnostic_df["empirical_residual_std_to_centroid_sigma"] = (
        centroid_diagnostic_df["residual_std"] / centroid_diagnostic_df["centroid_sigma"]
    )

    return centroid_diagnostic_df
