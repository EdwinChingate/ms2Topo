from __future__ import annotations
from greedy_growth_from_mixed_modules import *
from ms2_spectra_centroids_retrieval import *

def greedy_formatting(extraction_state,
                      modules):

    pseudo_all_ms2, aligned_centroids_mat = ms2_spectra_centroids_retrieval(new_modules = extraction_state['modules'],
                                                                            modules = modules,
                                                                            aligned_fragments_mat = extraction_state['aligned_fragments_mat'],
                                                                            n_spectra = len(extraction_state['sample_feature_module']))
    new_modules, assigned_spectra = greedy_growth_from_mixed_modules(new_modules = extraction_state['modules'],
                                                                     modules = modules,
                                                                     sample_feature_module = extraction_state['sample_feature_module'])

    return [new_modules, assigned_spectra, pseudo_all_ms2, aligned_centroids_mat]



# In[15]: