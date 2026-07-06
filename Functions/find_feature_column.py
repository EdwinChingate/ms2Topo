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
from clean_feature_or_sample_id import clean_feature_or_sample_id


def find_feature_column(aligned_df,
                        feat_id):
    """
    Find the column corresponding to a feature ID in a wide aligned table.
    """

    feat_id_clean = clean_feature_or_sample_id(feat_id)

    candidate_cols = [feat_id,
                      str(feat_id),
                      feat_id_clean]

    for candidate_col in candidate_cols:
        if candidate_col in aligned_df.columns:
            return candidate_col

    available_cols = [col for col in aligned_df.columns
                      if col != "aligned_fragment_mz"]

    raise ValueError("Feature ID was not found as a column: "
                     + str(feat_id)
                     + "\nAvailable examples: "
                     + str(available_cols[:10]))
