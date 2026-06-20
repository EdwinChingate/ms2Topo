from __future__ import annotations

import pandas as pd
import numpy as np
from clean_id_series import clean_id_series
from get_assignment_group_columns import get_assignment_group_columns

def ids_assigned_to_group(assignments,
                          group,
                          id_col,
                          metadata_cols = ("Unnamed: 0",
                                           "best_archetype",
                                           "n_active_sample_types",
                                           "archetype_size")):
    """
    Select row IDs assigned to one sample-distribution group.
    """

    if id_col not in assignments.columns:
        raise ValueError(
            f"ID column '{id_col}' was not found. "
            f"Available columns are: {list(assignments.columns)}"
        )

    group_cols = get_assignment_group_columns(assignments = assignments,
                                              id_col = id_col,
                                              metadata_cols = metadata_cols)

    if group not in group_cols:
        raise ValueError(f"Group column was not found: {group}")

    group_values = pd.to_numeric(assignments[group],
                                 errors = "coerce").fillna(0)

    selected_rows = group_values > 0

    selected_ids = clean_id_series(assignments.loc[selected_rows, id_col])
    selected_ids = pd.Series(pd.unique(selected_ids)).tolist()

    return selected_ids
