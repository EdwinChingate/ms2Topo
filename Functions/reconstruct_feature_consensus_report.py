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
from contrast_original_and_aligned_mz import contrast_original_and_aligned_mz
from read_feature_samples_table import read_feature_samples_table
from read_original_consensus_spectrum import read_original_consensus_spectrum
from reconstruct_consensus_spectrum_from_aligned_df import reconstruct_consensus_spectrum_from_aligned_df


def reconstruct_feature_consensus_report(aligned_intensity_df,
                                         consensus_spectra_folder,
                                         feat_id,
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
    Reconstruct the aligned consensus spectrum for one feature, read the
    original consensus spectrum, report actual samples containing the feature,
    and return a m/z contrast table.
    """

    feature_samples_df = read_feature_samples_table(consensus_spectra_folder = consensus_spectra_folder,
                                                    feat_id = feat_id,
                                                    aligned_features_df = aligned_features_df,
                                                    sample_names = sample_names,
                                                    sample_id_col = sample_id_col,
                                                    feat_id_col = feat_id_col)

    original_consensus_spectrum_df = read_original_consensus_spectrum(consensus_spectra_folder = consensus_spectra_folder,
                                                                      feat_id = feat_id,
                                                                      mz_col = mz_col,
                                                                      intensity_col = intensity_col,
                                                                      min_fragment_intensity = min_fragment_intensity)

    aligned_spectrum_df = reconstruct_consensus_spectrum_from_aligned_df(aligned_intensity_df = aligned_intensity_df,
                                                                         feat_id = feat_id,
                                                                         aligned_mz_df = aligned_mz_df,
                                                                         mz_col = "aligned_fragment_mz",
                                                                         drop_zero_intensity = True,
                                                                         sort_by_mz = True)

    mz_contrast_df = contrast_original_and_aligned_mz(original_consensus_spectrum_df = original_consensus_spectrum_df,
                                                     aligned_spectrum_df = aligned_spectrum_df,
                                                     original_mz_col = mz_col,
                                                     original_intensity_col = intensity_col,
                                                     mz_match_tolerance_da = mz_match_tolerance_da)

    if print_samples:
        actual_sample_ids = feature_samples_df["actual_sample_id"].dropna().unique().tolist()
        actual_sample_ids = [str(sample_id) for sample_id in actual_sample_ids]

        internal_sample_ids = feature_samples_df["internal_sample_id"].dropna().unique().tolist()

        print("Feature:", clean_feature_or_sample_id(feat_id))
        print("Number of samples containing feature:", len(actual_sample_ids))
        print("Actual sample IDs:", ", ".join(actual_sample_ids))
        print("Internal sample IDs:", ", ".join([str(sample_id) for sample_id in internal_sample_ids]))

        print("Original positive-intensity fragments:", len(original_consensus_spectrum_df))
        print("Aligned nonzero fragments:", len(aligned_spectrum_df))

        n_matched = mz_contrast_df["aligned_fragment_id"].notna().sum()
        print("Original fragments matched back to aligned rows:", int(n_matched))
        print("Original fragments without aligned match:", int(len(mz_contrast_df) - n_matched))

    return {"aligned_spectrum_df": aligned_spectrum_df,
            "original_consensus_spectrum_df": original_consensus_spectrum_df,
            "mz_contrast_df": mz_contrast_df,
            "feature_samples_df": feature_samples_df}
