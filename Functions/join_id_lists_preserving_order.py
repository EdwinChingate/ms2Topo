from __future__ import annotations

import pandas as pd
import numpy as np
from clean_id_series import clean_id_series

def join_id_lists_preserving_order(*id_lists):
    """
    Join ID lists while preserving order and removing duplicates.
    """

    joined_ids = []

    for id_list in id_lists:
        joined_ids.extend(id_list)

    joined_ids = clean_id_series(joined_ids)
    joined_ids = pd.Series(pd.unique(joined_ids)).tolist()

    return joined_ids
