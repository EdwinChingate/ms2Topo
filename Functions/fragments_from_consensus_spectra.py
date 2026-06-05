from __future__ import annotations

from pathlib import Path
import os
import re
import numpy as np
import pandas as pd
from scipy.sparse import coo_matrix, csr_matrix

def fragments_from_consensus_spectra(consensus_spectra_files,
                                     mz_col = "median_mz(Da)",
                                     intensity_col = None,
                                     min_fragment_intensity = None):
    """
    Gather all fragments from individual consensus MS2 spectra.

    Expected:
        consensus_spectra_files is a list of csv files.
        Each csv file contains one consensus spectrum.

    Required column:
        mz_col

    Optional:
        intensity_col
        min_fragment_intensity

    Output:
        fragments_df:
            one row per fragment from all consensus spectra.

        feature_id_map_df:
            map between spectrum_id, feature_id, and source file.
    """

    fragment_tables = []
    feature_id_map_rows = []

    for spectrum_id, consensus_spectra_file in enumerate(consensus_spectra_files):

        consensus_spectra_df = pd.read_csv(consensus_spectra_file,
                                           index_col = 0)

        if mz_col not in consensus_spectra_df.columns:
            raise ValueError("Missing mz_col in " + str(consensus_spectra_file) + ": " + str(mz_col))

        if intensity_col is not None:
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

        fragments_loc = np.isfinite(fragment_mz)

        if intensity_col is not None:
            fragment_intensity = consensus_spectra_df[intensity_col].to_numpy(float)
            fragments_loc = fragments_loc & np.isfinite(fragment_intensity)

            if min_fragment_intensity is not None:
                fragments_loc = fragments_loc & (fragment_intensity > min_fragment_intensity)

        if np.sum(fragments_loc) == 0:
            continue

        fragments_df_current_spectrum = consensus_spectra_df.loc[fragments_loc, :].copy()

        fragments_df_current_spectrum.insert(0,
                                             "fragment_id",
                                             np.arange(len(consensus_spectra_df),
                                                       dtype = int)[fragments_loc])

        fragments_df_current_spectrum.insert(0,
                                             "source_file",
                                             source_file)

        fragments_df_current_spectrum.insert(0,
                                             "feature_id",
                                             int(feature_id))

        fragments_df_current_spectrum.insert(0,
                                             "spectrum_id",
                                             int(spectrum_id))

        fragments_df_current_spectrum["fragment_mz"] = fragments_df_current_spectrum[mz_col].to_numpy(float)

        if intensity_col is not None:
            fragments_df_current_spectrum["fragment_intensity"] = fragments_df_current_spectrum[intensity_col].to_numpy(float)

        fragments_df_current_spectrum = fragments_df_current_spectrum.sort_values("fragment_mz")

        fragment_tables.append(fragments_df_current_spectrum)

    feature_id_map_df = pd.DataFrame(feature_id_map_rows)

    if len(fragment_tables) == 0:
        fragments_df = pd.DataFrame()

    else:
        fragments_df = pd.concat(fragment_tables,
                                 ignore_index = True)

    return {"fragments_df": fragments_df,
            "feature_id_map_df": feature_id_map_df}
