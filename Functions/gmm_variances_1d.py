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


def gmm_variances_1d(gmm):
    """
    Extract component variances from a 1D sklearn GaussianMixture.
    """

    if gmm.covariance_type == "full":
        variances = gmm.covariances_.reshape(-1)

    elif gmm.covariance_type == "diag":
        variances = gmm.covariances_.reshape(-1)

    elif gmm.covariance_type == "spherical":
        variances = gmm.covariances_.reshape(-1)

    elif gmm.covariance_type == "tied":
        variances = np.repeat(gmm.covariances_.reshape(-1)[0],
                              gmm.n_components)

    return variances
