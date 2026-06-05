from __future__ import annotations

from pathlib import Path
import os
import re
import numpy as np
import pandas as pd
from scipy.sparse import coo_matrix, csr_matrix

def neutral_losses_from_consensus_spectra(consensus_spectra_files,
                                          mz_col = "median_mz(Da)",
                                          intensity_col = "median_Int",
                                          min_neutral_loss = 18.0,
                                          max_neutral_loss = None,
                                          min_fragment_intensity = 0,
                                          pair_intensity = "min"):
    """
    Extract possible neutral losses directly from individual consensus MS2 spectra.

    Expected:
        consensus_spectra_files is a list of csv files.
        Each csv file contains one consensus spectrum.

    Required columns:
        mz_col
        intensity_col

    Output:
        neutral_losses_df:
            one row per possible neutral loss.

        feature_id_map_df:
            map between spectrum_id, feature_id, and source file.
    """

    neutral_loss_tables = []
    feature_id_map_rows = []

    for spectrum_id, consensus_spectra_file in enumerate(consensus_spectra_files):

        consensus_spectra_df = pd.read_csv(consensus_spectra_file,
                                           index_col = 0)

        if mz_col not in consensus_spectra_df.columns:
            raise ValueError("Missing mz_col in " + str(consensus_spectra_file) + ": " + str(mz_col))

        if intensity_col not in consensus_spectra_df.columns:
            raise ValueError("Missing intensity_col in " + str(consensus_spectra_file) + ": " + str(intensity_col))

        source_file = os.path.basename(consensus_spectra_file)

        feature_id_search = re.search(r"Consensus_ms2-spectra_(\d+)",
                                      source_file)

        if feature_id_search is None:
            feature_id = spectrum_id
        else:
            feature_id = int(feature_id_search.group(1))

        feature_id_map_rows.append({"spectrum_id": int(spectrum_id),
                                    "feature_id": int(feature_id),
                                    "source_file": source_file})

        fragment_mz = consensus_spectra_df[mz_col].to_numpy(float)
        fragment_intensity = consensus_spectra_df[intensity_col].to_numpy(float)
        fragment_ids = np.arange(len(consensus_spectra_df),
                                 dtype = int)

        fragments_loc = (np.isfinite(fragment_mz) &
                         np.isfinite(fragment_intensity) &
                         (fragment_intensity > min_fragment_intensity))

        if np.sum(fragments_loc) < 2:
            continue

        fragment_mz = fragment_mz[fragments_loc]
        fragment_intensity = fragment_intensity[fragments_loc]
        fragment_ids = fragment_ids[fragments_loc]

        order = np.argsort(fragment_mz)

        fragment_mz = fragment_mz[order]
        fragment_intensity = fragment_intensity[order]
        fragment_ids = fragment_ids[order]

        n_fragments = len(fragment_mz)

        loss_tables_current_spectrum = []

        for low_id in range(n_fragments - 1):

            start_id = np.searchsorted(fragment_mz,
                                       fragment_mz[low_id] + min_neutral_loss,
                                       side = "left")

            if max_neutral_loss is None:
                stop_id = n_fragments

            else:
                stop_id = np.searchsorted(fragment_mz,
                                          fragment_mz[low_id] + max_neutral_loss,
                                          side = "right")

            if start_id >= stop_id:
                continue

            high_ids = np.arange(start_id,
                                 stop_id,
                                 dtype = int)

            neutral_loss_mz = fragment_mz[high_ids] - fragment_mz[low_id]

            low_intensity = np.repeat(fragment_intensity[low_id],
                                      len(high_ids))

            high_intensity = fragment_intensity[high_ids]

            if pair_intensity == "min":
                neutral_loss_intensity = np.minimum(low_intensity,
                                                    high_intensity)

            elif pair_intensity == "geometric_mean":
                neutral_loss_intensity = np.sqrt(low_intensity * high_intensity)

            elif pair_intensity == "mean":
                neutral_loss_intensity = 0.5 * (low_intensity + high_intensity)

            elif pair_intensity == "product":
                neutral_loss_intensity = low_intensity * high_intensity

            elif pair_intensity == "binary":
                neutral_loss_intensity = np.ones(len(high_ids),
                                                 dtype = float)

            else:
                raise ValueError("Unknown pair_intensity: " + str(pair_intensity))

            loss_tables_current_spectrum.append(pd.DataFrame({"spectrum_id": int(spectrum_id),
                                                              "feature_id": int(feature_id),
                                                              "source_file": source_file,
                                                              "neutral_loss_mz": neutral_loss_mz,
                                                              "neutral_loss_intensity": neutral_loss_intensity,
                                                              "fragment_low_id": fragment_ids[low_id],
                                                              "fragment_high_id": fragment_ids[high_ids],
                                                              "fragment_low_mz": fragment_mz[low_id],
                                                              "fragment_high_mz": fragment_mz[high_ids],
                                                              "fragment_low_intensity": low_intensity,
                                                              "fragment_high_intensity": high_intensity}))

        if len(loss_tables_current_spectrum) > 0:
            neutral_loss_tables.append(pd.concat(loss_tables_current_spectrum,
                                                 ignore_index = True))

    feature_id_map_df = pd.DataFrame(feature_id_map_rows)

    if len(neutral_loss_tables) == 0:
        neutral_losses_df = pd.DataFrame()

    else:
        neutral_losses_df = pd.concat(neutral_loss_tables,
                                      ignore_index = True)

    return {"neutral_losses_df": neutral_losses_df,
            "feature_id_map_df": feature_id_map_df}
