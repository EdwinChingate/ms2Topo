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
from get_consensus_spectrum_paths import get_consensus_spectrum_paths
from read_consensus_ms2_spectrum import read_consensus_ms2_spectrum


def load_consensus_ms2_spectra_from_folder(consensus_spectra_folder,
                                           selected_feat_ids = None,
                                           file_name_template = "Consensus_ms2-spectra_{feat_id}.csv",
                                           mz_col = "median_mz(Da)",
                                           intensity_col = "median_Int",
                                           mz_std_col = "IQR_mz(Da)",
                                           mz_iqr_ppm_col = "IQR_mz(ppm)",
                                           drop_nonpositive_intensity = True,
                                           min_fragment_intensity = 0.0,
                                           normalization = "l2",
                                           continue_on_error = True):
    """
    Load consensus MS2 spectra directly from a folder.

    This is the input-loading layer for the centroid-assignment pathway. It
    does not require a features table.

    The returned summary_df now reports how many raw consensus fragments were
    read, how many were removed by missing-value/intensity filters, and how
    many positive-intensity fragments were passed to centroid assignment.
    """

    spectrum_rows = get_consensus_spectrum_paths(consensus_spectra_folder = consensus_spectra_folder,
                                                 selected_feat_ids = selected_feat_ids,
                                                 file_name_template = file_name_template)

    loaded_spectra = []
    summary_rows = []
    feature_id_rows = []
    spectrum_id = 0

    for spectrum_row in spectrum_rows:

        feat_id = spectrum_row["feat_id"]
        consensus_spectrum_path = spectrum_row["consensus_spectrum_path"]

        try:
            consensus_spectrum_df = read_consensus_ms2_spectrum(consensus_spectrum_path = consensus_spectrum_path,
                                                                feat_id = feat_id,
                                                                spectrum_id = spectrum_id,
                                                                mz_col = mz_col,
                                                                intensity_col = intensity_col,
                                                                mz_std_col = mz_std_col,
                                                                mz_iqr_ppm_col = mz_iqr_ppm_col,
                                                                drop_nonpositive_intensity = drop_nonpositive_intensity,
                                                                min_fragment_intensity = min_fragment_intensity,
                                                                normalization = normalization)

            filter_stats = consensus_spectrum_df.attrs.get("filter_stats", {})

            summary_row = {"feat_id": feat_id,
                           "spectrum_id": spectrum_id if len(consensus_spectrum_df) > 0 else np.nan,
                           "status": "ok" if len(consensus_spectrum_df) > 0 else "empty_after_filter",
                           "n_fragments": len(consensus_spectrum_df),
                           "consensus_spectrum_file": str(consensus_spectrum_path),
                           "error_message": ""}

            summary_row.update(filter_stats)
            summary_rows.append(summary_row)

            if len(consensus_spectrum_df) == 0:
                continue

            loaded_spectra.append(consensus_spectrum_df)

            feature_id_rows.append({"spectrum_id": spectrum_id,
                                    "feat_id": feat_id,
                                    "consensus_spectrum_file": str(consensus_spectrum_path)})

            spectrum_id += 1

        except Exception as error:
            summary_rows.append({"feat_id": feat_id,
                                 "spectrum_id": np.nan,
                                 "status": "failed",
                                 "n_fragments": 0,
                                 "consensus_spectrum_file": str(consensus_spectrum_path),
                                 "error_message": str(error)})

            if not continue_on_error:
                raise

    if len(loaded_spectra) > 0:
        loaded_consensus_fragments_df = pd.concat(loaded_spectra,
                                                  axis = 0,
                                                  ignore_index = True)

    else:
        loaded_consensus_fragments_df = pd.DataFrame()

    summary_df = pd.DataFrame(summary_rows)
    feature_id_map_df = pd.DataFrame(feature_id_rows)

    return {"loaded_consensus_fragments_df": loaded_consensus_fragments_df,
            "summary_df": summary_df,
            "feature_id_map_df": feature_id_map_df}
