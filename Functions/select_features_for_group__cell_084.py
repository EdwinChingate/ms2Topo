from __future__ import annotations

import numpy as np
import pandas as pd

def select_features_for_group(experiment_features_df,
                              group,
                              feature_id_col = "feat_id",
                              feature_unique_to_group = False,
                              presence_threshold = 0,
                              absence_threshold = 0,
                              group_col_prefix = "p__"):
    """
    Select features related to a sample-distribution group.

    If feature_unique_to_group is False:
        select features present in the group.

    If feature_unique_to_group is True:
        select features present only in the group.
    """

    if feature_unique_to_group:

        feature_ids = ids_unique_to_group(assignment_df = experiment_features_df,
                                          group = group,
                                          id_col = feature_id_col,
                                          presence_threshold = presence_threshold,
                                          absence_threshold = absence_threshold,
                                          group_col_prefix = group_col_prefix)

    else:

        feature_ids = ids_present_in_group(assignment_df = experiment_features_df,
                                           group = group,
                                           id_col = feature_id_col,
                                           presence_threshold = presence_threshold,
                                           group_col_prefix = group_col_prefix)

    return feature_ids
