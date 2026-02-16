import numpy as np
import pandas as pd
from ConsensusFragment import *
from MostIntenseFragmentNorm import *
def ConsensusSpectra(module,
                     N_Fragments,
                     AlignedFragments_mz_Mat,
                     AlignedFragmentsMat,
                     percentile_mz = 5,
                     percentile_Int = 10,
                     minSpectra = 3,
                     alpha = 0.01,
                     Columns_to_return = np.array([ 0, 3, 9, 10, 11, 17, 18, 19, 20, 21, 22])):
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
                                              alpha = alpha)
    Columns = np.array(["median_mz(Da)",
                        "mz_std(Da)",
                        "p-Shapiro",
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
    consensus_spectra = MostIntenseFragmentNorm(consensus_spectra = consensus_spectra)
    consensus_spectraDF = pd.DataFrame(consensus_spectra, columns = Columns)
    consensus_spectraDF = consensus_spectraDF[Columns[Columns_to_return]].copy()    
    return consensus_spectraDF
