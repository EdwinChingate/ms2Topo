from __future__ import annotations
import numpy as np

# TODO: unresolved names: centroid_seed, module

def balance_centroid(modules,
                     aligned_fragments_mat,
                     new_modules,
                     n_spectra):

    all_nodes_counter = np.array([np.max(list(module)) for module in new_modules])
    n_nodes = len(aligned_fragments_mat[0, :]) - 1
    nodes_weights = np.ones(n_nodes)  

    if n_nodes == n_spectra:
        return nodes_weights

    nodes_weights[n_spectra: ] = np.array([len(modules[centroid_seed])
                                           for centroid_seed in range(n_nodes - n_spectra)])
    return nodes_weights


# In[10]: