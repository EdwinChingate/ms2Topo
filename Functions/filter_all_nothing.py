from __future__ import annotations

import sys
import os
from ShowDF import *
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import networkx as nx
from draw_molecule_archetype_frontiers import *

def filter_all_nothing(vec,
                       experiments_df):
    
    if len(vec) == 0:
        
        return list(set(experiments_df['carbon source']))
    
    return vec
