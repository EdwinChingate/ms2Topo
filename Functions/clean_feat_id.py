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
