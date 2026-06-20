from __future__ import annotations

import pandas as pd
from filter_assignments_by_sample_types import *

def filter_assignments_by_sample_groups(assignments,
                                        carbon_sources = None,
                                        sample_sources = None,
                                        original_sample_types = None,
                                        clean_status = None,
                                        mode = "inclusive",
                                        require = "any",
                                        pattern_col_prefix = "",
                                        separator = " | ",
                                        copy = True,
                                        return_selected_sample_types = False):
    """
    Filter an archetype-assignment table using biological sample-group logic.

    This function selects sample-type columns based on carbon source and
    sample origin, then calls filter_assignments_by_sample_types.

    Examples of group dimensions:
        carbon_sources:
            Aniline, Histidine, Succinate

        sample_sources:
            Influent, Effluent

        original_sample_types:
            Influent, InfluentClean, Effluent, EffluentClean

        clean_status:
            clean, experimental
    """

    selected_sample_types = select_sample_types_by_groups(assignments = assignments,
                                                         carbon_sources = carbon_sources,
                                                         sample_sources = sample_sources,
                                                         original_sample_types = original_sample_types,
                                                         clean_status = clean_status,
                                                         pattern_col_prefix = pattern_col_prefix,
                                                         separator = separator)

    if len(selected_sample_types) == 0:
        raise ValueError("No sample types matched the requested groups.")

    filtered_assignments = filter_assignments_by_sample_types(assignments = assignments,
                                                              sample_types = selected_sample_types,
                                                              mode = mode,
                                                              require = require,
                                                              pattern_col_prefix = pattern_col_prefix,
                                                              copy = copy)

    if return_selected_sample_types:
        return filtered_assignments, selected_sample_types

    return filtered_assignments
