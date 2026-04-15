from __future__ import annotations
import numpy as np

def append_seeds(module,
                 sample_feature_module,
                 n_spectra,
                 modules):

    new_module = set(sample_feature_module[module])
    centroid_seeds = np.where(module >= n_spectra)[0]

    if len(centroid_seeds) == 0:
        return new_module    

    for centroid_seed in centroid_seeds:
        new_module = new_module | modules[centroid_seed - n_spectra]

    return new_module  


# In[50]: