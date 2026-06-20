from __future__ import annotations

import pandas as pd
import numpy as np

def clean_id_value(value):
    """
    Convert feature or fragment IDs into stable string IDs.
    """

    if pd.isna(value):
        return None

    try:
        float_value = float(value)

        if float_value.is_integer():
            return str(int(float_value))

    except:
        pass

    return str(value)
