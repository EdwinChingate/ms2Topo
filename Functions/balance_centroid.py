from __future__ import annotations
import numpy as np

# TODO: unresolved names: centroid_seed

def balance_centroid(modules,
                     module,
                     n_spectra):

    n_nodes = len(module)

    nodes_weights = np.ones(n_nodes)    
    centroid_seeds = np.where(module >= n_spectra)[0] 

    if len(centroid_seeds) == 0:
        return nodes_weights

    nodes_weights[centroid_seeds] = np.array([len(modules[centroid_seed - n_spectra])
                                                          for centroid_seed in centroid_seeds])
    return nodes_weights


# In[47]: