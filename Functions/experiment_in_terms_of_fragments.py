from __future__ import annotations

import sys
import os
from ShowDF import *
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import networkx as nx
from draw_molecule_archetype_frontiers import *

def experiment_in_terms_of_fragments(experiment_features_df,
                                     aligned_intensity_sparse_df,
                                     start_with = "p__",
                                     threshold = 0.4):
    
    p_cols = [col 
              for col in experiment_features_df.columns 
              if col.startswith(start_with)]
    n_experiments = len(p_cols)
    n_fragments = aligned_intensity_sparse_df.shape[0]
    experiment_fragments_matrix = np.zeros((n_fragments, n_experiments),
                                           dtype = 'int')
    aligned_cols = list(aligned_intensity_sparse_df.columns)
    sample_id = 0
    for sample in p_cols:
        features_loc = experiment_features_df[sample] > threshold
        carbon_source_features_list = experiment_features_df['feat_id'][features_loc].to_numpy(dtype = 'int').astype(str).tolist()    
        carbon_source_features = pd.Series(carbon_source_features_list)    
        carbon_source_features_present = carbon_source_features[carbon_source_features.isin(aligned_cols)]

        fragments_count = np.sum(aligned_intensity_sparse_df[carbon_source_features_present].to_numpy(),
                                                             axis = 1)
        fragments_count_loc = np.where(fragments_count > 0)[0]
        experiment_fragments_matrix[fragments_count_loc, sample_id] = 1
        sample_id += 1
    
    fragments_presence = np.sum(experiment_fragments_matrix,
                                axis = 1)
    fragments_presence_loc = np.where(fragments_presence > 0)[0]
    experiment_fragments_df = pd.DataFrame(experiment_fragments_matrix,
                                           columns = p_cols)
    experiment_fragments_df["aligned_fragment_id"] = aligned_intensity_sparse_df['aligned_fragment_id']
    experiment_fragments_df['median_mz(Da)'] = aligned_intensity_sparse_df['aligned_fragment_mz']
    
    return experiment_fragments_df.loc[fragments_presence_loc]
