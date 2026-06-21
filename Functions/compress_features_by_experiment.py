from __future__ import annotations

import sys
import os
from ShowDF import *
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import networkx as nx
from draw_molecule_archetype_frontiers import *

def compress_features_by_experiment(features_df,
                                    sample_experiments_df,
                                    sample_id_col = 'Sample ID',
                                    group_cols = ('Source', 'Primary carbon source'),
                                    metadata_cols = None,
                                    value_prefix = 'p__',
                                    sep = ' | '):
    """
    Compress a binary sample-level feature table into an experiment-level
    probability/prevalence table.

    Only samples listed in sample_experiments_df are used.
    """

    features_df = features_df.copy()
    sample_experiments_df = sample_experiments_df.copy()

    # Normalize sample IDs so Excel integers and CSV column names match
    sample_experiments_df[sample_id_col] = sample_experiments_df[sample_id_col].astype(str).str.strip()

    feature_col_lookup = {str(col).strip(): col
                          for col in features_df.columns}

    # Keep only samples from the experiment table that exist in the feature table
    sample_experiments_df["sample_col"] = sample_experiments_df[sample_id_col].map(feature_col_lookup)

    sample_experiments_df = sample_experiments_df.dropna(subset=["sample_col"])

    selected_sample_cols = sample_experiments_df["sample_col"].tolist()

    if metadata_cols is None:
        first_sample_idx = min(features_df.columns.get_loc(col)
                               for col in selected_sample_cols)

        metadata_cols = list(features_df.columns[:first_sample_idx])

    out_df = features_df[metadata_cols].copy()

    for group_values, group_df in sample_experiments_df.groupby(list(group_cols), sort=False):

        if not isinstance(group_values, tuple):
            group_values = (group_values,)

        group_name = sep.join(map(str, group_values))
        out_col = value_prefix + group_name

        sample_cols = group_df["sample_col"].tolist()

        out_df[out_col] = features_df[sample_cols].astype(float).mean(axis = 1)

    out_df.index = features_df['feat_id'].to_numpy(dtype = 'int')
    return out_df
