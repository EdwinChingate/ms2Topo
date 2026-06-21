from __future__ import annotations

import sys
import os
from ShowDF import *
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import networkx as nx
from draw_molecule_archetype_frontiers import *

def samples_labels_split(col,
                         remove = "pres_",
                         split_ = '|'):
    
    col = col.replace(' ',
                      '')
    col = col.replace(remove,
                      '')    
    
    return col.split(split_)
