from __future__ import annotations

import sys
import os
from ShowDF import *
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import networkx as nx
from draw_molecule_archetype_frontiers import *

def features2consider_from_inclusion(include_experiment_type,
                                     include_carbon_source,
                                     experiments_df,
                                     experiment_features_df):
    
    include_experiment_loc = experiments_df['experiment type'].isin(include_experiment_type)
    include_carbon_source_loc = experiments_df['carbon source'].isin(include_carbon_source)
    experiments2consider = experiments_df[include_experiment_loc & include_carbon_source_loc].index
    including_mat = experiment_features_df[experiments2consider].to_numpy()
    including_vec = np.sum(including_mat,
                           axis = 1)
    features_list = np.array(experiment_features_df.index)
    
    return set(features_list[including_vec > 0].tolist())
