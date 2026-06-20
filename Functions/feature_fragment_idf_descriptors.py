from __future__ import annotations

import numpy as np
import pandas as pd

def feature_fragment_idf_descriptors(aligned_intensity_df,
                                     feature_cols,
                                     IDF,
                                     descriptor_methods = ("weighted_mean",
                                                           "mean",
                                                           "median",
                                                           "max"),
                                     empty_value = np.nan):
    """
    Calculate feature-level descriptors of fragment IDF values.

    Rows of aligned_intensity_df:
        aligned fragments

    Columns:
        features

    IDF:
        fragment-level IDF values, one value per aligned fragment.

    descriptor_methods:
        Feature-level IDF descriptors to calculate.

        Available:
            "weighted_mean":
                Mean IDF weighted by the normalized fragment intensities
                inside each feature.

            "mean":
                Mean IDF of the fragments present in the feature.

            "median":
                Median IDF of the fragments present in the feature.

            "max":
                Highest IDF among the fragments present in the feature.

            "min":
                Lowest IDF among the fragments present in the feature.

            "top3_mean":
                Mean IDF of the three highest-IDF fragments present in the
                feature.

    empty_value:
        Value returned when a feature has no fragments.
    """

    if isinstance(descriptor_methods, str):
        descriptor_methods = [descriptor_methods]

    descriptor_methods = list(descriptor_methods)

    allowed_methods = ["weighted_mean",
                       "mean",
                       "median",
                       "max",
                       "min",
                       "top3_mean"]

    unknown_methods = [method for method in descriptor_methods
                       if method not in allowed_methods]

    if len(unknown_methods) > 0:
        raise ValueError(f"Unknown descriptor methods: {unknown_methods}")

    intensity_df = aligned_intensity_df[feature_cols].apply(pd.to_numeric,
                                                            errors = "coerce").fillna(0)

    intensity_mat = intensity_df.to_numpy(dtype = float)

    intensity_mat[intensity_mat < 0] = 0

    binary_fragment_mat = intensity_mat > 0

    feature_rows = []

    for feature_id, feature_col in enumerate(feature_cols):

        feature_intensities = intensity_mat[:, feature_id]
        feature_fragment_mask = binary_fragment_mat[:, feature_id]

        feature_fragment_idf = IDF[feature_fragment_mask]
        feature_fragment_intensities = feature_intensities[feature_fragment_mask]

        n_fragments = len(feature_fragment_idf)

        total_fragment_intensity = np.sum(feature_fragment_intensities)

        feature_row = {"feat_id": feature_col,
                       "n_fragments": n_fragments,
                       "total_fragment_intensity": total_fragment_intensity}

        if n_fragments == 0:

            for method in descriptor_methods:
                feature_row[f"{method}_fragment_IDF"] = empty_value

            feature_rows.append(feature_row)

            continue

        if "weighted_mean" in descriptor_methods:

            if total_fragment_intensity > 0:

                normalized_fragment_intensities = feature_fragment_intensities / total_fragment_intensity

                weighted_mean_IDF = np.sum(normalized_fragment_intensities *
                                           feature_fragment_idf)

            else:
                weighted_mean_IDF = empty_value

            feature_row["weighted_mean_fragment_IDF"] = weighted_mean_IDF

        if "mean" in descriptor_methods:
            feature_row["mean_fragment_IDF"] = np.mean(feature_fragment_idf)

        if "median" in descriptor_methods:
            feature_row["median_fragment_IDF"] = np.median(feature_fragment_idf)

        if "max" in descriptor_methods:
            feature_row["max_fragment_IDF"] = np.max(feature_fragment_idf)

        if "min" in descriptor_methods:
            feature_row["min_fragment_IDF"] = np.min(feature_fragment_idf)

        if "top3_mean" in descriptor_methods:

            top_n = min(3,
                        n_fragments)

            top3_mean_IDF = np.mean(np.sort(feature_fragment_idf)[-top_n:])

            feature_row["top3_mean_fragment_IDF"] = top3_mean_IDF

        feature_rows.append(feature_row)

    feature_idf_df = pd.DataFrame(feature_rows)

    return feature_idf_df
