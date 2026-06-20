from __future__ import annotations

import numpy as np
import pandas as pd

def match_feature_ids_to_aligned_columns(aligned_intensity_df,
                                         selected_feature_ids,
                                         metadata_cols = ("Unnamed: 0",
                                                          "aligned_fragment_id",
                                                          "aligned_fragment_mz")):
    """
    Match selected feature IDs to columns in the aligned intensity table.
    """

    metadata_cols = set(metadata_cols)

    aligned_feature_cols = [col for col in aligned_intensity_df.columns
                            if col not in metadata_cols]

    aligned_col_map = {
        clean_id_value(col): col
        for col in aligned_feature_cols
    }

    selected_feature_ids = clean_id_series(selected_feature_ids).tolist()

    selected_feature_cols = [aligned_col_map[feature_id]
                             for feature_id in selected_feature_ids
                             if feature_id in aligned_col_map]

    return selected_feature_cols
