# Extracted from notebook: 904937b2-026f-4f59-b3c0-21112b1589f8.ipynb
# One function per file. Auto-generated from top-level function definitions.
from __future__ import annotations

from pathlib import Path
import os
import re
import glob
import sys

import numpy as np
import pandas as pd
from scipy.sparse import coo_matrix, csr_matrix

try:
    import matplotlib.pyplot as plt
except Exception:
    plt = None

try:
    import networkx as nx
except Exception:
    nx = None

try:
    from sklearn.mixture import GaussianMixture
except Exception:
    GaussianMixture = None


def clean_feature_or_sample_id(value):
    """
    Convert IDs like 3475.0 or 11011.0 into '3475' or '11011'.
    """

    if pd.isna(value):
        return None

    if isinstance(value, float) and value.is_integer():
        return str(int(value))

    if isinstance(value, int):
        return str(value)

    value = str(value)

    if value.endswith(".0"):
        value = value[:-2]

    return value
