from __future__ import annotations

from pathlib import Path
import os
import re
import numpy as np
import pandas as pd
from scipy.sparse import coo_matrix, csr_matrix

def clean_feat_id(feat_id):
    """
    Convert feature IDs like 3475.0 into '3475'.
    """

    if pd.isna(feat_id):
        return None

    if isinstance(feat_id, float) and feat_id.is_integer():
        return str(int(feat_id))

    if isinstance(feat_id, int):
        return str(feat_id)

    feat_id = str(feat_id)

    if feat_id.endswith(".0"):
        feat_id = feat_id[:-2]

    return feat_id
