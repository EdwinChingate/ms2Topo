from __future__ import annotations

from pathlib import Path
import os
import re
import numpy as np
import pandas as pd
from scipy.sparse import coo_matrix, csr_matrix

def column_to_array(table,
                     col,
                     default = None,
                     dtype = float):
    """
    Extract one column from a pandas object or NumPy array.

    Numeric strings such as '6' are accepted as positional columns for NumPy
    arrays and as column labels for DataFrames when that label exists.
    """

    if isinstance(table, pd.Series):
        if col in [0, "0", None]:
            return pd.to_numeric(table,
                                 errors = "coerce").to_numpy(dtype = dtype)

        if default is not None:
            return np.full(len(table),
                           default,
                           dtype = dtype)

        raise ValueError("A pandas Series can only provide one centroid column.")

    if isinstance(table, pd.DataFrame):
        if col in table.columns:
            return pd.to_numeric(table[col],
                                 errors = "coerce").to_numpy(dtype = dtype)

        col_str = str(col)

        if col_str in table.columns:
            return pd.to_numeric(table[col_str],
                                 errors = "coerce").to_numpy(dtype = dtype)

        if isinstance(col, str) and col.isdigit():
            col_int = int(col)

            if col_int in table.columns:
                return pd.to_numeric(table[col_int],
                                     errors = "coerce").to_numpy(dtype = dtype)

            if col_int < table.shape[1]:
                return pd.to_numeric(table.iloc[:, col_int],
                                     errors = "coerce").to_numpy(dtype = dtype)

        if isinstance(col, int) and col < table.shape[1]:
            return pd.to_numeric(table.iloc[:, col],
                                 errors = "coerce").to_numpy(dtype = dtype)

        if default is not None:
            return np.full(len(table),
                           default,
                           dtype = dtype)

        raise ValueError(f"Column {col!r} was not found in centroid table.")

    table_array = np.asarray(table)

    if table_array.ndim == 1:
        if col in [0, "0", None]:
            return table_array.astype(dtype)

        if default is not None:
            return np.full(table_array.shape[0],
                           default,
                           dtype = dtype)

        raise ValueError("A 1D centroid vector only provides column 0.")

    if isinstance(col, str) and col.isdigit():
        col = int(col)

    if not isinstance(col, int):
        if default is not None:
            return np.full(table_array.shape[0],
                           default,
                           dtype = dtype)

        raise ValueError(f"Column {col!r} is not valid for a NumPy array.")

    if col >= table_array.shape[1]:
        if default is not None:
            return np.full(table_array.shape[0],
                           default,
                           dtype = dtype)

        raise ValueError(f"Column {col} is outside the centroid array shape {table_array.shape}.")

    return table_array[:, col].astype(dtype)
