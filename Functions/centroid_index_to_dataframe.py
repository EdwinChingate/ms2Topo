from __future__ import annotations

from pathlib import Path
import os
import re
import numpy as np
import pandas as pd
from scipy.sparse import coo_matrix, csr_matrix

def centroid_index_to_dataframe(centroid_index,
                                id_col = "aligned_fragment_id",
                                mz_col = "aligned_fragment_mz"):
    """
    Convert the internal centroid index into a report table.
    """

    centroid_df = pd.DataFrame({id_col: np.arange(len(centroid_index["centroid_mz"]),
                                                 dtype = int),
                                "centroid_original_id": centroid_index["centroid_original_id"],
                                mz_col: centroid_index["centroid_mz"],
                                "centroid_sigma": centroid_index["centroid_sigma"],
                                "centroid_edge": centroid_index["centroid_edge"],
                                "centroid_count": centroid_index["centroid_count"],
                                "centroid_prior": centroid_index["centroid_prior"]})

    centroid_df["centroid_min_mz"] = centroid_df[mz_col] - centroid_df["centroid_edge"]
    centroid_df["centroid_max_mz"] = centroid_df[mz_col] + centroid_df["centroid_edge"]

    return centroid_df
