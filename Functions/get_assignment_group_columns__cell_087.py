from __future__ import annotations

import numpy as np
import pandas as pd

def get_assignment_group_columns(assignments,
                                 id_col,
                                 metadata_cols = ("Unnamed: 0",
                                                  "best_archetype",
                                                  "n_active_sample_types",
                                                  "archetype_size")):
    """
    Get the sample-group columns from an assignment table.

    The ID column is removed dynamically, so the same function can work for
    feature assignments and fragment assignments.
    """

    metadata_cols = set(metadata_cols)
    metadata_cols.add(id_col)

    group_cols = [col for col in assignments.columns
                  if col not in metadata_cols]

    return group_cols
