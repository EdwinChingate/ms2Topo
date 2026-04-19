from __future__ import annotations
from append_seeds import *
import numpy as np

def greedy_growth_from_mixed_modules(new_modules,
                                     modules,
                                     sample_feature_module):

    if modules is None:
        modules = []

    n_spectra = len(sample_feature_module)
    touched_old_modules = set()
    updated_modules = []

    for module in new_modules:
        module_array = np.array(list(module),
                                dtype = int)

        old_module_nodes = module_array[module_array >= n_spectra]
        old_module_ids = set((old_module_nodes - n_spectra).astype(int).tolist())
        touched_old_modules.update(old_module_ids)

        grown_module = append_seeds(module = module_array,
                                    n_spectra = n_spectra,
                                    modules = modules,
                                    sample_feature_module = sample_feature_module)

        updated_modules.append(grown_module)

    for old_module_id, old_module in enumerate(modules):
        if old_module_id not in touched_old_modules:
            updated_modules.append(set(old_module))

    assigned_spectra = set()
    for module in updated_modules:
        assigned_spectra.update(module)

    return [np.array(updated_modules, dtype = object),
            assigned_spectra]


# In[14]: