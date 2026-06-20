from __future__ import annotations

import pandas as pd
import numpy as np
from clean_id_series import clean_id_series
from get_group_probability_columns import get_group_probability_columns
from group_to_probability_col import group_to_probability_col

def ids_unique_to_group(assignment_df,
                        group,
                        id_col = "feat_id",
                        presence_threshold = 0,
                        absence_threshold = 0,
                        group_col_prefix = "p__"):
    """
    Select IDs that appear in one group and are absent from all other groups.
    """

    group_col = group_to_probability_col(group = group,
                                         group_col_prefix = group_col_prefix)

    group_cols = get_group_probability_columns(assignment_df = assignment_df,
                                               group_col_prefix = group_col_prefix)

    if group_col not in group_cols:
        raise ValueError(f"Group column was not found: {group_col}")

    other_group_cols = [col for col in group_cols
                        if col != group_col]

    group_values = pd.to_numeric(assignment_df[group_col],
                                 errors = "coerce").fillna(0)

    other_group_values = assignment_df[other_group_cols].apply(pd.to_numeric,
                                                               errors = "coerce").fillna(0)

    selected_rows = (
        (group_values > presence_threshold) &
        (other_group_values.max(axis = 1) <= absence_threshold)
    )

    selected_ids = clean_id_series(assignment_df.loc[selected_rows, id_col])
    selected_ids = pd.Series(pd.unique(selected_ids)).tolist()

    return selected_ids
