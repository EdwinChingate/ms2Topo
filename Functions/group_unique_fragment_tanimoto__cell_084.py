from __future__ import annotations

import pandas as pd
import numpy as np

def group_unique_fragment_tanimoto(aligned_intensity_df,
                                   experiment_features_df,
                                   experiment_fragments_df,
                                   group,
                                   feature_id_col = "feat_id",
                                   fragment_id_col = "feat_id",
                                   aligned_fragment_id_col = "aligned_fragment_id",
                                   metadata_cols = ("Unnamed: 0",
                                                    "aligned_fragment_id",
                                                    "aligned_fragment_mz"),
                                   group_col_prefix = "p__",
                                   feature_presence_threshold = 0,
                                   fragment_presence_threshold = 0,
                                   fragment_absence_threshold = 0,
                                   feature_unique_to_group = False,
                                   feature_absence_threshold = 0,
                                   weight_mode = "global_idf",
                                   smooth_idf = False):
    """
    Calculate a group-specific Tanimoto-like similarity matrix.

    Features:
        selected from experiment_features_df as features related to `group`.

    Fragments:
        selected from experiment_fragments_df as fragments unique to `group`.

    Similarity:
        calculated between the selected features using only the selected
        group-unique fragments.

    weight_mode:
        "none":
            unweighted Tanimoto.

        "local_idf":
            IDF calculated only within the selected feature set.

        "global_idf":
            IDF calculated using all features in aligned_intensity_df.
    """

    selected_feature_ids = select_features_for_group(
        experiment_features_df = experiment_features_df,
        group = group,
        feature_id_col = feature_id_col,
        feature_unique_to_group = feature_unique_to_group,
        presence_threshold = feature_presence_threshold,
        absence_threshold = feature_absence_threshold,
        group_col_prefix = group_col_prefix
    )

    selected_fragment_ids = select_unique_fragments_for_group(
        experiment_fragments_df = experiment_fragments_df,
        group = group,
        fragment_id_col = fragment_id_col,
        presence_threshold = fragment_presence_threshold,
        absence_threshold = fragment_absence_threshold,
        group_col_prefix = group_col_prefix
    )

    selected_feature_cols = match_feature_ids_to_aligned_columns(
        aligned_intensity_df = aligned_intensity_df,
        selected_feature_ids = selected_feature_ids,
        metadata_cols = metadata_cols
    )

    selected_fragment_df, _ = filter_aligned_intensity_by_fragment_ids(
        aligned_intensity_df = aligned_intensity_df,
        selected_fragment_ids = selected_fragment_ids,
        aligned_fragment_id_col = aligned_fragment_id_col
    )

    filtered_aligned_intensity_df = selected_fragment_df.loc[:, [
        col for col in metadata_cols
        if col in selected_fragment_df.columns
    ] + selected_feature_cols].copy()

    binary_fragment_mat = aligned_fragments_to_binary_matrix(
        aligned_intensity_df = filtered_aligned_intensity_df,
        feature_cols = selected_feature_cols
    )

    fragment_idf_df = None

    if weight_mode == "none":

        tanimoto_df = tanimoto_from_binary_matrix(binary_fragment_mat = binary_fragment_mat,
                                                  feature_cols = selected_feature_cols)

    elif weight_mode == "local_idf":

        DF_vector = fragments_distribution_across_features(binary_fragment_mat = binary_fragment_mat)

        IDF = fragment_idf_from_distribution(DF_vector = DF_vector,
                                             n_features = binary_fragment_mat.shape[1],
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

    elif weight_mode == "global_idf":

        IDF, fragment_idf_df = selected_fragment_global_idf(
            aligned_intensity_df = aligned_intensity_df,
            selected_fragment_ids = selected_fragment_ids,
            metadata_cols = metadata_cols,
            aligned_fragment_id_col = aligned_fragment_id_col,
            smooth_idf = smooth_idf
        )

        tanimoto_df = idf_weighted_tanimoto_from_binary_matrix(binary_fragment_mat = binary_fragment_mat,
                                                               IDF = IDF,
                                                               feature_cols = selected_feature_cols)

    else:
        raise ValueError("weight_mode must be 'none', 'local_idf', or 'global_idf'.")

    summary = {"group": group,
               "n_selected_features_from_assignment": len(selected_feature_ids),
               "n_selected_features_present_in_aligned_table": len(selected_feature_cols),
               "n_unique_fragments_from_assignment": len(selected_fragment_ids),
               "n_unique_fragments_present_in_aligned_table": selected_fragment_df.shape[0],
               "weight_mode": weight_mode}

    return {"tanimoto_df": tanimoto_df,
            "filtered_aligned_intensity_df": filtered_aligned_intensity_df,
            "selected_feature_ids": selected_feature_ids,
            "selected_feature_cols": selected_feature_cols,
            "selected_fragment_ids": selected_fragment_ids,
            "fragment_idf_df": fragment_idf_df,
            "summary": summary}
