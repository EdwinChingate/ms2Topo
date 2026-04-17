from __future__ import annotations
import numpy as np

def modules_centroiding(aligned_fragments_mat,
                        module_id,
                        nodes_weights,
                        module,
                        norm2one = True):

    module_nodes_weights = np.zeros_like(nodes_weights)
    module_nodes_weights[list(module)] = 1
    n_fragments = len(aligned_fragments_mat[:, 0])
    ms2_spectrum = np.zeros((n_fragments, 11))
    ms2_spectrum[:, [0,1]] = aligned_fragments_mat[:, [0,1]]
    ms2_spectrum[:, 9] = np.average(aligned_fragments_mat[:, 1: ],
                                    axis = 1,
                                    weights = nodes_weights * module_nodes_weights)             
    ms2_spectrum[:, 10] = np.ones(n_fragments) * module_id

    if norm2one:
        norm = np.sqrt(np.sum(ms2_spectrum[:, 9] * ms2_spectrum[:, 9]))
        ms2_spectrum[:, 9] = ms2_spectrum[:, 9] / norm    

    return ms2_spectrum


# In[11]: