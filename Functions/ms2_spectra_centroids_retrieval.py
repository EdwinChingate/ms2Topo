from __future__ import annotations
from balance_centroid import *
from modules_centroiding import *
import numpy as np

def ms2_spectra_centroids_retrieval(modules,
                                    new_modules,
                                    aligned_fragments_mat,
                                    n_spectra):

    aligned_fragments_mat
    for module_id, module in enumerate(new_modules):
        nodes_weights = balance_centroid(modules = modules,
                                         module = np.array(list(module)),
                                         n_spectra = n_spectra)
        ms2_spectrum = modules_centroiding(aligned_fragments_mat = aligned_fragments_mat,
                                           nodes_weights = nodes_weights,
                                           module_id = module_id,
                                           module = np.array(list(module)),
                                           norm2one = True)        

        if module_id == 0:
            pseudo_all_ms2 = ms2_spectrum.copy()
            first_spectra = False
        else:
            pseudo_all_ms2 = np.append(pseudo_all_ms2,
                                       ms2_spectrum,
                                       axis = 0) 

    return pseudo_all_ms2


# In[49]: