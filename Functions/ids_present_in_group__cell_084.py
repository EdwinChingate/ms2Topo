from __future__ import annotations

import pandas as pd
import numpy as np

def ids_present_in_group(assignment_df,
                         group,
                         id_col = "feat_id",
                         presence_threshold = 0,
                         group_col_prefix = "p__"):
    """
    Select IDs whose group prevalence/probability is above a threshold.
    """

    group_col = group_to_probability_col(group = group,
                                         group_col_prefix = group_col_prefix)

    if group_col not in assignment_df.columns:
        raise ValueError(f"Group column was not found: {group_col}")

    group_values = pd.to_numeric(assignment_df[group_col],
                                 errors = "coerce").fillna(0)

    selected_rows = group_values > presence_threshold

    selected_ids = clean_id_series(assignment_df.loc[selected_rows, id_col])
    selected_ids = pd.Series(pd.unique(selected_ids)).tolist()

    return selected_ids
