from __future__ import annotations

import numpy as np
import pandas as pd

def get_feature_columns(aligned_intensity_df,
                        metadata_cols = ("Unnamed: 0",
                                         "aligned_fragment_id",
                                         "aligned_fragment_mz")):
    """
    Get the feature columns from an aligned fragments-by-features table.
    """

    metadata_cols = set(metadata_cols)

    feature_cols = [col for col in aligned_intensity_df.columns
                    if col not in metadata_cols]

    return feature_cols
