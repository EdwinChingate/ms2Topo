from __future__ import annotations

import numpy as np
import matplotlib.pyplot as plt
import networkx as nx
import pandas as pd
from find_seed_node import *

def get_node_numeric_attr(G,
                          node,
                          attr,
                          default = np.nan):
    """
    Get a node attribute as a numeric value.
    """

    value = G.nodes[node].get(attr,
                              default)

    try:
        value = float(value)

    except:
        value = default

    return value
