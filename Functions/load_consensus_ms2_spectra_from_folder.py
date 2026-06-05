from __future__ import annotations

from pathlib import Path
import os
import re
import numpy as np
import pandas as pd
from scipy.sparse import coo_matrix, csr_matrix
from get_consensus_spectrum_paths import *
from read_consensus_ms2_spectrum import *

def load_consensus_ms2_spectra_from_folder(consensus_spectra_folder,
                                           selected_feat_ids = None,
                                           file_name_template = "Consensus_ms2-spectra_{feat_id}.csv",
                                           mz_col = "median_mz(Da)",
                                           intensity_col = "median_Int",
                                           mz_std_col = "IQR_mz(Da)",
                                           mz_iqr_ppm_col = "IQR_mz(ppm)",
                                           drop_nonpositive_intensity = True,
                                           normalization = "l2",
                                           continue_on_error = True):
    """
    Load consensus MS2 spectra directly from a folder.

    This is the input-loading layer for the centroid-assignment pathway. It
    does not require a features table.
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
                                                                normalization = normalization)

            if len(consensus_spectrum_df) == 0:
                raise ValueError("Consensus spectrum has no positive fragments after filtering.")

            loaded_spectra.append(consensus_spectrum_df)

            summary_rows.append({"feat_id": feat_id,
                                 "spectrum_id": spectrum_id,
                                 "status": "ok",
                                 "n_fragments": len(consensus_spectrum_df),
                                 "consensus_spectrum_file": str(consensus_spectrum_path),
                                 "error_message": ""})

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
