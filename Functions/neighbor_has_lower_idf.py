from __future__ import annotations

import numpy as np
import matplotlib.pyplot as plt
import networkx as nx
import pandas as pd
from find_seed_node import *
from get_node_numeric_attr import get_node_numeric_attr

def neighbor_has_lower_idf(G,
                           node,
                           neighbor,
                           idf_attr = "weighted_mean_fragment_IDF",
                           idf_tolerance = 0,
                           missing_idf_policy = "allow"):
    """
    Check whether a neighbor has lower IDF than the current node.

    missing_idf_policy:
        "allow":
            if either IDF value is missing, do not stop the walk.

        "stop":
            if either IDF value is missing, stop the walk.
    """

    node_idf = get_node_numeric_attr(G = G,
                                     node = node,
                                     attr = idf_attr)

    neighbor_idf = get_node_numeric_attr(G = G,
                                         node = neighbor,
                                         attr = idf_attr)

    if np.isnan(node_idf) or np.isnan(neighbor_idf):

        if missing_idf_policy == "allow":
            return False

        if missing_idf_policy == "stop":
            return True

        raise ValueError("missing_idf_policy must be 'allow' or 'stop'.")

    has_lower_idf = neighbor_idf < (node_idf - idf_tolerance)

    return has_lower_idf
