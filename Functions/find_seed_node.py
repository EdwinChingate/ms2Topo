from __future__ import annotations

import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

def find_seed_node(G,
                   feat_id):
    """
    Find feat_id in G, trying int, str, and float-safe forms.
    """

    candidates = []

    candidates.append(feat_id)
    candidates.append(str(feat_id))

    try:
        candidates.append(int(feat_id))
        candidates.append(str(int(feat_id)))
    except:
        pass

    try:
        candidates.append(float(feat_id))
    except:
        pass

    for candidate in candidates:
        if candidate in G:
            return candidate

    return None
