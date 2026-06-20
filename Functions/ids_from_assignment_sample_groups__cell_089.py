from __future__ import annotations

import pandas as pd

def ids_from_assignment_sample_groups(assignments,
                                      id_col,
                                      carbon_sources = None,
                                      sample_sources = None,
                                      original_sample_types = None,
                                      clean_status = None,
                                      mode = "inclusive",
                                      require = "any",
                                      pattern_col_prefix = "",
                                      separator = " | ",
                                      return_filtered_assignments = False):
    """
    Select IDs from an assignment table using biological sample-group logic.

    This uses filter_assignments_by_sample_groups internally.

    Example:
        carbon_sources = "Aniline"
        sample_sources = "Effluent"

    keeps rows whose archetype contains at least one selected sample type.
    """

    if id_col not in assignments.columns:
        raise ValueError(
            f"ID column '{id_col}' was not found. "
            f"Available columns are: {list(assignments.columns)}"
        )

    filtered_assignments, selected_sample_types = filter_assignments_by_sample_groups(
        assignments = assignments,
        carbon_sources = carbon_sources,
        sample_sources = sample_sources,
        original_sample_types = original_sample_types,
        clean_status = clean_status,
        mode = mode,
        require = require,
        pattern_col_prefix = pattern_col_prefix,
        separator = separator,
        copy = True,
        return_selected_sample_types = True
    )

    selected_ids = clean_id_series(filtered_assignments[id_col])
    selected_ids = pd.Series(pd.unique(selected_ids)).tolist()

    if return_filtered_assignments:
        return selected_ids, selected_sample_types, filtered_assignments

    return selected_ids, selected_sample_types
