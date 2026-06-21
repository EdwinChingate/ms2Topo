from __future__ import annotations

import sys
import os
from ShowDF import *
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import networkx as nx
from draw_molecule_archetype_frontiers import *

def experiments_table(experiment_features_df,
                      start_with = "pres_",
                      split_ = '|'):
    
    p_cols = [col 
              for col in experiment_features_df.columns 
              if col.startswith(start_with)]
    
    samples_labels_split_w_par = lambda col: samples_labels_split(col,
                                                                  remove = start_with,
                                                                  split_ = split_)
    experiments_df = pd.DataFrame(list(map(samples_labels_split_w_par,
                                           p_cols)),
                                  index = p_cols,
                                  columns = ['experiment type', 'carbon source'])
    
    return experiments_df
