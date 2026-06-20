from __future__ import annotations

import pandas as pd
import numpy as np

def assignment_group_unique_fragment_tanimoto(aligned_intensity_df,
                                              assignments_features,
                                              assignments_fragments,
                                              group,
                                              feature_assignment_id_col = "feat_id",
                                              fragment_assignment_id_col = "feat_id",
                                              aligned_fragment_id_col = "aligned_fragment_id",
                                              metadata_cols = ("Unnamed: 0",
                                                               "aligned_fragment_id",
                                                               "aligned_fragment_mz"),
                                              assignment_metadata_cols = ("Unnamed: 0",
                                                                          "best_archetype",
                                                                          "n_active_sample_types",
                                                                          "archetype_size"),
                                              feature_unique_to_group = False,
                                              weight_mode = "none",
                                              smooth_idf = False):
    """
    Calculate a group-specific feature-feature Tanimoto matrix.

    assignments_features:
        One row per LC-HRMS feature.

    assignments_fragments:
        One row per aligned MS2 fragment.

    aligned_intensity_df:
        Rows are aligned MS2 fragments.
        Columns are LC-HRMS features.

    The selected feature columns come from assignments_features.

    The selected fragment rows come from assignments_fragments.

    The similarity is calculated between features using only fragments unique
    to the requested group.
    """

    if feature_unique_to_group:

        selected_feature_ids = ids_unique_to_assignment_group(
            assignments = assignments_features,
            group = group,
            id_col = feature_assignment_id_col,
            metadata_cols = assignment_metadata_cols
        )

    else:

        selected_feature_ids = ids_assigned_to_group(
            assignments = assignments_features,
            group = group,
            id_col = feature_assignment_id_col,
            metadata_cols = assignment_metadata_cols
        )

    selected_fragment_ids = ids_unique_to_assignment_group(
        assignments = assignments_fragments,
        group = group,
        id_col = fragment_assignment_id_col,
        metadata_cols = assignment_metadata_cols
    )

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

        if aligned_fragment_id_col in filtered_aligned_intensity_df.columns:
            fragment_idf_df.insert(0,
                                   aligned_fragment_id_col,
                                   filtered_aligned_intensity_df[aligned_fragment_id_col].to_numpy())

        if "aligned_fragment_mz" in filtered_aligned_intensity_df.columns:
            fragment_idf_df.insert(1,
                                   "aligned_fragment_mz",
                                   filtered_aligned_intensity_df["aligned_fragment_mz"].to_numpy())

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
        raise ValueError("weight_mode must be 'none', 'local_idf', or 'global_idf'.")

    summary = {"group": group,
               "n_features_assigned_to_group": len(selected_feature_ids),
               "n_features_present_in_aligned_table": len(selected_feature_cols),
               "n_fragments_unique_to_group": len(selected_fragment_ids),
               "n_fragments_present_in_aligned_table": filtered_aligned_intensity_df.shape[0],
               "feature_unique_to_group": feature_unique_to_group,
               "weight_mode": weight_mode}

    return {"tanimoto_df": tanimoto_df,
            "filtered_aligned_intensity_df": filtered_aligned_intensity_df,
            "selected_feature_ids": selected_feature_ids,
            "selected_feature_cols": selected_feature_cols,
            "selected_fragment_ids": selected_fragment_ids,
            "fragment_idf_df": fragment_idf_df,
            "summary": summary}
