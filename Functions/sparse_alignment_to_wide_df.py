from __future__ import annotations

from pathlib import Path
import os
import re
import numpy as np
import pandas as pd
from scipy.sparse import coo_matrix, csr_matrix

def sparse_alignment_to_wide_df(aligned_sparse_mat,
                                aligned_mz_vec,
                                feature_id_map_df,
                                id_col = "aligned_fragment_id",
                                mz_col = "aligned_fragment_mz"):

    """
    Convert a sparse aligned matrix into a wide DataFrame.

    Use this only when the dense table is small enough to fit in memory.
    """

    feature_id_map_df = feature_id_map_df.sort_values("spectrum_id").reset_index(drop = True)

    aligned_df = pd.DataFrame(aligned_sparse_mat.toarray())
    aligned_df.columns = [str(feat_id) for feat_id in feature_id_map_df["feat_id"].tolist()]

    aligned_df.insert(0,
                      mz_col,
                      aligned_mz_vec)

    aligned_df.insert(0,
                      id_col,
                      np.arange(len(aligned_mz_vec),
                                dtype = int))

    return aligned_df
