from __future__ import annotations

from pathlib import Path
import os
import re
import numpy as np
import pandas as pd
from scipy.sparse import coo_matrix, csr_matrix

def write_sparse_alignment_to_wide_csv(aligned_sparse_mat,
                                       aligned_mz_vec,
                                       feature_id_map_df,
                                       output_path,
                                       id_col = "aligned_fragment_id",
                                       mz_col = "aligned_fragment_mz",
                                       float_format = "%.10g",
                                       chunk_rows = 1000):
    """
    Write a wide aligned table without holding the dense DataFrame in memory.
    """

    output_path = Path(output_path)
    feature_id_map_df = feature_id_map_df.sort_values("spectrum_id").reset_index(drop = True)
    feat_id_vec = [str(feat_id) for feat_id in feature_id_map_df["feat_id"].tolist()]

    with open(output_path,
              "w",
              encoding = "utf-8") as output_file:

        header_cols = [id_col,
                       mz_col] + feat_id_vec

        output_file.write(",".join(header_cols) + "\n")

        n_rows = aligned_sparse_mat.shape[0]

        for start_id in range(0,
                              n_rows,
                              chunk_rows):

            end_id = min(start_id + chunk_rows,
                         n_rows)

            dense_chunk = aligned_sparse_mat[start_id:end_id, :].toarray()

            for local_id in range(dense_chunk.shape[0]):
                aligned_fragment_id = start_id + local_id
                row_values = dense_chunk[local_id, :]

                row_fields = [str(aligned_fragment_id),
                              f"{aligned_mz_vec[aligned_fragment_id]:.12f}"]

                row_fields += [float_format % value for value in row_values]
                output_file.write(",".join(row_fields) + "\n")
