from __future__ import annotations

import numpy as np
import pandas as pd
from ConsensusFragment import *
from MostIntenseFragmentNorm import *

def ConsensusSpectra(module,
                     AlignedFragments_mz_Mat,
                     AlignedFragmentsMat,
                     percentile_mz = 5,
                     percentile_Int = 10,
                     minSpectra = 3,
                     alpha = 0.01,
                     min_spectra = 3,
                     reduceIQR_factor = 1,
                     Columns_to_return = np.array([ 0, 3, 9, 10, 11, 17, 18, 19, 20, 21, 22])):
    N_Fragments = len(AlignedFragments_mz_Mat[:,0])    
    consensus_spectra = []
    for fragment in np.arange(N_Fragments):
        SpectraFragmentVec = AlignedFragments_mz_Mat[fragment, np.array(module)+1]
        SpectraIntensityVec = AlignedFragmentsMat[fragment, np.array(module)+1]
        consensus_spectra = ConsensusFragment(SpectraFragmentVec = SpectraFragmentVec,
                                              SpectraIntensityVec = SpectraIntensityVec,
                                              consensus_spectra = consensus_spectra,
                                              percentile_mz = percentile_mz,
                                              percentile_Int = percentile_Int,
                                              minSpectra = minSpectra,
                                              alpha = alpha,
                                              reduceIQR_factor = reduceIQR_factor)
    Columns = np.array(["median_mz(Da)",
                        "mz_std(Da)",
                        "IQR_mz(Da)",
                        "N_spectra",
                        "t-student Confidence_interval(Da)",
                        "t-student Confidence_interval(ppm)",
                        "mean_Int_NoNorm",
                        "min_Int_NoNorm",
                        "max_Int_NoNorm",
                        "min_mz",
                        "max_mz",
                        "IQR_mz(ppm)",
                        "Q1_mz",
                        "Q3_mz",
                        "median_Int_NoNorm",
                        "Q1_Int_NoNorm",
                        "Q3_Int_NoNorm",
                        "mean_Int",
                        "min_Int",
                        "max_Int",
                        "median_Int",
                        "Int_Q1",
                        "Int_Q3"])        
    if len(consensus_spectra) == 0:
        return []
    consensus_spectra = MostIntenseFragmentNorm(consensus_spectra = consensus_spectra)
    consensus_spectraDF = pd.DataFrame(consensus_spectra, columns = Columns)
    consensus_spectraDF = consensus_spectraDF[Columns[Columns_to_return]].copy() 
    return consensus_spectraDF