from __future__ import annotations

import sys
import os
from ShowDF import *
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import networkx as nx
from draw_molecule_archetype_frontiers import *

def filter_include_exclude(experiments_df,
                           include_experiment_type = ['Effluent'],
                           exclude_experiment_type = ['Influent', "EffluentClean", "InfluentClean"],
                           include_carbon_source = ['Aniline'],
                           exclude_carbon_source = []):
    '''
    includes the experiments to consider in as columns
    excludes the features from the rows
    '''
    filters_list = [include_experiment_type,
                    exclude_experiment_type,
                    include_carbon_source,
                    exclude_carbon_source]
    filter_table = lambda vec: filter_all_nothing(vec,
                                                  experiments_df = experiments_df)    
    filters_list = list(map(filter_table,
                            filters_list))
    
    return filters_list
