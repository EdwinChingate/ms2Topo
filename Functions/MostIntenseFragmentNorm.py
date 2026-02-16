import numpy as np
def MostIntenseFragmentNorm(consensus_spectra):
    consensus_spectra = np.array(consensus_spectra)
    maxInt = np.max(consensus_spectra[:, 6])
    maxIntFragLoc = np.where(consensus_spectra[:, 6] == maxInt)
    if len(maxIntFragLoc) > 1:
        maxIntFragLoc = maxIntFragLoc[0][0]
    else: 
        maxIntFragLoc = maxIntFragLoc[0]
    NormIntenseVec = 100 * consensus_spectra[:, 6] / consensus_spectra[maxIntFragLoc, 6]
    NormIntenseVec = NormIntenseVec.reshape(-1, 1)
    min_NormIntenseVec = 100 * consensus_spectra[:, 7] / consensus_spectra[maxIntFragLoc, 6]
    min_NormIntenseVec = min_NormIntenseVec.reshape(-1, 1)
    max_NormIntenseVec = 100 * consensus_spectra[:, 8] / consensus_spectra[maxIntFragLoc, 6]
    max_NormIntenseVec = max_NormIntenseVec.reshape(-1, 1)
    median_NormIntenseVec = 100 * consensus_spectra[:, 14] / consensus_spectra[maxIntFragLoc, 6]
    median_NormIntenseVec = median_NormIntenseVec.reshape(-1, 1)    
    NormIntenseVec_Q1 = 100 * consensus_spectra[:, 15] / consensus_spectra[maxIntFragLoc, 6]
    NormIntenseVec_Q1 = NormIntenseVec_Q1.reshape(-1, 1)
    NormIntenseVec_Q3 = 100 * consensus_spectra[:, 16] / consensus_spectra[maxIntFragLoc, 6]
    NormIntenseVec_Q3 = NormIntenseVec_Q3.reshape(-1, 1)    
    consensus_spectra = np.hstack((consensus_spectra, NormIntenseVec))
    consensus_spectra = np.hstack((consensus_spectra, min_NormIntenseVec))
    consensus_spectra = np.hstack((consensus_spectra, max_NormIntenseVec))
    consensus_spectra = np.hstack((consensus_spectra, median_NormIntenseVec))
    consensus_spectra = np.hstack((consensus_spectra, NormIntenseVec_Q1))
    consensus_spectra = np.hstack((consensus_spectra, NormIntenseVec_Q3))    
    return consensus_spectra
