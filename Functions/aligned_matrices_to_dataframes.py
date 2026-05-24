from __future__ import annotations

import numpy as np
import pandas as pd

def aligned_matrices_to_dataframes(aligned_fragments_mat,
                                   aligned_fragments_mz_mat,
                                   feature_id_map_df):
    """
    Convert aligned fragment matrices into labeled DataFrames.
    """

    feature_id_map_df = feature_id_map_df.sort_values("spectrum_id").reset_index(drop = True)

    feat_id_vec = feature_id_map_df["feat_id"].tolist()

    base_df = pd.DataFrame({
        "aligned_fragment_id": np.arange(aligned_fragments_mat.shape[0],
                                         dtype = int),
        "aligned_fragment_mz": aligned_fragments_mz_mat[:, 0],
    })

    aligned_intensity_df = base_df.copy()
    aligned_mz_df = base_df.copy()

    for spectrum_id, feat_id in enumerate(feat_id_vec):
        aligned_intensity_df[str(feat_id)] = aligned_fragments_mat[:, spectrum_id + 1]
        aligned_mz_df[str(feat_id)] = aligned_fragments_mz_mat[:, spectrum_id + 1]

    long_rows = []

    for spectrum_id, feat_id in enumerate(feat_id_vec):
        feature_long_df = pd.DataFrame({"aligned_fragment_id": np.arange(aligned_fragments_mat.shape[0],
                                                                         dtype = int),
                                        "aligned_fragment_mz": aligned_fragments_mz_mat[:, 0],
                                        "spectrum_id": spectrum_id,
                                        "feat_id": feat_id,
                                        "fragment_mz": aligned_fragments_mz_mat[:, spectrum_id + 1],
                                        "fragment_intensity": aligned_fragments_mat[:, spectrum_id + 1]})

        feature_long_df["fragment_present"] = ((feature_long_df["fragment_mz"] > 0) & (feature_long_df["fragment_intensity"] > 0))

        long_rows.append(feature_long_df)

    aligned_fragments_long_df = pd.concat(long_rows,
                                          axis = 0,
                                          ignore_index = True)

    return {"aligned_intensity_df": aligned_intensity_df,
            "aligned_mz_df": aligned_mz_df,
            "aligned_fragments_long_df": aligned_fragments_long_df}