from __future__ import annotations

import pandas as pd

def effluent_carbon_source_fragment_tanimoto_with_molecules(aligned_intensity_df,
                                                            assignments_features,
                                                            assignments_fragments,
                                                            carbon_source,
                                                            molecules_df = None,
                                                            feature_id_col = "feat_id",
                                                            molecule_feature_id_col = "feat_id",
                                                            fragment_id_col = "aligned_fragment_id",
                                                            aligned_fragment_id_col = "aligned_fragment_id",
                                                            metadata_cols = ("Unnamed: 0",
                                                                             "aligned_fragment_id",
                                                                             "aligned_fragment_mz"),
                                                            pattern_col_prefix = "",
                                                            separator = " | ",
                                                            weight_mode = "global_idf",
                                                            smooth_idf = False):
    """
    Calculate feature-feature similarity using an experimental-effluent
    carbon-source filter.

    Features:
        rows from assignments_features that:
            appear in Effluent | carbon_source
            do not appear in Influent, InfluentClean, or EffluentClean

        plus molecule features from molecules_df.

    Fragments:
        rows from assignments_fragments that:
            appear in Effluent | carbon_source
            do not appear in Influent, InfluentClean, or EffluentClean

    Similarity:
        calculated between selected features using only selected fragments.
    """

    group_feature_ids, filtered_feature_assignments, feature_filter_info = (
        ids_from_effluent_carbon_source_filter(
            assignments = assignments_features,
            carbon_source = carbon_source,
            id_col = feature_id_col,
            pattern_col_prefix = pattern_col_prefix,
            separator = separator,
            return_filter_info = True
        )
    )

    group_fragment_ids, filtered_fragment_assignments, fragment_filter_info = (
        ids_from_effluent_carbon_source_filter(
            assignments = assignments_fragments,
            carbon_source = carbon_source,
            id_col = fragment_id_col,
            pattern_col_prefix = pattern_col_prefix,
            separator = separator,
            return_filter_info = True
        )
    )

    if molecules_df is None:

        molecule_feature_ids = []

    else:

        molecule_feature_ids = ids_from_feature_table(feature_table = molecules_df,
                                                      id_col = molecule_feature_id_col)

    selected_feature_ids = join_id_lists_preserving_order(group_feature_ids,
                                                          molecule_feature_ids)

    selected_feature_cols = match_feature_ids_to_aligned_columns(
        aligned_intensity_df = aligned_intensity_df,
        selected_feature_ids = selected_feature_ids,
        metadata_cols = metadata_cols
    )

    selected_fragment_df = filter_aligned_intensity_by_fragment_ids(
        aligned_intensity_df = aligned_intensity_df,
        selected_fragment_ids = group_fragment_ids,
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

    feature_role_df = make_selected_feature_role_table(
        selected_feature_cols = selected_feature_cols,
        group_feature_ids = group_feature_ids,
        molecule_feature_ids = molecule_feature_ids
    )

    summary = {"carbon_source": carbon_source,
               "feature_filter_info": feature_filter_info,
               "fragment_filter_info": fragment_filter_info,
               "n_group_feature_ids": len(group_feature_ids),
               "n_molecule_feature_ids": len(molecule_feature_ids),
               "n_selected_feature_ids_after_join": len(selected_feature_ids),
               "n_selected_features_present_in_aligned_table": len(selected_feature_cols),
               "n_group_fragment_ids": len(group_fragment_ids),
               "n_selected_fragments_present_in_aligned_table": filtered_aligned_intensity_df.shape[0],
               "tanimoto_shape": tanimoto_df.shape,
               "weight_mode": weight_mode}

    return {"tanimoto_df": tanimoto_df,
            "filtered_aligned_intensity_df": filtered_aligned_intensity_df,
            "filtered_feature_assignments": filtered_feature_assignments,
            "filtered_fragment_assignments": filtered_fragment_assignments,
            "selected_feature_ids": selected_feature_ids,
            "selected_feature_cols": selected_feature_cols,
            "group_feature_ids": group_feature_ids,
            "molecule_feature_ids": molecule_feature_ids,
            "selected_fragment_ids": group_fragment_ids,
            "fragment_idf_df": fragment_idf_df,
            "feature_role_df": feature_role_df,
            "summary": summary}
