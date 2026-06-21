from __future__ import annotations

import sys
import os
from ShowDF import *
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import networkx as nx
from draw_molecule_archetype_frontiers import *

def group_features_on_samples_distribution(experiment_features_df,
                                           threshold = 0.4,
                                           start_with = "p__",
                                           presence_str = "pres_",
                                           feat_id_col = 'feat_id'):
    p_cols = [col 
              for col in experiment_features_df.columns 
              if col.startswith(start_with)]    
    
    bool_experiment_features_mat = (experiment_features_df[p_cols].to_numpy() > threshold).astype(int)
    presence_cols = [col.replace(start_with,presence_str)
                     for col in p_cols]
    bool_experiment_features_df = pd.DataFrame(bool_experiment_features_mat,
                                               columns = presence_cols)    
    bool_experiment_features_df.index = experiment_features_df[feat_id_col]
    
    assignments_asignment = list(map(compress_experiments_dist, bool_experiment_features_mat))
    features_groups = set(assignments_asignment)
    experiment_features_df["groups"] = assignments_asignment    
    
    return pd.concat([experiment_features_df, bool_experiment_features_df],
                     axis = 1)
