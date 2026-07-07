# Extracted from notebook: 713031fb-407a-42c5-b338-3c1aba9bdf96.ipynb
# One unique top-level function per file. Auto-generated from top-level function definitions.
from __future__ import annotations
import numpy as np
import pandas as pd


def summarize_resampled_gmm_search(gmm_resampling_rows,
                                   std_times = 1):
    """
    Summarize BIC/AIC curves across resampled GMM searches.

    BIC is minimized. The selected model is the smallest n_components whose
    lower BIC uncertainty band overlaps the best model's upper BIC uncertainty
    band. This is the BIC-direction analog of choosing the smallest plausible k
    from the resampled spectral-clustering silhouette workflow.
    """

    gmm_resampling_df = pd.DataFrame(gmm_resampling_rows)

    if len(gmm_resampling_df) == 0:
        raise ValueError("gmm_resampling_rows is empty.")

    summary_df = (gmm_resampling_df
                  .groupby("n_components")
                  .agg(mean_BIC = ("BIC", "mean"),
                       std_BIC = ("BIC", "std"),
                       median_BIC = ("BIC", "median"),
                       mean_AIC = ("AIC", "mean"),
                       std_AIC = ("AIC", "std"),
                       median_AIC = ("AIC", "median"),
                       n_evaluations = ("BIC", "count"),
                       n_selected_by_iteration = ("selected_in_iteration", "sum"))
                  .reset_index())

    summary_df["std_BIC"] = summary_df["std_BIC"].fillna(0.0)
    summary_df["std_AIC"] = summary_df["std_AIC"].fillna(0.0)

    best_row_id = int(summary_df["mean_BIC"].idxmin())

    best_mean_BIC = float(summary_df.loc[best_row_id,
                                         "mean_BIC"])

    best_std_BIC = float(summary_df.loc[best_row_id,
                                        "std_BIC"])

    upper_best_BIC = best_mean_BIC + std_times * best_std_BIC

    summary_df["lower_BIC"] = summary_df["mean_BIC"] - std_times * summary_df["std_BIC"]
    summary_df["upper_BIC"] = summary_df["mean_BIC"] + std_times * summary_df["std_BIC"]

    summary_df["plausible_by_BIC"] = summary_df["lower_BIC"] <= upper_best_BIC

    plausible_components = summary_df.loc[summary_df["plausible_by_BIC"],
                                          "n_components"].to_numpy(dtype = int)

    selected_n_components = int(np.min(plausible_components))

    summary_df["selected_n_components"] = selected_n_components

    return {"gmm_resampling_summary_df": summary_df,
            "selected_n_components": selected_n_components}
