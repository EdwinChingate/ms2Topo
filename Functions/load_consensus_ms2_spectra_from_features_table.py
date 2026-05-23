from __future__ import annotations

import numpy as np
import pandas as pd
from clean_feat_id import *
from consensus_spectrum_path_from_feat_id import *
from get_feat_ids_from_features_table import *
from read_consensus_ms2_spectrum import *

def load_consensus_ms2_spectra_from_features_table(features_table_df,
                                                   consensus_spectra_folder,
                                                   feat_id_col = "feat_id",
                                                   selected_feat_ids = None,
                                                   file_name_template = "Consensus_ms2-spectra_{feat_id}.csv",
                                                   mz_col = "median_mz(Da)",
                                                   intensity_col = "mean_Int",
                                                   mz_std_col = "IQR_mz(Da)",
                                                   mz_iqr_ppm_col = "IQR_mz(ppm)",
                                                   drop_nonpositive_intensity = True,
                                                   continue_on_error = True):
    """
    Load saved consensus spectra corresponding to feat_id values in a features table.
    """

    if selected_feat_ids is None:
        feat_ids = get_feat_ids_from_features_table(features_table_df = features_table_df,
                                                    feat_id_col = feat_id_col)

    else:
        feat_ids = [clean_feat_id(feat_id) for feat_id in selected_feat_ids
                    if clean_feat_id(feat_id) is not None]

    consensus_spectra = []
    summary_rows = []
    feature_id_rows = []
    spectrum_id = 0

    for feat_id in feat_ids:
        consensus_spectrum_path = consensus_spectrum_path_from_feat_id(consensus_spectra_folder = consensus_spectra_folder,
                                                                       feat_id = feat_id,
                                                                       file_name_template = file_name_template)

        try:
            consensus_spectrum_df = read_consensus_ms2_spectrum(consensus_spectrum_path = consensus_spectrum_path,
                                                                feat_id = feat_id,
                                                                spectrum_id = spectrum_id,
                                                                mz_col = mz_col,
                                                                intensity_col = intensity_col,
                                                                mz_std_col = mz_std_col,
                                                                mz_iqr_ppm_col = mz_iqr_ppm_col,
                                                                drop_nonpositive_intensity = drop_nonpositive_intensity)

            if len(consensus_spectrum_df) == 0:
                raise ValueError("Consensus spectrum has no positive fragments after filtering.")

            consensus_spectra.append(consensus_spectrum_df)

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

    if len(consensus_spectra) > 0:
        all_consensus_ms2_df = pd.concat(consensus_spectra,
                                         axis = 0,
                                         ignore_index = True)

    else:
        all_consensus_ms2_df = pd.DataFrame()

    summary_df = pd.DataFrame(summary_rows)
    feature_id_map_df = pd.DataFrame(feature_id_rows)

    return {"all_consensus_ms2_df": all_consensus_ms2_df,
            "summary_df": summary_df,
            "feature_id_map_df": feature_id_map_df}