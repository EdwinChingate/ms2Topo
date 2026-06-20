from __future__ import annotations

import pandas as pd

def ids_from_effluent_carbon_source_filter(assignments,
                                           carbon_source,
                                           id_col,
                                           pattern_col_prefix = "",
                                           separator = " | ",
                                           return_filter_info = False):
    """
    Return IDs after applying the effluent-carbon-source filter.
    """

    filtered_assignments, filter_info = filter_assignments_for_effluent_carbon_source(
        assignments = assignments,
        carbon_source = carbon_source,
        pattern_col_prefix = pattern_col_prefix,
        separator = separator,
        copy = True,
        return_filter_info = True
    )

    if id_col not in filtered_assignments.columns:
        raise ValueError(
            f"ID column '{id_col}' was not found. "
            f"Available columns are: {list(filtered_assignments.columns)}"
        )

    selected_ids = clean_id_series(filtered_assignments[id_col])
    selected_ids = pd.Series(pd.unique(selected_ids)).tolist()

    if return_filter_info:
        return selected_ids, filtered_assignments, filter_info

    return selected_ids
