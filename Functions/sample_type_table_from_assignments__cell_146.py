from __future__ import annotations

import pandas as pd
from filter_assignments_by_sample_types import *

def sample_type_table_from_assignments(assignments,
                                       pattern_col_prefix = "",
                                       separator = " | "):
    """
    Build a table describing the sample-type pattern columns in an
    archetype-assignment table.
    """

    sample_type_rows = []

    for col in assignments.columns:

        if pattern_col_prefix != "":
            if not col.startswith(pattern_col_prefix):
                continue

            sample_type = col.replace(pattern_col_prefix,
                                      "",
                                      1)

        else:
            sample_type = col

        parsed_sample_type = parse_carbon_source_sample_type(sample_type = sample_type,
                                                             separator = separator)

        if parsed_sample_type is None:
            continue

        parsed_sample_type["pattern_col"] = col

        sample_type_rows.append(parsed_sample_type)

    sample_type_df = pd.DataFrame(sample_type_rows)

    return sample_type_df
