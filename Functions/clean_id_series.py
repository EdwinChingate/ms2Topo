from __future__ import annotations

import pandas as pd
import numpy as np
from clean_id_value import clean_id_value

def clean_id_series(values):
    """
    Convert a vector of IDs into stable string IDs.
    """

    cleaned_ids = pd.Series(values).map(clean_id_value).dropna()

    return cleaned_ids
