from __future__ import annotations

import pandas as pd
import numpy as np
from clean_id_series import clean_id_series
from get_assignment_group_columns import get_assignment_group_columns

def ids_unique_to_assignment_group(assignments,
                                   group,
                                   id_col,
                                   metadata_cols = ("Unnamed: 0",
                                                    "best_archetype",
                                                    "n_active_sample_types",
                                                    "archetype_size")):
    """
    Select row IDs assigned only to one sample-distribution group.

    This function does not care whether the IDs represent features or aligned
    fragments. That is decided by the table passed to it.
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

    group_matrix = assignments[group_cols].apply(pd.to_numeric,
                                                 errors = "coerce").fillna(0)

    selected_rows = (
        (group_matrix[group] > 0) &
        (group_matrix.sum(axis = 1) == group_matrix[group])
    )

    selected_ids = clean_id_series(assignments.loc[selected_rows, id_col])
    selected_ids = pd.Series(pd.unique(selected_ids)).tolist()

    return selected_ids
