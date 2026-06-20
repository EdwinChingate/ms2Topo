from __future__ import annotations

import pandas as pd
import numpy as np
from aligned_fragments_to_binary_matrix import aligned_fragments_to_binary_matrix
from filter_aligned_intensity_by_fragment_ids import filter_aligned_intensity_by_fragment_ids
from fragment_idf_from_distribution import fragment_idf_from_distribution
from fragments_distribution_across_features import fragments_distribution_across_features
from get_feature_columns import get_feature_columns
from idf_weighted_tanimoto_from_binary_matrix import idf_weighted_tanimoto_from_binary_matrix
from ids_with_best_archetype import ids_with_best_archetype
from match_feature_ids_to_aligned_columns import match_feature_ids_to_aligned_columns
from tanimoto_from_binary_matrix import tanimoto_from_binary_matrix

def unique_archetype_fragment_tanimoto(aligned_intensity_df,
                                       assignments_features,
                                       assignments_fragments,
                                       group,
                                       feature_id_col = "feat_id",
                                       fragment_id_col = "aligned_fragment_id",
                                       aligned_fragment_id_col = "aligned_fragment_id",
                                       archetype_col = "best_archetype",
                                       metadata_cols = ("Unnamed: 0",
                                                        "aligned_fragment_id",
                                                        "aligned_fragment_mz"),
                                       weight_mode = "global_idf",
                                       smooth_idf = False):
    """
    Calculate feature-feature similarity for one exact archetype group.

    Features:
        features whose best_archetype == group

    Fragments:
        aligned fragments whose best_archetype == group

    Similarity:
        calculated between the selected features using only the selected
        group-specific fragments.
    """

    selected_feature_ids = ids_with_best_archetype(assignments = assignments_features,
                                                   group = group,
                                                   id_col = feature_id_col,
                                                   archetype_col = archetype_col)

    selected_fragment_ids = ids_with_best_archetype(assignments = assignments_fragments,
                                                    group = group,
                                                    id_col = fragment_id_col,
                                                    archetype_col = archetype_col)

    selected_feature_cols = match_feature_ids_to_aligned_columns(
        aligned_intensity_df = aligned_intensity_df,
        selected_feature_ids = selected_feature_ids,
        metadata_cols = metadata_cols
    )

    selected_fragment_df = filter_aligned_intensity_by_fragment_ids(
        aligned_intensity_df = aligned_intensity_df,
        selected_fragment_ids = selected_fragment_ids,
        aligned_fragment_id_col = aligned_fragment_id_col
    )

    metadata_cols_present = [col for col in metadata_cols
                             if col in selected_fragment_df.columns]

    filtered_aligned_intensity_df = selected_fragment_df.loc[
        :,
        metadata_cols_present + selected_feature_cols
    ].copy()

    binary_fragment_mat = aligned_fragments_to_binary_matrix(
        aligned_intensity_df = filtered_aligned_intensity_df,
        feature_cols = selected_feature_cols
    )

    fragment_idf_df = None

    if weight_mode == "none":

        tanimoto_df = tanimoto_from_binary_matrix(binary_fragment_mat = binary_fragment_mat,
                                                  feature_cols = selected_feature_cols)

    elif weight_mode == "global_idf":

        all_feature_cols = get_feature_columns(aligned_intensity_df = aligned_intensity_df,
                                               metadata_cols = metadata_cols)

        global_binary_fragment_mat = aligned_fragments_to_binary_matrix(
            aligned_intensity_df = selected_fragment_df,
            feature_cols = all_feature_cols
        )

        DF_vector = fragments_distribution_across_features(binary_fragment_mat = global_binary_fragment_mat)

        IDF = fragment_idf_from_distribution(DF_vector = DF_vector,
                                             n_features = global_binary_fragment_mat.shape[1],
                                             smooth_idf = smooth_idf)

        tanimoto_df = idf_weighted_tanimoto_from_binary_matrix(binary_fragment_mat = binary_fragment_mat,
                                                               IDF = IDF,
                                                               feature_cols = selected_feature_cols)

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

    else:
        raise ValueError("weight_mode must be 'none' or 'global_idf'.")

    summary = {"group": group,
               "n_selected_feature_ids": len(selected_feature_ids),
               "n_selected_features_present_in_aligned_table": len(selected_feature_cols),
               "n_selected_fragment_ids": len(selected_fragment_ids),
               "n_selected_fragments_present_in_aligned_table": filtered_aligned_intensity_df.shape[0],
               "tanimoto_shape": tanimoto_df.shape,
               "weight_mode": weight_mode}

    return {"tanimoto_df": tanimoto_df,
            "filtered_aligned_intensity_df": filtered_aligned_intensity_df,
            "selected_feature_ids": selected_feature_ids,
            "selected_feature_cols": selected_feature_cols,
            "selected_fragment_ids": selected_fragment_ids,
            "fragment_idf_df": fragment_idf_df,
            "summary": summary}
