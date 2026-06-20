from __future__ import annotations

import pandas as pd
import numpy as np
from clean_id_series import clean_id_series

def ids_with_best_archetype(assignments,
                            group,
                            id_col,
                            archetype_col = "best_archetype"):
    """
    Select IDs whose best_archetype is exactly the requested group.
    """

    selected_rows = assignments[archetype_col].astype(str) == str(group)

    selected_ids = clean_id_series(assignments.loc[selected_rows, id_col])
    selected_ids = pd.Series(pd.unique(selected_ids)).tolist()

    return selected_ids
