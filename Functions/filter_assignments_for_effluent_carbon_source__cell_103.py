from __future__ import annotations

import pandas as pd

def filter_assignments_for_effluent_carbon_source(assignments,
                                                  carbon_source,
                                                  pattern_col_prefix = "",
                                                  separator = " | ",
                                                  copy = True,
                                                  return_filter_info = False):
    """
    Keep rows that appear in experimental effluent for one carbon source,
    while removing rows that appear in influent, influent clean, or effluent
    clean samples.

    Example for carbon_source = "Aniline":

    Required:
        Effluent | Aniline

    Forbidden:
        Influent | Aniline
        Influent | Histidine
        Influent | Succinate
        InfluentClean | Aniline
        InfluentClean | Histidine
        InfluentClean | Succinate
        EffluentClean | Aniline
        EffluentClean | Histidine
        EffluentClean | Succinate

    Allowed:
        Effluent | Histidine
        Effluent | Succinate
    """

    required_assignments, required_sample_types = filter_assignments_by_sample_groups(
        assignments = assignments,
        carbon_sources = carbon_source,
        original_sample_types = "Effluent",
        mode = "inclusive",
        require = "any",
        pattern_col_prefix = pattern_col_prefix,
        separator = separator,
        copy = True,
        return_selected_sample_types = True
    )

    filtered_assignments, forbidden_sample_types = filter_assignments_by_sample_groups(
        assignments = required_assignments,
        original_sample_types = ["Influent",
                                 "InfluentClean",
                                 "EffluentClean"],
        mode = "exclusive",
        require = "any",
        pattern_col_prefix = pattern_col_prefix,
        separator = separator,
        copy = copy,
        return_selected_sample_types = True
    )

    if return_filter_info:

        filter_info = {"carbon_source": carbon_source,
                       "required_sample_types": required_sample_types,
                       "forbidden_sample_types": forbidden_sample_types,
                       "n_rows_before_filter": assignments.shape[0],
                       "n_rows_after_required_filter": required_assignments.shape[0],
                       "n_rows_after_forbidden_filter": filtered_assignments.shape[0]}

        return filtered_assignments, filter_info

    return filtered_assignments
