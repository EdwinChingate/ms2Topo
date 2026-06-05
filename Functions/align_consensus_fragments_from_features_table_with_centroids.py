from __future__ import annotations

from pathlib import Path
import os
import re
import numpy as np
import pandas as pd
from scipy.sparse import coo_matrix, csr_matrix
from align_consensus_spectra_to_fragment_centroids import *
from get_feat_ids_from_features_table import *

def align_consensus_fragments_from_features_table_with_centroids(features_table_df,
                                                                 consensus_spectra_folder,
                                                                 clustered_fragments_df,
                                                                 feat_id_col = "feat_id",
                                                                 selected_feat_ids = None,
                                                                 **kwargs):
    """
    Optional compatibility wrapper.

    The features table is used only to choose selected_feat_ids. The alignment
    itself is performed by align_consensus_spectra_to_fragment_centroids.
    """

    if selected_feat_ids is None:
        selected_feat_ids = get_feat_ids_from_features_table(features_table_df = features_table_df,
                                                            feat_id_col = feat_id_col)

    return align_consensus_spectra_to_fragment_centroids(consensus_spectra_folder = consensus_spectra_folder,
                                                         clustered_fragments_df = clustered_fragments_df,
                                                         selected_feat_ids = selected_feat_ids,
                                                         **kwargs)
