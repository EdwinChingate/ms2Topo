from __future__ import annotations
import pandas as pd
from samples_labels_split import *

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
