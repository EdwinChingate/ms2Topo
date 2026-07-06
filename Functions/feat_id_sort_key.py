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

# Local function dependencies extracted from the same notebook.
from clean_feat_id import clean_feat_id


def feat_id_sort_key(feat_id):
    """
    Sort feature IDs numerically when possible, otherwise lexicographically.
    """

    feat_id = clean_feat_id(feat_id)

    try:
        return (0, int(feat_id))

    except Exception:
        return (1, str(feat_id))
