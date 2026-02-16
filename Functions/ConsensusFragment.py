from ttest import *
from scipy import stats
import numpy as np
def ConsensusFragment(SpectraFragmentVec,
                      SpectraIntensityVec,
                      consensus_spectra,
                      percentile_mz = 5,
                      percentile_Int = 10,
                      alpha = 0.01,
                      minSpectra = 3):
    SpectraFragmentLoc = np.where(SpectraFragmentVec > 0)
    N_spectra = len(SpectraFragmentVec[SpectraFragmentLoc])
    if N_spectra < minSpectra:
        return consensus_spectra
    mz = np.median(SpectraFragmentVec[SpectraFragmentLoc])
    min_mz = np.percentile(SpectraFragmentVec[SpectraFragmentLoc],
                           percentile_mz)
    max_mz = np.percentile(SpectraFragmentVec[SpectraFragmentLoc],
                           100 - percentile_mz)  
    Q1_mz = np.percentile(SpectraFragmentVec[SpectraFragmentLoc],
                          25)
    Q3_mz = np.percentile(SpectraFragmentVec[SpectraFragmentLoc],
                          75)    
    IQR_mz = Q3_mz - Q1_mz
    mz_std = 0#np.std(SpectraFragmentVec[SpectraFragmentLoc])
    p = 0#stat, p = stats.shapiro(SpectraFragmentVec[SpectraFragmentLoc])
    t_ref = 0#ttest(Nsignals = N_spectra,alpha = alpha)
    mz_CI = 0#t_ref * mz_std / np.sqrt(N_spectra)
    mz_CIppm = 0#mz_CI / mz * 1e6       
    median_Int = np.median(SpectraIntensityVec) 
    mean_Int = np.mean(SpectraIntensityVec) 
    min_Int = np.percentile(SpectraIntensityVec,
                            percentile_Int)
    max_Int = np.percentile(SpectraIntensityVec,
                            100 - percentile_Int)
    Q1_Int = np.percentile(SpectraIntensityVec,
                            25)
    Q3_Int = np.percentile(SpectraIntensityVec,
                            75)    
    consensus_spectra.append([mz,
                              mz_std,
                              p,
                              N_spectra,
                              mz_CI,
                              mz_CIppm,
                              mean_Int,
                              min_Int,
                              max_Int,
                              min_mz,
                              max_mz,
                              IQR_mz / mz * 1e6,
                              Q1_mz,
                              Q3_mz,
                              median_Int,
                              Q1_Int,
                              Q3_Int])    
    return consensus_spectra
