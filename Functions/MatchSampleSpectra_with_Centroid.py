from __future__ import annotations
import numpy as np
def MatchSampleSpectra_with_Centroid(CosineToCentroids,           # ← ADDED
                                     SamplesSamplesList,           # ← ADDED
                                     Modules,                      # ← ADDED
                                     BigFeature_Module,            # ← ADDED
                                     IntramoduleSimilarityModulesMat): # ← ADDED

    N_uncovered_spectra = len(SamplesSamplesList)  # ← FIXED: was Spectra_idVec (undefined)

    for spectrum_idx in np.arange(N_uncovered_spectra):
        best_module_id = np.argmax(CosineToCentroids[spectrum_idx, :])
        best_cosine = CosineToCentroids[spectrum_idx, best_module_id]
        
        # Adaptive threshold: use this module's 10th percentile cosine (column 1)
        module_threshold = IntramoduleSimilarityModulesMat[best_module_id, 1]
        
        if best_cosine >= module_threshold:
            true_spectrum_id = SamplesSamplesList[spectrum_idx]
            Modules[best_module_id].append(true_spectrum_id)
            if true_spectrum_id not in BigFeature_Module:
                BigFeature_Module.append(true_spectrum_id)

    return [Modules, BigFeature_Module]
