from __future__ import annotations
import numpy as np
from Cosine_2VecSpec import *

def ContrastSamplesCentroids(AlignedFragmentsSamplesSpectraMat,  # ← ADDED
                             CentroidsAlignedFragmentsMat,        # ← ADDED
                             N_modules):                          # ← ADDED

    N_uncovered_spectra = AlignedFragmentsSamplesSpectraMat.shape[1] - 1  # ← FIXED: was Spectra_idVec (undefined)

    CosineToCentroids = np.zeros((N_uncovered_spectra, N_modules))
    
    for spectrum_idx in np.arange(N_uncovered_spectra):
        spectrum_vec = AlignedFragmentsSamplesSpectraMat[:, spectrum_idx + 1]
        
        for module_id in np.arange(N_modules):
            centroid_vec = CentroidsAlignedFragmentsMat[:, module_id + 1]
            AlignedSpecMat = np.column_stack([AlignedFragmentsSamplesSpectraMat[:, 0],
                                              centroid_vec,
                                              spectrum_vec])
            CosineToCentroids[spectrum_idx, module_id] = Cosine_2VecSpec(AlignedSpecMat = AlignedSpecMat)

    return CosineToCentroids
