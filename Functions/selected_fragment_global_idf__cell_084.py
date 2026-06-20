from __future__ import annotations

import pandas as pd
import numpy as np

def selected_fragment_global_idf(aligned_intensity_df,
                                 selected_fragment_ids,
                                 metadata_cols = ("Unnamed: 0",
                                                  "aligned_fragment_id",
                                                  "aligned_fragment_mz"),
                                 aligned_fragment_id_col = "aligned_fragment_id",
                                 smooth_idf = False):
    """
    Calculate global IDF for selected fragments using all feature columns in
    the aligned fragment-intensity table.
    """

    all_feature_cols = get_feature_columns(aligned_intensity_df = aligned_intensity_df,
                                           metadata_cols = metadata_cols)

    selected_fragment_df, _ = filter_aligned_intensity_by_fragment_ids(
        aligned_intensity_df = aligned_intensity_df,
        selected_fragment_ids = selected_fragment_ids,
        aligned_fragment_id_col = aligned_fragment_id_col
    )

    binary_fragment_mat = aligned_fragments_to_binary_matrix(aligned_intensity_df = selected_fragment_df,
                                                             feature_cols = all_feature_cols)

    DF_vector = fragments_distribution_across_features(binary_fragment_mat = binary_fragment_mat)

    n_features = binary_fragment_mat.shape[1]

    IDF = fragment_idf_from_distribution(DF_vector = DF_vector,
                                         n_features = n_features,
                                         smooth_idf = smooth_idf)

    fragment_idf_df = pd.DataFrame({"fragment_DF": DF_vector,
                                    "fragment_IDF": IDF})

    if aligned_fragment_id_col in selected_fragment_df.columns:
        fragment_idf_df.insert(0,
                               aligned_fragment_id_col,
                               selected_fragment_df[aligned_fragment_id_col].to_numpy())

    if "aligned_fragment_mz" in selected_fragment_df.columns:
        fragment_idf_df.insert(1,
                               "aligned_fragment_mz",
                               selected_fragment_df["aligned_fragment_mz"].to_numpy())

    return IDF, fragment_idf_df
