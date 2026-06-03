from __future__ import annotations

import numpy as np

def normalize_feat_id_column_name(column_name):
    """
    Normalize feature IDs used as matrix columns.

    This avoids treating 123, 123.0, and '123' as different features.
    Non-numeric column names are kept as strings.
    """

    if isinstance(column_name, (int, np.integer)):
        return int(column_name)

    if isinstance(column_name, (float, np.floating)):
        if float(column_name).is_integer():
            return int(column_name)

        return column_name

    column_name_str = str(column_name)

    if column_name_str.isdigit():
        return int(column_name_str)

    try:
        column_name_float = float(column_name_str)

        if column_name_float.is_integer():
            return int(column_name_float)

    except Exception:
        pass

    return column_name_str
