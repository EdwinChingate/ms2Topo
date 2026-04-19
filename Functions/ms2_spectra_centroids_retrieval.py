from __future__ import annotations
from balance_centroid import *
from modules_centroiding import *
import numpy as np

def ms2_spectra_centroids_retrieval(modules,
                                    new_modules,
                                    aligned_fragments_mat,
                                    n_spectra):

    nodes_weights = balance_centroid(modules = modules,
                                     aligned_fragments_mat = aligned_fragments_mat,
                                     new_modules = new_modules,
                                     n_spectra = n_spectra)
    n_fragments = len(aligned_fragments_mat[:, 0])
    n_modules = len(new_modules)
    aligned_centroids_mat = np.zeros((n_fragments, n_modules + 1))
    aligned_centroids_mat[:, 0] = aligned_fragments_mat[:, 0]

    for module_id, module in enumerate(new_modules):
        ms2_spectrum = modules_centroiding(aligned_fragments_mat = aligned_fragments_mat,
                                           nodes_weights = nodes_weights.copy(),
                                           module_id = module_id,
                                           module = np.array(list(module)),
                                           norm2one = True)        
        aligned_centroids_mat[:, module_id + 1] = ms2_spectrum[:, 9]
        if module_id == 0:
            pseudo_all_ms2 = ms2_spectrum.copy()
            first_spectra = False
        else:
            pseudo_all_ms2 = np.append(pseudo_all_ms2,
                                       ms2_spectrum,
                                       axis = 0) 

    return [pseudo_all_ms2, aligned_centroids_mat]


# In[12]: