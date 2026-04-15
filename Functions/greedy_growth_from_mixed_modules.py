from __future__ import annotations
from append_seeds import *
import numpy as np

def greedy_growth_from_mixed_modules(new_modules,
                                     modules,
                                     sample_feature_module):

    for module_id, module in enumerate(new_modules):
        module = append_seeds(module = np.array(list(module)),
                              n_spectra = len(sample_feature_module),
                              modules = modules,
                              sample_feature_module = sample_feature_module)
        if module_id == 0:
            assigned_spectra = module
        else:
            assigned_spectra = assigned_spectra | module

    return [new_modules, assigned_spectra]


# In[54]: