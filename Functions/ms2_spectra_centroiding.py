from __future__ import annotations
from modules_centroiding import *
import numpy as np

def ms2_spectra_centroiding(modules,
                            aligned_fragments_mat):

    n_fragments = len(aligned_fragments_mat[:, 0])
    n_modules = len(modules)
    n_spectra = len(aligned_fragments_mat[0, :]) - 1
    aligned_centroids_mat = np.zeros((n_fragments, n_modules + 1))
    aligned_centroids_mat[:, 0] = aligned_fragments_mat[:, 0]

    for module_id, module in enumerate(modules):
        print(module)
        ms2_spectrum = modules_centroiding(aligned_fragments_mat = aligned_fragments_mat,
                                           nodes_weights = np.ones(n_spectra),
                                           module_id = module_id,
                                           module = np.array(list(module)),
                                           norm2one = True)        
        aligned_centroids_mat[:, module_id + 1] = ms2_spectrum[:, 9]

    return aligned_centroids_mat