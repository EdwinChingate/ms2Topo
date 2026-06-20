from __future__ import annotations

import pandas as pd
import numpy as np
from aligned_fragments_to_binary_matrix import aligned_fragments_to_binary_matrix
from feature_fragment_idf_descriptors import feature_fragment_idf_descriptors
from fragment_idf_from_distribution import fragment_idf_from_distribution
from fragments_distribution_across_features import fragments_distribution_across_features
from get_feature_columns import get_feature_columns
from idf_weighted_tanimoto_from_binary_matrix import idf_weighted_tanimoto_from_binary_matrix

def idf_weighted_fragment_tanimoto(aligned_intensity_df,
                                   metadata_cols = ("Unnamed: 0",
                                                    "aligned_fragment_id",
                                                    "aligned_fragment_mz"),
                                   smooth_idf = False,
                                   return_idf_table = True,
                                   return_feature_idf_table = True,
                                   feature_idf_methods = ("weighted_mean",
                                                          "mean",
                                                          "median",
                                                          "max")):
    """
    Calculate an IDF-weighted fragment Tanimoto matrix between features.

    The Tanimoto matrix is calculated from binary fragment presence/absence.

    The feature-level IDF table is calculated from the IDF distribution of the
    fragments present in each feature.
    """

    feature_cols = get_feature_columns(aligned_intensity_df = aligned_intensity_df,
                                       metadata_cols = metadata_cols)

    binary_fragment_mat = aligned_fragments_to_binary_matrix(aligned_intensity_df = aligned_intensity_df,
                                                             feature_cols = feature_cols)

    DF_vector = fragments_distribution_across_features(binary_fragment_mat = binary_fragment_mat)

    n_features = binary_fragment_mat.shape[1]

    IDF = fragment_idf_from_distribution(DF_vector = DF_vector,
                                         n_features = n_features,
                                         smooth_idf = smooth_idf)

    weighted_tanimoto_df = idf_weighted_tanimoto_from_binary_matrix(binary_fragment_mat = binary_fragment_mat,
                                                                    IDF = IDF,
                                                                    feature_cols = feature_cols)

    returned_objects = [weighted_tanimoto_df]

    if return_idf_table:

        fragment_idf_df = pd.DataFrame({"fragment_DF": DF_vector,
                                        "fragment_IDF": IDF})

        if "aligned_fragment_id" in aligned_intensity_df.columns:
            fragment_idf_df.insert(0,
                                   "aligned_fragment_id",
                                   aligned_intensity_df["aligned_fragment_id"].to_numpy())

        if "aligned_fragment_mz" in aligned_intensity_df.columns:
            fragment_idf_df.insert(1,
                                   "aligned_fragment_mz",
                                   aligned_intensity_df["aligned_fragment_mz"].to_numpy())

        returned_objects.append(fragment_idf_df)

    if return_feature_idf_table:

        feature_idf_df = feature_fragment_idf_descriptors(aligned_intensity_df = aligned_intensity_df,
                                                          feature_cols = feature_cols,
                                                          IDF = IDF,
                                                          descriptor_methods = feature_idf_methods)

        returned_objects.append(feature_idf_df)

    if len(returned_objects) == 1:
        return returned_objects[0]

    return tuple(returned_objects)
