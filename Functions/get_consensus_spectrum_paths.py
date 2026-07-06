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
from feat_id_sort_key import feat_id_sort_key


def get_consensus_spectrum_paths(consensus_spectra_folder,
                                 selected_feat_ids = None,
                                 file_name_template = "Consensus_ms2-spectra_{feat_id}.csv"):
    """
    Get consensus spectrum paths directly from a folder.

    If selected_feat_ids is None, all files matching file_name_template are
    discovered and the feat_id is extracted from the file name.

    Returns a list of dictionaries with:
        feat_id
        consensus_spectrum_path
    """

    consensus_spectra_folder = Path(consensus_spectra_folder)

    if "{feat_id}" not in file_name_template:
        raise ValueError("file_name_template must contain '{feat_id}'.")

    prefix, suffix = file_name_template.split("{feat_id}")

    if selected_feat_ids is not None:
        spectrum_rows = []

        for feat_id in selected_feat_ids:
            feat_id = clean_feat_id(feat_id)

            if feat_id is None:
                continue

            consensus_spectrum_path = consensus_spectra_folder / file_name_template.format(feat_id = feat_id)

            spectrum_rows.append({"feat_id": feat_id,
                                  "consensus_spectrum_path": consensus_spectrum_path})

        return spectrum_rows

    glob_pattern = file_name_template.replace("{feat_id}", "*")
    spectrum_paths = list(consensus_spectra_folder.glob(glob_pattern))

    spectrum_rows = []

    for consensus_spectrum_path in spectrum_paths:

        file_name = consensus_spectrum_path.name

        if not file_name.startswith(prefix):
            continue

        if not file_name.endswith(suffix):
            continue

        feat_id = file_name[len(prefix):]

        if suffix != "":
            feat_id = feat_id[:-len(suffix)]

        feat_id = clean_feat_id(feat_id)

        if feat_id is None:
            continue

        spectrum_rows.append({"feat_id": feat_id,
                              "consensus_spectrum_path": consensus_spectrum_path})

    spectrum_rows = sorted(spectrum_rows,
                           key = lambda row: feat_id_sort_key(row["feat_id"]))

    return spectrum_rows
