from __future__ import annotations

import pandas as pd
import numpy as np
from clean_id_series import clean_id_series

def ids_from_feature_table(feature_table,
                           id_col = "feat_id"):
    """
    Extract feature IDs from a table such as molecules_df.
    """

    if id_col not in feature_table.columns:
        raise ValueError(
            f"ID column '{id_col}' was not found. "
            f"Available columns are: {list(feature_table.columns)}"
        )

    feature_ids = clean_id_series(feature_table[id_col])
    feature_ids = pd.Series(pd.unique(feature_ids)).tolist()

    return feature_ids
