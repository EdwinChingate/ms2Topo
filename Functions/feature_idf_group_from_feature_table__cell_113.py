from __future__ import annotations

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import textwrap

def feature_idf_group_from_feature_table(feature_idf_df,
                                         feature_table,
                                         group_label,
                                         feat_id_col = "feat_id",
                                         idf_col = "weighted_mean_fragment_IDF",
                                         group_col = "best_archetype"):
    """
    Extract feature-level IDF values for a table of selected features and
    return them as an extra plotting group.

    This does not modify the original archetype assignments. It just creates
    a new table where all selected features are assigned to one custom label.
    """

    feature_idf_subset = feature_idf_df[[feat_id_col,
                                         idf_col]].copy()

    feature_idf_subset[feat_id_col] = feature_idf_subset[feat_id_col].astype(str)

    selected_feat_ids = pd.Series(feature_table[feat_id_col]).dropna()
    selected_feat_ids = selected_feat_ids.astype(float).astype(int).astype(str)

    selected_feat_ids = pd.Series(pd.unique(selected_feat_ids))

    extra_group_df = feature_idf_subset[
        feature_idf_subset[feat_id_col].isin(selected_feat_ids)
    ].copy()

    extra_group_df[group_col] = group_label

    return extra_group_df
