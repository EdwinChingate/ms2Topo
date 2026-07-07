# Extracted from notebook: 713031fb-407a-42c5-b338-3c1aba9bdf96.ipynb
# One unique top-level function per file. Auto-generated from top-level function definitions.
from __future__ import annotations
import numpy as np
import pandas as pd
from get_consensus_spectrum_paths import get_consensus_spectrum_paths
from read_consensus_neutral_losses_spectrum import read_consensus_neutral_losses_spectrum


def load_consensus_neutral_losses_from_folder(consensus_spectra_folder,
                                              selected_feat_ids = None,
                                              file_name_template = "Consensus_ms2-spectra_{feat_id}.csv",
                                              mz_col = "median_mz(Da)",
                                              intensity_col = "median_Int",
                                              mz_std_col = "IQR_mz(Da)",
                                              mz_iqr_ppm_col = "IQR_mz(ppm)",
                                              min_mz_col = "min_mz(Da)",
                                              max_mz_col = "max_mz(Da)",
                                              min_source_fragment_intensity = 0.0,
                                              min_neutral_loss = 18.0,
                                              max_neutral_loss = None,
                                              neutral_loss_iqr_rule = "max_fragment_iqr",
                                              continue_on_error = True):
    """
    Load consensus spectra from a folder and generate neutral-loss observations
    for centroid assignment.

    Returns the same structural keys as load_consensus_ms2_spectra_from_folder:
        loaded_consensus_fragments_df
        summary_df
        feature_id_map_df

    The key loaded_consensus_fragments_df is intentionally reused so the
    existing centroid-assignment function can be recycled without modification.
    """

    spectrum_rows = get_consensus_spectrum_paths(consensus_spectra_folder = consensus_spectra_folder,
                                                 selected_feat_ids = selected_feat_ids,
                                                 file_name_template = file_name_template)

    loaded_neutral_loss_tables = []
    summary_rows = []
    feature_id_rows = []
    spectrum_id = 0

    for spectrum_row in spectrum_rows:

        feat_id = spectrum_row["feat_id"]
        consensus_spectrum_path = spectrum_row["consensus_spectrum_path"]

        try:
            neutral_losses_df = read_consensus_neutral_losses_spectrum(consensus_spectrum_path = consensus_spectrum_path,
                                                                       feat_id = feat_id,
                                                                       spectrum_id = spectrum_id,
                                                                       mz_col = mz_col,
                                                                       intensity_col = intensity_col,
                                                                       mz_std_col = mz_std_col,
                                                                       mz_iqr_ppm_col = mz_iqr_ppm_col,
                                                                       min_mz_col = min_mz_col,
                                                                       max_mz_col = max_mz_col,
                                                                       min_source_fragment_intensity = min_source_fragment_intensity,
                                                                       min_neutral_loss = min_neutral_loss,
                                                                       max_neutral_loss = max_neutral_loss,
                                                                       neutral_loss_iqr_rule = neutral_loss_iqr_rule)

            filter_stats = neutral_losses_df.attrs.get("filter_stats", {})

            summary_row = {"feat_id": feat_id,
                           "spectrum_id": spectrum_id if len(neutral_losses_df) > 0 else np.nan,
                           "status": "ok" if len(neutral_losses_df) > 0 else "empty_after_neutral_loss_generation",
                           "n_neutral_losses": int(len(neutral_losses_df)),
                           "consensus_spectrum_file": str(consensus_spectrum_path),
                           "error_message": ""}

            summary_row.update(filter_stats)
            summary_rows.append(summary_row)

            if len(neutral_losses_df) == 0:
                continue

            loaded_neutral_loss_tables.append(neutral_losses_df)

            feature_id_rows.append({"spectrum_id": spectrum_id,
                                    "feat_id": feat_id,
                                    "consensus_spectrum_file": str(consensus_spectrum_path)})

            spectrum_id += 1

        except Exception as error:
            summary_rows.append({"feat_id": feat_id,
                                 "spectrum_id": np.nan,
                                 "status": "failed",
                                 "n_neutral_losses": 0,
                                 "consensus_spectrum_file": str(consensus_spectrum_path),
                                 "error_message": str(error)})

            if not continue_on_error:
                raise

    if len(loaded_neutral_loss_tables) > 0:
        loaded_consensus_fragments_df = pd.concat(loaded_neutral_loss_tables,
                                                  axis = 0,
                                                  ignore_index = True)

    else:
        loaded_consensus_fragments_df = pd.DataFrame()

    summary_df = pd.DataFrame(summary_rows)
    feature_id_map_df = pd.DataFrame(feature_id_rows)

    return {"loaded_consensus_fragments_df": loaded_consensus_fragments_df,
            "summary_df": summary_df,
            "feature_id_map_df": feature_id_map_df}
