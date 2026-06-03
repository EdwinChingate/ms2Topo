from __future__ import annotations

import pandas as pd
from normalize_feat_id_column_name import *

def prepare_aligned_annotation_matrix(aligned_matrix_df,
                                      annotation_type,
                                      fill_value = 0,
                                      binary_matrix = True):
    """
    Prepare one aligned annotation matrix before concatenation.

    It normalizes feature IDs in columns and prefixes row IDs with the
    annotation type to avoid collisions between fragment formulas and
    loss formulas.
    """

    if not isinstance(aligned_matrix_df, pd.DataFrame):
        raise TypeError("aligned_matrix_df must be a pandas DataFrame.")

    if aligned_matrix_df.shape[0] == 0:
        raise ValueError("aligned_matrix_df has zero rows.")

    if aligned_matrix_df.shape[1] == 0:
        raise ValueError("aligned_matrix_df has zero columns.")

    prepared_df = aligned_matrix_df.copy()

    prepared_df.columns = [normalize_feat_id_column_name(col)
                           for col in prepared_df.columns]

    if len(set(prepared_df.columns)) != len(prepared_df.columns):
        prepared_df = prepared_df.T.groupby(level = 0).max().T

    prepared_df.index = prepared_df.index.astype(str)

    prepared_df.index = [str(annotation_type) + "::" + annotation_id
                         for annotation_id in prepared_df.index]

    prepared_df = prepared_df.apply(pd.to_numeric,
                                    errors = "coerce").fillna(fill_value)

    if binary_matrix:
        prepared_df = (prepared_df > fill_value).astype(int)

    return prepared_df
