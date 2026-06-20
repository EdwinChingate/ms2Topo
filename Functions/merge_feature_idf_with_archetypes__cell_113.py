from __future__ import annotations

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import textwrap

def merge_feature_idf_with_archetypes(feature_idf_df,
                                      assignments,
                                      feat_id_col = "feat_id",
                                      archetype_col = "best_archetype",
                                      idf_col = "weighted_mean_fragment_IDF"):
    """
    Merge feature-level IDF values with archetype labels.
    """

    feature_idf_subset = feature_idf_df[[feat_id_col,
                                         idf_col]].copy()

    archetype_subset = assignments[[feat_id_col,
                                    archetype_col]].copy()

    feature_idf_subset[feat_id_col] = feature_idf_subset[feat_id_col].astype(str)
    archetype_subset[feat_id_col] = archetype_subset[feat_id_col].astype(str)

    merged_df = pd.merge(feature_idf_subset,
                         archetype_subset,
                         on = feat_id_col,
                         how = "inner")

    return merged_df
