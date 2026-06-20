from __future__ import annotations

import numpy as np
import pandas as pd

def filter_aligned_intensity_by_fragment_ids(aligned_intensity_df,
                                             selected_fragment_ids,
                                             aligned_fragment_id_col = "aligned_fragment_id"):
    """
    Keep only aligned-fragment rows whose ID is in selected_fragment_ids.
    """

    if aligned_fragment_id_col not in aligned_intensity_df.columns:
        raise ValueError(f"Aligned fragment ID column was not found: {aligned_fragment_id_col}")

    selected_fragment_ids = set(clean_id_series(selected_fragment_ids).tolist())

    aligned_fragment_ids = clean_id_series(aligned_intensity_df[aligned_fragment_id_col])

    fragment_mask = aligned_fragment_ids.isin(selected_fragment_ids).to_numpy()

    filtered_aligned_intensity_df = aligned_intensity_df.loc[fragment_mask].copy()

    return filtered_aligned_intensity_df, fragment_mask
