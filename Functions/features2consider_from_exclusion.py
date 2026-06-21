from __future__ import annotations

import sys
import os
from ShowDF import *
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import networkx as nx
from draw_molecule_archetype_frontiers import *

def features2consider_from_exclusion(exclude_experiment_type,
                                     exclude_carbon_source,
                                     experiments_df,
                                     experiment_features_df):
    
    exclude_experiment_loc = experiments_df['experiment type'].isin(exclude_experiment_type)
    exclude_carbon_source_loc = experiments_df['carbon source'].isin(exclude_carbon_source)
    experiments2consider = experiments_df[exclude_experiment_loc & exclude_carbon_source_loc].index
    excluding_mat = experiment_features_df[experiments2consider].to_numpy()
    excluding_vec = np.sum(excluding_mat,
                           axis = 1)
    features_list = np.array(experiment_features_df.index,
                             dtype = 'int')
    
    return set(features_list[excluding_vec == 0].tolist())
