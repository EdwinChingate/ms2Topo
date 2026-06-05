from __future__ import annotations

from pathlib import Path
import os
import re
import numpy as np
import pandas as pd
from scipy.sparse import coo_matrix, csr_matrix
from clean_feat_id import *

def feat_id_sort_key(feat_id):
    """
    Sort feature IDs numerically when possible, otherwise lexicographically.
    """

    feat_id = clean_feat_id(feat_id)

    try:
        return (0, int(feat_id))

    except Exception:
        return (1, str(feat_id))
