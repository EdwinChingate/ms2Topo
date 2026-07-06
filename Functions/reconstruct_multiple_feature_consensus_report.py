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
from make_selected_aligned_spectra_wide_df import make_selected_aligned_spectra_wide_df
from reconstruct_feature_consensus_report import reconstruct_feature_consensus_report


def reconstruct_multiple_feature_consensus_report(aligned_intensity_df,
                                                  consensus_spectra_folder,
                                                  feat_id_list,
                                                  aligned_mz_df = None,
                                                  aligned_features_df = None,
                                                  sample_names = None,
                                                  mz_col = "median_mz(Da)",
                                                  intensity_col = "median_Int",
                                                  min_fragment_intensity = 0.0,
                                                  sample_id_col = "Sample_id",
                                                  feat_id_col = "feat_id",
                                                  mz_match_tolerance_da = 0.01,
                                                  print_samples = True):
    """
    Run reconstruct_feature_consensus_report for several features.

    Returns:
        feature_reports
        aligned_spectra_long_df
        aligned_spectra_wide_df
        mz_contrast_long_df
        feature_samples_long_df
        feature_summary_df
    """

    feature_reports = {}

    aligned_spectra_tables = []
    mz_contrast_tables = []
    feature_samples_tables = []
    feature_summary_rows = []

    for current_feat_id in feat_id_list:

        current_feat_id_clean = clean_feature_or_sample_id(current_feat_id)

        current_report = reconstruct_feature_consensus_report(
            aligned_intensity_df = aligned_intensity_df,
            aligned_mz_df = aligned_mz_df,
            aligned_features_df = aligned_features_df,
            sample_names = sample_names,
            consensus_spectra_folder = consensus_spectra_folder,
            feat_id = current_feat_id,
            mz_col = mz_col,
            intensity_col = intensity_col,
            min_fragment_intensity = min_fragment_intensity,
            sample_id_col = sample_id_col,
            feat_id_col = feat_id_col,
            mz_match_tolerance_da = mz_match_tolerance_da,
            print_samples = print_samples
        )

        feature_reports[current_feat_id_clean] = current_report

        aligned_spectrum_df = current_report["aligned_spectrum_df"].copy()
        mz_contrast_df = current_report["mz_contrast_df"].copy()
        feature_samples_df = current_report["feature_samples_df"].copy()
        original_consensus_spectrum_df = current_report["original_consensus_spectrum_df"].copy()

        actual_sample_ids = feature_samples_df["actual_sample_id"].dropna().unique().tolist()
        actual_sample_ids = [str(sample_id) for sample_id in actual_sample_ids]

        aligned_spectrum_df.insert(0,
                                   "feat_id",
                                   current_feat_id_clean)

        aligned_spectrum_df["n_samples_containing_feature"] = len(actual_sample_ids)
        aligned_spectrum_df["actual_sample_ids"] = ";".join(actual_sample_ids)

        mz_contrast_df.insert(0,
                              "feat_id",
                              current_feat_id_clean)

        feature_samples_df.insert(0,
                                  "feat_id",
                                  current_feat_id_clean)

        aligned_spectra_tables.append(aligned_spectrum_df)
        mz_contrast_tables.append(mz_contrast_df)
        feature_samples_tables.append(feature_samples_df)

        feature_summary_rows.append({
            "feat_id": current_feat_id_clean,
            "n_samples_containing_feature": len(actual_sample_ids),
            "actual_sample_ids": ";".join(actual_sample_ids),
            "n_original_positive_intensity_fragments": len(original_consensus_spectrum_df),
            "n_aligned_nonzero_fragments": len(aligned_spectrum_df),
            "n_original_fragments_matched_to_aligned_rows": int(mz_contrast_df["aligned_fragment_id"].notna().sum()),
            "n_original_fragments_without_aligned_match": int(mz_contrast_df["aligned_fragment_id"].isna().sum())
        })

    if len(aligned_spectra_tables) > 0:
        aligned_spectra_long_df = pd.concat(aligned_spectra_tables,
                                            axis = 0,
                                            ignore_index = True)

    else:
        aligned_spectra_long_df = pd.DataFrame()

    if len(mz_contrast_tables) > 0:
        mz_contrast_long_df = pd.concat(mz_contrast_tables,
                                        axis = 0,
                                        ignore_index = True)

    else:
        mz_contrast_long_df = pd.DataFrame()

    if len(feature_samples_tables) > 0:
        feature_samples_long_df = pd.concat(feature_samples_tables,
                                            axis = 0,
                                            ignore_index = True)

    else:
        feature_samples_long_df = pd.DataFrame()

    feature_summary_df = pd.DataFrame(feature_summary_rows)

    aligned_spectra_wide_df = make_selected_aligned_spectra_wide_df(
        aligned_spectra_long_df = aligned_spectra_long_df
    )

    return {"feature_reports": feature_reports,
            "aligned_spectra_long_df": aligned_spectra_long_df,
            "aligned_spectra_wide_df": aligned_spectra_wide_df,
            "mz_contrast_long_df": mz_contrast_long_df,
            "feature_samples_long_df": feature_samples_long_df,
            "feature_summary_df": feature_summary_df}
